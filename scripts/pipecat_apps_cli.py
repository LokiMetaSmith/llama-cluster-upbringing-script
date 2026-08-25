#!/usr/bin/env python3
import sys
import argparse
import requests
import json
import os

BASE_URL = os.getenv("PIPECAT_API_URL", f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8000")
USER_ROLE = os.getenv("X_USER_ROLE", "admin")
HEADERS = {"X-User-Role": USER_ROLE}

def list_catalog():
    res = requests.get(f"{BASE_URL}/api/apps/catalog")
    if res.status_code == 200:
        print("Community Apps Catalog:")
        for app in res.json():
            print(f"  - {app['id']:<15} {app['name']:<15} ({app['category']}) | {app['description']}")
    else:
        print(f"Error fetching catalog: {res.status_code} {res.text}")

def list_installed():
    res = requests.get(f"{BASE_URL}/api/apps/installed")
    if res.status_code == 200:
        installed = res.json()
        if not installed:
            print("No community container applications currently installed.")
            return
        print("Installed Community Apps:")
        for app in installed:
            print(f"  - {app['id']:<15} Status: {app['status']:<10} Type: {app['type']}")
    else:
        print(f"Error fetching installed apps: {res.status_code} {res.text}")

def install_app(app_id, domain):
    res = requests.post(f"{BASE_URL}/api/apps/install", json={"app_id": app_id, "domain_name": domain}, headers=HEADERS)
    print(f"Install Result ({res.status_code}):", res.json())

def upgrade_app(app_id, target_image):
    res = requests.post(f"{BASE_URL}/api/apps/upgrade", json={"app_id": app_id, "target_image": target_image}, headers=HEADERS)
    print(f"Upgrade Result ({res.status_code}):", res.json())

def remove_app(app_id):
    res = requests.delete(f"{BASE_URL}/api/apps/remove/{app_id}", headers=HEADERS)
    print(f"Remove Result ({res.status_code}):", res.json())

def app_status(app_id):
    res = requests.get(f"{BASE_URL}/api/apps/status/{app_id}")
    if res.status_code == 200:
        print(json.dumps(res.json(), indent=2))
    else:
        print(f"Error fetching status for {app_id}: {res.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Swarm Community Apps CLI Manager")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("catalog", help="List community apps catalog")
    subparsers.add_parser("list", help="List installed community apps")

    install_p = subparsers.add_parser("install", help="Install a community app")
    install_p.add_argument("app_id", help="Application ID (e.g. pihole, nextcloud)")
    install_p.add_argument("--domain", default="pihole.local", help="Domain name for Traefik ingress")

    upgrade_p = subparsers.add_parser("upgrade", help="Upgrade a community app")
    upgrade_p.add_argument("app_id", help="Application ID")
    upgrade_p.add_argument("--image", required=True, help="Target container image version")

    remove_p = subparsers.add_parser("remove", help="Remove/purge a community app")
    remove_p.add_argument("app_id", help="Application ID")

    status_p = subparsers.add_parser("status", help="Investigate app status")
    status_p.add_argument("app_id", help="Application ID")

    args = parser.parse_args()

    if args.command == "catalog":
        list_catalog()
    elif args.command == "list":
        list_installed()
    elif args.command == "install":
        install_app(args.app_id, args.domain)
    elif args.command == "upgrade":
        upgrade_app(args.app_id, args.image)
    elif args.command == "remove":
        remove_app(args.app_id)
    elif args.command == "status":
        app_status(args.app_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
