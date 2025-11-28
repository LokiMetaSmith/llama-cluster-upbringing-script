#!/usr/bin/env python3
"""
Prune Stale Nomad Services from Consul

This script identifies and deregisters stale Nomad services in Consul.
It specifically targets 'nomad-server' and 'nomad-client' services (and their
internal '_nomad-server-*' representations) that are in a CRITICAL state.

This is useful when Nomad node IDs change (e.g. after wiping data dir) but
Consul still retains the old service registrations.

Usage:
    python3 prune_consul_services.py [--dry-run] [--force]
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
    parser = argparse.ArgumentParser(description="Prune stale Nomad services from Consul.")
    parser.add_argument("--url", default=DEFAULT_CONSUL_URL, help="Consul Agent URL (default: http://localhost:8500)")
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
    service_health = {} # ServiceID -> {'all_critical': True, 'checks': []}

    for check_id, check in checks.items():
        service_id = check.get("ServiceID")
        if not service_id:
            continue

        status = check.get("Status")
        if service_id not in service_health:
            service_health[service_id] = {'checks': []}

        service_health[service_id]['checks'].append(status)

    # 2. Identify services to prune
    services_to_prune = []

    for service_id, data in service_health.items():
        # Check if it looks like a Nomad internal service
        # Nomad server/client IDs usually start with _nomad-server- or _nomad-client-
        # Or sometimes just match the node ID pattern if registered differently.
        # We target the specific pattern seen in the issue.
        if service_id.startswith("_nomad-server-") or service_id.startswith("_nomad-client-"):
            check_statuses = data['checks']
            if not check_statuses:
                continue

            # If ALL checks are critical, it's a candidate for pruning
            if all(s == "critical" for s in check_statuses):
                services_to_prune.append(service_id)

    if not services_to_prune:
        print("No stale Nomad services found.")
        return

    print(f"Found {len(services_to_prune)} stale Nomad services:")
    for svc_id in services_to_prune:
        print(f" - {svc_id}")

    if args.dry_run:
        print("\n[DRY-RUN] Would deregister the above services.")
    else:
        print("\nDeregistering services...")
        for svc_id in services_to_prune:
            print(f"Deregistering {svc_id}...", end=" ")
            res = consul_request(args.url, f"v1/agent/service/deregister/{svc_id}", method="PUT", token=token)
            if res is not None:
                print("OK")
            else:
                print("Failed")

if __name__ == "__main__":
    main()
