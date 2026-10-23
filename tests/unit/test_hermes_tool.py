import pytest
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pipecatapp.tools.hermes_tool import HermesTool

def test_hermes_tool_init_and_schema():
    tool = HermesTool(sif_image="/opt/apptainer/images/test.sif")
    assert tool.name == "hermes_tool"
    schema = tool.get_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "hermes_tool"
    assert "run_hermes_cmd" in schema["function"]["parameters"]["properties"]["action"]["description"]

@patch('subprocess.run')
def test_hermes_tool_run_hermes_cmd_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="Hermes 1.0.0\n", stderr="")
    tool = HermesTool(sif_image="/opt/apptainer/images/test.sif")

    result = tool.run_hermes_cmd("version")
    assert result == "Hermes 1.0.0\n"

@patch('subprocess.run')
def test_hermes_tool_run_hermes_cmd_failure(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="command not found")
    tool = HermesTool(sif_image="/opt/apptainer/images/test.sif")

    result = tool.run_hermes_cmd("invalid_cmd")
    assert "Hermes Command Failed (Exit Code 1)" in result
    assert "command not found" in result

@patch('subprocess.run')
def test_hermes_tool_run_apptainer_task(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="task completed\n", stderr="")
    tool = HermesTool(sif_image="/opt/apptainer/images/test.sif")

    result = tool.execute("run_apptainer_task", kwargs={"command": "python3 -c 'print(1)'"})
    assert result == "task completed\n"
