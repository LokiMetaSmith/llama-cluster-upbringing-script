import os
import pytest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.zpm_tool import ZeroPointModulatorTool, ZPMTool

def test_zpm_tool_schema_and_alias():
    tool = ZeroPointModulatorTool()
    assert tool == ZPMTool() or isinstance(tool, ZPMTool)

    schema = tool.get_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "zpm_tool"
    assert "status" in schema["function"]["parameters"]["properties"]["action"]["enum"]
    assert "reconcile" in schema["function"]["parameters"]["properties"]["action"]["enum"]
    assert "target" in schema["function"]["parameters"]["properties"]["action"]["enum"]

    info = tool.get_info()
    assert info["name"] == "zpm_tool"

def test_zpm_path_validation_security(tmp_path):
    root = str(tmp_path)
    tool = ZeroPointModulatorTool(root_dir=root)

    safe_file = tmp_path / "config.json"
    safe_file.write_text("{}")

    validated = tool._validate_path(str(safe_file))
    assert validated == os.path.realpath(str(safe_file))

    # Path traversal with .. outside root
    with pytest.raises(ValueError, match="Path traversal detected"):
        tool._validate_path("../../etc/passwd")

@patch("pipecatapp.tools.zpm_tool.CommandRunner.run")
def test_zpm_tool_actions(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=0, stdout="ZPM Output", stderr="")

    state_file = str(tmp_path / "state.sqlite3")
    tool = ZeroPointModulatorTool(state_file=state_file, deployment_id="test-deploy", root_dir=str(tmp_path))

    # Status
    res = tool.execute("status")
    assert res == "ZPM Output"
    assert "status" in mock_run.call_args[0][0]

    # Plan
    res = tool.execute("plan")
    assert res == "ZPM Output"
    assert "plan" in mock_run.call_args[0][0]

    # Target
    res = tool.execute("target", repository="owner/repo", target_workers=3)
    assert res == "ZPM Output"
    assert "target" in mock_run.call_args[0][0]
    assert "3" in mock_run.call_args[0][0]

    # Pause
    res = tool.execute("pause", repository="owner/repo")
    assert res == "ZPM Output"
    assert "pause" in mock_run.call_args[0][0]

    # Resume
    res = tool.execute("resume", repository="owner/repo", target_workers=2)
    assert res == "ZPM Output"
    assert "resume" in mock_run.call_args[0][0]
    assert "2" in mock_run.call_args[0][0]

    # Remove
    res = tool.execute("remove", repository="owner/repo")
    assert res == "ZPM Output"
    assert "remove" in mock_run.call_args[0][0]

    # Reconcile
    provider_file = tmp_path / "provider.json"
    provider_file.write_text("{}")
    res = tool.execute("reconcile", provider_file=str(provider_file), max_actions=5)
    assert res == "ZPM Output"
    assert "reconcile" in mock_run.call_args[0][0]
    assert "--max-actions" in mock_run.call_args[0][0]
    assert "5" in mock_run.call_args[0][0]

def test_zpm_tool_missing_params():
    tool = ZeroPointModulatorTool()
    assert "required" in tool.execute("enroll")
    assert "required" in tool.execute("target")
    assert "required" in tool.execute("pause")
    assert "required" in tool.execute("resume")
    assert "required" in tool.execute("remove")
    assert "required" in tool.execute("validate")
    assert "required" in tool.execute("reconcile")
    assert "Unknown action" in tool.execute("fake_action")
