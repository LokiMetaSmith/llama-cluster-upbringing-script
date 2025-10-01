import unittest
from unittest.mock import patch, MagicMock

# Import the class to be tested
from ssh_tool import SSH_Tool

class TestSSHTool(unittest.TestCase):

    def setUp(self):
        """Set up the tool instance for each test."""
        self.ssh_tool = SSH_Tool()

    @patch('ssh_tool.paramiko')
    def test_run_command_with_key_success(self, mock_paramiko):
        """Test successful command execution using key-based authentication."""
        # Configure the mock SSH client
        mock_client = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_client

        # Configure the mock for key loading
        mock_key = MagicMock()
        mock_paramiko.RSAKey.from_private_key_file.return_value = mock_key

        # Configure the mock for command execution
        mock_stdin, mock_stdout, mock_stderr = MagicMock(), MagicMock(), MagicMock()
        mock_stdout.read.return_value = b'command output'
        mock_stderr.read.return_value = b''
        mock_client.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)

        with patch('ssh_tool.os.path.expanduser', return_value='/home/user/.ssh/id_rsa') as mock_expanduser:
            result = self.ssh_tool.run_command(
                host='testhost',
                username='testuser',
                command='ls -l',
                key_filename='~/.ssh/id_rsa'
            )

            # Verify the results and mock calls
            self.assertEqual(result, 'command output')
            mock_expanduser.assert_called_once_with('~/.ssh/id_rsa')
            mock_paramiko.RSAKey.from_private_key_file.assert_called_once_with('/home/user/.ssh/id_rsa')
            mock_client.connect.assert_called_once_with('testhost', username='testuser', pkey=mock_key)
            mock_client.exec_command.assert_called_once_with('ls -l')
            mock_client.close.assert_called_once()

    @patch('ssh_tool.paramiko')
    def test_run_command_with_password_success(self, mock_paramiko):
        """Test successful command execution using password-based authentication."""
        mock_client = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_client
        mock_stdin, mock_stdout, mock_stderr = MagicMock(), MagicMock(), MagicMock()
        mock_stdout.read.return_value = b'password output'
        mock_stderr.read.return_value = b''
        mock_client.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)

        result = self.ssh_tool.run_command(
            host='testhost',
            username='testuser',
            command='whoami',
            password='secretpassword'
        )

        self.assertEqual(result, 'password output')
        mock_client.connect.assert_called_once_with('testhost', username='testuser', password='secretpassword')
        mock_client.exec_command.assert_called_once_with('whoami')

    @patch('ssh_tool.paramiko')
    def test_run_command_with_error(self, mock_paramiko):
        """Test command execution that results in an error."""
        mock_client = MagicMock()
        mock_paramiko.SSHClient.return_value = mock_client
        mock_stdin, mock_stdout, mock_stderr = MagicMock(), MagicMock(), MagicMock()
        mock_stdout.read.return_value = b''
        mock_stderr.read.return_value = b'permission denied'
        mock_client.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)

        result = self.ssh_tool.run_command(host='testhost', username='testuser', command='cat /root/file', password='p')
        self.assertEqual(result, 'Error executing command: permission denied')

    def test_no_auth_method_provided(self):
        """Test the case where no authentication method is given."""
        result = self.ssh_tool.run_command(host='testhost', username='testuser', command='ls')
        self.assertEqual(result, "Error: No authentication method provided. Use key_filename or password.")

    @patch('ssh_tool.paramiko.SSHClient')
    def test_connection_exception(self, mock_ssh_client):
        """Test that an exception during connection is handled gracefully."""
        mock_client_instance = mock_ssh_client.return_value
        mock_client_instance.connect.side_effect = Exception("Connection refused")

        result = self.ssh_tool.run_command(host='testhost', username='testuser', command='ls', password='p')
        self.assertEqual(result, "An error occurred: Connection refused")
        mock_client_instance.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()