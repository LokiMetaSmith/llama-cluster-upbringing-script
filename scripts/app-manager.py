#!/usr/bin/env python3
"""
CLI wrapper for External Application Package/Plugin Manager.
Allows human operators and developers to install, uninstall, list, and monitor containerized apps on the cluster.
"""

import sys
import os
import json
import argparse

# Dynamic pathing configuration to prevent ModuleNotFoundError
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, "pipecatapp"))

from pipecatapp.utils.app_manager import AppManager

def handle_install(args, manager: AppManager):
    """Installs/updates an app from a JSON manifest."""
    manifest_path = args.manifest
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest file '{manifest_path}' does not exist.")
        sys.exit(1)

    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"Error: Failed to parse manifest JSON file: {e}")
        sys.exit(1)

    print(f"Initiating installation of application: {manifest.get('name', 'unknown')}...")
    success, msg = manager.deploy_app(manifest)
    if success:
        print(f"✅ Success: {msg}")
    else:
        print(f"❌ Failure: {msg}")
        sys.exit(1)

def handle_uninstall(args, manager: AppManager):
    """Uninstalls and purges an app."""
    name = args.name.lower().strip()
    print(f"Initiating purge of application: {name}...")
    success, msg = manager.purge_app(name)
    if success:
        print(f"✅ Success: {msg}")
    else:
        print(f"❌ Failure: {msg}")
        sys.exit(1)

def handle_list(args, manager: AppManager):
    """Lists installed external apps."""
    print("Fetching list of installed external applications...")
    apps = manager.list_apps()
    if not apps:
        print("No external applications found.")
        return

    print(f"{'App Name':<20} | {'Status':<15} | {'Type':<12}")
    print("-" * 53)
    for app in apps:
        print(f"{app['name']:<20} | {app['status']:<15} | {app['type']:<12}")

def handle_status(args, manager: AppManager):
    """Gets real-time status details of an app."""
    name = args.name.lower().strip()
    print(f"Retrieving status for application: {name}...")
    status_info = manager.get_app_status(name)
    print(json.dumps(status_info, indent=2))

def main():
    if os.getuid() != 0:
        print("Warning: This tool should be run with root (sudo) privileges if dynamic Btrfs subvolume provisioning is required.")

    parser = argparse.ArgumentParser(
        description="CLI Package Manager for External Containerized Applications on the Tailscale Cluster Mesh."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommand to execute")

    # install command
    install_parser = subparsers.add_parser("install", help="Install or update an app from a JSON manifest")
    install_parser.add_argument("manifest", help="Path to manifest.json file")

    # uninstall command
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall and purge an app")
    uninstall_parser.add_argument("name", help="Name of the application to uninstall")

    # list command
    subparsers.add_parser("list", help="List all installed external applications")

    # status command
    status_parser = subparsers.add_parser("status", help="Get real-time execution status of an app")
    status_parser.add_argument("name", help="Name of the application")

    args = parser.parse_args()
    manager = AppManager()

    if args.command == "install":
        handle_install(args, manager)
    elif args.command == "uninstall":
        handle_uninstall(args, manager)
    elif args.command == "list":
        handle_list(args, manager)
    elif args.command == "status":
        handle_status(args, manager)

if __name__ == "__main__":
    main()
