import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure we can import from pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.git_tool import Git_Tool

class TestGitToolSecurity:

    def setup_method(self):
        self.tool = Git_Tool()
        # Mock _run_git_command to avoid actual git calls and just check validation
        self.tool._run_git_command = MagicMock(return_value="Success")

    def test_diff_security(self):
        # Should block arguments starting with -
        result = self.tool.diff(".", commit1="--output=pwned.txt")
        assert "Security Error" in result
        self.tool._run_git_command.assert_not_called()

        result = self.tool.diff(".", commit2="-rf")
        assert "Security Error" in result
        self.tool._run_git_command.assert_not_called()

        # Valid args should pass
        self.tool.diff(".", commit1="HEAD", commit2="main")
        self.tool._run_git_command.assert_called()

    def test_branch_security(self):
        # Should block branch name starting with -
        result = self.tool.branch(".", branch_name="-D")
        assert "Security Error" in result
        self.tool._run_git_command.assert_not_called()

        # Valid args should pass
        self.tool.branch(".", branch_name="feature/secure")
        self.tool._run_git_command.assert_called()

    def test_checkout_security(self):
        # Should block branch name starting with -
        result = self.tool.checkout(".", branch_name="--detach")
        assert "Security Error" in result
        self.tool._run_git_command.assert_not_called()

        # Valid args should pass
        self.tool.checkout(".", branch_name="main")
        self.tool._run_git_command.assert_called()

    def test_merge_security(self):
        # Should block branch name starting with -
        result = self.tool.merge(".", branch="--no-ff")
        assert "Security Error" in result
        self.tool._run_git_command.assert_not_called()

        # Valid args should pass
        self.tool.merge(".", branch="dev")
        self.tool._run_git_command.assert_called()

    def test_clone_security(self):
        # Should block repo url starting with - (unlikely but safer)
        result = self.tool.clone(repo_url="--upload-pack=...", directory="repo")
        assert "Security Error" in result
        self.tool._run_git_command.assert_not_called()

        # Should block directory starting with -
        result = self.tool.clone(repo_url="https://github.com/example/repo.git", directory="-p")
        assert "Security Error" in result
        self.tool._run_git_command.assert_not_called()

        # Valid args should pass
        self.tool.clone("https://github.com/example/repo.git", "my-repo")
        self.tool._run_git_command.assert_called()
