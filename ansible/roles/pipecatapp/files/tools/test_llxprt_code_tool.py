import unittest
from unittest.mock import patch, MagicMock
import subprocess

# Assume llxprt_code_tool is in the same directory
from .llxprt_code_tool import LLxprt_Code_Tool

class TestLLxprtCodeTool(unittest.TestCase):

    def setUp(self):
        """Set up the tool instance before each test."""
        self.llxprt_tool = LLxprt_Code_Tool()

    @patch('subprocess.run')
    def test_run_success(self, mock_run):
        """Test a successful command execution."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Command finished successfully."
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        result = self.llxprt_tool.run('command')

        self.assertIn("llxprt-code command run completed successfully", result)
        self.assertIn("Command finished successfully", result)
        mock_run.assert_called_once_with(
            ['llxprt', 'command'],
            capture_output=True,
            text=True,
            timeout=300
        )

    @patch('subprocess.run')
    def test_run_with_args_success(self, mock_run):
        """Test a successful command execution with arguments."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Command finished successfully."
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        result = self.llxprt_tool.run('review --file=foo.py')

        self.assertIn("llxprt-code command run completed successfully", result)
        self.assertIn("Command finished successfully", result)
        mock_run.assert_called_once_with(
            ['llxprt', 'review', '--file=foo.py'],
            capture_output=True,
            text=True,
            timeout=300
        )

    @patch('subprocess.run')
    def test_run_failure(self, mock_run):
        """Test a failed command execution."""
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = "Something went wrong."
        mock_process.stderr = "Error details."
        mock_run.return_value = mock_process

        result = self.llxprt_tool.run('command')

        self.assertIn("llxprt-code command run failed with return code 1", result)
        self.assertIn("STDOUT:\nSomething went wrong.", result)
        self.assertIn("STDERR:\nError details.", result)

    @patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd="llxprt", timeout=300, output="Timed out stdout.", stderr="Timed out stderr."))
    def test_run_timeout(self, mock_run):
        """Test a command execution that times out."""
        result = self.llxprt_tool.run('command')
        self.assertIn("Error: llxprt-code command run timed out after 5 minutes.", result)
        self.assertIn("STDOUT:\nTimed out stdout.", result)
        self.assertIn("STDERR:\nTimed out stderr.", result)

    @patch('subprocess.run', side_effect=FileNotFoundError)
    def test_command_not_found(self, mock_run):
        """Test when the llxprt command is not found."""
        result = self.llxprt_tool.run('command')
        self.assertEqual(result, "Error: `llxprt` command not found. Is it installed and in the system's PATH?")

    def test_empty_command(self):
        """Test when an empty command is provided."""
        result = self.llxprt_tool.run('')
        self.assertEqual(result, "Error: command cannot be empty.")

if __name__ == '__main__':
    unittest.main()
