import sys
import os
from unittest.mock import patch, MagicMock

# Add the scripts directory to path to import recover_os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../scripts"))
import recover_os

def test_recover_os_excludes_in_rsync():
    """Test that recover_os.py uses the correct rsync exclude options during snapshot creation."""
    # Mock checks to return true so snapshot creation is permitted
    with patch("recover_os.check_btrfs", return_value=True), \
         patch("recover_os.check_btrfs_mount", return_value=True), \
         patch("recover_os.get_protected_dirs", return_value=["/opt/cluster-infra"]), \
         patch("os.path.exists", return_value=True), \
         patch("os.path.islink", return_value=True), \
         patch("os.remove") as mock_remove, \
         patch("os.symlink") as mock_symlink, \
         patch("os.makedirs") as mock_makedirs, \
         patch("subprocess.check_call") as mock_check_call:

        # Call create_snapshot
        recover_os.create_snapshot()

        # Verify that subprocess.check_call was called with rsync and the excludes
        called = False
        for call in mock_check_call.call_args_list:
            args = call[0][0]
            if args[0] == "rsync":
                called = True
                assert "--exclude=.venv/" in args
                assert "--exclude=venv/" in args
                assert "--exclude=node_modules/" in args
                assert "--exclude=__pycache__/" in args
                assert "--exclude=.pytest_cache/" in args
                assert "--exclude=.mypy_cache/" in args
                assert "--exclude=target/" in args
                assert "--delete" in args
        assert called, "rsync was not called during snapshot creation"
        assert mock_remove.called
        assert mock_symlink.called

def test_recover_os_excludes_in_rollback():
    """Test that recover_os.py uses the correct rsync exclude options during snapshot rollback."""
    # Mock checks to return true
    with patch("recover_os.check_btrfs", return_value=True), \
         patch("recover_os.check_btrfs_mount", return_value=True), \
         patch("recover_os.get_protected_dirs", return_value=["/opt/cluster-infra"]), \
         patch("os.path.exists", return_value=True), \
         patch("os.makedirs") as mock_makedirs, \
         patch("builtins.input", return_value="y"), \
         patch("subprocess.call") as mock_call, \
         patch("subprocess.check_call") as mock_check_call:

        # Call rollback_snapshot for target='latest'
        recover_os.rollback_snapshot("latest")

        # Verify that subprocess.check_call was called with rsync and the excludes for restoration
        called = False
        for call in mock_check_call.call_args_list:
            args = call[0][0]
            if args[0] == "rsync":
                called = True
                assert "--exclude=.venv/" in args
                assert "--exclude=venv/" in args
                assert "--exclude=node_modules/" in args
                assert "--exclude=__pycache__/" in args
                assert "--exclude=.pytest_cache/" in args
                assert "--exclude=.mypy_cache/" in args
                assert "--exclude=target/" in args
                assert "--delete" in args
        assert called, "rsync was not called during rollback restoration"
