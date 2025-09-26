import json
import os
import subprocess
import time

def run_playbook(playbook_path, extra_vars=None):
    """A helper function to run an Ansible playbook."""
    command = ["ansible-playbook", playbook_path]
    if extra_vars:
        command.extend(["-e", json.dumps(extra_vars)])

    print(f"--- Running playbook: {' '.join(command)} ---")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running playbook {playbook_path}:")
        print(result.stdout)
        print(result.stderr)
        return False

    print(result.stdout)
    return True

def run_script(script_path, args=None):
    """A helper function to run a Python script."""
    command = ["python", script_path]
    if args:
        command.extend(args)

    print(f"--- Running script: {' '.join(command)} ---")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running script {script_path}:")
        print(result.stdout)
        print(result.stderr)
        return None

    return result.stdout

def cleanup_files(files):
    """A helper function to remove temporary files."""
    for f in files:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed temporary file: {f}")

def main():
    """The main supervisor loop."""
    failed_jobs_file = "failed_jobs.json"

    while True:
        print("\n--- Starting new health check cycle ---")

        # 1. Check for failed jobs
        if not run_playbook("health_check.yaml"):
            print("Halting cycle due to error in health_check.yaml.")
            time.sleep(60)
            continue

        if not os.path.exists(failed_jobs_file):
            print("No failed jobs found. All systems nominal.")
            time.sleep(60)
            continue

        # 2. Process failed jobs
        try:
            with open(failed_jobs_file, 'r') as f:
                data = json.load(f)
                failed_jobs = data.get("unhealthy_jobs", [])
        except (IOError, json.JSONDecodeError):
            print("Could not read or parse failed_jobs.json.")
            cleanup_files([failed_jobs_file])
            time.sleep(60)
            continue

        for job in failed_jobs:
            job_id = job.get("ID")
            if not job_id:
                continue

            print(f"\n--- Processing failed job: {job_id} ---")
            diagnostics_file = f"{job_id}.diagnostics.json"

            # 3. Diagnose the failure
            if not run_playbook("diagnose_failure.yaml", extra_vars={"job_id": job_id}):
                print(f"Could not diagnose job {job_id}. Skipping.")
                continue

            # 4. Reflect on the failure to get a solution
            solution_json = run_script("reflection/reflect.py", [diagnostics_file])
            if not solution_json:
                print(f"Could not get a healing solution for {job_id}. Skipping.")
                cleanup_files([diagnostics_file])
                continue

            # 5. Attempt to heal the job
            if not run_playbook("heal_job.yaml", extra_vars={"solution_json": solution_json}):
                print(f"Healing attempt failed for {job_id}.")
            else:
                print(f"Healing attempt completed for {job_id}.")

            # 6. Cleanup diagnostic file
            cleanup_files([diagnostics_file])

        # 7. Cleanup failed jobs file
        cleanup_files([failed_jobs_file])

        print("\n--- Health check cycle complete. Waiting for next cycle. ---")
        time.sleep(60)

if __name__ == "__main__":
    main()