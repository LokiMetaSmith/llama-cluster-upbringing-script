import argparse
import json
import os
import subprocess
import sys
import yaml

def generate_test_case(diagnostics_data):
    """Generates a YAML test case from diagnostic data.

    This function creates a structured test case that captures the essence of
    a job failure, making it reproducible for the prompt evolution process.

    Args:
        diagnostics_data (dict): The parsed JSON data from the diagnostics file.

    Returns:
        str: The file path to the newly created YAML test case file.
    """
    job_id = diagnostics_data.get("job_id", "unknown_job")
    test_case = {
        "test_name": f"test_failure_reproduction_{job_id}",
        "steps": [
            {
                "action": "deploy_job",
                "job_id": job_id,
                "expected_outcome": "job_should_be_healthy"
            }
        ]
    }

    test_case_path = f"/tmp/{job_id}.test_case.yaml"
    with open(test_case_path, 'w') as f:
        yaml.dump(test_case, f)

    print(f"Generated test case for job {job_id} at {test_case_path}")
    return test_case_path

def run_evolution(test_case_path):
    """Triggers the prompt evolution process with a specific test case.

    This function calls the `evolve.py` script as a subprocess, ensuring that
    the self-adaptation loop is focused on resolving the specific failure
    captured in the provided test case.

    Args:
        test_case_path (str): The path to the YAML test case file.
    """
    evolve_script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "prompt_engineering", "evolve.py")
    )

    if not os.path.exists(evolve_script_path):
        print(f"Error: Could not find evolution script at {evolve_script_path}", file=sys.stderr)
        return

    command = ["python", evolve_script_path, "--test-case", test_case_path]
    print(f"--- Triggering prompt evolution: {' '.join(command)} ---")

    # Using Popen for fire-and-forget, as evolution is a long-running process
    subprocess.Popen(command)

def main():
    """The main entry point for the adaptation manager.

    This script orchestrates the self-adaptation process by taking a failed
    job's diagnostic data, converting it into a reproducible test case, and
    then launching the prompt evolution workflow to find a solution.
    """
    parser = argparse.ArgumentParser(
        description="""
        Orchestrates the self-adaptation loop by generating a test case from
        a failed job's diagnostics and triggering the prompt evolution process.
        """
    )
    parser.add_argument(
        "diagnostics_file",
        type=str,
        help="Path to the JSON diagnostics file for the failed job."
    )
    args = parser.parse_args()

    try:
        with open(args.diagnostics_file, 'r') as f:
            diagnostics_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing diagnostics file {args.diagnostics_file}: {e}", file=sys.stderr)
        sys.exit(1)

    test_case_path = generate_test_case(diagnostics_data)
    run_evolution(test_case_path)

    print("--- Adaptation process initiated. ---")

if __name__ == "__main__":
    main()
