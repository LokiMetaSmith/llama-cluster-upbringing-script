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
