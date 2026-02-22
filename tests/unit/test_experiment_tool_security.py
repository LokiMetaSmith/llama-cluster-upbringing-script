import unittest
import os
import sys
import shutil
import tempfile
from unittest.mock import MagicMock, patch

# Ensure pipecatapp is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
# Add pipecatapp folder to path so 'import tools' works (legacy import style)
sys.path.append(os.path.join(project_root, 'pipecatapp'))

from pipecatapp.tools.experiment_tool import ExperimentTool

class TestExperimentToolSecurity(unittest.TestCase):
    def setUp(self):
        self.tool = ExperimentTool()

        # Mock os.path.exists and shutil.copytree to avoid needing actual source code
        self.original_exists = os.path.exists
        self.original_copytree = shutil.copytree

        self.exists_patcher = patch('os.path.exists')
        self.mock_exists = self.exists_patcher.start()
        self.mock_exists.side_effect = self._mock_exists

        self.copytree_patcher = patch('shutil.copytree')
        self.mock_copytree = self.copytree_patcher.start()

    def tearDown(self):
        self.exists_patcher.stop()
        self.copytree_patcher.stop()

    def _mock_exists(self, path):
        if path == "/opt/pipecatapp":
            return True
        return self.original_exists(path)

    def test_command_injection_prevention(self):
        """Test that command injection attempts fail."""
        artifact = {
            "file_path": "solution.py",
            "content": "print('Hello')"
        }

        # Attempt to inject a command
        # With shell=False, this will look for an executable named "true;" which fails
        test_command = "true; echo 'vulnerable'"

        result = self.tool._run_sandbox_eval(artifact, test_command)

        self.assertFalse(result["passed"])
        self.assertIn("No such file or directory", result["output"])

    def test_valid_command_execution(self):
        """Test that valid commands execute correctly."""
        artifact = {
            "file_path": "solution.py",
            "content": "print('Hello')"
        }

        # Valid command
        test_command = "echo Hello"

        result = self.tool._run_sandbox_eval(artifact, test_command)

        self.assertTrue(result["passed"])
        self.assertIn("Hello", result["output"])

    def test_quoted_arguments(self):
        """Test that quoted arguments are handled correctly by shlex."""
        artifact = {
            "file_path": "solution.py",
            "content": "print('Hello')"
        }

        test_command = 'echo "Hello World"'

        result = self.tool._run_sandbox_eval(artifact, test_command)

        self.assertTrue(result["passed"])
        self.assertIn("Hello World", result["output"])

    def test_artifact_size_limit(self):
        """Test that large artifacts are rejected."""
        large_content = "A" * (1024 * 1024 + 1) # 1MB + 1 byte
        artifact = {
            "file_path": "solution.py",
            "content": large_content
        }

        test_command = "echo Hello"

        result = self.tool._run_sandbox_eval(artifact, test_command)

        self.assertFalse(result["passed"])
        self.assertIn("Artifact too large", result["output"])

if __name__ == '__main__':
    unittest.main()
