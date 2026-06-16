#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Run benchmark and optionally apply updates")
    parser.add_argument("--apply", action="store_true", help="Apply the parameters by reloading jobs")
    args = parser.parse_args()

    print("Running benchmark script...")
    res = subprocess.run([sys.executable, "scripts/benchmark_resources.py"], capture_output=True, text=True)
    if res.returncode != 0:
        print("Error running benchmark:")
        print(res.stderr)
        sys.exit(1)

    print(res.stdout)

    if args.apply:
        print("Applying the new configuration...")
        ansible_cmd = [
            "ansible-playbook",
            "-i", "inventory.yaml",
            "playbooks/redeploy_pipecat.yaml"
        ]
        try:
            print(f"Running: {' '.join(ansible_cmd)}")
            subprocess.run(ansible_cmd, check=True)
            print("Successfully applied configuration and restarted jobs.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to apply configuration. Ansible exited with code {e.returncode}")
            sys.exit(e.returncode)
        except FileNotFoundError:
            print("Error: 'ansible-playbook' command not found. Is Ansible installed in this environment?")
            sys.exit(1)

if __name__ == "__main__":
    main()
