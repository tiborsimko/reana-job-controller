# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2026 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for the CERN Docker build configuration."""

import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
DOCKERFILE = (REPOSITORY / "Dockerfile").read_text()


def _docker_build_arguments():
    """Return Docker build arguments with literal default values."""
    return dict(re.findall(r"^ARG ([A-Z0-9_]+)=([^\s]+)$", DOCKERFILE, re.MULTILINE))


def _assert_sha256_argument(name):
    """Assert that a Docker build argument contains a SHA-256 digest."""
    assert re.fullmatch(r"[0-9a-f]{64}", _docker_build_arguments()[name])


def test_kerberos_profile_is_valid_for_every_backend():
    """Every image must create its include directory and preserve delegation."""
    kerberos_config = (REPOSITORY / "etc" / "krb5.conf").read_text()
    reana_profiles = sorted(
        path
        for path in (REPOSITORY / "etc" / "krb5.conf.d").iterdir()
        if path.is_file()
    )
    reana_config = "\n".join(path.read_text() for path in reana_profiles)

    assert kerberos_config.strip().endswith("includedir /etc/krb5.conf.d/")
    assert reana_profiles
    assert all(path.suffix == ".conf" for path in reana_profiles)
    assert all(path.name < "cern-" for path in reana_profiles)
    assert "COPY etc/krb5.conf.d/ /etc/krb5.conf.d/" in DOCKERFILE
    assert re.search(r"^\s*forwardable\s*=\s*true\s*$", reana_config, re.MULTILINE)
    assert "default_tkt_enctypes" not in kerberos_config
    assert "allow_weak_crypto" not in kerberos_config


def test_cern_image_configures_kerberos_credential_producer():
    """The CERN image must keep the producer required by ``CredType.Kerberos``."""
    cern_config = (REPOSITORY / "etc" / "10_cernsubmit.config").read_text()

    assert "SEC_CREDENTIAL_PRODUCER = /usr/bin/batch_krb5_credential" in cern_config
    assert 'Authen::Krb5->can("cc_copy_creds")' in DOCKERFILE
    assert "perl -T -c /usr/bin/batch_krb5_credential" in DOCKERFILE


def test_cern_image_uses_managed_kerberos_configuration():
    """CERN backends must source current Kerberos policy from CERN RPMs."""
    arguments = _docker_build_arguments()

    assert arguments["CERN_KRB5_CONF_VERSION"]
    _assert_sha256_argument("CERN_KRB5_CONF_DEFAULTS_SHA256")
    _assert_sha256_argument("CERN_KRB5_CONF_REALM_SHA256")
    assert "cern-krb5-conf-defaults-cernch-$CERN_KRB5_CONF_VERSION" in DOCKERFILE
    assert "cern-krb5-conf-realm-cernch-$CERN_KRB5_CONF_VERSION" in DOCKERFILE
    assert "dns_canonicalize_hostname = fallback" in DOCKERFILE


def test_cern_image_uses_every_managed_ca_certificate():
    """CERN backends must install the complete managed CA certificate bundle."""
    arguments = _docker_build_arguments()

    assert arguments["CERN_CA_CERTS_VERSION"]
    _assert_sha256_argument("CERN_CA_CERTS_SHA256")
    assert "CERN-CA-certs-$CERN_CA_CERTS_VERSION" in DOCKERFILE
    assert "for certificate in /tmp/cern-ca-certs/etc/pki/tls/certs/*.pem" in (
        DOCKERFILE
    )
    assert "tr -d '\\r'" in DOCKERFILE
    assert "grep -c '^-----BEGIN CERTIFICATE-----$'" in DOCKERFILE
    assert "cern-${certificate_name}.crt" in DOCKERFILE
    assert 'test "$certificate_count" -ge 3' in DOCKERFILE
    assert "COPY etc/cerngridca.crt" not in DOCKERFILE
    assert "COPY etc/cernroot.crt" not in DOCKERFILE


def test_cern_batch_package_fallbacks_verify_downloaded_artifacts():
    """Every downloaded batch RPM must match its pinned artefact digest."""
    arguments = _docker_build_arguments()

    assert arguments["NGBAUTH_SUBMIT_VERSION"]
    assert arguments["MYSCHEDD_VERSION"]
    _assert_sha256_argument("NGBAUTH_SUBMIT_SHA256")
    _assert_sha256_argument("MYSCHEDD_AMD64_SHA256")
    _assert_sha256_argument("MYSCHEDD_ARM64_SHA256")
    assert (
        DOCKERFILE.count(
            'echo "$NGBAUTH_SUBMIT_SHA256  /ngbauth-submit.rpm" | sha256sum -c -'
        )
        == 2
    )
    assert (
        DOCKERFILE.count('echo "$MYSCHEDD_SHA256  /myschedd.rpm" | sha256sum -c -') == 2
    )
    for package, checksum in (
        ("ngbauth-submit", "NGBAUTH_SUBMIT_SHA256"),
        ("myschedd", "MYSCHEDD_SHA256"),
    ):
        stable_fetch = DOCKERFILE.index(f"if wget -q -O /{package}.rpm")
        stable_fetch_end = DOCKERFILE.index("; then", stable_fetch)
        stable_checksum = DOCKERFILE.index(
            f'echo "${checksum}  /{package}.rpm" | sha256sum -c -', stable_fetch
        )
        qa_fallback = DOCKERFILE.index("else \\", stable_fetch_end)
        qa_checksum = DOCKERFILE.index(
            f'echo "${checksum}  /{package}.rpm" | sha256sum -c -', qa_fallback
        )

        assert stable_fetch_end < stable_checksum < qa_fallback < qa_checksum
    assert "unavailable or invalid" not in DOCKERFILE
    assert "myschedd-$MYSCHEDD_VERSION.rh9.cern.$RPM_ARCH.rpm" in DOCKERFILE
