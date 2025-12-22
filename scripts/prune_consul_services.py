#!/usr/bin/env python3
"""
Prune Stale Critical Services from Consul

This script identifies and deregisters stale services in Consul that are in a
CRITICAL state. It can target specific services or find all critical services.

Usage:
    python3 prune_consul_services.py [--service SERVICE_NAME] [--dry-run] [--force]
"""

import urllib.request
import urllib.error
import json
import argparse
import sys
import os

DEFAULT_CONSUL_URL = "http://localhost:8500"

def get_consul_token():
    """Retrieve Consul token from env or standard file location."""
    token = os.environ.get("CONSUL_HTTP_TOKEN")
    if token:
        return token

    token_file = "/etc/consul.d/management_token"
    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                return f.read().strip()
        except Exception:
            pass
    return None

def consul_request(base_url, path, method='GET', token=None, data=None):
    """Make a request to the Consul API."""
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    headers = {}
    if token:
        headers['X-Consul-Token'] = token

    if data:
        json_data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    else:
        json_data = None

    req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                body = response.read().decode('utf-8')
                return json.loads(body) if body else {}
            return True
    except urllib.error.HTTPError as e:
        print(f"Error calling {url}: {e.code} {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error calling {url}: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Prune stale services from Consul.")
    parser.add_argument("--url", default=DEFAULT_CONSUL_URL, help="Consul Agent URL (default: http://localhost:8500)")
    parser.add_argument("--service", help="Filter by specific service name (partial match on ServiceName)")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing them (default)")
    parser.add_argument("--force", action="store_true", help="Actually execute the deregistration")

    args = parser.parse_args()

    # Safety: Default to dry-run unless --force is specified
    if not args.force:
        args.dry_run = True
        print("Running in DRY-RUN mode. Use --force to execute changes.\n")

    token = get_consul_token()
    if token:
        print("Using Consul token from environment or file.")

    # 1. Get all checks to identify critical ones
    checks = consul_request(args.url, "v1/agent/checks", token=token)
    if checks is None:
        print("Failed to retrieve checks from Consul.")
        sys.exit(1)

    # Group checks by ServiceID
    # Structure: ServiceID -> {'name': ServiceName, 'checks': [status1, status2, ...]}
    service_health = {}

    for check_id, check in checks.items():
        service_id = check.get("ServiceID")
        service_name = check.get("ServiceName")
        if not service_id:
            continue

        status = check.get("Status")
        if service_id not in service_health:
            service_health[service_id] = {'name': service_name, 'checks': []}

        service_health[service_id]['checks'].append(status)

    # 2. Identify services to prune
    services_to_prune = []

    for service_id, data in service_health.items():
        service_name = data['name']
        check_statuses = data['checks']

        # If user specified a service name, filter by it
        if args.service and args.service not in service_name:
            continue

        if not check_statuses:
            continue

        # If ALL checks are critical, it's a candidate for pruning
        if all(s == "critical" for s in check_statuses):
            services_to_prune.append({'id': service_id, 'name': service_name})

    if not services_to_prune:
        print("No stale critical services found.")
        return

    print(f"Found {len(services_to_prune)} stale critical services:")
    for svc in services_to_prune:
        print(f" - {svc['name']} (ID: {svc['id']})")

    if args.dry_run:
        print("\n[DRY-RUN] Would deregister the above services.")
    else:
        print("\nDeregistering services...")
        for svc in services_to_prune:
            print(f"Deregistering {svc['name']} (ID: {svc['id']})...", end=" ")
            res = consul_request(args.url, f"v1/agent/service/deregister/{svc['id']}", method="PUT", token=token)
            if res is not None:
                print("OK")
            else:
                print("Failed")

if __name__ == "__main__":
    main()
