import argparse
import json
import os
import subprocess
import sys
import yaml

def generate_test_case(failure_data, test_case_path):
    """
    Generates a YAML test case from the failure data.
    """
    # This is a placeholder implementation.
    # In a real scenario, this would involve a more sophisticated
    # transformation of the failure data into a meaningful test case.
    test_case = {
        "test_name": f"failure_driven_test_{failure_data.get('job_id', 'unknown_job')}",
        "user_query": f"Analyze and resolve the issue described in the following failure data: {json.dumps(failure_data)}",
        "expected_outcome": "A successful resolution or a more accurate diagnosis."
    }
    with open(test_case_path, 'w') as f:
        yaml.dump([test_case], f)

def run_prompt_evolution(test_case_path):
    """
    Runs the prompt evolution script with the generated test case.
    """
    evolve_script_path = os.path.join(os.path.dirname(__file__), '..', 'prompt_engineering', 'evolve.py')
    command = [
        sys.executable,  # Use the same python interpreter
        evolve_script_path,
        '--test-case', test_case_path
    ]

    print(f"--- Running prompt evolution for test case: {test_case_path} ---", file=sys.stderr)

    # We run this as a blocking process. In a real-world scenario,
    # this might be a long-running process that we'd want to
    # manage asynchronously.
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=os.path.join(os.path.dirname(__file__), '..') # Run from project root
    )

    if result.returncode != 0:
        print(f"--- Prompt evolution failed ---", file=sys.stderr)
        print(f"STDOUT:\n{result.stdout}", file=sys.stderr)
        print(f"STDERR:\n{result.stderr}", file=sys.stderr)
        return False

    print(f"--- Prompt evolution completed successfully ---", file=sys.stderr)
    print(f"STDOUT:\n{result.stdout}", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(description="Orchestrate the self-adaptation loop.")
    parser.add_argument(
        "failure_data_file",
        type=str,
        help="Path to the JSON file containing the failure data."
    )
    args = parser.parse_args()

    try:
        with open(args.failure_data_file, 'r') as f:
            failure_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing failure data file: {e}", file=sys.stderr)
        sys.exit(1)

    # Define a path for the temporary test case
    temp_test_case_path = os.path.join('/tmp', f"temp_test_{failure_data.get('job_id', 'unknown')}.yaml")

    print(f"--- Generating dynamic test case for job {failure_data.get('job_id')} ---", file=sys.stderr)
    generate_test_case(failure_data, temp_test_case_path)
    print(f"--- Test case generated at: {temp_test_case_path} ---", file=sys.stderr)

    success = run_prompt_evolution(temp_test_case_path)

    # Clean up the temporary test case file
    os.remove(temp_test_case_path)

    if not success:
        print("--- Self-adaptation cycle failed. ---", file=sys.stderr)
        sys.exit(1)

    print("--- Self-adaptation cycle completed. A new prompt may be available for promotion. ---", file=sys.stderr)


if __name__ == "__main__":
    main()