import json
import pytest
from unittest.mock import patch, MagicMock

# Dynamically import troubleshoot as it is a script
import importlib.util
import sys
import os

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
