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
                assert "--exclude=*.log" in args
                assert "--exclude=.git/" in args
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
                assert "--exclude=*.log" in args
                assert "--exclude=.git/" in args
                assert "--delete" in args
        assert called, "rsync was not called during rollback restoration"


def test_recover_os_nfs_skip_in_rsync():
    """Test that recover_os.py skips NFS mounted folders during snapshot creation."""
    with patch("recover_os.check_btrfs", return_value=True), \
         patch("recover_os.check_btrfs_mount", return_value=True), \
         patch("recover_os.get_protected_dirs", return_value=["/opt/cluster-infra", "/opt/unified_fs_backend"]), \
         patch("os.path.exists", return_value=True), \
         patch("os.path.islink", return_value=True), \
         patch("os.remove"), \
         patch("os.symlink"), \
         patch("os.makedirs") as mock_makedirs, \
         patch("subprocess.check_call") as mock_check_call, \
         patch("subprocess.check_output") as mock_check_output:

        # Let's mock check_output such that /opt/cluster-infra returns 'ext4' and /opt/unified_fs_backend returns 'nfs4'
        def check_output_side_effect(args, **kwargs):
            cmd_str = " ".join(args)
            if "/opt/cluster-infra" in cmd_str:
                return "ext4\n"
            elif "/opt/unified_fs_backend" in cmd_str:
                return "nfs4\n"
            return ""

        mock_check_output.side_effect = check_output_side_effect

        # Call create_snapshot
        recover_os.create_snapshot()

        # Verify that rsync was called for /opt/cluster-infra but NOT for /opt/unified_fs_backend
        synced_dirs = []
        for call in mock_check_call.call_args_list:
            args = call[0][0]
            if args[0] == "rsync":
                # The source dir is one of the last args
                synced_dirs.append(args[-2])

        assert "/opt/cluster-infra/" in synced_dirs
        assert "/opt/unified_fs_backend/" not in synced_dirs


def test_recover_os_nfs_skip_in_rollback():
    """Test that recover_os.py skips NFS mounted folders during snapshot rollback."""
    with patch("recover_os.check_btrfs", return_value=True), \
         patch("recover_os.check_btrfs_mount", return_value=True), \
         patch("recover_os.get_protected_dirs", return_value=["/opt/cluster-infra", "/opt/unified_fs_backend"]), \
         patch("os.path.exists", return_value=True), \
         patch("os.makedirs") as mock_makedirs, \
         patch("builtins.input", return_value="y"), \
         patch("subprocess.call"), \
         patch("subprocess.check_call") as mock_check_call, \
         patch("subprocess.check_output") as mock_check_output:

        # Let's mock check_output such that /opt/cluster-infra returns 'ext4' and /opt/unified_fs_backend returns 'nfs'
        def check_output_side_effect(args, **kwargs):
            cmd_str = " ".join(args)
            if "/opt/cluster-infra" in cmd_str:
                return "ext4\n"
            elif "/opt/unified_fs_backend" in cmd_str:
                return "nfs\n"
            return ""

        mock_check_output.side_effect = check_output_side_effect

        # Call rollback_snapshot for target='latest'
        recover_os.rollback_snapshot("latest")

        # Verify that rsync (restore) was called for /opt/cluster-infra but NOT for /opt/unified_fs_backend
        restored_dirs = []
        for call in mock_check_call.call_args_list:
            args = call[0][0]
            if args[0] == "rsync":
                # In rollback rsync, target is the last arg (p_dir)
                restored_dirs.append(args[-1])

        assert "/opt/cluster-infra/" in restored_dirs
        assert "/opt/unified_fs_backend/" not in restored_dirs
