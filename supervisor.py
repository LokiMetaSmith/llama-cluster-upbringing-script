import json
import os
import subprocess
import time
import requests

def run_playbook(playbook_path, extra_vars=None):
    """Executes an Ansible playbook as a subprocess.

    This function provides a standardized way to call `ansible-playbook`
    from within the supervisor script, handling command construction and
    error reporting.

    Args:
        playbook_path (str): The file path to the Ansible playbook.
        extra_vars (dict, optional): A dictionary of extra variables to pass
            to the playbook. Defaults to None.

    Returns:
        bool: True if the playbook ran successfully, False otherwise.
    """
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
    """Executes a Python script as a subprocess.

    This function is used to run other Python scripts, such as the reflection
    and adaptation managers, and captures their standard output.

    Args:
        script_path (str): The file path to the Python script.
        args (list, optional): A list of command-line arguments to pass to
            the script. Defaults to None.

    Returns:
        str: The standard output of the script, or None if an error occurred.
    """
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
    """Removes a list of temporary files.

    This is a utility function to ensure that transient files generated during
    the supervision loop (like diagnostic reports) are cleaned up.

    Args:
        files (list): A list of file paths to remove.
    """
    for f in files:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed temporary file: {f}")

def main():
    """The main entry point for the supervisor's self-healing loop.

    This function orchestrates the entire process of monitoring, diagnosing,
    and healing failed services. It runs in an infinite loop, periodically
    checking system health and taking corrective action as needed.
    """
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

            # 5. Parse the solution and decide on the next step
            try:
                solution = json.loads(solution_json)
                action = solution.get("action")
            except (json.JSONDecodeError, AttributeError):
                print(f"Could not parse solution for job {job_id}. Skipping.")
                cleanup_files([diagnostics_file])
                continue

            if action == "error":
                # 5a. If reflection fails, trigger self-adaptation AND notify the agent
                print(f"--- Reflection could not find a direct solution. Triggering self-adaptation for job {job_id}. ---")
                run_script("reflection/adaptation_manager.py", [diagnostics_file])

                # Notify TwinService
                try:
                    alert_msg = f"Job {job_id} failed and automated reflection could not find a solution. Please investigate."
                    requests.post("http://localhost:8000/internal/system_message",
                                  json={"text": alert_msg, "priority": "high", "job_id": job_id},
                                  timeout=5)
                    print(f"Notified TwinService about {job_id}")
                except Exception as e:
                    print(f"Failed to notify TwinService: {e}")

            else:
                # 5b. Otherwise, attempt to heal the job directly
                if not run_playbook("heal_job.yaml", extra_vars={"solution_json": json.dumps(solution)}):
                    print(f"Healing attempt failed for {job_id}.")
                    # Notify TwinService on healing failure
                    try:
                         alert_msg = f"Automated healing failed for {job_id} (Action: {action}). Please intervene."
                         requests.post("http://localhost:8000/internal/system_message",
                                       json={"text": alert_msg, "priority": "high", "job_id": job_id},
                                       timeout=5)
                    except Exception:
                        pass
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