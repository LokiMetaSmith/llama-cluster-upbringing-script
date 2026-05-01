#!/usr/bin/env python3
"""
Provisioning Script for Hybrid Architecture.
Replaces the logic of bootstrap.sh with a more robust, extensible Python script.

Usage:
    python3 provisioning.py [--role ROLE] [--tags TAGS] [--continue] [--verbose LEVEL] ...
"""

import argparse
import os
import re
import sys
import subprocess
import time
import socket
import yaml
import shutil
import glob
import json

# --- Constants ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
STATE_FILE = os.path.join(REPO_ROOT, ".provisioning_state")
LOG_FILE = os.path.join(REPO_ROOT, "playbook_output.log")
INVENTORY_FILE = os.path.join(REPO_ROOT, "local_inventory.ini")

# --- Colors & formatting ---
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

WARNINGS = []
ERRORS = []

# --- Helper Functions ---

def print_warning(msg):
    """Prints a warning message and adds it to the tracking list."""
    full_msg = f"{Colors.WARNING}⚠️  {msg}{Colors.ENDC}"
    print(full_msg)
    WARNINGS.append(msg)

def print_error(msg):
    """Prints an error message and adds it to the tracking list."""
    full_msg = f"{Colors.FAIL}❌ {msg}{Colors.ENDC}"
    print(full_msg)
    ERRORS.append(msg)

def print_header(msg):
    """Prints a styled header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}")
    print(f" {msg}")
    print(f"{'=' * 60}{Colors.ENDC}")

def print_task_header(msg):
    """Prints a styled task header."""
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}┌────────────────────────────────────────────────────────┐")
    print(f"│ 🚀 {msg:<50} │")
    print(f"└────────────────────────────────────────────────────────┘{Colors.ENDC}")

def load_playbooks_from_manifest(manifest_path):
    """Parses a YAML manifest to extract the list of playbooks."""
    if not os.path.exists(manifest_path):
        print_error(f"Manifest file '{manifest_path}' not found.")
        sys.exit(1)

    with open(manifest_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print_error(f"Error parsing YAML manifest: {e}")
            sys.exit(1)

    playbooks = []
    if isinstance(data, list):
        for item in data:
            if 'import_playbook' in item:
                # Resolve relative paths relative to the manifest location or script dir
                # In playbook.yaml, paths are 'playbooks/...' which is relative to root.
                pb_path = item['import_playbook']
                # Determine tags if any (not used for filtering here, but available)
                tags = item.get('tags', [])
                playbooks.append({'path': pb_path, 'tags': tags})

    return playbooks

def check_port_open(host, port, timeout=2):
    """Checks if a port is open on the given host, supporting both IPv4 and IPv6."""
    try:
        # getaddrinfo handles both IPv4 and IPv6 resolution and formatting
        # It returns a list of (family, type, proto, canonname, sockaddr) tuples
        addr_info = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        # Hostname could not be resolved
        return False

    for family, socktype, proto, canonname, sockaddr in addr_info:
        try:
            sock = socket.socket(family, socktype, proto)
            sock.settimeout(timeout)
            sock.connect(sockaddr)
            sock.close()
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            continue

    return False

def wait_for_ports_freed(ports, timeout=10):
    """Waits for specified ports to be free (not listening), and forcibly kills blocking processes if needed."""
    print(f"Waiting for ports {ports} to be free...")
    start_time = time.time()

    for port in ports:
        print(f"Checking port {port}...")
        if check_port_open("127.0.0.1", port):
            print(f"{Colors.WARNING}⚠️  Port {port} is in use. Attempting to kill blocking processes...{Colors.ENDC}")
            try:
                # Try to use lsof or fuser to kill the process on the port
                subprocess.run(f"fuser -k {port}/tcp", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                time.sleep(2) # Give it a moment to release the port
            except Exception as e:
                print_warning(f"Failed to kill processes on port {port}: {e}")

        while check_port_open("127.0.0.1", port):
            if time.time() - start_time > timeout:
                print_warning(f"Timeout waiting for port {port} to be free. Proceeding anyway.")
                break # Move to next port
            time.sleep(2)
        else:
            print(f"{Colors.OKGREEN}✅ Port {port} is free.{Colors.ENDC}")

def get_current_ram_usage():
    """Returns the current memory usage in MB by parsing /proc/meminfo."""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()

        mem_total_match = re.search(r'MemTotal:\s+(\d+)', meminfo)
        mem_available_match = re.search(r'MemAvailable:\s+(\d+)', meminfo)

        if mem_total_match and mem_available_match:
            total_kb = int(mem_total_match.group(1))
            available_kb = int(mem_available_match.group(1))
            used_kb = total_kb - available_kb
            return used_kb // 1024
    except Exception:
        pass
    return None

def cleanup_memory_for_core_ai():
    """Performs cleanup to free RAM before heavy AI services start."""
    print(f"{Colors.OKCYAN}🧹 Performing pre-Core AI Services cleanup to free RAM...{Colors.ENDC}")

    # Stop llamacpp-rpc jobs
    try:
        if shutil.which("nomad"):
            # Get job IDs containing 'llamacpp-rpc'
            cmd = "nomad job status | awk '/llamacpp-rpc/ {print $1}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            job_ids = result.stdout.strip().split('\n')

            for job_id in job_ids:
                if job_id:
                    print(f"Stopping job: {job_id}")
                    subprocess.run(["nomad", "job", "stop", "-purge", job_id],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print_warning(f"Failed to cleanup Nomad jobs: {e}")

    # Note: drop_caches requires sudo, which we might not have if running as user.
    # The original script commented out the 'sync; echo 3 > drop_caches' part,
    # so we will stick to just stopping jobs.

    subprocess.run(["free", "-h"])

def kill_if_running(pattern):
    """Kills processes matching a pattern."""
    try:
        # pgrep -f matches against full command line
        cmd = ["pgrep", "-f", pattern]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split()
            if pids:
                print(f"{Colors.WARNING}⚠️  Found orphaned process matching '{pattern}'. Terminating...{Colors.ENDC}")
                subprocess.run(["kill", "-9"] + pids, stderr=subprocess.DEVNULL)
    except Exception as e:
        print_warning(f"Failed to kill process matching '{pattern}': {e}")

def purge_nomad_jobs():
    """Stops and purges all Nomad jobs."""
    if not shutil.which("nomad"):
        print_warning("'nomad' command not found. Cannot purge jobs. Skipping.")
        return

    print(f"{Colors.WARNING}🔥 --purge-jobs flag detected. Stopping and purging all Nomad jobs...{Colors.ENDC}")
    try:
        # Get all job IDs
        cmd = "nomad job status | awk 'NR>1 {print $1}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        job_ids = result.stdout.strip().split('\n')

        found_jobs = False
        for job_id in job_ids:
            if job_id and job_id != "No": # awk might catch "No running jobs"
                found_jobs = True
                print(f"Stopping and purging job: {job_id}")
                subprocess.run(["nomad", "job", "stop", "-purge", job_id],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if found_jobs:
            print(f"{Colors.OKGREEN}✅ All Nomad jobs have been purged.{Colors.ENDC}")
        else:
            print("No running Nomad jobs found to purge.")

    except Exception as e:
        print_error(f"Error purging jobs: {e}")

    # Check for orphaned processes
    print("Checking for orphaned application processes...")

    # Check if Nomad is running (if we purged, we assume it might still be running the agent,
    # but we killed the jobs. If nomad is NOT running, we definitely want to kill orphans.)
    nomad_running = False
    try:
        if subprocess.run(["nomad", "node", "status"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            nomad_running = True
    except:
        pass

    # If we purged jobs, OR nomad is not running, force kill orphans.
    # If nomad IS running and we didn't purge (this function is only called if purge=True),
    # then this logic holds.

    kill_if_running("dllama-api")
    kill_if_running("/opt/pipecatapp/venv/bin/python3 /opt/pipecatapp/app.py")
    print("Process cleanup complete.")


def run_playbook(playbook_path, extra_vars, tags, verbose_level):
    """Runs a single ansible playbook."""
    cmd = ["ansible-playbook", "-i", INVENTORY_FILE, playbook_path]

    for key, value in extra_vars.items():
        cmd.extend(["--extra-vars", f"{key}={value}"])

    if tags:
        cmd.extend(["--tags", tags])

    # Add verbosity flags based on level
    if verbose_level >= 4:
        cmd.append("-vvvv")
    elif verbose_level == 3:
        cmd.append("-v")

    # Level 2 is normal ansible output (no flag needed typically, or maybe -v if one wants slightly more info?)
    # Default ansible output is decent.
    # Level 0, 1: Suppress output.

    print_task_header(f"Running task: {os.path.basename(playbook_path)}")

    if verbose_level >= 1:
        print(f"  Path: {playbook_path}")

    start_time = time.time()

    # Streaming logic
    # We want to ALWAYS capture to LOG_FILE.
    # If verbose_level >= 2, we ALSO print to stdout.

    # We open the log file in append mode.
    # Using subprocess.Popen to stream.

    # Ensure stdout flushes immediately
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["ANSIBLE_FORCE_COLOR"] = "1" # Keep colors if possible
    env["ANSIBLE_CONFIG"] = os.path.join(REPO_ROOT, "ansible.cfg")

    try:
        with open(LOG_FILE, "a") as log_file:
            # We add a header to the log file for this run
            log_file.write(f"\n--- Running Task: {playbook_path} ---\n")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Merge stderr into stdout
                text=True,
                env=env,
                bufsize=1, # Line buffered
                cwd=REPO_ROOT
            )

            captured_lines = []

            for line in process.stdout:
                # Write to log
                log_file.write(line)

                # If verbose, write to stdout
                if verbose_level >= 2:
                    sys.stdout.write(line)
                elif verbose_level < 2:
                    # Keep a small buffer in case of error?
                    # If error happens, we might want to dump the last N lines or point to the log.
                    # The user said "highlight when errors occur... running list of warnings and errors".
                    # We can store everything in memory if it's not too huge, or just rely on the file.
                    captured_lines.append(line)

            process.wait()
            return_code = process.returncode

    except Exception as e:
        print_error(f"Failed to execute playbook: {e}")
        sys.exit(1)

    duration = time.time() - start_time
    print(f"Task finished in {duration:.2f}s")

    if return_code != 0:
        print_error(f"Task '{playbook_path}' failed.")

        # If we suppressed output, dump the relevant parts now
        if verbose_level < 2:
            print(f"{Colors.WARNING}--- Task Output (Last 50 lines) ---{Colors.ENDC}")
            # Dump last 50 lines from capture
            for line in captured_lines[-50:]:
                sys.stdout.write(line)
            print(f"{Colors.WARNING}--- End Task Output ---{Colors.ENDC}")

            # --- Smart Error Parsing ---
            last_task = "Unknown Task"
            error_details = []
            capturing_error = False

            for line in captured_lines:
                # Capture the last TASK header we saw
                if line.startswith("TASK ["):
                    last_task = line.strip()
                    capturing_error = False
                    error_details = [] # Reset error details for new task
                # Capture fatal or error lines
                elif "fatal:" in line or "ERROR!" in line:
                    capturing_error = True
                    error_details.append(line.strip())
                elif capturing_error and line.strip():
                    # Capture subsequent lines of the error block (often indented)
                    if line.startswith(" ") or line.startswith("	"):
                        error_details.append(line.strip())
                    elif "MSG:" in line:
                         error_details.append(line.strip())
                    else:
                        capturing_error = False # Stop if it's a new top-level un-indented log (not part of the error block)

            print(f"\n{Colors.FAIL}{Colors.BOLD}=== Parsed Error Summary ==={Colors.ENDC}")
            print(f"{Colors.BOLD}Failed Task:{Colors.ENDC} {last_task}")
            print(f"{Colors.BOLD}Reason:{Colors.ENDC}")
            if error_details:
                for err_line in error_details:
                    print(f"  {err_line}")
            else:
                print("  Could not explicitly parse error details. Please check the logs above.")
            print(f"{Colors.FAIL}{Colors.BOLD}============================{Colors.ENDC}\n")

            print(f"Full log available in: {LOG_FILE}")

        sys.exit(return_code)

    print(f"{Colors.OKGREEN}✅ Task '{playbook_path}' completed successfully.{Colors.ENDC}")

def wait_for_async_tasks():
    """Waits for any background Ansible async tasks to complete."""
    async_dir = os.path.expanduser("~/.ansible_async")
    if not os.path.exists(async_dir):
        return

    print_header("Checking for background Async Tasks")

    while True:
        pending_job_ids = []
        files = glob.glob(os.path.join(async_dir, "*"))

        for fpath in files:
            try:
                with open(fpath, 'r') as f:
                    data = json.load(f)

                # If explicitly finished, ignore
                if data.get('finished') == 1:
                    continue

                # Check if PID is still alive
                pid = data.get('pid')
                if pid:
                    try:
                        os.kill(pid, 0)
                        # Process exists
                        pending_job_ids.append(os.path.basename(fpath))
                    except OSError:
                        # Process dead, likely crashed or finished without updating file?
                        pass
            except Exception:
                pass

        if not pending_job_ids:
            print(f"{Colors.OKGREEN}✅ All async tasks completed.{Colors.ENDC}")
            break

        print(f"⏳ Waiting for {len(pending_job_ids)} async task(s) to complete: {', '.join(pending_job_ids)}")
        time.sleep(2)

def print_summary():
    """Prints a summary of warnings and errors."""
    if not WARNINGS and not ERRORS:
        return

    print_header("Summary of Warnings and Errors")

    if WARNINGS:
        print(f"\n{Colors.WARNING}{Colors.BOLD}Warnings:{Colors.ENDC}")
        for w in WARNINGS:
            print(f"  • {w}")

    if ERRORS:
        print(f"\n{Colors.FAIL}{Colors.BOLD}Errors:{Colors.ENDC}")
        for e in ERRORS:
            print(f"  • {e}")
    print("\n")




def get_primary_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def print_final_status(args, executed_playbooks):
    print_header("Final Status Report")

    # 1. Node Role & Controller info
    print(f"{Colors.BOLD}Node Role:{Colors.ENDC} {args.role}")
    if args.role == "worker" and args.controller_ip:
        print(f"{Colors.BOLD}Controller IP:{Colors.ENDC} {args.controller_ip}")
    elif args.role == "controller" or args.role == "all":
        print(f"{Colors.BOLD}Controller IP:{Colors.ENDC} This node is the controller.")

    # 2. Access IPs
    ip = get_primary_ip()
    print(f"\n{Colors.BOLD}Access Interfaces:{Colors.ENDC}")
    print(f"  • {Colors.OKCYAN}Node IP Address:{Colors.ENDC} {ip}")

    interfaces = [
        ("Nomad UI", 4646, f"http://{ip}:4646"),
        ("Consul UI", 8500, f"http://{ip}:8500"),
        ("Pipecat App", 8000, f"http://{ip}:8000"),
        ("Home Assistant", 8123, f"http://{ip}:8123"),
    ]

    for name, port, url in interfaces:
        is_open = check_port_open(ip, port)
        status = f"{Colors.OKGREEN}(Active){Colors.ENDC}" if is_open else f"{Colors.FAIL}(Inactive){Colors.ENDC}"
        print(f"  • {Colors.OKCYAN}{name:<15}:{Colors.ENDC} {url:<25} {status}")

    # 3. Intended Services
    print(f"\n{Colors.BOLD}Executed Playbooks (Intended Configuration):{Colors.ENDC}")
    for pb in executed_playbooks:
        print(f"  • {os.path.basename(pb)}")

    # 4. Running System Services
    print(f"\n{Colors.BOLD}System Services Status:{Colors.ENDC}")

    potential_services = [
        "nomad", "consul", "docker", "headscale",
        "provisioning-api", "power-agent", "paddler-balancer",
        "paddler-agent", "librarian", "spacedrive",
        "unified_fs", "tpm-ssh-agent"
    ]
    core_services = ["nomad", "consul", "docker"]

    for svc in potential_services:
        try:
            # First check if the service exists
            check_exists = subprocess.run(["systemctl", "list-unit-files", f"{svc}.service"], capture_output=True, text=True)
            if check_exists.returncode != 0 or "0 unit files listed" in check_exists.stdout:
                if svc in core_services:
                    print(f"  • {svc.capitalize()}: {Colors.WARNING}Not Installed{Colors.ENDC}")
                continue

            result = subprocess.run(["systemctl", "is-active", svc], capture_output=True, text=True)
            status = result.stdout.strip()
            if status == "active":
                print(f"  • {svc.capitalize()}: {Colors.OKGREEN}Active{Colors.ENDC}")
            else:
                print(f"  • {svc.capitalize()}: {Colors.FAIL}{status}{Colors.ENDC}")
        except FileNotFoundError:
            if svc in core_services:
                print(f"  • {svc.capitalize()}: {Colors.WARNING}systemctl not found{Colors.ENDC}")

    # 5. Running Nomad Jobs
    try:
        # Check if nomad is reachable
        env = os.environ.copy()
        env["NOMAD_ADDR"] = f"http://{ip}:4646"
        result = subprocess.run(["nomad", "job", "status", "-short"], capture_output=True, text=True, env=env)
        if result.returncode == 0 and result.stdout.strip():
            print(f"\n{Colors.BOLD}Running Nomad Jobs:{Colors.ENDC}")
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    print(f"  • {line.strip()}")
        elif result.returncode == 0:
            print(f"\n{Colors.BOLD}Running Nomad Jobs:{Colors.ENDC} None")
        else:
            print(f"\n{Colors.BOLD}Running Nomad Jobs:{Colors.ENDC} {Colors.FAIL}Unable to query Nomad (is it running?){Colors.ENDC}")
    except FileNotFoundError:
        pass # nomad not installed or in path

    print("\n")

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(description="Hybrid Architecture Provisioning Script")
    parser.add_argument("--role", default="all", choices=["all", "controller", "worker"], help="Role of this node")
    parser.add_argument("--controller-ip", help="IP of the controller (required for workers)")
    parser.add_argument("--tags", help="Ansible tags to run")
    parser.add_argument("--user", default="pipecatapp", dest="target_user", help="Target user for Ansible")
    parser.add_argument("--github-ssh-user", action="append", default=[], help="GitHub username to import SSH keys for. Can be used multiple times.")
    parser.add_argument("--debug", action="store_true", help="Enable verbose logging (Legacy flag)")
    parser.add_argument("--verbose", type=int, default=0, help="Verbosity level (0-4)")
    parser.add_argument("--continue", action="store_true", dest="continue_run", help="Resume from last state")

    # Pass-through flags that are handled as extra-vars
    parser.add_argument("--benchmark", action="store_true", help="Run benchmarks")
    parser.add_argument("--external-model-server", action="store_true", help="Skip model downloads")
    parser.add_argument("--leave-services-running", action="store_true", help="Don't cleanup Nomad/Consul")
    parser.add_argument("--purge-jobs", action="store_true", help="Purge Nomad jobs (handled by wrapper mostly, but var passed)")
    parser.add_argument("--only-purge", action="store_true", help="Only purge jobs and exit (requires --purge-jobs)")
    parser.add_argument("--deploy-docker", action="store_true", help="Deploy via Docker")
    parser.add_argument("--run-local", action="store_true", help="Deploy via raw_exec")
    parser.add_argument("--home-assistant-debug", action="store_true", help="Debug Home Assistant")
    parser.add_argument("--watch", help="Pause for inspection after target")
    parser.add_argument("--deploy-full-stack", action="store_true", help="Deploy the full application stack instead of just infrastructure")
    parser.add_argument("--deploy-partial-stack", action="store_true", help="Deploy a partial application stack (e.g. 4-8B models) for mid-tier worker nodes")
    parser.add_argument("--deploy-minimal-stack", action="store_true", help="Deploy a minimal application stack (e.g. kiosk, audio) for low resource nodes")
    parser.add_argument("--tier", default="mid", choices=["edge", "mid", "core"], help="Specify the node tier")

    args, _ = parser.parse_known_args()

    # Consolidate debug flag into verbose level
    if args.debug and args.verbose == 0:
        args.verbose = 4

    verbose_level = args.verbose

    print_header("Provisioning Started")
    if verbose_level > 0:
        print(f"Verbosity Level: {verbose_level}")

    # --- Validation ---
    if args.role == "worker" and not args.controller_ip:
        print_error("--controller-ip is required when using --role=worker")
        sys.exit(1)

    # --- Pre-Provisioning Actions ---
    if args.purge_jobs:
        purge_nomad_jobs()
        if args.only_purge:
            print(f"{Colors.OKGREEN}✅ Purge complete. Exiting as requested.{Colors.ENDC}")
            sys.exit(0)

    # --- Build Extra Vars ---
    extra_vars = {
        "target_user": args.target_user
    }

    if args.github_ssh_user:
        extra_vars["github_ssh_users"] = json.dumps(args.github_ssh_user)

    if args.role == "worker":
        extra_vars["controller_ip"] = args.controller_ip

    if args.deploy_full_stack:
        extra_vars["deploy_full_stack"] = "true"

    if args.deploy_partial_stack:
        extra_vars["deploy_partial_stack"] = "true"

    if args.deploy_minimal_stack:
        extra_vars["deploy_minimal_stack"] = "true"

    if args.benchmark:
        extra_vars["run_benchmarks"] = "true"
    if args.external_model_server:
        extra_vars["external_model_server"] = "true"
    if args.purge_jobs:
        extra_vars["purge_jobs"] = "true"
    if args.leave_services_running:
        extra_vars["cleanup_services"] = "false"
        print(f"{Colors.OKGREEN}✅ --leave-services-running detected. Nomad and Consul data will not be cleaned up.{Colors.ENDC}")
    else:
        extra_vars["cleanup_services"] = "true"
        print(f"{Colors.OKCYAN}🧹 Nomad and Consul data will be cleaned up by default.{Colors.ENDC}")

    if args.deploy_docker:
        extra_vars["pipecat_deployment_style"] = "docker"
    if args.tier:
        extra_vars["node_tier"] = args.tier
    if args.run_local:
        extra_vars["pipecat_deployment_style"] = "raw_exec"
    if args.home_assistant_debug:
        extra_vars["home_assistant_debug_mode"] = "true"
    if args.watch:
        extra_vars["watch_target"] = args.watch

    # --- Determine Manifest ---
    if args.role == "all":
        manifest_file = "playbook.yaml"
    elif args.role == "controller":
        manifest_file = "playbooks/controller.yaml"
    elif args.role == "worker":
        manifest_file = "playbooks/worker.yaml"

    manifest_path = os.path.join(REPO_ROOT, manifest_file)
    print(f"Loading tasks from: {manifest_file}")

    playbooks = load_playbooks_from_manifest(manifest_path)

    # --- State Management ---
    start_index = 0
    if args.continue_run:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                start_index = int(f.read().strip()) + 1
            print(f"{Colors.BOLD}{Colors.OKCYAN}🔄 Resuming from task {start_index} ({os.path.basename(playbooks[min(start_index, len(playbooks)-1)]['path'])}){Colors.ENDC}")
        else:
            print(f"{Colors.OKBLUE}ℹ️  --continue flag set but no state file found. Starting from 0.{Colors.ENDC}")
    else:
        if os.path.exists(STATE_FILE):
            try:
                os.remove(STATE_FILE)
            except OSError:
                pass

    # --- Execution Loop ---
    executed_playbooks = []
    for i, pb in enumerate(playbooks):
        # In worker.yaml, playbooks use {{ playbook_dir }}
        normalized_path = pb['path'].replace("{{ playbook_dir }}", "playbooks")

        if i < start_index:
            # Shorten path for display
            display_path = os.path.basename(normalized_path)
            print(f"{Colors.OKBLUE}⏭️  Skipping completed: {display_path}{Colors.ENDC}")
            continue

        pb_path = os.path.join(REPO_ROOT, normalized_path)

        # --- Hooks / Smart Logic ---

        # Check deployment mode (infrastructure vs application stack)
        app_services_playbooks = [
            "playbooks/services/app_services.yaml",
            "playbooks/services/monitoring.yaml",
            "playbooks/services/model_services.yaml",
            "playbooks/services/core_ai_services.yaml",
            "playbooks/services/ai_experts.yaml",
            "playbooks/services/training_services.yaml",
            "playbooks/services/distributed_compute.yaml",
            "playbooks/services/streaming_services.yaml",
            "playbooks/services/final_verification.yaml",
        ]

        # Define what constitutes a "partial" stack
        partial_stack_playbooks = [
            "playbooks/services/app_services.yaml",
            "playbooks/services/monitoring.yaml",
            "playbooks/services/model_services.yaml",
            "playbooks/services/core_ai_services.yaml",
        ]

        # Define what constitutes a "minimal" stack
        minimal_stack_playbooks = [
            "playbooks/services/app_services.yaml", # Needed for basic app connectivity, audio, kiosk
            "playbooks/services/monitoring.yaml",   # Needed for health checks and status
        ]

        if normalized_path in app_services_playbooks:
            if args.deploy_full_stack:
                print(f"{Colors.OKCYAN}ℹ️  Including playbook '{os.path.basename(normalized_path)}' because full stack mode is enabled.{Colors.ENDC}")
            elif args.deploy_partial_stack and normalized_path in partial_stack_playbooks:
                print(f"{Colors.OKCYAN}ℹ️  Including playbook '{os.path.basename(normalized_path)}' because partial stack mode is enabled.{Colors.ENDC}")
            elif args.deploy_minimal_stack and normalized_path in minimal_stack_playbooks:
                print(f"{Colors.OKCYAN}ℹ️  Including playbook '{os.path.basename(normalized_path)}' because minimal stack mode is enabled.{Colors.ENDC}")
            else:
                # Skip
                display_path = os.path.basename(normalized_path)
                if args.deploy_partial_stack:
                    mode_reason = "not part of partial stack"
                elif args.deploy_minimal_stack:
                    mode_reason = "not part of minimal stack"
                else:
                    mode_reason = "infrastructure only mode"
                print(f"{Colors.OKCYAN}⏭️  Skipping application playbook ({mode_reason}): {display_path}{Colors.ENDC}")
                continue
        else:
            print(f"{Colors.OKCYAN}ℹ️  Including playbook '{os.path.basename(normalized_path)}' as a core infrastructure dependency.{Colors.ENDC}")

        # Wait for ports before app services
        if "app_services.yaml" in normalized_path:
            wait_for_ports_freed([8000, 8081, 1883])

        # Cleanup before Core AI
        if "core_ai_services.yaml" in normalized_path:
            cleanup_memory_for_core_ai()

        # --- RAM Profiling Before ---
        ram_before = get_current_ram_usage()

        # --- Run ---
        run_playbook(pb_path, extra_vars, args.tags, verbose_level)
        executed_playbooks.append(pb_path)

        # --- RAM Profiling After ---
        ram_after = get_current_ram_usage()
        if ram_before is not None and ram_after is not None:
            ram_delta = ram_after - ram_before
            delta_str = f"+{ram_delta} MB" if ram_delta >= 0 else f"{ram_delta} MB"
            print(f"{Colors.OKCYAN}📊 RAM Usage: {ram_after} MB ({delta_str} after running {os.path.basename(pb_path)}){Colors.ENDC}")

        # Save State
        with open(STATE_FILE, 'w') as f:
            f.write(str(i))

    # Wait for any background/async tasks (like home-assistant)
    wait_for_async_tasks()

    print_header("Provisioning Complete")
    print(f"{Colors.OKGREEN}✅ All tasks completed successfully.{Colors.ENDC}")

    print_summary()
    print_final_status(args, executed_playbooks)

if __name__ == "__main__":
    main()
