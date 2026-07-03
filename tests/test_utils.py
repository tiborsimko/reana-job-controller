# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2024, 2026 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import logging
from unittest import mock

import pytest

import reana_job_controller.utils as utils
from reana_job_controller.utils import MultilineFormatter

"""REANA-Job-Controller utils tests."""


@pytest.mark.parametrize(
    "message,expected_output",
    [
        (
            "test",
            "name | INFO | test",
        ),
        (
            "test\n",
            "name | INFO | test",
        ),
        (
            "test\ntest",
            "name | INFO | test\nname | INFO | test",
        ),
        (
            "test\ntest\n\n\n",
            "name | INFO | test\nname | INFO | test\nname | INFO | \nname | INFO |",
        ),
        (
            "   test\ntest   ",
            "name | INFO |    test\nname | INFO | test",
        ),
        (
            "   t e s\tt\n     t e s t   ",
            "name | INFO |    t e s\tt\nname | INFO |      t e s t",
        ),
    ],
)
def test_multiline_formatter_format(message, expected_output):
    """Test MultilineFormatter formatting."""
    formatter = MultilineFormatter("%(name)s | " "%(levelname)s | %(message)s")
    assert (
        formatter.format(
            logging.LogRecord(
                "name",
                logging.INFO,
                "pathname",
                1,
                message,
                None,
                None,
            ),
        )
        == expected_output
    )


def test_ssh_client_uses_resolved_ipv4_for_connection_and_hostname_for_gss():
    """Test SSHClient keeps hostname as Kerberos target when PTR is unavailable."""
    ssh_client = mock.MagicMock()
    paramiko_mock = mock.MagicMock()
    paramiko_mock.SSHClient.return_value = ssh_client

    with (
        mock.patch.object(
            utils.SSHClient.__closure__[0].cell_contents, "paramiko", paramiko_mock
        ),
        mock.patch.object(
            utils.socket,
            "gethostbyname_ex",
            return_value=("slurm.example.org", [], ["10.0.0.10"]),
        ),
        mock.patch.object(utils.socket, "getfqdn", return_value="10.0.0.10"),
    ):
        utils.SSHClient.__closure__[1].cell_contents.clear()
        try:
            utils.SSHClient(hostname="slurm.example.org", port=22)
        finally:
            utils.SSHClient.__closure__[1].cell_contents.clear()

    ssh_client.connect.assert_called_once_with(
        hostname="10.0.0.10",
        allow_agent=False,
        auth_timeout=None,
        banner_timeout=None,
        gss_auth=True,
        gss_host="slurm.example.org",
        gss_trust_dns=False,
        look_for_keys=False,
        port=22,
        timeout=None,
        auth_strategy=None,
    )


def test_ssh_client_uses_reverse_dns_name_for_gss_when_available():
    """Test SSHClient uses selected IPv4 PTR name as Kerberos target."""
    ssh_client = mock.MagicMock()
    paramiko_mock = mock.MagicMock()
    paramiko_mock.SSHClient.return_value = ssh_client

    with (
        mock.patch.object(
            utils.SSHClient.__closure__[0].cell_contents, "paramiko", paramiko_mock
        ),
        mock.patch.object(
            utils.socket,
            "gethostbyname_ex",
            return_value=("slurm.example.org", [], ["10.0.0.11"]),
        ),
        mock.patch.object(
            utils.socket, "getfqdn", return_value="slurmgate01.example.org"
        ),
    ):
        utils.SSHClient.__closure__[1].cell_contents.clear()
        try:
            utils.SSHClient(hostname="slurm.example.org", port=22)
        finally:
            utils.SSHClient.__closure__[1].cell_contents.clear()

    ssh_client.connect.assert_called_once_with(
        hostname="10.0.0.11",
        allow_agent=False,
        auth_timeout=None,
        banner_timeout=None,
        gss_auth=True,
        gss_host="slurmgate01.example.org",
        gss_trust_dns=False,
        look_for_keys=False,
        port=22,
        timeout=None,
        auth_strategy=None,
    )


def test_ssh_client_prefers_explicit_gss_host():
    """Test SSHClient supports overriding the Kerberos target."""
    ssh_client = mock.MagicMock()
    paramiko_mock = mock.MagicMock()
    paramiko_mock.SSHClient.return_value = ssh_client

    with (
        mock.patch.object(
            utils.SSHClient.__closure__[0].cell_contents, "paramiko", paramiko_mock
        ),
        mock.patch.object(
            utils.socket,
            "gethostbyname_ex",
            return_value=("slurm.example.org", [], ["10.0.0.11"]),
        ),
        mock.patch.object(utils.socket, "getfqdn") as getfqdn,
    ):
        utils.SSHClient.__closure__[1].cell_contents.clear()
        try:
            utils.SSHClient(
                hostname="slurm.example.org",
                gss_host="slurmgate04.example.org",
                port=22,
            )
        finally:
            utils.SSHClient.__closure__[1].cell_contents.clear()

    getfqdn.assert_not_called()
    ssh_client.connect.assert_called_once_with(
        hostname="10.0.0.11",
        allow_agent=False,
        auth_timeout=None,
        banner_timeout=None,
        gss_auth=True,
        gss_host="slurmgate04.example.org",
        gss_trust_dns=False,
        look_for_keys=False,
        port=22,
        timeout=None,
        auth_strategy=None,
    )
