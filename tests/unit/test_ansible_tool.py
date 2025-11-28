import pytest
import sys
import os
import subprocess
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from ansible_tool import Ansible_Tool

def test_ansible_tool_instantiation():
    """Tests that the Ansible_Tool class can be instantiated."""
    tool = Ansible_Tool()
    assert tool.name == "ansible_tool"
    assert tool.project_root == "/opt/cluster-infra"

@patch('subprocess.run')
@patch('os.path.exists', return_value=True)
def test_run_playbook_success(mock_exists, mock_run):
    """Tests a successful playbook run."""
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "Playbook output"
    mock_run.return_value = mock_process

    tool = Ansible_Tool()
    result = tool.run_playbook()

    assert "Playbook run completed successfully" in result
    mock_run.assert_called_once()

@patch('subprocess.run')
@patch('os.path.exists', return_value=True)
def test_run_playbook_with_args(mock_exists, mock_run):
    """Tests a playbook run with all arguments."""
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "Playbook output"
    mock_run.return_value = mock_process

    tool = Ansible_Tool()
    tool.run_playbook(playbook='test.yaml', limit='testhost', tags='testtag', extra_vars={'key': 'value'})

    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    assert args[0][2] == '--limit'
    assert args[0][3] == 'testhost'
    assert args[0][4] == '--tags'
    assert args[0][5] == 'testtag'
    assert args[0][6] == '--extra-vars'
    assert '{"key": "value"}' in args[0][7]

@patch('subprocess.run')
@patch('os.path.exists', return_value=True)
def test_run_playbook_failure(mock_exists, mock_run):
    """Tests a failed playbook run."""
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.stdout = "Playbook stdout"
    mock_process.stderr = "Playbook stderr"
    mock_run.return_value = mock_process

    tool = Ansible_Tool()
    result = tool.run_playbook()

    assert "Playbook run failed" in result
    assert "Playbook stderr" in result

@patch('os.path.exists', return_value=False)
def test_run_playbook_not_found(mock_exists):
    """Tests the case where the playbook file is not found."""
    tool = Ansible_Tool()
    result = tool.run_playbook()
    assert "Error: Playbook" in result and "not found" in result

@patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd='ansible-playbook', timeout=900))
@patch('os.path.exists', return_value=True)
def test_run_playbook_timeout(mock_exists, mock_run):
    """Tests a playbook run that times out."""
    tool = Ansible_Tool()
    result = tool.run_playbook()
    assert "Error: Ansible playbook run timed out" in result

@patch('subprocess.run', side_effect=Exception("Test exception"))
@patch('os.path.exists', return_value=True)
def test_run_playbook_unexpected_error(mock_exists, mock_run):
    """Tests an unexpected error during a playbook run."""
    tool = Ansible_Tool()
    result = tool.run_playbook()
    assert "An unexpected error occurred" in result
