import argparse
import json
import os
import subprocess
import sys
import yaml
from datetime import datetime

def generate_test_case(diagnostic_data):
    """Creates a structured YAML test case from diagnostic information.

    This function transforms the raw JSON output from a diagnostic run into a
    formal YAML test case that can be consumed by the evaluation and evolution
    scripts. The generated test case is designed to reproduce the failure
    scenario.

    Args:
        diagnostic_data (dict): The parsed JSON data from the diagnostic file.

    Returns:
        str: A string containing the formatted YAML test case.
    """
    job_id = diagnostic_data.get("job_id", "unknown_job")
    error_logs = diagnostic_data.get("logs", {}).get("stderr", "No stderr logs.")

    test_case = {
        "test_name": f"test_failure_reproduction_{job_id}",
        "description": (
            f"This test case is generated automatically from a runtime failure "
            f"of job '{job_id}'. The goal is to evolve the reflection agent "
            f"to produce a valid healing action instead of an error."
        ),
        "steps": [
            {
                "type": "run_script",
                "name": "reflection/reflect.py",
                "parameters": {
                    # The parameter is the diagnostic data itself, representing the input
                    "diagnostic_data": diagnostic_data
                },
                "expected_outcome": {
                    "action_not_equals": "error"
                },
                "failure_evidence": {
                    "stderr": error_logs
                }
            }
        ]
    }
    return yaml.dump([test_case], default_flow_style=False)

def main():
    """Main entry point for the adaptation manager script.

    Orchestrates the process of reading diagnostics, generating a test case,
    and invoking the prompt evolution script.
    """
    parser = argparse.ArgumentParser(
        description="Generate a test case from a failed job's diagnostics and run prompt evolution."
    )
    parser.add_argument(
        "diagnostic_file",
        type=str,
        help="Path to the JSON diagnostic file for the failed job."
    )
    args = parser.parse_args()

    # 1. Read and parse the diagnostic file
    try:
        with open(args.diagnostic_file, 'r') as f:
            diagnostic_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error: Could not read or parse diagnostic file '{args.diagnostic_file}': {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Generate the YAML test case content
    job_id = diagnostic_data.get("job_id", "unknown")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_case_yaml = generate_test_case(diagnostic_data)

    # 3. Write the test case to a new file
    # Ensure the target directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'prompt_engineering', 'generated_evaluators')
    os.makedirs(output_dir, exist_ok=True)

    test_case_filename = f"failure_{job_id}_{timestamp}.yaml"
    test_case_filepath = os.path.join(output_dir, test_case_filename)

    try:
        with open(test_case_filepath, 'w') as f:
            f.write(test_case_yaml)
        print(f"--- Successfully generated test case: {test_case_filepath} ---")
    except IOError as e:
        print(f"Error: Could not write test case file to '{test_case_filepath}': {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Invoke the evolve.py script with the new test case
    evolve_script_path = os.path.join(os.path.dirname(__file__), '..', 'prompt_engineering', 'evolve.py')
    command = [
        "python",
        evolve_script_path,
        "--test-case",
        test_case_filepath
    ]

    print(f"--- Invoking prompt evolution script: {' '.join(command)} ---")
    try:
        # We use Popen for a "fire and forget" approach, as evolution can be a long-running process.
        # The supervisor can continue its loop without waiting for this to finish.
        subprocess.Popen(command, stdout=open('adaptation.log', 'a'), stderr=subprocess.STDOUT)
        print("--- Prompt evolution process started in the background. See adaptation.log for details. ---")
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"Error: Failed to start evolution script '{evolve_script_path}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
