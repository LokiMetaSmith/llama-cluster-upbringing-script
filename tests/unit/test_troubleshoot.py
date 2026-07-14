import json
import pytest
from unittest.mock import patch, MagicMock

import importlib.util
import sys
import os

# Add repo root and pipecatapp to path to resolve imports correctly
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO_ROOT)

spec = importlib.util.spec_from_file_location("troubleshoot", "scripts/troubleshoot.py")
troubleshoot = importlib.util.module_from_spec(spec)
sys.modules["troubleshoot"] = troubleshoot
spec.loader.exec_module(troubleshoot)

@pytest.fixture
def mock_api_get():
    with patch('troubleshoot.api_get') as mock:
        yield mock

@pytest.fixture
def mock_run_command():
    with patch('troubleshoot.run_command') as mock:
        yield mock

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        self.job_id = None
        self.interval = 1
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_list_dead_pending(mock_api_get, capsys):
    mock_api_get.return_value = [
        {"ID": "job1", "Type": "service", "Status": "running"},
        {"ID": "job2", "Type": "service", "Status": "dead"},
        {"ID": "job3", "Type": "system", "Status": "pending"}
    ]

    args = DummyArgs(json=False)
    troubleshoot.cmd_list(args)

    captured = capsys.readouterr()
    assert "job2" in captured.out
    assert "job3" in captured.out
    assert "job1" not in captured.out

def test_list_dead_pending_json(mock_api_get, capsys):
    mock_api_get.return_value = [
        {"ID": "job1", "Type": "service", "Status": "running"},
        {"ID": "job2", "Type": "service", "Status": "dead"},
        {"ID": "job3", "Type": "system", "Status": "pending"}
    ]

    args = DummyArgs(json=True)
    troubleshoot.cmd_list(args)

    captured = capsys.readouterr()
    output_json = json.loads(captured.out)

    assert len(output_json) == 2
    assert output_json[0]["ID"] == "job2"
    assert output_json[1]["ID"] == "job3"

def test_inspect_job(mock_api_get, mock_run_command, capsys):
    def api_get_side_effect(endpoint):
        if endpoint == "/v1/job/job2":
            return {"ID": "job2", "Status": "dead", "SubmitTime": 1700000000000000000}
        elif endpoint == "/v1/job/job2/allocations":
            return [
                {
                    "ID": "alloc1",
                    "NodeID": "node1",
                    "ClientStatus": "failed",
                    "DesiredStatus": "run",
                    "CreateTime": 1700000000000000000,
                    "ModifyTime": 1700000000000000000,
                    "TaskStates": {
                        "web": {
                            "State": "dead",
                            "Failed": True,
                            "Events": [
                                {"Type": "Terminated", "Time": 1700000000000000000, "Message": "Exit code 1"}
                            ]
                        }
                    }
                }
            ]
        return None

    mock_api_get.side_effect = api_get_side_effect
    mock_run_command.return_value = {"exit_code": 0, "stdout": "error in app\n", "stderr": ""}

    args = DummyArgs(json=False, job_id="job2")
    troubleshoot.cmd_inspect(args)

    captured = capsys.readouterr()

    assert "Inspecting Job: job2" in captured.out
    assert "Status: dead" in captured.out
    assert "error in app" in captured.out

def test_retry_job(mock_run_command, capsys):
    mock_run_command.return_value = {"exit_code": 0, "stdout": "Job modified", "stderr": ""}

    args = DummyArgs(json=False, job_id="job2")
    troubleshoot.cmd_retry(args)

    captured = capsys.readouterr()
    assert "Successfully triggered restart for job job2" in captured.out

@patch('troubleshoot.run_legacy_command')
def test_report_job(mock_run_legacy_command, capsys):
    mock_run_legacy_command.return_value = "Mocked legacy output\n"

    args = DummyArgs(json=False)
    troubleshoot.cmd_report(args)

    captured = capsys.readouterr()
    assert "Report generation complete" in captured.out


def test_probe_health(mock_api_get, mock_run_command, capsys):
    """Verifies that the system-wide health probe returns correct JSON and prints formatted text."""
    # Mock Nomad API
    mock_api_get.return_value = [
        {"ID": "pipecat-app", "Type": "service", "Status": "running"},
        {"ID": "dead-expert", "Type": "service", "Status": "dead"}
    ]

    # Mock commands (Systemd show & Docker commands)
    def run_cmd_side_effect(command, shell=False):
        if "systemctl" in command and "show" in command:
            return {
                "exit_code": 0,
                "stdout": "ActiveState=active\nSubState=running\nLoadState=loaded\nUnitFileState=enabled\n",
                "stderr": ""
            }
        elif "systemctl" in command and "list-units" in command:
            return {
                "exit_code": 0,
                "stdout": "failed-service.service loaded failed failed Failed Service Description\n",
                "stderr": ""
            }
        elif "docker" in command and "ps" in command:
            return {
                "exit_code": 0,
                "stdout": "cid1|test-container|running|Up 2 hours\n",
                "stderr": ""
            }
        return {"exit_code": 0, "stdout": "", "stderr": ""}

    mock_run_command.side_effect = run_cmd_side_effect

    # Test JSON mode
    args_json = DummyArgs(json=True)
    report = troubleshoot.cmd_probe(args_json)

    assert report["summary"]["status"] == "degraded"
    assert len(report["nomad_jobs"]) == 2
    assert report["nomad_jobs"][0]["id"] == "pipecat-app"
    assert report["nomad_jobs"][1]["healthy"] is False

    # Test text print mode
    args_txt = DummyArgs(json=False)
    troubleshoot.cmd_probe(args_txt)
    captured = capsys.readouterr()
    assert "System Health Probe: DEGRADED" in captured.out
    assert "pipecat-app" in captured.out
    assert "dead-expert" in captured.out


def test_heal_services(mock_api_get, mock_run_command, capsys):
    """Verifies that healing triggers correct restart commands for failed jobs and services."""
    # 1. Mock the probe inside cmd_heal
    # Returns 1 failed Nomad job and 1 failed Systemd service
    def api_get_side_effect(endpoint):
        if endpoint == "/v1/jobs":
            return [{"ID": "pipecat-app", "Type": "service", "Status": "dead"}]
        elif endpoint == "/v1/job/pipecat-app/allocations":
            return [
                {
                    "ID": "failedalloc123",
                    "ModifyTime": 1700000000,
                    "TaskStates": {"pipecat": {"State": "dead", "Failed": True}}
                }
            ]
        return None
    mock_api_get.side_effect = api_get_side_effect

    def run_cmd_side_effect(command, shell=False):
        if "list-units" in command:
            # Report a failed systemd service
            return {"exit_code": 0, "stdout": "failed-service.service\n", "stderr": ""}
        elif "show" in command:
            if any("failed-service" in c for c in command):
                return {"exit_code": 0, "stdout": "ActiveState=failed\nSubState=failed\n", "stderr": ""}
            return {"exit_code": 0, "stdout": "ActiveState=active\nSubState=running\n", "stderr": ""}
        elif "docker" in command:
            return {"exit_code": 0, "stdout": "", "stderr": ""}
        elif "nomad" in command and "alloc" in command and "logs" in command:
            # Mock allocation logs returning 404
            return {"exit_code": 1, "stdout": "Unexpected response code: 404", "stderr": ""}
        elif "nomad" in command and "restart" in command:
            return {"exit_code": 0, "stdout": "Restarted Nomad job", "stderr": ""}
        elif "systemctl" in command and "restart" in command:
            return {"exit_code": 0, "stdout": "Restarted Systemd Service", "stderr": ""}
        return {"exit_code": 0, "stdout": "", "stderr": ""}

    mock_run_command.side_effect = run_cmd_side_effect

    # Run healing
    args = DummyArgs(json=True)
    troubleshoot.cmd_heal(args)

    captured = capsys.readouterr()
    assert "Attempting to force-run failed Nomad Job: pipecat-app" in captured.out
    assert "Attempting to force-run failed Systemd Service: failed-service" in captured.out
    assert "Restarting Systemd service failed-service" in captured.out


@patch("troubleshoot.time.sleep")
def test_daemon_loop(mock_sleep, mock_api_get, mock_run_command):
    """Verifies that daemon loops correctly and can exit."""
    # Force daemon loop to exit by raising StopIteration in time.sleep mock
    mock_sleep.side_effect = StopIteration

    mock_api_get.return_value = []
    mock_run_command.return_value = {"exit_code": 0, "stdout": "", "stderr": ""}

    args = DummyArgs(json=True, interval=1)
    with pytest.raises(StopIteration):
        troubleshoot.cmd_daemon(args)


def test_fetch_alloc_logs_with_fallback(mock_api_get, mock_run_command):
    """Verifies fallback log capturing when Nomad API returns 404."""
    # Mock standard nomad alloc logs failure
    def run_cmd_side_effect(command, shell=False):
        if "nomad" in command and "logs" in command:
            return {"exit_code": 1, "stdout": "Unexpected response code: 404", "stderr": ""}
        elif "docker" in command and "ps" in command:
            # Mock Docker finding a container matching allocation
            return {"exit_code": 0, "stdout": "docker-container-xyz\n", "stderr": ""}
        elif "docker" in command and "logs" in command:
            return {"exit_code": 0, "stdout": "Actual docker stderr fallback log line!", "stderr": ""}
        return {"exit_code": 0, "stdout": "", "stderr": ""}

    mock_run_command.side_effect = run_cmd_side_effect

    # Mock allocation status details
    mock_api_get.return_value = {
        "ID": "alloc123",
        "TaskStates": {
            "web": {
                "State": "dead",
                "Events": [
                    {"Time": 1700000000000000000, "Type": "DriverError", "Message": "Docker container died on startup"}
                ]
            }
        }
    }

    logs = troubleshoot.fetch_alloc_logs_with_fallback("alloc123", "web", "stderr")

    assert "[LOG FALLBACK]" in logs
    assert "DriverError" in logs
    assert "Docker container died on startup" in logs
    assert "Actual docker stderr fallback log line!" in logs
