import pytest
from ssh_tool import SSH_Tool
from unittest.mock import MagicMock

@pytest.fixture
def ssh_tool():
    return SSH_Tool()

def test_run_command_success(ssh_tool, mocker):
    """
    Test that run_command successfully executes a command.
    """
    # Mock the entire paramiko library
    mock_ssh_client = MagicMock()
    mock_ssh_client.exec_command.return_value = (None, MagicMock(read=lambda: b"success"), MagicMock(read=lambda: b""))

    mocker.patch('paramiko.SSHClient', return_value=mock_ssh_client)
    mocker.patch('paramiko.RSAKey.from_private_key_file')

    result = ssh_tool.run_command(host="localhost", username="test", command="ls", key_filename="dummy.key")

    assert result == "success"
    mock_ssh_client.connect.assert_called_with("localhost", username="test", pkey=mocker.ANY)
    mock_ssh_client.exec_command.assert_called_with("ls")

def test_run_command_error(ssh_tool, mocker):
    """
    Test that run_command returns an error message on failure.
    """
    mock_ssh_client = MagicMock()
    mock_ssh_client.exec_command.return_value = (None, MagicMock(read=lambda: b""), MagicMock(read=lambda: b"command not found"))

    mocker.patch('paramiko.SSHClient', return_value=mock_ssh_client)
    mocker.patch('paramiko.RSAKey.from_private_key_file')

    result = ssh_tool.run_command(host="localhost", username="test", command="badcommand", key_filename="dummy.key")

    assert "Error executing command: command not found" in result
