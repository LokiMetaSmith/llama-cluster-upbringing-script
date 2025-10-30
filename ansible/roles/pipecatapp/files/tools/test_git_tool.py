import unittest
from unittest.mock import patch, MagicMock
import os
# Assuming git_tool is in the same directory or adjust the import path accordingly.
# To run this test standalone, you might need to adjust sys.path.
# For example:
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'your_module_path')))
from .git_tool import Git_Tool

class TestGitTool(unittest.TestCase):
    def setUp(self):
        """Set up a new Git_Tool instance before each test."""
        self.git_tool = Git_Tool()
        # Mock os.path.isdir to always return True for the tests,
        # as we are not testing the file system interactions here.
        self.isdir_patcher = patch('os.path.isdir', return_value=True)
        self.mock_isdir = self.isdir_patcher.start()
        self.addCleanup(self.isdir_patcher.stop)


    @patch("subprocess.run")
    def test_clone_successful(self, mock_run):
        """Test successful cloning of a repository."""
        mock_run.return_value = MagicMock(returncode=0, stdout="Cloned successfully.", stderr="")
        result = self.git_tool.clone("https://github.com/test/repo.git", "/tmp/repo")
        self.assertIn("Command successful.", result)
        self.assertIn("Cloned successfully.", result)
        mock_run.assert_called_once_with(
            ["git", "clone", "https://github.com/test/repo.git", "/tmp/repo"],
            cwd=".", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_pull_successful(self, mock_run):
        """Test successful pull from a repository."""
        mock_run.return_value = MagicMock(returncode=0, stdout="Pulled successfully.", stderr="")
        result = self.git_tool.pull("/tmp/repo")
        self.assertIn("Command successful.", result)
        self.assertIn("Pulled successfully.", result)
        mock_run.assert_called_once_with(
            ["git", "pull"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_push_successful(self, mock_run):
        """Test successful push to a repository."""
        mock_run.return_value = MagicMock(returncode=0, stdout="Pushed successfully.", stderr="")
        result = self.git_tool.push("/tmp/repo")
        self.assertIn("Command successful.", result)
        self.assertIn("Pushed successfully.", result)
        mock_run.assert_called_once_with(
            ["git", "push"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_commit_successful(self, mock_run):
        """Test successful commit."""
        mock_run.return_value = MagicMock(returncode=0, stdout="Committed successfully.", stderr="")
        result = self.git_tool.commit("/tmp/repo", "Test commit")
        self.assertIn("Command successful.", result)
        self.assertIn("Committed successfully.", result)
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "Test commit"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_branch_creation_successful(self, mock_run):
        """Test successful branch creation."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        result = self.git_tool.branch("/tmp/repo", "new-feature")
        self.assertIn("Command successful.", result)
        mock_run.assert_called_once_with(
            ["git", "branch", "new-feature"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_list_branches_successful(self, mock_run):
        """Test successfully listing branches."""
        mock_run.return_value = MagicMock(returncode=0, stdout="* main\n  new-feature", stderr="")
        result = self.git_tool.branch("/tmp/repo")
        self.assertIn("* main", result)
        self.assertIn("new-feature", result)
        mock_run.assert_called_once_with(
            ["git", "branch"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_checkout_successful(self, mock_run):
        """Test successful checkout of a branch."""
        mock_run.return_value = MagicMock(returncode=0, stdout="Switched to branch 'new-feature'", stderr="")
        result = self.git_tool.checkout("/tmp/repo", "new-feature")
        self.assertIn("Switched to branch 'new-feature'", result)
        mock_run.assert_called_once_with(
            ["git", "checkout", "new-feature"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_status_successful(self, mock_run):
        """Test successful status check."""
        mock_run.return_value = MagicMock(returncode=0, stdout="On branch main\nYour branch is up to date with 'origin/main'.", stderr="")
        result = self.git_tool.status("/tmp/repo")
        self.assertIn("On branch main", result)
        mock_run.assert_called_once_with(
            ["git", "status"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_command_failed(self, mock_run):
        """Test handling of a failed git command."""
        mock_run.return_value = MagicMock(returncode=128, stdout="", stderr="fatal: not a git repository")
        result = self.git_tool.status("/not/a/repo")
        self.assertIn("Command failed", result)
        self.assertIn("fatal: not a git repository", result)

    def test_directory_not_found(self):
        """Test handling of a non-existent working directory."""
        # We need to stop the class-level patch for this specific test
        self.isdir_patcher.stop()
        with patch('os.path.isdir', return_value=False):
            result = self.git_tool.status("/non/existent/dir")
            self.assertIn("Error: Working directory '/non/existent/dir' not found.", result)
        # Restart it for other tests if they run after this one in the same instance
        self.isdir_patcher.start()

    @patch("subprocess.run")
    def test_diff_successful(self, mock_run):
        """Test successful diff command."""
        diff_output = "diff --git a/file.txt b/file.txt\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-hello\n+goodbye"
        mock_run.return_value = MagicMock(returncode=0, stdout=diff_output, stderr="")
        result = self.git_tool.diff("/tmp/repo")
        self.assertIn(diff_output, result)
        mock_run.assert_called_once_with(
            ["git", "diff"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_diff_with_commits_successful(self, mock_run):
        """Test successful diff command between two commits."""
        diff_output = "diff --git a/file.txt b/file.txt\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-hello\n+goodbye"
        mock_run.return_value = MagicMock(returncode=0, stdout=diff_output, stderr="")
        result = self.git_tool.diff("/tmp/repo", "HEAD~1", "HEAD")
        self.assertIn(diff_output, result)
        mock_run.assert_called_once_with(
            ["git", "diff", "HEAD~1", "HEAD"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

    @patch("subprocess.run")
    def test_merge_successful(self, mock_run):
        """Test successful merge command."""
        mock_run.return_value = MagicMock(returncode=0, stdout="Merge made by the 'recursive' strategy.", stderr="")
        result = self.git_tool.merge("/tmp/repo", "feature-branch")
        self.assertIn("Merge made by the 'recursive' strategy.", result)
        mock_run.assert_called_once_with(
            ["git", "merge", "feature-branch"],
            cwd="/tmp/repo", capture_output=True, text=True, timeout=300
        )

if __name__ == '__main__':
    unittest.main()
