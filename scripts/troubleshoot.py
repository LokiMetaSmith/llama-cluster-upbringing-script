#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
import getpass
import json
import urllib.request
import urllib.error
import tempfile
import shutil

def get_consul_token():
    """Retrieve Consul management token."""
    # Check environment first
    if "CONSUL_HTTP_TOKEN" in os.environ:
        return os.environ["CONSUL_HTTP_TOKEN"]

    token_file = "/etc/consul.d/management_token"

    # 1. Try reading directly (fast, silent)
    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                return f.read().strip()
        except PermissionError:
            pass  # Fall through to sudo
        except Exception:
            pass

    # 2. Try sudo -n cat (silent check)
    try:
        result = subprocess.run(
            ["sudo", "-n", "cat", token_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    return None

def run_command(command, shell=False, env=None):
    """Run a shell command and return its output."""
    try:
        # If command is a list, shell should be False (usually)
        # If command is a string, shell should be True
        if isinstance(command, list):
            cmd_str = " ".join(command)
        else:
            cmd_str = command
            shell = True

        print(f"Running: {cmd_str}...")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=shell,
            universal_newlines=True,
            timeout=30,
            env=env
        )
        return f"$ {cmd_str}\n{result.stdout}\n"
    except Exception as e:
        return f"Error running command '{command}': {e}\n"

def get_nomad_allocations():
    """Fetch allocations from Nomad API."""
    url = "http://localhost:4646/v1/allocations"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching allocations: {e}")
        return []

def section(title):
    return f"\n{'='*80}\n {title}\n{'='*80}\n"

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_file = f"troubleshoot_report_{timestamp}.txt"

    print(f"Generating troubleshooting report: {report_file}")

    with open(report_file, 'w') as f:
        # Header
        f.write(section("TROUBLESHOOTING REPORT"))
        f.write(f"Date: {datetime.datetime.now()}\n")
        f.write(f"Hostname: {os.uname().nodename}\n")
        try:
            user = getpass.getuser()
        except Exception:
            user = os.environ.get('USER', 'unknown')
        f.write(f"User: {user}\n")

        # System Info
        f.write(section("SYSTEM RESOURCES"))
        f.write(run_command("uptime"))
        f.write(run_command("free -h"))
        f.write(run_command("df -h"))

        # Docker
        f.write(section("DOCKER STATUS"))
        f.write(run_command("docker ps -a"))

        # Consul
        f.write(section("CONSUL STATUS"))

        # Setup Consul Token environment
        env = os.environ.copy()
        consul_token = get_consul_token()
        if consul_token:
            env["CONSUL_HTTP_TOKEN"] = consul_token
            print("Using Consul token for queries.")
        else:
            print("Warning: Could not retrieve Consul token. Service queries might be empty.")

        f.write(run_command("consul members", env=env))
        f.write(run_command("consul catalog services", env=env))

        f.write("\n--- Stale Services Analysis ---\n")
        # Run prune_consul_services.py in dry-run mode
        script_dir = os.path.dirname(os.path.abspath(__file__))
        prune_script = os.path.join(script_dir, "prune_consul_services.py")
        if os.path.exists(prune_script):
            f.write(run_command([sys.executable, prune_script, "--dry-run"], env=env))
        else:
            f.write(f"Script not found: {prune_script}\n")

        # Nomad
        f.write(section("NOMAD STATUS"))
        f.write(run_command("nomad server members"))
        f.write(run_command("nomad node status"))
        f.write(run_command("nomad job status"))

        # Nomad Analysis
        f.write(section("NOMAD JOB ANALYSIS"))
        analyze_script = os.path.join(script_dir, "analyze_nomad_allocs.py")

        allocs = get_nomad_allocations()
        if allocs:
            # Save to temp file for the analyzer script
            fd, temp_path = tempfile.mkstemp(suffix=".json")
            try:
                with os.fdopen(fd, 'w') as tmp:
                    json.dump(allocs, tmp)

                # Run the analyzer
                if os.path.exists(analyze_script):
                    f.write(run_command([sys.executable, analyze_script, temp_path]))
                else:
                    f.write(f"Script not found: {analyze_script}\n")

                # Enhanced Log Capture for Failed Allocs
                f.write(section("RECENT FAILED ALLOCATION LOGS"))

                # Filter for failed allocs
                failed_allocs = [a for a in allocs if a.get('ClientStatus') == 'failed']
                # Sort by ModifyTime desc
                failed_allocs.sort(key=lambda x: x.get('ModifyTime', 0), reverse=True)

                # Take top 5
                top_failures = failed_allocs[:5]

                if not top_failures:
                    f.write("No failed allocations found.\n")

                for alloc in top_failures:
                    alloc_id = alloc.get('ID')
                    short_id = alloc_id[:8]
                    job_id = alloc.get('JobID')

                    f.write(f"\n--- Logs for Allocation {short_id} (Job: {job_id}) ---\n")

                    # Find failed tasks
                    task_states = alloc.get('TaskStates', {})
                    for task_name, state in task_states.items():
                        if state.get('Failed') or state.get('State') == 'dead':
                            f.write(f"Task: {task_name} (State: {state.get('State')})\n")
                            # Fetch stderr
                            f.write(f"Fetching stderr for task '{task_name}'...\n")
                            f.write(run_command(["nomad", "alloc", "logs", "-stderr", "-tail", "-n", "100", alloc_id, task_name]))
            finally:
                os.remove(temp_path)
        else:
            f.write("Could not retrieve allocations for analysis.\n")

    print(f"Report generation complete. Output saved to: {report_file}")

if __name__ == "__main__":
    main()
