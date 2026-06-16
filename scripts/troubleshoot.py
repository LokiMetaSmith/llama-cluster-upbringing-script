#!/usr/bin/env python3
"""
Nomad Job Troubleshooting CLI

A tool designed for both humans and AI agents to debug and retry failed Nomad jobs.
Includes a legacy report generator.
"""
import os
import sys
import json
import ssl
import argparse
import urllib.request
import urllib.error
import urllib.parse
import subprocess
import getpass
import tempfile
from datetime import datetime

NOMAD_URL = os.environ.get("NOMAD_ADDR", "https://127.0.0.1:4646")

def get_ssl_context():
    if NOMAD_URL.startswith("https"):
        context = ssl.create_default_context()
        if hasattr(ssl, 'VERIFY_X509_STRICT'):
            context.verify_flags &= ~ssl.VERIFY_X509_STRICT

        if os.environ.get("NOMAD_TLS_SKIP_VERIFY") in ["1", "true", "True"]:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        else:
            cacert = os.environ.get("NOMAD_CACERT")
            if cacert and os.path.exists(cacert):
                context.load_verify_locations(cafile=cacert)

        client_cert = os.environ.get("NOMAD_CLIENT_CERT")
        client_key = os.environ.get("NOMAD_CLIENT_KEY")
        if client_cert and client_key and os.path.exists(client_cert) and os.path.exists(client_key):
            context.load_cert_chain(certfile=client_cert, keyfile=client_key)

        return context
    return None


# --- Legacy Report Helpers ---
def get_consul_token():
    """Retrieve Consul management token."""
    if "CONSUL_HTTP_TOKEN" in os.environ:
        return os.environ["CONSUL_HTTP_TOKEN"]

    token_file = "/etc/consul.d/management_token"
    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                return f.read().strip()
        except PermissionError:
            pass
        except Exception:
            pass
    try:
        result = subprocess.run(["sudo", "-n", "cat", token_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None

def run_legacy_command(command, shell=False, env=None, quiet=False):
    """Run a shell command and return its output for the legacy report."""
    try:
        if isinstance(command, list):
            cmd_str = " ".join(command)
        else:
            cmd_str = command
            shell = True

        if not quiet:
            print(f"Running: {cmd_str}...")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell, universal_newlines=True, timeout=30, env=env)
        return f"$ {cmd_str}\n{result.stdout}\n"
    except Exception as e:
        return f"Error running command '{command}': {e}\n"

def get_nomad_allocations(quiet=False):
    """Fetch allocations from Nomad API."""
    url = f"{NOMAD_URL}/v1/allocations"
    try:
        with urllib.request.urlopen(url, context=get_ssl_context()) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        if not quiet:
            print(f"Error fetching allocations: {e}", file=sys.stderr)
        return []

def section(title):
    return f"\n{'='*80}\n {title}\n{'='*80}\n"

def cmd_report(args):
    """Generate a comprehensive legacy troubleshooting report."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_file = f"troubleshoot_report_{timestamp}.txt"

    if not args.json:
        print(f"Generating troubleshooting report: {report_file}")

    with open(report_file, 'w') as f:
        f.write(section("TROUBLESHOOTING REPORT"))
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Hostname: {os.uname().nodename}\n")
        try:
            user = getpass.getuser()
        except Exception:
            user = os.environ.get('USER', 'unknown')
        f.write(f"User: {user}\n")

        f.write(section("SYSTEM RESOURCES"))
        f.write(run_legacy_command("uptime", quiet=args.json))
        f.write(run_legacy_command("free -h", quiet=args.json))
        f.write(run_legacy_command("df -h", quiet=args.json))

        f.write(section("DOCKER STATUS"))
        f.write(run_legacy_command("docker ps -a", quiet=args.json))

        f.write(section("CONSUL STATUS"))
        env = os.environ.copy()
        consul_token = get_consul_token()
        if consul_token:
            env["CONSUL_HTTP_TOKEN"] = consul_token
            if not args.json:
                print("Using Consul token for queries.")
        else:
            if not args.json:
                print("Warning: Could not retrieve Consul token. Service queries might be empty.")

        f.write(run_legacy_command("consul members", env=env, quiet=args.json))
        f.write(run_legacy_command("consul catalog services", env=env, quiet=args.json))

        f.write("\n--- Stale Services Analysis ---\n")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prune_script = os.path.join(script_dir, "prune_consul_services.py")
        if os.path.exists(prune_script):
            f.write(run_legacy_command([sys.executable, prune_script, "--dry-run"], env=env, quiet=args.json))
        else:
            f.write(f"Script not found: {prune_script}\n")

        f.write(section("NOMAD STATUS"))
        f.write(run_legacy_command("nomad server members", quiet=args.json))
        f.write(run_legacy_command("nomad node status", quiet=args.json))
        f.write(run_legacy_command("nomad job status", quiet=args.json))

        f.write(section("NOMAD JOB ANALYSIS"))
        analyze_script = os.path.join(script_dir, "analyze_nomad_allocs.py")
        allocs = get_nomad_allocations(quiet=args.json)
        if allocs:
            fd, temp_path = tempfile.mkstemp(suffix=".json")
            try:
                with os.fdopen(fd, 'w') as tmp:
                    json.dump(allocs, tmp)
                if os.path.exists(analyze_script):
                    f.write(run_legacy_command([sys.executable, analyze_script, temp_path], quiet=args.json))
                else:
                    f.write(f"Script not found: {analyze_script}\n")

                f.write(section("RECENT FAILED ALLOCATION LOGS"))
                failed_allocs = []
                for a in allocs:
                    if a.get('ClientStatus') == 'failed':
                        failed_allocs.append(a)
                        continue
                    task_states = a.get('TaskStates', {})
                    for state in task_states.values():
                        if state.get('Failed', False):
                            failed_allocs.append(a)
                            break
                failed_allocs.sort(key=lambda x: x.get('ModifyTime', 0), reverse=True)
                top_failures = failed_allocs[:5]

                if not top_failures:
                    f.write("No failed allocations found.\n")

                for alloc in top_failures:
                    alloc_id = alloc.get('ID')
                    short_id = alloc_id[:8]
                    job_id = alloc.get('JobID')
                    f.write(f"\n--- Logs for Allocation {short_id} (Job: {job_id}) ---\n")
                    task_states = alloc.get('TaskStates', {})
                    for task_name, state in task_states.items():
                        if state.get('Failed') or state.get('State') == 'dead':
                            f.write(f"Task: {task_name} (State: {state.get('State')})\n")
                            f.write(f"Fetching stderr for task '{task_name}'...\n")
                            f.write(run_legacy_command(["nomad", "alloc", "logs", "-stderr", "-tail", "-n", "100", alloc_id, task_name], quiet=args.json))
            finally:
                os.remove(temp_path)
        else:
            f.write("Could not retrieve allocations for analysis.\n")

    if args.json:
        print(json.dumps({"status": "success", "report_file": report_file}, indent=2))
        return

    print(f"Report generation complete. Output saved to: {report_file}")

# --- Agent CLI Helpers ---
def api_get(endpoint):
    url = f"{NOMAD_URL}{endpoint}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=get_ssl_context()) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error calling {url}: {e}", file=sys.stderr)
    return None

def run_command(command, shell=False):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, universal_newlines=True, timeout=30)
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
    res = run_command(["nomad", "alloc", "logs", f"-{log_type}", "-tail", "-n", "100", alloc_id, task_name])
    return res.get("stdout", "")

def cmd_inspect(args):
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
        allocs.sort(key=lambda x: x.get('ModifyTime', 0), reverse=True)
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
                events = state.get("Events", [])
                for evt in events[-5:]:
                    task_data["events"].append({
                        "type": evt.get("Type"),
                        "time": format_time(evt.get("Time")),
                        "message": evt.get("Message", ""),
                        "details": evt.get("Details", {})
                    })
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
                for line in lines[-20:]:
                    print(f"      {line}")

def cmd_retry(args):
    job_id = args.job_id
    if not args.json:
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

    list_parser = subparsers.add_parser("list", help="List jobs in dead or pending state")
    list_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    list_parser.set_defaults(func=cmd_list)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a specific job")
    inspect_parser.add_argument("job_id", help="The Nomad Job ID to inspect")
    inspect_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    inspect_parser.set_defaults(func=cmd_inspect)

    retry_parser = subparsers.add_parser("retry", help="Retry/Restart a specific job")
    retry_parser.add_argument("job_id", help="The Nomad Job ID to restart")
    retry_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    retry_parser.set_defaults(func=cmd_retry)

    report_parser = subparsers.add_parser("report", help="Generate a legacy full system troubleshooting report")
    report_parser.add_argument("--json", action="store_true", help="Output status in JSON format")
    report_parser.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
