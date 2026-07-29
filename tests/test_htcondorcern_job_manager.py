# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2026 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for the CERN HTCondor job manager."""

from unittest import mock

import pytest

classad = pytest.importorskip("classad2")
htcondor = pytest.importorskip("htcondor2")

from reana_job_controller import htcondorcern_job_manager  # noqa: E402
from reana_job_controller import job_monitor  # noqa: E402


@pytest.fixture
def manager_dependencies():
    """Patch the heavy dependencies of the HTCondor manager constructor."""
    mock_workflow = mock.MagicMock()
    mock_workflow.get_full_workflow_name.return_value = "wf"
    with mock.patch.object(
        htcondorcern_job_manager.HTCondorJobManagerCERN,
        "_get_workflow",
        return_value=mock_workflow,
    ), mock.patch.object(htcondorcern_job_manager, "initialize_krb5_token"):
        yield


@pytest.fixture
def manager(manager_dependencies):
    """Construct an HTCondor manager with its external dependencies patched."""
    return htcondorcern_job_manager.HTCondorJobManagerCERN(
        docker_img="img",
        cmd="ls",
        env_vars={},
        workflow_uuid="uuid",
        workflow_workspace="/data",
        job_name="job",
        htcondor_max_runtime="3600",
    )


@pytest.fixture
def captured_submit(manager_dependencies):
    """Patch ``execute()``'s side effects and capture the submit description.

    Returns a builder ``submit(**kwargs)`` that constructs the manager
    with the given kwargs, calls ``execute()``, and returns the
    ``htcondor2.Submit`` object that the manager would send to the schedd.
    """
    captured = {}

    def fake_executor_submit(_fn, submit):
        captured["submit"] = submit
        future = mock.MagicMock()
        future.result.return_value = "cluster123"
        return future

    fake_app = mock.MagicMock()
    fake_app.htcondor_executor.submit.side_effect = fake_executor_submit

    Manager = htcondorcern_job_manager.HTCondorJobManagerCERN
    with mock.patch.object(
        htcondorcern_job_manager, "current_app", fake_app
    ), mock.patch.object(htcondorcern_job_manager.os, "chdir"), mock.patch.object(
        Manager, "_format_arguments", return_value="echo|base64 -d"
    ), mock.patch.object(
        Manager, "_get_input_files", return_value=""
    ), mock.patch.object(
        Manager, "before_execution"
    ), mock.patch.object(
        Manager, "create_job_in_db"
    ):

        def build_and_execute(**kwargs):
            captured.clear()
            base = dict(
                docker_img="img",
                cmd="ls",
                env_vars={},
                workflow_uuid="uuid",
                workflow_workspace="/data",
                job_name="job",
                htcondor_max_runtime="3600",
            )
            base.update(kwargs)
            manager = Manager(**base)
            manager.execute()
            return captured["submit"]

        yield build_and_execute


# --- constructor wiring -------------------------------------------------------


def test_constructor_stores_htcondor_request_attributes(manager_dependencies):
    """Constructor must store the four new HTCondor request attributes."""
    manager = htcondorcern_job_manager.HTCondorJobManagerCERN(
        docker_img="img",
        cmd="ls",
        env_vars={},
        workflow_uuid="uuid",
        workflow_workspace="/data",
        job_name="job",
        htcondor_request_cpus="4",
        htcondor_request_memory="4000",
        htcondor_request_disk="100000",
        htcondor_requirements='(Arch =?= "aarch64")',
    )
    assert manager.htcondor_request_cpus == "4"
    assert manager.htcondor_request_memory == "4000"
    assert manager.htcondor_request_disk == "100000"
    assert manager.htcondor_requirements == '(Arch =?= "aarch64")'


def test_constructor_defaults_htcondor_request_attributes_to_empty(
    manager_dependencies,
):
    """When unset, the four new HTCondor request attributes default to empty."""
    manager = htcondorcern_job_manager.HTCondorJobManagerCERN(
        docker_img="img",
        cmd="ls",
        env_vars={},
        workflow_uuid="uuid",
        workflow_workspace="/data",
        job_name="job",
    )
    assert manager.htcondor_request_cpus == ""
    assert manager.htcondor_request_memory == ""
    assert manager.htcondor_request_disk == ""
    assert manager.htcondor_requirements == ""


# --- submit-description mapping in execute() ----------------------------------


def test_execute_builds_v2_submit_description(captured_submit):
    """The manager must use the v2 Submit API with string values."""
    submit = captured_submit()

    assert isinstance(submit, htcondor.Submit)
    assert submit["description"] == "wf_job"
    assert submit["executable"] == "./job_wrapper.sh"
    assert submit["MY.JobMaxRetries"] == "3"
    assert submit["MY.DockerImage"] == classad.quote("img")
    assert submit["MY.WantDocker"] == "True"
    assert submit["MY.DockerNetworkType"] == classad.quote("host")
    assert submit["MY.MaxRunTime"] == "3600"
    assert submit["MY.Requirements"] == "True"
    assert "log" not in submit.keys()
    assert all(isinstance(value, str) for value in submit.values())


def test_execute_preserves_unpacked_image_submission(captured_submit):
    """Unpacked images must keep using the generated Singularity wrapper."""
    submit = captured_submit(unpacked_img=True)

    assert submit["executable"] == "./job_singularity_wrapper.sh"
    assert "arguments" not in submit.keys()
    assert "MY.DockerImage" not in submit.keys()
    assert "MY.WantDocker" not in submit.keys()


def test_execute_sets_request_cpus_as_string(captured_submit):
    submit = captured_submit(htcondor_request_cpus="4")
    assert submit["request_cpus"] == "4"


def test_execute_converts_request_memory_to_mib(captured_submit):
    submit = captured_submit(htcondor_request_memory="4 GB")
    assert submit["request_memory"] == "4096"


def test_execute_rounds_up_request_memory(captured_submit):
    """A ``1 KB`` request must not silently become ``0`` MiB."""
    submit = captured_submit(htcondor_request_memory="1 KB")
    assert submit["request_memory"] == "1"


def test_execute_converts_request_disk_to_kib(captured_submit):
    submit = captured_submit(htcondor_request_disk="10 GB")
    assert submit["request_disk"] == "10485760"


def test_execute_sets_requirements_as_complete_classad_expression(captured_submit):
    submit = captured_submit(htcondor_requirements='(Arch =?= "aarch64")')
    rendered = submit["MY.Requirements"]
    expr = classad.ExprTree(rendered)

    assert isinstance(expr, classad.ExprTree)
    # Asserting on stable fragments rather than exact normal form, since
    # classad2's str() can vary in spacing/case across library versions.
    assert "Arch" in rendered
    assert "=?=" in rendered
    assert "aarch64" in rendered


def test_execute_formats_multiple_environment_variables(captured_submit):
    """Environment variables must use HTCondor's portable new syntax."""
    submit = captured_submit(env_vars={"CACHE": "on", "LABEL": "two words"})
    environment = submit["environment"]

    assert environment.startswith("\"'CACHE=on' 'LABEL=two words' ")
    assert "'REANA_WORKSPACE=/data'" in environment
    assert "'REANA_WORKFLOW_UUID=uuid'" in environment
    assert environment.endswith('"')


def test_format_env_vars_escapes_quotes(manager):
    """Environment syntax must preserve literal single and double quotes."""
    manager.env_vars = {"QUOTED": "a'b\"c"}

    assert manager._format_env_vars() == "\"'QUOTED=a''b\"\"c'\""


@pytest.mark.parametrize("forbidden_character", ["\n", "\r", "\x00"])
def test_execute_rejects_submit_command_injection(captured_submit, forbidden_character):
    """Untrusted values must not create additional submit-file lines."""
    job_name = "job{}MY.MaxRunTime = 999999".format(forbidden_character)

    with pytest.raises(ValueError, match="description"):
        captured_submit(job_name=job_name)


def test_execute_rejects_environment_command_injection(captured_submit):
    """Environment values must not inject additional submit-file lines."""
    env_vars = {"CACHE": "on\nMY.MaxRunTime = 999999"}

    with pytest.raises(ValueError, match="environment"):
        captured_submit(env_vars=env_vars)


def test_execute_omits_optional_request_attrs_when_absent(captured_submit):
    """Absent resource requests must not appear in the submit description."""
    submit = captured_submit()
    keys = submit.keys()

    assert "request_cpus" not in keys
    assert "request_memory" not in keys
    assert "request_disk" not in keys
    assert submit["MY.Requirements"] == "True"


# --- schedd interactions ------------------------------------------------------


def test_get_schedd_locates_configured_remote_schedd():
    """The v2 API must receive the remote schedd advertisement explicitly."""
    Manager = htcondorcern_job_manager.HTCondorJobManagerCERN
    schedd_host = "bigbird23.cern.ch"
    schedd_location = mock.sentinel.schedd_location
    schedd = mock.sentinel.schedd
    collector = mock.MagicMock()
    collector.locate.return_value = schedd_location
    mock_htcondor = mock.MagicMock()
    mock_htcondor.param = {"SCHEDD_HOST": schedd_host}
    mock_htcondor.Collector.return_value = collector
    mock_htcondor.Schedd.return_value = schedd

    with mock.patch.object(
        htcondorcern_job_manager, "htcondor", mock_htcondor
    ), mock.patch.object(
        htcondorcern_job_manager.thread_local,
        "MONITOR_THREAD_SCHEDD",
        None,
        create=True,
    ):
        assert Manager._get_schedd() is schedd
        assert Manager._get_schedd() is schedd

    collector.locate.assert_called_once_with(
        mock_htcondor.DaemonType.Schedd, schedd_host
    )
    mock_htcondor.Schedd.assert_called_once_with(schedd_location)


def test_get_schedd_does_not_fall_back_to_local_daemon():
    """A missing remote advertisement must not trigger local daemon lookup."""
    Manager = htcondorcern_job_manager.HTCondorJobManagerCERN
    collector = mock.MagicMock()
    collector.locate.return_value = None
    mock_htcondor = mock.MagicMock()
    mock_htcondor.param = {"SCHEDD_HOST": "missing.cern.ch"}
    mock_htcondor.Collector.return_value = collector

    with mock.patch.object(
        htcondorcern_job_manager, "htcondor", mock_htcondor
    ), mock.patch.object(
        htcondorcern_job_manager.thread_local,
        "MONITOR_THREAD_SCHEDD",
        None,
        create=True,
    ), pytest.raises(
        RuntimeError, match="missing.cern.ch"
    ):
        Manager._get_schedd.__wrapped__()

    mock_htcondor.Schedd.assert_not_called()


def test_submit_spools_submit_result_and_returns_cluster(manager):
    """A spooled v2 submission returns the cluster from SubmitResult."""
    submit = htcondor.Submit({"executable": "/bin/true"})
    result = mock.MagicMock()
    result.cluster.return_value = 123
    schedd = mock.MagicMock()
    schedd.submit.return_value = result
    Manager = htcondorcern_job_manager.HTCondorJobManagerCERN

    with mock.patch.object(
        Manager, "_get_schedd", return_value=schedd
    ), mock.patch.object(Manager, "_spool_input") as spool_input:
        assert manager._submit(submit) == 123

    schedd.submit.assert_called_once_with(submit, count=1, spool=True)
    spool_input.assert_called_once_with(result)


def test_spool_input_passes_submit_result_to_schedd():
    """The v2 spool API must receive the original SubmitResult."""
    result = mock.sentinel.submit_result
    schedd = mock.MagicMock()
    Manager = htcondorcern_job_manager.HTCondorJobManagerCERN

    with mock.patch.object(Manager, "_get_schedd", return_value=schedd):
        Manager._spool_input(result)

    schedd.spool.assert_called_once_with(result)


@pytest.mark.parametrize(
    "history, expected", [([], None), ([{"ClusterId": 123}], {"ClusterId": 123})]
)
def test_find_job_in_history_handles_v2_list_result(history, expected):
    """The v2 history API returns a list rather than an iterator."""
    schedd = mock.MagicMock()
    schedd.history.return_value = history
    Manager = htcondorcern_job_manager.HTCondorJobManagerCERN

    with mock.patch.object(Manager, "_get_schedd", return_value=schedd):
        assert Manager.find_job_in_history(123) == expected


def test_query_condor_jobs_uses_v2_query():
    """Job monitoring must use query(), because v2 removed xquery()."""
    expected_jobs = [{"ClusterId": 1}]
    schedd = mock.MagicMock()
    schedd.query.return_value = expected_jobs
    manager = mock.MagicMock()
    manager._get_schedd.return_value = schedd
    manager_factory = mock.MagicMock(return_value=manager)
    backend_job_ids = [1, 2]

    with mock.patch.dict(
        job_monitor.COMPUTE_BACKENDS, {"htcondorcern": manager_factory}
    ):
        assert job_monitor.query_condor_jobs(None, backend_job_ids) == expected_jobs

    schedd.query.assert_called_once_with(
        constraint=job_monitor.format_condor_job_que_query(backend_job_ids),
        projection=[
            "ClusterId",
            "JobStatus",
            "ExitCode",
            "ExitStatus",
            "HoldReasonCode",
        ],
    )
