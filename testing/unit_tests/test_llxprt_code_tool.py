import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import subprocess

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from llxprt_code_tool import LLxprt_Code_Tool

@pytest.fixture
def llxprt_tool():
    return LLxprt_Code_Tool()

@patch('subprocess.run')
def test_run_success(mock_run, llxprt_tool):
    """Test a successful command execution."""
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "Command finished successfully."
    mock_process.stderr = ""
    mock_run.return_value = mock_process

    result = llxprt_tool.run('command')

    assert "llxprt-code command run completed successfully" in result
    assert "Command finished successfully" in result
    mock_run.assert_called_once_with(
        ['llxprt', 'command'],
        capture_output=True,
        text=True,
        timeout=300
    )

@patch('subprocess.run')
def test_run_with_args_success(mock_run, llxprt_tool):
    """Test a successful command execution with arguments."""
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "Command finished successfully."
    mock_process.stderr = ""
    mock_run.return_value = mock_process

    result = llxprt_tool.run('review --file=foo.py')

    assert "llxprt-code command run completed successfully" in result
    assert "Command finished successfully" in result
    mock_run.assert_called_once_with(
        ['llxprt', 'review', '--file=foo.py'],
        capture_output=True,
        text=True,
        timeout=300
    )

@patch('subprocess.run')
def test_run_failure(mock_run, llxprt_tool):
    """Test a failed command execution."""
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.stdout = "Something went wrong."
    mock_process.stderr = "Error details."
    mock_run.return_value = mock_process

    result = llxprt_tool.run('command')

    assert "llxprt-code command run failed with return code 1" in result
    assert "STDOUT:\nSomething went wrong." in result
    assert "STDERR:\nError details." in result

@patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd="llxprt", timeout=300, output="Timed out stdout.", stderr="Timed out stderr."))
def test_run_timeout(mock_run, llxprt_tool):
    """Test a command execution that times out."""
    result = llxprt_tool.run('command')
    assert "Error: llxprt-code command run timed out after 5 minutes." in result
    assert "STDOUT:\nTimed out stdout." in result
    assert "STDERR:\nTimed out stderr." in result

@patch('subprocess.run', side_effect=FileNotFoundError)
def test_command_not_found(mock_run, llxprt_tool):
    """Test when the llxprt command is not found."""
    result = llxprt_tool.run('command')
    assert result == "Error: `llxprt` command not found. Is it installed and in the system's PATH?"

def test_empty_command(llxprt_tool):
    """Test when an empty command is provided."""
    result = llxprt_tool.run('')
    assert result == "Error: command cannot be empty."
