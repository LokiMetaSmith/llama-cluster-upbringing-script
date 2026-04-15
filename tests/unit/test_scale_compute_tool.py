import pytest
import os
from unittest.mock import MagicMock, patch
from pipecatapp.tools.scale_compute_tool import ScaleComputeTool

def test_scale_compute_tool_initialization():
    tool = ScaleComputeTool()
    assert tool.name == "scale_compute"

@patch("os.path.exists", return_value=False)
def test_scale_missing_script(mock_exists):
    tool = ScaleComputeTool()
    res = tool.scale("192.168.1.100")
    assert "Could not find bootstrap.sh" in res

@patch("os.path.exists", return_value=True)
@patch("subprocess.run")
def test_scale_success(mock_run, mock_exists):
    mock_run.return_value = MagicMock(returncode=0, stdout="Success output", stderr="")
    tool = ScaleComputeTool()
    res = tool.scale("192.168.1.100")
    assert "Success" in res
    assert "Success output" in res

@patch("os.path.exists", return_value=True)
@patch("subprocess.run")
def test_scale_failure(mock_run, mock_exists):
    mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Error output")
    tool = ScaleComputeTool()
    res = tool.scale("192.168.1.100")
    assert "Failed to add node" in res
    assert "Error output" in res

def test_execute():
    tool = ScaleComputeTool()

    with patch.object(tool, 'scale', return_value="Scaled"):
        res = tool.execute({"node_ip": "10.0.0.1"})
        assert res == "Scaled"

def test_execute_missing_arg():
    tool = ScaleComputeTool()
    res = tool.execute({})
    assert "node_ip is required" in res
