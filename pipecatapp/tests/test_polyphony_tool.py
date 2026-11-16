import pytest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.polyphony_tool import PolyphonyTool

def test_polyphony_tool_schema_and_info():
    tool = PolyphonyTool()
    schema = tool.get_schema()
    assert schema["type"] == "function"
    assert "baton_acquire" in schema["function"]["parameters"]["properties"]["action"]["enum"]
    assert "baton_release" in schema["function"]["parameters"]["properties"]["action"]["enum"]
    assert "task_claim" in schema["function"]["parameters"]["properties"]["action"]["enum"]

    info = tool.get_info()
    assert info["name"] == "polyphony_tool"
    assert "baton_acquire" in info["parameters"]["properties"]["action"]["enum"]

def test_polyphony_tool_get_info_via_execute():
    tool = PolyphonyTool()
    info = tool.execute("get_info")
    assert isinstance(info, dict)
    assert info["name"] == "polyphony_tool"

@patch("pipecatapp.tools.polyphony_tool.CommandRunner.run")
@patch("os.path.exists", return_value=True)
def test_polyphony_tool_actions(mock_exists, mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")

    tool = PolyphonyTool()

    # Share
    res = tool.execute("share", thought="Hello world")
    assert res == "Success"
    mock_run.assert_called_with([tool.cli_path, "share", "Hello world"], env=mock_run.call_args[1]["env"], capture_output=True, text=True)

    # Baton acquire
    res = tool.execute("baton_acquire", resource="file.py")
    assert res == "Success"
    mock_run.assert_called_with([tool.cli_path, "baton", "acquire", "file.py"], env=mock_run.call_args[1]["env"], capture_output=True, text=True)

    # Baton release
    res = tool.execute("baton_release", resource="file.py")
    assert res == "Success"
    mock_run.assert_called_with([tool.cli_path, "baton", "release", "file.py"], env=mock_run.call_args[1]["env"], capture_output=True, text=True)

    # Task claim
    res = tool.execute("task_claim", task_id="task-123")
    assert res == "Success"
    mock_run.assert_called_with([tool.cli_path, "task", "claim", "task-123"], env=mock_run.call_args[1]["env"], capture_output=True, text=True)

    # Task complete
    res = tool.execute("task_complete", task_id="task-123")
    assert res == "Success"
    mock_run.assert_called_with([tool.cli_path, "task", "complete", "task-123"], env=mock_run.call_args[1]["env"], capture_output=True, text=True)

    # Status
    res = tool.execute("status")
    assert res == "Success"
    mock_run.assert_called_with([tool.cli_path, "status"], env=mock_run.call_args[1]["env"], capture_output=True, text=True)

def test_polyphony_tool_missing_params():
    tool = PolyphonyTool()
    assert "required" in tool.execute("share")
    assert "required" in tool.execute("ping")
    assert "required" in tool.execute("task_add")
    assert "required" in tool.execute("task_claim")
    assert "required" in tool.execute("task_complete")
    assert "required" in tool.execute("baton_acquire")
    assert "required" in tool.execute("baton_release")
    assert "Unknown action" in tool.execute("non_existent_action")
