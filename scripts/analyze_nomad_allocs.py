#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime

def format_timestamp(ns_timestamp):
    if not ns_timestamp:
        return ""
    try:
        # Convert nanoseconds to seconds
        ts = int(ns_timestamp) / 1e9
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ns_timestamp)

def analyze_allocs(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return

    try:
        with open(filepath, 'r') as f:
            allocs = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {filepath}: {e}")
        return
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    if not isinstance(allocs, list):
        print("Error: JSON content is not a list of allocations.")
        return

    # Filter for failed allocations or allocations with recent failures
    failed_allocs = [a for a in allocs if a.get('ClientStatus') == 'failed']

    if not failed_allocs:
        print("No failed allocations found in the dump.")
        return

    print(f"Found {len(failed_allocs)} failed allocations:")

    # Sort by ModifyTime descending to show most recent failures first
    try:
        failed_allocs.sort(key=lambda x: x.get('ModifyTime', 0), reverse=True)
    except:
        pass

    for alloc in failed_allocs:
        alloc_id = alloc.get('ID', 'unknown')[:8]
        node_name = alloc.get('NodeName', 'unknown')
        modify_time = format_timestamp(alloc.get('ModifyTime'))

        print(f"\n--- Allocation {alloc_id} on {node_name} (Last modified: {modify_time}) ---")

        task_states = alloc.get('TaskStates', {})
        if not task_states:
            print("  No TaskStates found.")
            continue

        for task_name, state in task_states.items():
            # Check if task failed
            if state.get('Failed', False) or state.get('State') == 'dead':
                print(f"  Task '{task_name}': {state.get('State', 'unknown').upper()}")
                events = state.get('Events', [])
                # Show last 5 events
                recent_events = events[-5:] if events else []
                for evt in recent_events:
                    evt_type = evt.get('Type', '')
                    msg = evt.get('Message', '')
                    details = evt.get('Details', {})
                    ts = format_timestamp(evt.get('Time'))

                    # Construct a readable line
                    line = f"    [{ts}] [{evt_type}]"
                    if msg:
                        line += f" {msg}"

                    print(line)
                    if details:
                        # Print details indented
                        for k, v in details.items():
                            print(f"      {k}: {v}")

                    # Check specific error fields if they exist and aren't empty
                    for field in ['ValidationError', 'DriverError', 'KillError', 'DownloadError', 'VaultError', 'SetupError']:
                        err_val = evt.get(field)
                        if err_val:
                            print(f"      {field}: {err_val}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze_nomad_allocs.py <json_file>")
        sys.exit(1)

    analyze_allocs(sys.argv[1])
