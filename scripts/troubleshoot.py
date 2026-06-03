#!/usr/bin/env python3
"""
Nomad Job Troubleshooting CLI

A tool designed for both humans and AI agents to debug and retry failed Nomad jobs.
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
import subprocess
from datetime import datetime

NOMAD_URL = os.environ.get("NOMAD_ADDR", "http://localhost:4646")

def api_get(endpoint):
    """Helper to fetch JSON from Nomad API."""
    url = f"{NOMAD_URL}{endpoint}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error calling {url}: {e}", file=sys.stderr)
    return None

def api_post(endpoint, data=None):
    """Helper to POST to Nomad API."""
    url = f"{NOMAD_URL}{endpoint}"
    try:
        req = urllib.request.Request(url, method='POST')
        if data:
            req.add_header('Content-Type', 'application/json')
            req.data = json.dumps(data).encode('utf-8')
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error calling {url}: {e}", file=sys.stderr)
    return None

def run_command(command, shell=False):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            universal_newlines=True,
            timeout=30
        )
        return {"exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"exit_code": -1, "stdout": "", "stderr": str(e)}

def format_time(ns_timestamp):
    if not ns_timestamp:
        return ""
    try:
        ts = int(ns_timestamp) / 1e9
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ns_timestamp)

def cmd_list(args):
    """List pending or dead jobs."""
    jobs = api_get("/v1/jobs")
    if jobs is None:
        sys.exit(1)

    problem_jobs = []
    for job in jobs:
        status = job.get("Status", "").lower()
        if status in ["dead", "pending"]:
            problem_jobs.append(job)

    if args.json:
        print(json.dumps(problem_jobs, indent=2))
        return

    if not problem_jobs:
        print("No dead or pending jobs found.")
        return

    print("=== Problematic Nomad Jobs ===")
    print(f"{'Job ID':<30} | {'Type':<15} | {'Status':<10}")
    print("-" * 60)
    for job in problem_jobs:
        print(f"{job.get('ID', 'N/A'):<30} | {job.get('Type', 'N/A'):<15} | {job.get('Status', 'N/A'):<10}")

def fetch_alloc_logs(alloc_id, task_name, log_type="stderr"):
    """Fetch recent logs for an allocation using the CLI (easier than raw API streaming)."""
    # Use the local CLI since it handles formatting and streaming
    res = run_command(["nomad", "alloc", "logs", f"-{log_type}", "-tail", "-n", "100", alloc_id, task_name])
    return res.get("stdout", "")

def cmd_inspect(args):
    """Inspect a specific job, gathering alloc histories and logs."""
    job_id = args.job_id

    job_info = api_get(f"/v1/job/{job_id}")
    allocs = api_get(f"/v1/job/{job_id}/allocations")

    if not job_info:
        print(f"Error: Job {job_id} not found or accessible.")
        sys.exit(1)

    inspect_data = {
        "job_id": job_id,
        "job_status": job_info.get("Status"),
        "submit_time": format_time(job_info.get("SubmitTime")),
        "allocations": []
    }

    if allocs:
        # Sort by most recent
        allocs.sort(key=lambda x: x.get('ModifyTime', 0), reverse=True)
        # Limit to the top 3 most recent allocs to keep output sane
        for alloc in allocs[:3]:
            alloc_data = {
                "alloc_id": alloc.get("ID"),
                "node_id": alloc.get("NodeID"),
                "client_status": alloc.get("ClientStatus"),
                "desired_status": alloc.get("DesiredStatus"),
                "create_time": format_time(alloc.get("CreateTime")),
                "tasks": {}
            }

            task_states = alloc.get("TaskStates", {})
            for task_name, state in task_states.items():
                task_data = {
                    "state": state.get("State"),
                    "failed": state.get("Failed"),
                    "events": [],
                    "logs": {"stderr": ""}
                }

                # Grab events
                events = state.get("Events", [])
                for evt in events[-5:]: # Last 5 events
                    task_data["events"].append({
                        "type": evt.get("Type"),
                        "time": format_time(evt.get("Time")),
                        "message": evt.get("Message", ""),
                        "details": evt.get("Details", {})
                    })

                # If failed or dead, fetch logs
                if state.get("Failed") or state.get("State") == "dead":
                    task_data["logs"]["stderr"] = fetch_alloc_logs(alloc.get("ID"), task_name, "stderr")

                alloc_data["tasks"][task_name] = task_data

            inspect_data["allocations"].append(alloc_data)

    if args.json:
        print(json.dumps(inspect_data, indent=2))
        return

    print(f"=== Inspecting Job: {job_id} ===")
    print(f"Status: {inspect_data['job_status']} | Submitted: {inspect_data['submit_time']}")

    if not inspect_data["allocations"]:
        print("No allocations found for this job.")
        return

    for alloc in inspect_data["allocations"]:
        print(f"\n--- Allocation: {alloc['alloc_id'][:8]} (Status: {alloc['client_status']}) ---")
        for task_name, task in alloc["tasks"].items():
            print(f"  Task: {task_name} | State: {task['state']} | Failed: {task['failed']}")

            if task["events"]:
                print("  Recent Events:")
                for evt in task["events"]:
                    print(f"    - [{evt['time']}] {evt['type']}: {evt['message']}")
                    for k, v in evt.get("details", {}).items():
                        print(f"        {k}: {v}")

            if task["logs"].get("stderr"):
                print("  Recent Stderr Logs:")
                lines = task["logs"]["stderr"].splitlines()
                for line in lines[-20:]: # Last 20 lines of logs in human readable mode
                    print(f"      {line}")


def cmd_retry(args):
    """Restart a job."""
    job_id = args.job_id

    # We'll use the CLI for restarting, as it handles the job registration flow well
    # `nomad job restart` simply issues an eval, which is safe.
    print(f"Attempting to restart job {job_id}...")
    res = run_command(["nomad", "job", "restart", job_id])

    if args.json:
        print(json.dumps({
            "job_id": job_id,
            "success": res["exit_code"] == 0,
            "stdout": res["stdout"],
            "stderr": res["stderr"]
        }, indent=2))
        return

    if res["exit_code"] == 0:
        print(f"Successfully triggered restart for job {job_id}.")
        print(res["stdout"])
    else:
        print(f"Failed to restart job {job_id}.")
        print("stderr:", res["stderr"])

def main():
    parser = argparse.ArgumentParser(description="Troubleshoot Nomad jobs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list command
    list_parser = subparsers.add_parser("list", help="List jobs in dead or pending state")
    list_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    list_parser.set_defaults(func=cmd_list)

    # inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a specific job")
    inspect_parser.add_argument("job_id", help="The Nomad Job ID to inspect")
    inspect_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    inspect_parser.set_defaults(func=cmd_inspect)

    # retry command
    retry_parser = subparsers.add_parser("retry", help="Retry/Restart a specific job")
    retry_parser.add_argument("job_id", help="The Nomad Job ID to restart")
    retry_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    retry_parser.set_defaults(func=cmd_retry)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
