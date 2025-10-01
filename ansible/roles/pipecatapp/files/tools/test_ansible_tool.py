import unittest
from unittest.mock import patch, MagicMock
import subprocess

# Assume ansible_tool is in the same directory or adjust path as needed
from ansible_tool import Ansible_Tool

class TestAnsibleTool(unittest.TestCase):

    def setUp(self):
        """Set up the tool instance before each test."""
        self.ansible_tool = Ansible_Tool()
        # We can override the project root for testing purposes if needed
        self.ansible_tool.project_root = "/tmp/fake_ansible"

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_run_playbook_success(self, mock_run, mock_exists):
        """Test a successful playbook execution."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Playbook finished successfully."
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        result = self.ansible_tool.run_playbook('test.yaml')

        self.assertIn("Playbook run completed successfully", result)
        self.assertIn("Playbook finished successfully", result)
        mock_run.assert_called_once()
        self.assertEqual(mock_run.call_args[0][0], ['ansible-playbook', '/tmp/fake_ansible/test.yaml'])

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_run_playbook_failure(self, mock_run, mock_exists):
        """Test a failed playbook execution."""
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = "Something went wrong."
        mock_process.stderr = "Error details."
        mock_run.return_value = mock_process

        result = self.ansible_tool.run_playbook('test.yaml')

        self.assertIn("Playbook run failed with return code 1", result)
        self.assertIn("STDOUT:\nSomething went wrong.", result)
        self.assertIn("STDERR:\nError details.", result)

    @patch('os.path.exists', return_value=False)
    def test_run_playbook_not_found(self, mock_exists):
        """Test when the playbook file does not exist."""
        result = self.ansible_tool.run_playbook('nonexistent.yaml')
        self.assertEqual(result, "Error: Playbook '/tmp/fake_ansible/nonexistent.yaml' not found.")

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd="ansible-playbook", timeout=900, output="Timed out stdout.", stderr="Timed out stderr."))
    def test_run_playbook_timeout(self, mock_run, mock_exists):
        """Test a playbook execution that times out."""
        result = self.ansible_tool.run_playbook('test.yaml')
        self.assertIn("Error: Ansible playbook run timed out after 15 minutes.", result)
        self.assertIn("STDOUT:\nTimed out stdout.", result)
        self.assertIn("STDERR:\nTimed out stderr.", result)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_run_playbook_with_all_args(self, mock_run, mock_exists):
        """Test running a playbook with limit, tags, and extra_vars."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Success"
        mock_run.return_value = mock_process

        extra_vars = {"key": "value", "another_key": 123}
        self.ansible_tool.run_playbook(
            playbook='test.yaml',
            limit='testhost',
            tags='setup,configure',
            extra_vars=extra_vars
        )

        expected_command = [
            'ansible-playbook', '/tmp/fake_ansible/test.yaml',
            '--limit', 'testhost',
            '--tags', 'setup,configure',
            '--extra-vars', '{"key": "value", "another_key": 123}'
        ]
        mock_run.assert_called_once_with(
            expected_command,
            cwd="/tmp/fake_ansible",
            capture_output=True,
            text=True,
            timeout=900
        )

if __name__ == '__main__':
    unittest.main()