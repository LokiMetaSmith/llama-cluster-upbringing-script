#!/usr/bin/env python3
"""
Unified Btrfs Snapshot and Rollback Recovery Tool
"""

import os
import sys
import subprocess
import argparse
import json

BTRFS_SUBVOLUME_PATH = "/btrfs_root"
BTRFS_ACTIVE_SUBVOLUME = f"{BTRFS_SUBVOLUME_PATH}/active"
BTRFS_SNAPSHOT_DIR = f"{BTRFS_SUBVOLUME_PATH}/snapshots"
CONFIG_FILE = "/etc/btrfs-snapshot-config.json"

def check_btrfs():
    """Checks if btrfs-progs is available."""
    if subprocess.call(["which", "btrfs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        print("Error: 'btrfs' command not found. Please install 'btrfs-progs'.")
        return False
    return True

def check_btrfs_mount():
    """Checks if the BTRFS_SUBVOLUME_PATH is a valid Btrfs mount point."""
    try:
        output = subprocess.check_output(
            ["findmnt", "-n", "-o", "FSTYPE", BTRFS_SUBVOLUME_PATH],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        if output == "btrfs":
            return True
    except Exception:
        pass
    print(f"Error: {BTRFS_SUBVOLUME_PATH} is not mounted as a Btrfs filesystem.")
    print("Pre-deployment OS recovery/snapshotting is not available on this node.")
    return False

def get_protected_dirs():
    """Loads configuration detailing which directories are protected."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("protected_dirs", [])
        except Exception as e:
            print(f"Warning: Failed to load config from {CONFIG_FILE}: {e}")
    # Fallback default
    return ["/etc/nomad.d", "/etc/consul.d", "/opt/cluster-infra", "/opt/pipecatapp"]

def create_snapshot():
    """Syncs protected directories to active subvolume, then creates a snapshot."""
    if not check_btrfs() or not check_btrfs_mount():
        return False

    protected_dirs = get_protected_dirs()
    print("Synchronizing protected directories to Btrfs active subvolume...")
    for p_dir in protected_dirs:
        if os.path.exists(p_dir):
            target_sub_dir = f"{BTRFS_ACTIVE_SUBVOLUME}{p_dir}"
            os.makedirs(target_sub_dir, exist_ok=True)
            print(f"  Syncing {p_dir} -> {target_sub_dir}")
            try:
                subprocess.check_call(["rsync", "-a", "--delete", f"{p_dir}/", f"{target_sub_dir}/"])
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to sync {p_dir}: {e}")

    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    snapshot_path = f"{BTRFS_SNAPSHOT_DIR}/pre-deploy-{timestamp}"
    latest_symlink = f"{BTRFS_SNAPSHOT_DIR}/pre-deploy-latest"

    # Create snapshot directory if missing
    os.makedirs(BTRFS_SNAPSHOT_DIR, exist_ok=True)

    print(f"Creating snapshot of {BTRFS_ACTIVE_SUBVOLUME} at {snapshot_path}...")
    try:
        subprocess.check_call(["btrfs", "subvolume", "snapshot", BTRFS_ACTIVE_SUBVOLUME, snapshot_path])

        # Link latest
        if os.path.exists(latest_symlink) or os.path.islink(latest_symlink):
            os.remove(latest_symlink)
        os.symlink(snapshot_path, latest_symlink)

        print("Snapshot created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Btrfs snapshot: {e}")
        return False

def list_snapshots():
    """Lists existing Btrfs snapshots."""
    if not check_btrfs() or not check_btrfs_mount():
        return False

    print("\nAvailable Pre-deployment Snapshots:")
    if not os.path.exists(BTRFS_SNAPSHOT_DIR):
        print("No snapshot directory found.")
        return False

    try:
        snapshots = os.listdir(BTRFS_SNAPSHOT_DIR)
        snapshots = [s for s in snapshots if s.startswith("pre-deploy-") and not s.endswith("-latest")]
        snapshots.sort(reverse=True)
        for idx, snap in enumerate(snapshots):
            print(f" [{idx}] {snap}")
        return snapshots
    except OSError as e:
        print(f"Error reading snapshots: {e}")
        return []

def rollback_snapshot(target=None):
    """Rolls back the active subvolume and restores the protected folders."""
    if not check_btrfs() or not check_btrfs_mount():
        return False

    if not target:
        snapshots = list_snapshots()
        if not snapshots or not isinstance(snapshots, list):
            print("No snapshots available to rollback.")
            return False

        try:
            choice = input("\nEnter snapshot index to rollback to (default 0): ").strip()
            if not choice:
                idx = 0
            else:
                idx = int(choice)
            target = snapshots[idx]
        except (ValueError, IndexError):
            print("Invalid selection. Aborting rollback.")
            return False

    target_path = f"{BTRFS_SNAPSHOT_DIR}/{target}"
    if not os.path.exists(target_path):
        print(f"Error: Target snapshot {target_path} does not exist.")
        return False

    print(f"\nCRITICAL: You are about to rollback to: {target}")
    confirm = input("Are you absolutely sure you want to continue? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Rollback cancelled.")
        return False

    try:
        print("Stopping services before rollback...")
        # Gracefully stop cluster services if systemctl is present
        for svc in ["nomad", "consul", "docker"]:
            subprocess.call(["systemctl", "stop", svc], stderr=subprocess.DEVNULL)

        print(f"Deleting active subvolume {BTRFS_ACTIVE_SUBVOLUME}...")
        subprocess.check_call(["btrfs", "subvolume", "delete", BTRFS_ACTIVE_SUBVOLUME])

        print(f"Restoring snapshot {target_path} to active subvolume...")
        subprocess.check_call(["btrfs", "subvolume", "snapshot", target_path, BTRFS_ACTIVE_SUBVOLUME])

        # Restore from active subvolume back to the system locations
        protected_dirs = get_protected_dirs()
        print("Restoring protected directories from snapshot back to system...")
        for p_dir in protected_dirs:
            snapshot_source_dir = f"{BTRFS_ACTIVE_SUBVOLUME}{p_dir}"
            if os.path.exists(snapshot_source_dir):
                print(f"  Restoring {snapshot_source_dir} -> {p_dir}")
                os.makedirs(p_dir, exist_ok=True)
                try:
                    subprocess.check_call(["rsync", "-a", "--delete", f"{snapshot_source_dir}/", f"{p_dir}/"])
                except subprocess.CalledProcessError as e:
                    print(f"Warning: Failed to restore {p_dir}: {e}")

        print("Restarting core services...")
        for svc in ["docker", "consul", "nomad"]:
            subprocess.call(["systemctl", "start", svc], stderr=subprocess.DEVNULL)

        print("\n✅ OS Rollback complete! System restored successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed during rollback execution: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="OS Recovery Snapshot & Rollback Utility")
    parser.add_argument("--create", action="store_true", help="Create a pre-deployment snapshot")
    parser.add_argument("--list", action="store_true", help="List existing pre-deployment snapshots")
    parser.add_argument("--rollback", type=str, nargs='?', const='latest', help="Rollback to a snapshot (default: latest)")

    args = parser.parse_args()

    # If no arguments, show menu
    if not (args.create or args.list or args.rollback):
        print("=== OS Recovery Snapshot & Rollback Menu ===")
        print(" 1. Create a Pre-deployment Snapshot")
        print(" 2. List Existing Snapshots")
        print(" 3. Rollback to Latest Snapshot")
        print(" 4. Rollback to Specific Snapshot")
        print(" 5. Exit")
        try:
            choice = input("Enter choice [1-5]: ").strip()
            if choice == "1":
                create_snapshot()
            elif choice == "2":
                list_snapshots()
            elif choice == "3":
                rollback_snapshot("pre-deploy-latest")
            elif choice == "4":
                rollback_snapshot()
            else:
                print("Exiting.")
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)
    else:
        success = False
        if args.create:
            success = create_snapshot()
        elif args.list:
            res = list_snapshots()
            success = isinstance(res, list)
        elif args.rollback:
            target = "pre-deploy-latest" if args.rollback == "latest" else args.rollback
            success = rollback_snapshot(target)

        if not success:
            sys.exit(1)

if __name__ == "__main__":
    if os.getuid() != 0:
        print("This tool must be run with root (sudo) privileges.")
        sys.exit(1)
    main()
