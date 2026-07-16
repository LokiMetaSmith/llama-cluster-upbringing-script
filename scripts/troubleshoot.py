#!/usr/bin/env python3
"""
Nomad & Systemd Cluster Troubleshooting, Health Probing, and Healing CLI

A comprehensive health probing, logging, and self-healing daemon designed for both
human operators and autonomous agents. It diagnoses, retries, and heals failed
Nomad allocations and Systemd services system-wide.
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
import time
from datetime import datetime


try:
    from sudo_env import load_sudo_env
    load_sudo_env()
except ImportError:
    pass


NOMAD_URL = os.environ.get("NOMAD_ADDR", "http://localhost:4646")

# Determine Repo Root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

# List of critical systemd services to monitor system-wide
CRITICAL_SYSTEMD_SERVICES = [
    "consul",
    "nomad",
    "docker",
    "tailscaled",
    "unified_fs",
    "power-agent",
    "provisioning-api",
    "paddler-balancer",
]


class DummyArgs:
    """Helper class to mock parsed CLI arguments for programmatic calls."""
    def __init__(self, **kwargs):
        self.json = False
        self.interval = 60
        self.job_id = None
        for k, v in kwargs.items():
            setattr(self, k, v)


def get_ssl_context():
    """Generates the appropriate SSL context for Nomad API connections."""
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


def get_git_commit_hash():
    """Queries git for the current repository commit hash."""
    res = run_command(["git", "rev-parse", "HEAD"])
    if res["exit_code"] == 0:
        return res["stdout"].strip()
    return "unknown (not a git repo or git not installed)"


def run_legacy_command(command, shell=False, env=None, quiet=False):
    """Run a shell command and return its output for reports."""
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
    """Generates formatted section headings for reports."""
    return f"\n{'='*80}\n {title}\n{'='*80}\n"


def check_systemd_service(service_name):
    """Checks systemd service status via systemctl show."""
    res = run_command(["systemctl", "show", service_name, "--property=ActiveState,SubState,LoadState,UnitFileState"])
    if res["exit_code"] != 0:
        return {"name": service_name, "status": "unknown", "error": res["stderr"]}

    props = {}
    for line in res["stdout"].splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            props[k.strip()] = v.strip()

    active_state = props.get("ActiveState", "unknown")
    sub_state = props.get("SubState", "unknown")
    load_state = props.get("LoadState", "unknown")

    status = "healthy"
    if active_state != "active":
        status = "failed" if active_state in ["failed", "inactive"] else "unhealthy"

    return {
        "name": service_name,
        "active_state": active_state,
        "sub_state": sub_state,
        "load_state": load_state,
        "status": status,
        "unit_file_state": props.get("UnitFileState", "unknown")
    }


def get_failed_systemd_services():
    """Queries systemctl for failed services."""
    res = run_command(["systemctl", "list-units", "--type=service", "--state=failed", "--no-legend"])
    failed_services = []
    if res["exit_code"] == 0:
        for line in res["stdout"].splitlines():
            parts = line.split()
            if parts:
                svc_name = parts[0]
                failed_services.append(svc_name)
    return failed_services


def restart_systemd_service(service_name):
    """Restarts a systemd service (using sudo if necessary)."""
    res = run_command(["systemctl", "restart", service_name])
    if res["exit_code"] != 0 and "permission" in res["stderr"].lower():
        res = run_command(["sudo", "-n", "systemctl", "restart", service_name])
    return res


def get_systemd_logs(service_name, lines=50):
    """Fetches systemd logs for a service from journalctl."""
    res = run_command(["journalctl", "-u", service_name, "-n", str(lines), "--no-pager"])
    if res["exit_code"] != 0 and "permission" in res["stderr"].lower():
        res = run_command(["sudo", "-n", "journalctl", "-u", service_name, "-n", str(lines), "--no-pager"])
    return res["stdout"] if res["exit_code"] == 0 else ""


def get_docker_containers():
    """Queries docker daemon for status of all containers."""
    res = run_command(["docker", "ps", "-a", "--format", "{{.ID}}|{{.Names}}|{{.State}}|{{.Status}}"])
    containers = []
    if res["exit_code"] == 0:
        for line in res["stdout"].splitlines():
            if "|" in line:
                parts = line.split("|")
                if len(parts) == 4:
                    cid, name, state, status = parts
                    containers.append({
                        "id": cid,
                        "name": name,
                        "state": state,
                        "status": status,
                        "healthy": state == "running"
                    })
    return containers


def api_get(endpoint):
    """Generic HTTP GET helper for Nomad API."""
    url = f"{NOMAD_URL}{endpoint}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=get_ssl_context()) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        # Avoid noisy print if on programmatic checks
        pass
    return None


def run_command(command, shell=False):
    """Runs a system command cleanly, capturing exit code and streams."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, universal_newlines=True, timeout=30)
        return {"exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"exit_code": -1, "stdout": "", "stderr": str(e)}


def format_time(ns_timestamp):
    """Formats a nanosecond timestamp into human-readable local time."""
    if not ns_timestamp:
        return ""
    try:
        ts = int(ns_timestamp) / 1e9
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ns_timestamp)


def fetch_alloc_logs_with_fallback(alloc_id, task_name, log_type="stderr"):
    """
    Fetches the logs of an allocation, with fallback to task events or docker container logs
    if Nomad client returns 404 (state not found on client).
    """
    res = run_command(["nomad", "alloc", "logs", f"-{log_type}", "-tail", "-n", "100", alloc_id, task_name])
    if res["exit_code"] == 0 and res["stdout"].strip() != "":
        return res["stdout"]

    err_str = res["stderr"] + res["stdout"]
    is_404 = "404" in err_str or "state for allocation" in err_str or "not found on client" in err_str or res["exit_code"] != 0

    fallback_report = []
    if is_404:
        fallback_report.append(f"⚠️  [LOG FALLBACK] Standard Nomad log retrieval for alloc {alloc_id[:8]} task '{task_name}' failed or returned 404.")

        # Fallback A: Query allocation status API to find TaskStates and Events
        alloc_info = api_get(f"/v1/allocation/{alloc_id}")
        if alloc_info:
            task_states = alloc_info.get("TaskStates", {})
            task_state = task_states.get(task_name, {})
            events = task_state.get("Events", [])
            fallback_report.append("--- Parsed Task Allocation Events ---")
            if events:
                for evt in events[-10:]:
                    ts = format_time(evt.get("Time"))
                    evt_type = evt.get("Type", "N/A")
                    msg = evt.get("Message", "")
                    fallback_report.append(f"  [{ts}] [{evt_type}] {msg}")
                    for field in ['ValidationError', 'DriverError', 'KillError', 'DownloadError', 'VaultError', 'SetupError']:
                        err_val = evt.get(field)
                        if err_val:
                            fallback_report.append(f"      {field}: {err_val}")
            else:
                fallback_report.append("  No events found in task state.")
        else:
            fallback_report.append("  Could not fetch allocation state via Nomad API.")

        # Fallback B: Look for docker container
        docker_res = run_command(["docker", "ps", "-a", "--filter", f"label=com.hashicorp.nomad.alloc_id={alloc_id}", "--format", "{{.ID}}"])
        if docker_res["exit_code"] == 0 and docker_res["stdout"].strip():
            container_id = docker_res["stdout"].splitlines()[0].strip()
            fallback_report.append(f"--- Fallback Docker Container Found: {container_id[:12]} ---")
            docker_logs_res = run_command(["docker", "logs", "--tail", "100", container_id])
            if docker_logs_res["exit_code"] == 0:
                fallback_report.append(docker_logs_res["stdout"])
                fallback_report.append(docker_logs_res["stderr"])
            else:
                fallback_report.append(f"  Failed to get docker logs: {docker_logs_res['stderr']}")

        # Fallback C: Look in local nomad allocation logs directory directly if on the node
        alloc_dir = f"/opt/nomad/data/alloc/{alloc_id}/alloc/logs"
        if os.path.exists(alloc_dir):
            fallback_report.append(f"--- Fallback Direct Directory Read: {alloc_dir} ---")
            log_file_path = os.path.join(alloc_dir, f"{task_name}.{log_type}.0")
            if os.path.exists(log_file_path):
                try:
                    with open(log_file_path, "r") as lf:
                        fallback_report.append(lf.read()[-5000:])
                except Exception as lf_err:
                    fallback_report.append(f"  Error reading log file directly: {lf_err}")
            else:
                fallback_report.append(f"  Log file not found directly at {log_file_path}")

        return "\n".join(fallback_report)

    return res.get("stdout", "")


def cmd_list(args):
    """List jobs in dead or pending state."""
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


def cmd_inspect(args):
    """Inspects a specific job ID and outputs failure diagnostics."""
    job_id = args.job_id
    job_info = api_get(f"/v1/job/{job_id}")
    allocs = api_get(f"/v1/job/{job_id}/allocations")

    if not job_info:
        print(f"Error: Job {job_id} not found or accessible.")
        sys.exit(1)

    evaluations = api_get(f"/v1/job/{job_id}/evaluations")

    inspect_data = {
        "job_id": job_id,
        "job_status": job_info.get("Status"),
        "submit_time": format_time(job_info.get("SubmitTime")),
        "allocations": [],
        "placement_failures": []
    }

    if evaluations:
        evaluations.sort(key=lambda x: x.get('CreateIndex', 0), reverse=True)
        for ev in evaluations[:1]:
            failed_allocs = ev.get("FailedTGAllocs")
            if failed_allocs:
                for tg, metrics in failed_allocs.items():
                    fail_info = {
                        "task_group": tg,
                        "dimension_exhausted": metrics.get("DimensionExhausted", {}),
                        "class_exhausted": metrics.get("ClassExhausted", {}),
                        "constraint_filtered": metrics.get("ConstraintFiltered", {}),
                        "nodes_evaluated": metrics.get("NodesEvaluated", 0),
                        "nodes_filtered": metrics.get("NodesFiltered", 0),
                        "nodes_exhausted": metrics.get("NodesExhausted", 0)
                    }
                    inspect_data["placement_failures"].append(fail_info)

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
                    task_data["logs"]["stderr"] = fetch_alloc_logs_with_fallback(alloc.get("ID"), task_name, "stderr")
                alloc_data["tasks"][task_name] = task_data
            inspect_data["allocations"].append(alloc_data)

    if args.json:
        print(json.dumps(inspect_data, indent=2))
        return

    print(f"=== Inspecting Job: {job_id} ===")
    print(f"Status: {inspect_data['job_status']} | Submitted: {inspect_data['submit_time']}")

    if inspect_data["placement_failures"]:
        print("\n=== Placement Failures ===")
        for failure in inspect_data["placement_failures"]:
            print(f"Task Group: {failure['task_group']}")
            print(f"  Nodes Evaluated: {failure['nodes_evaluated']}")
            print(f"  Nodes Filtered: {failure['nodes_filtered']}")
            print(f"  Nodes Exhausted: {failure['nodes_exhausted']}")

    if not inspect_data["allocations"]:
        print("\nNo allocations found for this job.")
        return
    for alloc in inspect_data["allocations"]:
        print(f"\n--- Allocation: {alloc['alloc_id'][:8]} (Status: {alloc['client_status']}) ---")
        for task_name, task in alloc["tasks"].items():
            print(f"  Task: {task_name} | State: {task['state']} | Failed: {task['failed']}")
            if task["events"]:
                print("  Recent Events:")
                for evt in task["events"]:
                    print(f"    - [{evt['time']}] {evt['type']}: {evt['message']}")
            if task["logs"].get("stderr"):
                print("  Recent Stderr Logs:")
                lines = task["logs"]["stderr"].splitlines()
                for line in lines[-20:]:
                    print(f"      {line}")


def cmd_retry(args):
    """Triggers restart of a specific job ID."""
    job_id = args.job_id
    if not args.json:
        print(f"Attempting to restart job {job_id}...")
    res = run_command(["nomad", "job", "restart", "-yes", job_id])
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


def cmd_report(args):
    """Generates a comprehensive legacy troubleshooting report."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_file = f"troubleshoot_report_{timestamp}.txt"

    if not args.json:
        print(f"Generating troubleshooting report: {report_file}")

    with open(report_file, 'w') as f:
        f.write(section("TROUBLESHOOTING REPORT"))
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Hostname: {os.uname().nodename}\n")
        f.write(f"Git Commit Hash: {get_git_commit_hash()}\n")
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
        f.write(run_legacy_command("consul members", env=env, quiet=args.json))
        f.write(run_legacy_command("consul catalog services", env=env, quiet=args.json))

        f.write(section("NOMAD STATUS"))
        f.write(run_legacy_command("nomad server members", quiet=args.json))
        f.write(run_legacy_command("nomad node status", quiet=args.json))
        f.write(run_legacy_command("nomad job status", quiet=args.json))

        f.write(section("NOMAD JOB ANALYSIS"))
        allocs = get_nomad_allocations(quiet=args.json)
        if allocs:
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

            for alloc in top_failures:
                alloc_id = alloc.get('ID')
                short_id = alloc_id[:8]
                job_id = alloc.get('JobID')
                f.write(f"\n--- Logs for Allocation {short_id} (Job: {job_id}) ---\n")
                task_states = alloc.get('TaskStates', {})
                for task_name, state in task_states.items():
                    if state.get('Failed') or state.get('State') == 'dead':
                        f.write(f"Task: {task_name} (State: {state.get('State')})\n")
                        f.write(f"Fetching stderr fallback logs for task '{task_name}'...\n")
                        f.write(fetch_alloc_logs_with_fallback(alloc_id, task_name, "stderr") + "\n")
        else:
            f.write("Could not retrieve allocations for analysis.\n")

    if args.json:
        print(json.dumps({"status": "success", "report_file": report_file}, indent=2))
        return

    print(f"Report generation complete. Output saved to: {report_file}")


def cmd_probe(args):
    """Probes system-wide health of Nomad jobs, Systemd services, and Docker containers."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = {
        "timestamp": timestamp,
        "system": {
            "hostname": os.uname().nodename,
            "user": getpass.getuser(),
            "git_commit_hash": get_git_commit_hash()
        },
        "nomad_jobs": [],
        "systemd_services": [],
        "docker_containers": [],
        "summary": {
            "unhealthy_count": 0,
            "total_count": 0,
            "status": "nominal"
        }
    }

    # 1. Probe Nomad
    jobs = api_get("/v1/jobs")
    if jobs is not None:
        for job in jobs:
            job_id = job.get("ID")
            status = job.get("Status", "").lower()
            job_report = {
                "id": job_id,
                "type": job.get("Type"),
                "status": status,
                "healthy": status not in ["dead", "failed"]
            }
            report["nomad_jobs"].append(job_report)
            report["summary"]["total_count"] += 1
            if not job_report["healthy"]:
                report["summary"]["unhealthy_count"] += 1

    # 2. Probe Systemd critical services
    for svc in CRITICAL_SYSTEMD_SERVICES:
        svc_state = check_systemd_service(svc)
        report["systemd_services"].append(svc_state)
        report["summary"]["total_count"] += 1
        if svc_state.get("status") != "healthy":
            report["summary"]["unhealthy_count"] += 1

    # Dynamic failed Systemd units addition
    failed_svcs = get_failed_systemd_services()
    for svc in failed_svcs:
        # Avoid duplicating critical services
        clean_name = svc.replace(".service", "")
        if clean_name not in CRITICAL_SYSTEMD_SERVICES and svc not in CRITICAL_SYSTEMD_SERVICES:
            svc_state = check_systemd_service(svc)
            report["systemd_services"].append(svc_state)
            report["summary"]["total_count"] += 1
            report["summary"]["unhealthy_count"] += 1

    # 3. Probe Docker containers
    containers = get_docker_containers()
    for container in containers:
        report["docker_containers"].append(container)
        report["summary"]["total_count"] += 1
        if not container["healthy"]:
            report["summary"]["unhealthy_count"] += 1

    if report["summary"]["unhealthy_count"] > 0:
        report["summary"]["status"] = "degraded"

    if args.json:
        print(json.dumps(report, indent=2))
        return report

    print(f"=== System Health Probe: {report['summary']['status'].upper()} ===")
    print(f"Time: {timestamp} | Host: {report['system']['hostname']} | Git Hash: {report['system']['git_commit_hash']}")
    print("-" * 60)

    print("\n--- Nomad Jobs ---")
    if report["nomad_jobs"]:
        for job in report["nomad_jobs"]:
            status_char = "✅" if job["healthy"] else "❌"
            print(f" {status_char} {job['id']:<30} | {job['type']:<15} | {job['status']}")
    else:
        print(" No Nomad jobs detected.")

    print("\n--- Systemd Services ---")
    for svc in report["systemd_services"]:
        status_char = "✅" if svc["status"] == "healthy" else "❌"
        print(f" {status_char} {svc['name']:<30} | Active: {svc.get('active_state', 'unknown'):<12} | SubState: {svc.get('sub_state', 'unknown')}")

    print("\n--- Docker Containers ---")
    if report["docker_containers"]:
        for container in report["docker_containers"]:
            status_char = "✅" if container["healthy"] else "❌"
            print(f" {status_char} {container['name']:<30} | State: {container['state']:<12} | Status: {container['status']}")
    else:
        print(" No Docker containers detected.")

    print("-" * 60)
    print(f"Summary: {report['summary']['unhealthy_count']} / {report['summary']['total_count']} units unhealthy.")
    return report


def cmd_heal(args):
    """Force runs dead/failed services/jobs system-wide and verifies execution."""
    print("🚀 Initiating System Healing / Force-Run Sequence...")
    probe_args = DummyArgs(json=True)
    health_state = cmd_probe(probe_args)

    healed_units = []

    # 1. Heal Nomad Jobs
    for job in health_state["nomad_jobs"]:
        if not job["healthy"]:
            job_id = job["id"]
            print(f"\n[Heal] Attempting to force-run failed Nomad Job: {job_id}")
            allocs = api_get(f"/v1/job/{job_id}/allocations")
            if allocs:
                allocs.sort(key=lambda x: x.get('ModifyTime', 0), reverse=True)
                latest_alloc = allocs[0]
                alloc_id = latest_alloc.get("ID")
                print(f"[Heal] Capturing diagnostics for allocation {alloc_id[:8]}...")
                task_states = latest_alloc.get("TaskStates", {})
                for task_name in task_states.keys():
                    err_logs = fetch_alloc_logs_with_fallback(alloc_id, task_name, "stderr")
                    out_logs = fetch_alloc_logs_with_fallback(alloc_id, task_name, "stdout")
                    log_file_dir = os.path.join(REPO_ROOT, "logs", "healer")
                    os.makedirs(log_file_dir, exist_ok=True)
                    log_filepath = os.path.join(log_file_dir, f"{job_id}_{task_name}_{alloc_id[:8]}_stderr.log")
                    with open(log_filepath, "w") as lf:
                        lf.write(f"Timestamp: {datetime.now()}\n--- STDERR LOGS ---\n{err_logs}\n--- STDOUT LOGS ---\n{out_logs}\n")
                    print(f"  Captured and saved logs to: {log_filepath}")

            print(f"[Heal] Restarting Nomad job {job_id}...")
            res = run_command(["nomad", "job", "restart", "-yes", job_id])
            if res["exit_code"] == 0:
                healed_units.append({"type": "Nomad Job", "id": job_id})
                print(f"  Successfully triggered restart command for {job_id}.")
            else:
                print(f"  Nomad command line restart failed. Attempting Ansible healing playbook for {job_id}...")
                solution_json = json.dumps({"action": "restart", "parameters": {"job_id": job_id}})
                playbook_res = run_command(["ansible-playbook", os.path.join(REPO_ROOT, "playbooks", "heal_job.yaml"), "-e", f"solution_json={solution_json}"])
                if playbook_res["exit_code"] == 0:
                    healed_units.append({"type": "Nomad Job", "id": job_id})
                    print(f"  Successfully healed {job_id} using heal_job.yaml playbook.")
                else:
                    print(f"  Failed to heal {job_id} via playbook: {playbook_res['stderr']}")

    # 2. Heal Systemd Services
    for svc in health_state["systemd_services"]:
        if svc["status"] != "healthy":
            svc_name = svc["name"]
            print(f"\n[Heal] Attempting to force-run failed Systemd Service: {svc_name}")
            logs = get_systemd_logs(svc_name, lines=100)
            log_file_dir = os.path.join(REPO_ROOT, "logs", "healer")
            os.makedirs(log_file_dir, exist_ok=True)
            log_filepath = os.path.join(log_file_dir, f"systemd_{svc_name}_stderr.log")
            with open(log_filepath, "w") as lf:
                lf.write(f"Timestamp: {datetime.now()}\nSystemd Logs:\n{logs}\n")
            print(f"  Captured and saved logs to: {log_filepath}")

            print(f"[Heal] Restarting Systemd service {svc_name}...")
            restart_res = restart_systemd_service(svc_name)
            if restart_res["exit_code"] == 0:
                healed_units.append({"type": "Systemd Service", "id": svc_name})
                print(f"  Successfully restarted {svc_name}.")
            else:
                print(f"  Failed to restart service {svc_name}: {restart_res['stderr']}")

    # 3. Post-Heal Verification
    if healed_units:
        print("\n⌛ Waiting 10 seconds for services to initialize...")
        time.sleep(10)

        print("\n🔍 Verifying healed systems...")
        verify_state = cmd_probe(probe_args)

        print("\n=== Healing Verification Report ===")
        for unit in healed_units:
            utype = unit["type"]
            uid = unit["id"]
            found_healthy = False

            if utype == "Nomad Job":
                for job in verify_state["nomad_jobs"]:
                    if job["id"] == uid and job["healthy"]:
                        found_healthy = True
                        break
            elif utype == "Systemd Service":
                for svc in verify_state["systemd_services"]:
                    if svc["name"] == uid and svc["status"] == "healthy":
                        found_healthy = True
                        break

            status_char = "✅ SUCCESS" if found_healthy else "❌ FAILED"
            print(f" {status_char} | {utype}: {uid}")
    else:
        print("\n✅ All systems were already healthy. No healing required.")

    print("\n✅ Healing process run complete.")
    if args.json:
        print(json.dumps({"status": "complete", "healed_units": healed_units}, indent=2))


def cmd_daemon(args):
    """Runs the continuous daemon loop that periodically probes and heals the cluster."""
    interval = args.interval if hasattr(args, "interval") and args.interval else 60
    print(f"🔄 Starting Autonomous Self-Healing Daemon Loop (Interval: {interval}s)...")

    cycle_count = 0
    while True:
        cycle_count += 1
        print(f"\n--- [Daemon Loop Cycle {cycle_count}] Starting health check at {datetime.now()} ---")

        probe_args = DummyArgs(json=True)
        health_state = cmd_probe(probe_args)

        unhealthy_count = health_state["summary"]["unhealthy_count"]
        if unhealthy_count > 0:
            print(f"⚠️  Detected {unhealthy_count} unhealthy unit(s). Triggering self-healing...")
            heal_args = DummyArgs(json=False)
            cmd_heal(heal_args)
        else:
            print("✅ All systems nominal. No healing needed.")

        # Periodic summary log writing
        log_file_dir = os.path.join(REPO_ROOT, "logs")
        os.makedirs(log_file_dir, exist_ok=True)
        daemon_log_path = os.path.join(log_file_dir, "self_healing_daemon.log")
        with open(daemon_log_path, "a") as lf:
            lf.write(f"[{datetime.now()}] Cycle {cycle_count} completed. Unhealthy: {unhealthy_count} | Status: {health_state['summary']['status']}\n")

        print(f"--- [Daemon Loop Cycle {cycle_count}] Complete. Sleeping for {interval}s... ---")
        time.sleep(interval)


def cmd_opencode_status(args):
    """Checks the status of Opencode cross-referencing Nomad, Consul, and system processes."""
    if not args.json:
        print("=== Opencode Unified Diagnostic Report ===")

    # 1. Query Nomad Allocations
    allocations = get_nomad_allocations(quiet=True)
    opencode_allocs = []
    if allocations:
        for alloc in allocations:
            job_id = alloc.get("JobID", "")
            if "opencode" in job_id.lower():
                opencode_allocs.append({
                    "id": alloc.get("ID"),
                    "job_id": job_id,
                    "node_name": alloc.get("NodeName", "N/A"),
                    "client_status": alloc.get("ClientStatus", "N/A"),
                    "desired_status": alloc.get("DesiredStatus", "N/A"),
                    "create_time": format_time(alloc.get("CreateTime", 0))
                })

    # 2. Query Consul Health Checks
    consul_url = "http://127.0.0.1:8500/v1/health/service/opencode-api"
    consul_checks = []
    try:
        req = urllib.request.Request(consul_url)
        consul_token = get_consul_token()
        if consul_token:
            req.add_header("X-Consul-Token", consul_token)
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for node_svc in data:
                    node_name = node_svc.get("Node", {}).get("Node", "N/A")
                    address = node_svc.get("Service", {}).get("Address", "N/A")
                    port = node_svc.get("Service", {}).get("Port", "N/A")
                    checks = node_svc.get("Checks", [])
                    status = "passing"
                    for chk in checks:
                        if chk.get("ServiceName") == "opencode-api" and chk.get("Status") != "passing":
                            status = chk.get("Status")
                    consul_checks.append({
                        "node": node_name,
                        "address": address,
                        "port": port,
                        "status": status
                    })
    except Exception:
        pass

    # 3. Query System-level Processes
    system_processes = []
    res = run_command(["ps", "-eo", "pid,ppid,%cpu,%mem,etime,cmd"])
    if res["exit_code"] == 0:
        for line in res["stdout"].splitlines():
            if "opencode" in line and "grep" not in line and "troubleshoot.py" not in line:
                parts = line.strip().split(None, 5)
                if len(parts) >= 6:
                    pid, ppid, cpu, mem, etime, cmd = parts
                    system_processes.append({
                        "pid": pid,
                        "ppid": ppid,
                        "cpu": cpu,
                        "mem": mem,
                        "etime": etime,
                        "cmd": cmd
                    })

    if args.json:
        report = {
            "nomad_allocations": opencode_allocs,
            "consul_health_checks": consul_checks,
            "system_processes": system_processes
        }
        print(json.dumps(report, indent=2))
        return

    print("\n--- Nomad Allocations ---")
    if opencode_allocs:
        print(f"{'Alloc ID':<10} | {'Job ID':<30} | {'Node':<15} | {'ClientStatus':<12} | {'Desired':<10}")
        print("-" * 85)
        for alloc in opencode_allocs:
            print(f"{alloc['id'][:8]:<10} | {alloc['job_id']:<30} | {alloc['node_name']:<15} | {alloc['client_status']:<12} | {alloc['desired_status']:<10}")
    else:
        print("No opencode allocations found in Nomad.")

    print("\n--- Consul Service Status ---")
    if consul_checks:
        print(f"{'Node':<20} | {'Address':<20} | {'Port':<8} | {'Status':<10}")
        print("-" * 64)
        for chk in consul_checks:
            print(f"{chk['node']:<20} | {chk['address']:<20} | {chk['port']:<8} | {chk['status']:<10}")
    else:
        print("No opencode-api services registered in Consul.")

    print("\n--- System-level Processes ---")
    if system_processes:
        print(f"{'PID':<8} | {'PPID':<8} | {'%CPU':<5} | {'%MEM':<5} | {'Running Time':<12} | {'Command'}")
        print("-" * 100)
        for proc in system_processes:
            print(f"{proc['pid']:<8} | {proc['ppid']:<8} | {proc['cpu']:<5} | {proc['mem']:<5} | {proc['etime']:<12} | {proc['cmd'][:60]}")
        print(f"\nTotal system processes found: {len(system_processes)}")
    else:
        print("No opencode processes found running on this host.")


def main():
    """Main CLI execution entry point."""
    parser = argparse.ArgumentParser(description="Troubleshoot Nomad & Systemd services.")
    subparsers = parser.add_subparsers(dest="command")

    opencode_status_parser = subparsers.add_parser("opencode-status", help="Unified Opencode status diagnostics")
    opencode_status_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    opencode_status_parser.set_defaults(func=cmd_opencode_status)

    list_parser = subparsers.add_parser("list", help="List Nomad jobs in dead or pending state")
    list_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    list_parser.set_defaults(func=cmd_list)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a specific job failed diagnostics")
    inspect_parser.add_argument("job_id", help="The Nomad Job ID to inspect")
    inspect_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    inspect_parser.set_defaults(func=cmd_inspect)

    retry_parser = subparsers.add_parser("retry", help="Retry/Restart a specific Nomad job")
    retry_parser.add_argument("job_id", help="The Nomad Job ID to restart")
    retry_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    retry_parser.set_defaults(func=cmd_retry)

    report_parser = subparsers.add_parser("report", help="Generate a comprehensive troubleshooting report")
    report_parser.add_argument("--json", action="store_true", help="Output status in JSON format")
    report_parser.set_defaults(func=cmd_report)

    probe_parser = subparsers.add_parser("probe", help="Probe system-wide health (Nomad, Systemd, Docker, Consul)")
    probe_parser.add_argument("--json", action="store_true", help="Output probe results in JSON format")
    probe_parser.set_defaults(func=cmd_probe)

    heal_parser = subparsers.add_parser("heal", help="Force run dead/failed services/jobs and validate")
    heal_parser.add_argument("--json", action="store_true", help="Output healing summary in JSON format")
    heal_parser.set_defaults(func=cmd_heal)

    daemon_parser = subparsers.add_parser("daemon", help="Run self-healing daemon loop")
    daemon_parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds (default: 60)")
    daemon_parser.add_argument("--json", action="store_true", help="Output daemon stats in JSON format")
    daemon_parser.set_defaults(func=cmd_daemon)

    args = parser.parse_args()
    if args.command is None:
        # Default to comprehensive troubleshooting report
        args.json = False
        cmd_report(args)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
