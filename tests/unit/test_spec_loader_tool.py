import unittest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.spec_loader_tool import SpecLoaderTool

class TestSpecLoaderSecurity(unittest.TestCase):
    def setUp(self):
        self.tool = SpecLoaderTool(work_dir="/tmp/test_specs")

    @patch("subprocess.run")
    def test_dangerous_protocol(self, mock_run):
        # Test with file:// protocol
        result = self.tool.clone_and_ingest("file:///etc/passwd", "passwd_repo")
        self.assertIn("Security Error", result)
        mock_run.assert_not_called()

    @patch("subprocess.run")
    def test_argument_injection(self, mock_run):
        # Test with argument injection
        result = self.tool.clone_and_ingest("-v", "repo")
        self.assertIn("Security Error", result)
        mock_run.assert_not_called()

    @patch("subprocess.run")
    def test_path_traversal(self, mock_run):
        # Test with path traversal in repo_name
        result = self.tool.clone_and_ingest("https://github.com/user/repo.git", "../../../etc/passwd")
        self.assertIn("Security Error", result)
        mock_run.assert_not_called()

    @patch("subprocess.run")
    def test_symlink_path_traversal(self, mock_run):
        import os
        import tempfile
        import shutil

        # Create a temporary environment to test symlinks
        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = os.path.join(temp_dir, "work_dir")
            secret_dir = os.path.join(temp_dir, "secret_dir")
            os.makedirs(work_dir)
            os.makedirs(secret_dir)

            # Create a secret file outside the work_dir
            secret_file = os.path.join(secret_dir, "secret.txt")
            with open(secret_file, "w") as f:
                f.write("SUPER SECRET")

            # Create a symlink in work_dir pointing to secret_dir
            symlink_path = os.path.join(work_dir, "symlink")
            os.symlink(secret_dir, symlink_path)

            # Re-initialize tool with new temp work_dir
            self.tool = SpecLoaderTool(work_dir=work_dir)

            # The tool should reject the path because realpath resolves the symlink
            # and sees it points outside work_dir
            with self.assertRaises(ValueError) as context:
                self.tool._validate_path("symlink/secret.txt")

            self.assertIn("Security Error: Access denied", str(context.exception))

    @patch("subprocess.run")
    def test_valid_clone(self, mock_run):
        # Test with valid inputs
        mock_run.return_value = MagicMock(returncode=0)
        # Mock _scan_files to avoid file system interaction
        with patch.object(self.tool, '_scan_files', return_value={"count": 5}):
             result = self.tool.clone_and_ingest("https://github.com/user/repo.git", "repo")
             self.assertIn("Successfully loaded spec", result)
             mock_run.assert_called()

if __name__ == "__main__":
    unittest.main()
