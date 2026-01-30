import unittest
from unittest.mock import MagicMock, patch
import os
from pipecatapp.tools.git_tool import Git_Tool

class TestGitTool(unittest.TestCase):
    def setUp(self):
        self.tool = Git_Tool()

    @patch("pipecatapp.tools.git_tool.subprocess.run")
    def test_ls_files(self, mock_run):
        # Setup mock
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "file1.txt\nfile2.py"
        mock_run.return_value = mock_process

        # Run method
        result = self.tool.ls_files(".")

        # Assertions
        expected_cmd = ["git", "ls-files"]
        # The working_dir will be resolved to absolute path by _validate_path
        # We can check that the command was called
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], expected_cmd)
        self.assertIn("Command successful", result)
        self.assertIn("file1.txt", result)

    def test_ls_files_integration(self):
        # Real integration test on the current repo
        result = self.tool.ls_files(".")
        print(f"Integration test result: {result}")
        self.assertIn("Command successful", result)
        self.assertIn("pipecatapp/tools/git_tool.py", result)

if __name__ == "__main__":
    unittest.main()
