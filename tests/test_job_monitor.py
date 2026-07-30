# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2019, 2020, 2021, 2022, 2023, 2024, 2026 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA-Job-Controller Job Monitor tests."""

import uuid

import mock
import pytest
from kubernetes.client.models import V1PodCondition

from reana_job_controller.job_monitor import (
    JobMonitorHTCondorCERN,
    JobMonitorKubernetes,
    JobMonitorSlurmCERN,
)


def test_if_singelton(app, mocked_job_managers):
    """Test if job monitor classes are singelton."""
    with mock.patch("reana_job_controller.job_monitor.threading"):
        first_k8s_instance = JobMonitorKubernetes(app=app)
        second_k8s_instance = JobMonitorKubernetes(app=app)
        assert first_k8s_instance is second_k8s_instance
        first_htc_instance = JobMonitorHTCondorCERN(app=app)
        second_htc_instance = JobMonitorHTCondorCERN(app=app)
        assert first_htc_instance is second_htc_instance


def test_initialisation(app):
    """Test initialisation of HTCondor job monitor."""
    with mock.patch("reana_job_controller.job_monitor.threading"):
        JobMonitorHTCondorCERN(app=app)
        JobMonitorKubernetes(app=app)
        JobMonitorSlurmCERN(app=app)


@pytest.mark.parametrize("exit_code,expected_status", [(0, "finished"), (1, "failed")])
def test_htcondor_finalises_job_after_promoting_output(exit_code, expected_status):
    """Publish the final job status only after output has been retrieved."""
    calls = mock.Mock()
    app = mock.MagicMock()
    manager = mock.MagicMock()
    manager.workflow_workspace = "/workspace"
    manager.promote_output.side_effect = calls.promote_output
    job = {
        "backend_job_id": 123,
        "deleted": False,
        "obj": manager,
    }

    def submit(function, *args, **kwargs):
        future = mock.Mock()
        if function == manager.spool_output:
            future.result.side_effect = calls.retrieve_output
        else:

            def read_logs():
                calls.read_logs()
                return "job logs"

            future.result.side_effect = read_logs
        return future

    app.htcondor_executor.submit.side_effect = submit
    with (
        mock.patch("reana_job_controller.job_monitor.threading"),
        mock.patch(
            "reana_job_controller.job_monitor.store_job_logs",
            side_effect=calls.store_logs,
        ) as store_job_logs,
        mock.patch(
            "reana_job_controller.job_monitor.update_job_status",
            side_effect=calls.update_status,
        ) as update_job_status,
    ):
        monitor = JobMonitorHTCondorCERN(app=app)
        monitor.job_manager_cls = manager
        monitor._finalise_completed_job(
            "reana-job-id", job, {"ExitCode": exit_code}, app
        )

    assert calls.mock_calls == [
        mock.call.retrieve_output(),
        mock.call.promote_output(),
        mock.call.read_logs(),
        mock.call.store_logs("reana-job-id", "job logs"),
        mock.call.update_status("reana-job-id", expected_status),
    ]
    store_job_logs.assert_called_once_with("reana-job-id", "job logs")
    update_job_status.assert_called_once_with("reana-job-id", expected_status)
    manager.stop.assert_not_called()
    assert job["deleted"] is True


def test_htcondor_fails_job_when_retrieving_output_fails():
    """Do not report success when retrieving the HTCondor output fails."""
    app = mock.MagicMock()
    manager = mock.MagicMock()
    manager.workflow_workspace = "/workspace"
    job = {
        "backend_job_id": 123,
        "deleted": False,
        "obj": manager,
    }
    future = mock.Mock()
    future.result.side_effect = RuntimeError("sandbox transfer failed")
    app.htcondor_executor.submit.return_value = future

    with (
        mock.patch("reana_job_controller.job_monitor.threading"),
        mock.patch("reana_job_controller.job_monitor.store_job_logs") as store_job_logs,
        mock.patch(
            "reana_job_controller.job_monitor.update_job_status"
        ) as update_job_status,
    ):
        monitor = JobMonitorHTCondorCERN(app=app)
        monitor.job_manager_cls = manager
        monitor._finalise_completed_job("reana-job-id", job, {"ExitCode": 0}, app)

    stored_logs = store_job_logs.call_args.args[1]
    assert "Failed to retrieve output" in stored_logs
    assert "sandbox transfer failed" in stored_logs
    update_job_status.assert_called_once_with("reana-job-id", "failed")
    assert app.htcondor_executor.submit.call_count == 1
    manager.stop.assert_called_once_with(123)
    manager.cleanup_file_transfer.assert_called_once_with()
    manager.promote_output.assert_not_called()
    assert job["deleted"] is True


def test_htcondor_fails_job_when_promoting_output_fails():
    """Do not report success when promoting the retrieved output fails."""
    app = mock.MagicMock()
    manager = mock.MagicMock()
    manager.workflow_workspace = "/workspace"
    manager.promote_output.side_effect = RuntimeError("workspace conflict")
    job = {"backend_job_id": 123, "deleted": False, "obj": manager}
    future = mock.Mock()
    future.result.return_value = None
    app.htcondor_executor.submit.return_value = future

    with (
        mock.patch("reana_job_controller.job_monitor.threading"),
        mock.patch("reana_job_controller.job_monitor.store_job_logs") as store_job_logs,
        mock.patch(
            "reana_job_controller.job_monitor.update_job_status"
        ) as update_job_status,
    ):
        monitor = JobMonitorHTCondorCERN(app=app)
        monitor.job_manager_cls = manager
        monitor._finalise_completed_job("reana-job-id", job, {"ExitCode": 0}, app)

    stored_logs = store_job_logs.call_args.args[1]
    assert "Failed to promote output" in stored_logs
    assert "workspace conflict" in stored_logs
    update_job_status.assert_called_once_with("reana-job-id", "failed")
    assert app.htcondor_executor.submit.call_count == 1
    manager.stop.assert_not_called()
    manager.cleanup_file_transfer.assert_called_once_with()
    assert job["deleted"] is True


def _watch_one_htcondor_iteration(monitor, job_db, app):
    """Run one monitor iteration before interrupting its polling loop."""
    with (
        mock.patch(
            "reana_job_controller.job_monitor.time.sleep",
            side_effect=KeyboardInterrupt,
        ),
        pytest.raises(KeyboardInterrupt),
    ):
        monitor.watch_jobs(job_db, app)


def test_htcondor_cleans_file_transfer_for_job_found_in_history():
    """Clean local staging when a missing queue job is found in history."""
    app = mock.MagicMock()
    query_future = mock.Mock()
    query_future.result.return_value = []
    history_future = mock.Mock()
    history_future.result.return_value = {"ClusterId": 123, "JobStatus": 4}
    app.htcondor_executor.submit.side_effect = [query_future, history_future]
    manager = mock.MagicMock()
    job = {
        "backend_job_id": 123,
        "compute_backend": "htcondorcern",
        "deleted": False,
        "obj": manager,
        "status": "running",
    }
    job_db = {"reana-job-id": job}

    with (
        mock.patch("reana_job_controller.job_monitor.threading"),
        mock.patch("reana_job_controller.job_monitor.store_job_logs") as store_logs,
        mock.patch(
            "reana_job_controller.job_monitor.update_job_status"
        ) as update_status,
    ):
        monitor = JobMonitorHTCondorCERN(app=app)
        monitor.job_manager_cls = mock.MagicMock()
        _watch_one_htcondor_iteration(monitor, job_db, app)

    update_status.assert_called_once_with("reana-job-id", "failed")
    store_logs.assert_called_once()
    manager.cleanup_file_transfer.assert_called_once_with()
    assert job["deleted"] is True


def test_htcondor_cleans_file_transfer_for_held_job():
    """Fail held jobs and clean their local staging directory."""
    app = mock.MagicMock()
    query_future = mock.Mock()
    query_future.result.return_value = [
        {"ClusterId": 123, "JobStatus": 5, "HoldReasonCode": 1}
    ]
    app.htcondor_executor.submit.return_value = query_future
    manager = mock.MagicMock()
    job = {
        "backend_job_id": 123,
        "compute_backend": "htcondorcern",
        "deleted": False,
        "obj": manager,
        "status": "running",
    }
    job_db = {"reana-job-id": job}

    with (
        mock.patch("reana_job_controller.job_monitor.threading"),
        mock.patch("reana_job_controller.job_monitor.store_job_logs") as store_logs,
        mock.patch(
            "reana_job_controller.job_monitor.update_job_status"
        ) as update_status,
    ):
        monitor = JobMonitorHTCondorCERN(app=app)
        monitor.job_manager_cls = mock.MagicMock()
        _watch_one_htcondor_iteration(monitor, job_db, app)

    monitor.job_manager_cls.stop.assert_called_once_with(123)
    store_logs.assert_called_once_with(
        "reana-job-id", "HTCondor job 123 was held with reason code 1."
    )
    update_status.assert_called_once_with("reana-job-id", "failed")
    manager.cleanup_file_transfer.assert_called_once_with()
    assert job["deleted"] is True


@pytest.mark.parametrize(
    "k8s_phase,k8s_container_state,expected_reana_status",
    [
        ("Pending", "ErrImagePull", "failed"),
        ("Pending", "InvalidImageName", "failed"),
        ("Succeeded", "Completed", "finished"),
        ("Failed", "Error", "failed"),
        ("Pending", ["Running", "ErrImagePull"], "failed"),
        ("Succeeded", "OOMKilled", "failed"),
    ],
)
def test_kubernetes_get_job_status(
    k8s_phase, k8s_container_state, expected_reana_status, app, kubernetes_job_pod
):
    """Test retrieval of job status."""
    with mock.patch("reana_job_controller.job_monitor.threading"):
        job_monitor_k8s = JobMonitorKubernetes(app=app)
        job_pod = kubernetes_job_pod(k8s_phase, k8s_container_state)
        assert job_monitor_k8s.get_job_status(job_pod) == expected_reana_status


def test_kubernetes_clean_job(app, mocked_job_managers):
    """Test clean jobs in the Kubernetes compute backend."""
    with mock.patch("reana_job_controller.job_monitor." "threading"):
        job_monitor_k8s = JobMonitorKubernetes(app=app)
        job_id = str(uuid.uuid4())
        job_metadata = {
            "deleted": False,
            "compute_backend": "kubernetes",
            "status": "finished",
            "backend_job_id": str(uuid.uuid4()),
        }
        job_monitor_k8s.job_db = {job_id: job_metadata}
        job_monitor_k8s.clean_job(job_metadata["backend_job_id"])
        kubernetes_job_manager = mocked_job_managers["kubernetes"]()
        assert kubernetes_job_manager.stop.called_once()
        assert job_monitor_k8s.job_db[job_id]["deleted"] is True


@pytest.mark.parametrize(
    "compute_backend,deleted,should_process",
    [
        ("slurm", False, False),
        ("htcondor", False, False),
        ("kubernetes", True, False),
        ("kubernetes", False, True),
    ],
)
def test_kubernetes_should_process_job(
    app, compute_backend, deleted, should_process, kubernetes_job_pod
):
    """Test should process job."""
    with mock.patch("reana_job_controller.job_monitor.threading"):
        job_monitor_k8s = JobMonitorKubernetes(app=app)
        job_id = str(uuid.uuid4())
        backend_job_id = str(uuid.uuid4())
        job_metadata = {
            "deleted": deleted,
            "compute_backend": compute_backend,
            "status": "running",
            "backend_job_id": backend_job_id,
        }
        job_monitor_k8s.job_db = {job_id: job_metadata}
        job_pod_event = kubernetes_job_pod(
            "Succeeded", "Completed", job_id=backend_job_id
        )

        assert bool(job_monitor_k8s.should_process_job(job_pod_event)) == should_process


@pytest.mark.parametrize(
    "conditions,is_call_expected,expected_message",
    [
        (
            [
                V1PodCondition(
                    type="PodScheduled",
                    status="True",
                ),
                V1PodCondition(
                    type="DisruptionTarget",
                    status="True",
                    reason="EvictionByEvictionAPI",
                    message="Eviction API: evicting",
                ),
                V1PodCondition(
                    type="Initialized",
                    status="True",
                ),
            ],
            True,
            "EvictionByEvictionAPI: Job backend_job_id was disrupted: Eviction API: evicting",
        ),
        (
            [
                V1PodCondition(
                    type="PodScheduled",
                    status="True",
                ),
                V1PodCondition(
                    type="Initialized",
                    status="True",
                ),
            ],
            False,
            "",
        ),
        (
            [],
            False,
            "",
        ),
    ],
)
def test_log_disruption_evicted(conditions, is_call_expected, expected_message):
    """Test logging of disruption target condition."""
    with (
        mock.patch("reana_job_controller.job_monitor.threading"),
        mock.patch("reana_job_controller.job_monitor.logging.warn") as log_mock,
    ):
        job_monitor_k8s = JobMonitorKubernetes(app=None)
        job_monitor_k8s.log_disruption(conditions, "backend_job_id")
        if is_call_expected:
            log_mock.assert_called_with(expected_message)
        else:
            log_mock.assert_not_called()
