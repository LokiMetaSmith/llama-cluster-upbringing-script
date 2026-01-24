import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from git_tool import Git_Tool

@pytest.fixture
def git_tool():
    # Mock os.path.isdir to always return True for the tests
    with patch('os.path.isdir', return_value=True):
        yield Git_Tool()

@patch("subprocess.run")
def test_clone_successful(mock_run, git_tool):
    """Test successful cloning of a repository."""
    mock_run.return_value = MagicMock(returncode=0, stdout="Cloned successfully.", stderr="")
    result = git_tool.clone("https://github.com/test/repo.git", "repo")
    assert "Command successful." in result
    assert "Cloned successfully." in result
    mock_run.assert_called_once_with(
        ["git", "clone", "https://github.com/test/repo.git", "repo"],
        cwd=os.path.abspath("."), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_pull_successful(mock_run, git_tool):
    """Test successful pull from a repository."""
    mock_run.return_value = MagicMock(returncode=0, stdout="Pulled successfully.", stderr="")
    result = git_tool.pull("repo")
    assert "Command successful." in result
    assert "Pulled successfully." in result
    mock_run.assert_called_once_with(
        ["git", "pull"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_push_successful(mock_run, git_tool):
    """Test successful push to a repository."""
    mock_run.return_value = MagicMock(returncode=0, stdout="Pushed successfully.", stderr="")
    result = git_tool.push("repo")
    assert "Command successful." in result
    assert "Pushed successfully." in result
    mock_run.assert_called_once_with(
        ["git", "push"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_commit_successful(mock_run, git_tool):
    """Test successful commit."""
    mock_run.return_value = MagicMock(returncode=0, stdout="Committed successfully.", stderr="")
    result = git_tool.commit("repo", "Test commit")
    assert "Command successful." in result
    assert "Committed successfully." in result
    mock_run.assert_called_once_with(
        ["git", "commit", "-m", "Test commit"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_branch_creation_successful(mock_run, git_tool):
    """Test successful branch creation."""
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
    result = git_tool.branch("repo", "new-feature")
    assert "Command successful." in result
    mock_run.assert_called_once_with(
        ["git", "branch", "new-feature"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_list_branches_successful(mock_run, git_tool):
    """Test successfully listing branches."""
    mock_run.return_value = MagicMock(returncode=0, stdout="* main\n  new-feature", stderr="")
    result = git_tool.branch("repo")
    assert "* main" in result
    assert "new-feature" in result
    mock_run.assert_called_once_with(
        ["git", "branch"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_checkout_successful(mock_run, git_tool):
    """Test successful checkout of a branch."""
    mock_run.return_value = MagicMock(returncode=0, stdout="Switched to branch 'new-feature'", stderr="")
    result = git_tool.checkout("repo", "new-feature")
    assert "Switched to branch 'new-feature'" in result
    mock_run.assert_called_once_with(
        ["git", "checkout", "new-feature"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_status_successful(mock_run, git_tool):
    """Test successful status check."""
    mock_run.return_value = MagicMock(returncode=0, stdout="On branch main\nYour branch is up to date with 'origin/main'.", stderr="")
    result = git_tool.status("repo")
    assert "On branch main" in result
    mock_run.assert_called_once_with(
        ["git", "status"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_command_failed(mock_run, git_tool):
    """Test handling of a failed git command."""
    mock_run.return_value = MagicMock(returncode=128, stdout="", stderr="fatal: not a git repository")
    result = git_tool.status("not_a_repo")
    assert "Command failed" in result
    assert "fatal: not a git repository" in result

def test_directory_not_found():
    """Test handling of a non-existent working directory."""
    with patch('os.path.isdir', return_value=False):
        tool = Git_Tool()
        result = tool.status("non_existent_dir")
        assert "Error: Working directory" in result and "non_existent_dir" in result

@patch("subprocess.run")
def test_diff_successful(mock_run, git_tool):
    """Test successful diff command."""
    diff_output = "diff --git a/file.txt b/file.txt\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-hello\n+goodbye"
    mock_run.return_value = MagicMock(returncode=0, stdout=diff_output, stderr="")
    result = git_tool.diff("repo")
    assert diff_output in result
    mock_run.assert_called_once_with(
        ["git", "diff"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_diff_with_commits_successful(mock_run, git_tool):
    """Test successful diff command between two commits."""
    diff_output = "diff --git a/file.txt b/file.txt\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-hello\n+goodbye"
    mock_run.return_value = MagicMock(returncode=0, stdout=diff_output, stderr="")
    result = git_tool.diff("repo", "HEAD~1", "HEAD")
    assert diff_output in result
    mock_run.assert_called_once_with(
        ["git", "diff", "HEAD~1", "HEAD"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )

@patch("subprocess.run")
def test_merge_successful(mock_run, git_tool):
    """Test successful merge command."""
    mock_run.return_value = MagicMock(returncode=0, stdout="Merge made by the 'recursive' strategy.", stderr="")
    result = git_tool.merge("repo", "feature-branch")
    assert "Merge made by the 'recursive' strategy." in result
    mock_run.assert_called_once_with(
        ["git", "merge", "feature-branch"],
        cwd=os.path.abspath("repo"), capture_output=True, text=True, timeout=300
    )
