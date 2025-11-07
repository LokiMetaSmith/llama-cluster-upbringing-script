# Agent Task: Generate a Custom Code Evaluator Script

Last updated: 2025-11-06

## Goal

Your task is to generate a Python script that will act as an "evaluator" for the `openevolve` library. This script will be used to test a candidate code file against a specific test suite in a controlled, isolated environment managed by Nomad and Consul.

## Context

The `openevolve` library works by iteratively modifying a piece of code (the "candidate") and testing its performance. The evaluator script is the testing mechanism. It must:

1. Receive the full content of the candidate code as a string.
2. Set up an environment to run the candidate code.
3. Run a test suite against the running code.
4. Report a "fitness score" (1.0 for success, 0.0 for failure) and other results back to `openevolve` by printing a JSON object to standard output.

## Core Library: `evaluation_lib.py`

You will use the helper functions provided in the `prompt_engineering.evaluation_lib` module. You must import and use these functions correctly.

### Available Functions

- **`render_nomad_job(template_path: str, context: dict) -> dict`**:
  - Renders a Jinja2 Nomad job template into a dictionary that the Nomad API can accept.
  - `template_path`: The file path to the `.j2` template for the Nomad job.
  - `context`: A dictionary of values to render inside the template.

- **`wait_for_service_healthy(service_name: str, retries: int, delay: int) -> bool`**:
  - Polls the Consul health API until the specified service is registered and all its health checks are passing.
  - Returns `True` if the service becomes healthy, `False` otherwise.

- **`get_test_results(job_id: str, evaluation_timeout_seconds: int) -> dict`**:
  - Monitors a Nomad batch job until it completes.
  - Fetches the logs from the `run-tests` task.
  - Parses the logs to check for `pytest` success or failure.
  - Returns a dictionary with `passed` (bool), `details` (str), and `log` (str) keys.

- **`cleanup(job_ids: list, temp_dir: str)`**:
  - Stops all specified Nomad jobs and removes the temporary directory used for the evaluation.

- **`nomad_client`**:
  - A pre-configured `nomad.Nomad` client instance is available in the library. You can import it via `from evaluation_lib import nomad_client`.

## Generation Task

You must generate a complete Python script. The script should not be invoked directly with command-line arguments in production, but it should include a `if __name__ == "__main__":` block for standalone testing, which reads the candidate code from a file path given as the first argument.

### Script Requirements

1. **Imports**: Import necessary standard libraries (`os`, `sys`, `json`, `uuid`, `shutil`, `logging`, `asyncio`) and the functions from `evaluation_lib`.
2. **Configuration**: Define constants for file paths and environment settings. These should be clearly defined at the top of the script. The user will provide these values.
3. **`evaluate_code` async function**: This will be the main function. It must accept one argument: `candidate_code: str`.
4. **Unique IDs**: Generate a unique ID (`eval_id`) for each evaluation run to ensure that job names and temporary directories are isolated.
5. **Temporary Directory Setup**:
    - Create a temporary directory (e.g., `/tmp/eval-{eval_id}`).
    - Copy the *entire source directory* of the application being tested into this temp directory.
    - Overwrite the target file within the temp directory (e.g., `app.py`) with the `candidate_code`.
    - Copy any necessary startup scripts or other assets.
6. **Deployment**:
    - Render the Nomad job template for the main application, passing in the `job_name`, `service_name`, and the path to the temporary directory (`host_volume_source`).
    - Register the job with Nomad using the `nomad_client`.
7. **Health Check**: Use `wait_for_service_healthy` to ensure the application is running before starting tests.
8. **Test Execution**:
    - Render the Nomad job template for the test runner.
    - Set the target service URL in the test runner's environment variables so it knows which instance to test against.
    - Register the test runner job with Nomad.
9. **Result Processing**:
    - Call `get_test_results` to get the outcome.
    - Calculate the fitness score (1.0 for pass, 0.0 for fail).
    - Return a dictionary containing `fitness`, `passed`, `details`, and `log`.
10. **Error Handling & Cleanup**: Wrap the entire process in a `try...finally` block. The `finally` block **must** call the `cleanup` function to stop the Nomad jobs and remove the temporary directory, regardless of success or failure.
11. **Main Block**: Include a standard `if __name__ == "__main__":` block that allows the script to be run from the command line for testing. It should read the code from a file, call `evaluate_code`, and print the results as a JSON string.

### Example Script Template

```python
import os
import sys
import json
import uuid
import shutil
import logging
import asyncio

# IMPORTANT: Assume this script will be run from the repository root.
# Adjust paths accordingly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evaluation_lib import (
    render_nomad_job,
    wait_for_service_healthy,
    get_test_results,
    cleanup,
    nomad_client
)

# --- USER-CONFIGURABLE PARAMETERS ---
# These will be replaced by the generator script
APP_JOB_TEMPLATE_PATH = "path/to/your/app.nomad.j2"
TEST_RUNNER_JOB_TEMPLATE_PATH = "path/to/your/test_runner.nomad.j2"
APP_SOURCE_DIR = "path/to/the/source/code/directory/"
# The file within APP_SOURCE_DIR that will be replaced by the candidate code
TARGET_CODE_FILE = "app.py"
# An essential startup script that might not be in the source dir
# Use None if not applicable
AUXILIARY_STARTUP_SCRIPT = "/path/to/start.sh"


# --- STATIC CONFIGURATION ---
EVALUATION_TIMEOUT_SECONDS = 300
HEALTH_CHECK_RETRIES = 60
HEALTH_CHECK_DELAY = 5
LOG_LEVEL = logging.INFO

# --- Logging ---
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')


async def evaluate_code(candidate_code: str) -> dict:
    """
    Evaluates candidate Python code by deploying it in an isolated Nomad
    environment and running integration tests against it.
    """
    eval_id = str(uuid.uuid4())[:8]
    temp_dir = f"/tmp/eval-{eval_id}"
    app_job_id = f"app-eval-{eval_id}"
    service_name = f"service-eval-{eval_id}"
    test_job_id = f"test-runner-eval-{eval_id}"
    jobs_to_clean = []

    try:
        # 1. Setup temporary directory
        logging.info(f"Creating temporary directory: {temp_dir}")
        shutil.copytree(APP_SOURCE_DIR, temp_dir)
        with open(os.path.join(temp_dir, TARGET_CODE_FILE), "w") as f:
            f.write(candidate_code)

        if AUXILIARY_STARTUP_SCRIPT and os.path.exists(AUXILIARY_STARTUP_SCRIPT):
            dest_script_path = os.path.join(temp_dir, os.path.basename(AUXILIARY_STARTUP_SCRIPT))
            shutil.copy(AUXILIARY_STARTUP_SCRIPT, dest_script_path)
            os.chmod(dest_script_path, 0o755)

        # 2. Deploy the application
        logging.info(f"Deploying application job '{app_job_id}'")
        app_job_context = {
            "job_name": app_job_id,
            "service_name": service_name,
            "host_volume_source": temp_dir
        }
        app_job_spec = render_nomad_job(APP_JOB_TEMPLATE_PATH, app_job_context)
        nomad_client.jobs.register_job({'Job': app_job_spec})
        jobs_to_clean.append(app_job_id)

        # 3. Wait for the service to be healthy
        if not wait_for_service_healthy(service_name, HEALTH_CHECK_RETRIES, HEALTH_CHECK_DELAY):
            raise RuntimeError(f"Application service '{service_name}' failed to become healthy.")

        # 4. Run the test job
        logging.info(f"Running test job '{test_job_id}' against service '{service_name}'")
        test_job_spec = render_nomad_job(TEST_RUNNER_JOB_TEMPLATE_PATH, {})
        test_job_spec['ID'] = test_job_id
        test_job_spec['TaskGroups'][0]['Tasks'][0]['Env']['TARGET_SERVICE_URL'] = f"http://{service_name}.service.consul:8000"
        nomad_client.jobs.register_job({'Job': test_job_spec})
        jobs_to_clean.append(test_job_id)

        # 5. Get test results
        results = get_test_results(test_job_id, EVALUATION_TIMEOUT_SECONDS)
        fitness = 1.0 if results.get("passed") else 0.0
        logging.info(f"Evaluation finished. Fitness: {fitness}. Details: {results.get('details')}")
        results["fitness"] = fitness
        return results

    except Exception as e:
        logging.error(f"An error occurred during evaluation: {e}", exc_info=True)
        return {"fitness": 0.0, "error": str(e)}
    finally:
        cleanup(jobs_to_clean, temp_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path_to_candidate_code_file>")
        sys.exit(1)

    code_file_path = sys.argv[1]
    with open(code_file_path, 'r') as f:
        code = f.read()

    results = asyncio.run(evaluate_code(code))
    print(json.dumps(results, indent=2))

```
