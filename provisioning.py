#!/usr/bin/env python3
"""
Provisioning Script for Hybrid Architecture.
Replaces the logic of bootstrap.sh with a more robust, extensible Python script.

Usage:
    python3 provisioning.py [--role ROLE] [--tags TAGS] [--continue] ...
"""

import argparse
import os
import sys
import subprocess
import time
import socket
import yaml
import shutil

# --- Constants ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, ".provisioning_state")
LOG_FILE = os.path.join(SCRIPT_DIR, "playbook_output.log")
INVENTORY_FILE = os.path.join(SCRIPT_DIR, "local_inventory.ini")

# --- Helper Functions ---

def load_playbooks_from_manifest(manifest_path):
    """Parses a YAML manifest to extract the list of playbooks."""
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest file '{manifest_path}' not found.")
        sys.exit(1)

    with open(manifest_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML manifest: {e}")
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
    """Checks if a port is open on the given host."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    except OSError:
        return False

def wait_for_ports_freed(ports, timeout=60):
    """Waits for specified ports to be free (not listening)."""
    print(f"Waiting for ports {ports} to be free...")
    start_time = time.time()

    for port in ports:
        print(f"Checking port {port}...")
        while check_port_open("127.0.0.1", port):
            if time.time() - start_time > timeout:
                print(f"⚠️  Timeout waiting for port {port} to be free. Proceeding anyway.")
                return
            time.sleep(2)
        print(f"✅ Port {port} is free.")

def cleanup_memory_for_core_ai():
    """Performs cleanup to free RAM before heavy AI services start."""
    print("🧹 Performing pre-Core AI Services cleanup to free RAM...")

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
        print(f"Warning: Failed to cleanup Nomad jobs: {e}")

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
                print(f"⚠️  Found orphaned process matching '{pattern}'. Terminating...")
                subprocess.run(["kill", "-9"] + pids, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Warning: Failed to kill process matching '{pattern}': {e}")

def purge_nomad_jobs():
    """Stops and purges all Nomad jobs."""
    if not shutil.which("nomad"):
        print("⚠️  Warning: 'nomad' command not found. Cannot purge jobs. Skipping.")
        return

    print("🔥 --purge-jobs flag detected. Stopping and purging all Nomad jobs...")
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
            print("✅ All Nomad jobs have been purged.")
        else:
            print("No running Nomad jobs found to purge.")

    except Exception as e:
        print(f"Error purging jobs: {e}")

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


def run_playbook(playbook_path, extra_vars, tags, debug_mode):
    """Runs a single ansible playbook."""
    cmd = ["ansible-playbook", "-i", INVENTORY_FILE, playbook_path]

    for key, value in extra_vars.items():
        cmd.extend(["--extra-vars", f"{key}={value}"])

    if tags:
        cmd.extend(["--tags", tags])

    if debug_mode:
        cmd.append("-vvvv")

    print(f"--------------------------------------------------")
    print(f"🚀 Running playbook: {playbook_path}")
    print(f"--------------------------------------------------")

    start_time = time.time()

    # In debug mode, we might want to capture output to file, but simpler to just let it stream
    # and rely on the wrapper script to redirect if needed, or use subprocess.PIPE.
    # The original script used `>> $LOG_FILE 2>&1`.

    if debug_mode:
        with open(LOG_FILE, "a") as log:
            result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
    else:
        result = subprocess.run(cmd)

    duration = time.time() - start_time
    print(f"Playbook finished in {duration:.2f}s")

    if result.returncode != 0:
        print(f"❌ Playbook '{playbook_path}' failed.")
        sys.exit(result.returncode)

    print(f"✅ Playbook '{playbook_path}' completed successfully.")

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(description="Hybrid Architecture Provisioning Script")
    parser.add_argument("--role", default="all", choices=["all", "controller", "worker"], help="Role of this node")
    parser.add_argument("--controller-ip", help="IP of the controller (required for workers)")
    parser.add_argument("--tags", help="Ansible tags to run")
    parser.add_argument("--user", default="pipecatapp", dest="target_user", help="Target user for Ansible")
    parser.add_argument("--debug", action="store_true", help="Enable verbose logging")
    parser.add_argument("--continue", action="store_true", dest="continue_run", help="Resume from last state")

    # Pass-through flags that are handled as extra-vars
    parser.add_argument("--benchmark", action="store_true", help="Run benchmarks")
    parser.add_argument("--external-model-server", action="store_true", help="Skip model downloads")
    parser.add_argument("--leave-services-running", action="store_true", help="Don't cleanup Nomad/Consul")
    parser.add_argument("--purge-jobs", action="store_true", help="Purge Nomad jobs (handled by wrapper mostly, but var passed)")
    parser.add_argument("--deploy-docker", action="store_true", help="Deploy via Docker")
    parser.add_argument("--run-local", action="store_true", help="Deploy via raw_exec")
    parser.add_argument("--home-assistant-debug", action="store_true", help="Debug Home Assistant")
    parser.add_argument("--watch", help="Pause for inspection after target")

    args = parser.parse_args()

    # --- Validation ---
    if args.role == "worker" and not args.controller_ip:
        print("Error: --controller-ip is required when using --role=worker")
        sys.exit(1)

    # --- Pre-Provisioning Actions ---
    if args.purge_jobs:
        purge_nomad_jobs()

    # --- Build Extra Vars ---
    extra_vars = {
        "target_user": args.target_user
    }

    if args.role == "worker":
        extra_vars["controller_ip"] = args.controller_ip

    if args.benchmark:
        extra_vars["run_benchmarks"] = "true"
    if args.external_model_server:
        extra_vars["external_model_server"] = "true"
    if args.purge_jobs:
        extra_vars["purge_jobs"] = "true"
    if args.leave_services_running:
        extra_vars["cleanup_services"] = "false"
        print("✅ --leave-services-running detected. Nomad and Consul data will not be cleaned up.")
    else:
        extra_vars["cleanup_services"] = "true"
        print("🧹 Nomad and Consul data will be cleaned up by default.")

    if args.deploy_docker:
        extra_vars["pipecat_deployment_style"] = "docker"
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

    manifest_path = os.path.join(SCRIPT_DIR, manifest_file)
    print(f"Loading playbooks from: {manifest_file}")

    playbooks = load_playbooks_from_manifest(manifest_path)

    # --- State Management ---
    start_index = 0
    if args.continue_run:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                start_index = int(f.read().strip()) + 1
            print(f"🔄 Resuming from index {start_index}")
        else:
            print("ℹ️  --continue flag set but no state file found. Starting from 0.")
    else:
        if os.path.exists(STATE_FILE):
            try:
                os.remove(STATE_FILE)
            except OSError:
                pass

    # --- Execution Loop ---
    for i, pb in enumerate(playbooks):
        if i < start_index:
            print(f"⏭️  Skipping completed: {pb['path']}")
            continue

        pb_path = os.path.join(SCRIPT_DIR, pb['path'])

        # --- Hooks / Smart Logic ---

        # Wait for ports before app services
        if "app_services.yaml" in pb['path']:
             wait_for_ports_freed([8000, 8081, 1883])

        # Cleanup before Core AI
        if "core_ai_services.yaml" in pb['path']:
            cleanup_memory_for_core_ai()

        # --- Run ---
        run_playbook(pb_path, extra_vars, args.tags, args.debug)

        # Save State
        with open(STATE_FILE, 'w') as f:
            f.write(str(i))

    print("--------------------------------------------------")
    print("✅ All playbooks completed successfully.")
    print("Provisioning complete.")

if __name__ == "__main__":
    main()
