import os
import sys
import json
import uuid
import shutil
import logging

from evaluation_lib import (
    render_nomad_job,
    wait_for_service_healthy,
    get_test_results,
    cleanup,
)

# --- Configuration ---
JOB_TEMPLATE_PATH = "ansible/roles/pipecatapp/templates/pipecatapp.nomad.j2"
TEST_RUNNER_TEMPLATE_PATH = "ansible/jobs/test-runner.nomad.j2"
APP_SOURCE_DIR = "ansible/roles/pipecatapp/files"
EVALUATION_TIMEOUT_SECONDS = 300  # 5 minutes
HEALTH_CHECK_RETRIES = 60
HEALTH_CHECK_DELAY = 5

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def evaluate_code(candidate_code: str) -> dict:
    """Evaluates candidate code by deploying it and running integration tests.

    This function now expects the `candidate_code` to be a JSON string
    containing both the code and the LLM's rationale for the change.

    This function orchestrates the end-to-end evaluation of a candidate code
    string. It performs the following steps:
    1. Creates a temporary directory and copies the application source code.
    2. Overwrites the target file (e.g., `app.py`) with the candidate code.
    3. Renders and deploys a Nomad job for the application.
    4. Waits for the application's service to become healthy in Consul.
    5. Renders and deploys a Nomad batch job to run integration tests against
       the new service.
    6. Monitors the test job and captures its logs to determine the outcome.
    7. Cleans up all created resources (Nomad jobs, temporary directories).

    Args:
        candidate_code (str): The Python code to be evaluated.

    Returns:
        dict: A dictionary containing the fitness score (1.0 for pass, 0.0 for
              fail), a boolean 'passed' status, and details from the test run.
    """
    eval_id = str(uuid.uuid4())[:8]
    archive_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "archive"))
    os.makedirs(archive_dir, exist_ok=True)
    agent_code_path = os.path.join(archive_dir, f"{eval_id}.py")
    agent_meta_path = os.path.join(archive_dir, f"{eval_id}.json")

    # Parse the incoming JSON from the LLM
    try:
        data = json.loads(candidate_code)
        actual_code = data['code']
        rationale = data.get('rationale', 'No rationale provided.')
    except (json.JSONDecodeError, TypeError, KeyError):
        # The LLM failed to produce valid JSON. Treat the whole thing as code.
        logging.warning("Could not parse LLM output as JSON. Treating the entire response as code.")
        actual_code = candidate_code
        rationale = "N/A - Invalid JSON response from LLM."

    # Save the candidate's code (only the code part) to the archive
    with open(agent_code_path, "w") as f:
        f.write(actual_code)
    logging.info(f"Saved candidate agent to {agent_code_path}")


    temp_dir = f"/tmp/eval-{eval_id}"
    app_job_id = f"pipecat-app-eval-{eval_id}"
    service_name = f"llama-api-eval-{eval_id}"
    test_job_id = f"test-runner-eval-{eval_id}"

    jobs_to_clean = []

    try:
        # 1. Setup temporary directory with candidate code
        logging.info(f"Creating temporary directory: {temp_dir}")
        shutil.copytree(APP_SOURCE_DIR, temp_dir)
        with open(os.path.join(temp_dir, "app.py"), "w") as f:
            f.write(actual_code)

        # Also copy the startup script, which is not in the source dir
        main_startup_script = "/opt/pipecatapp/start_pipecat.sh"
        if not os.path.exists(main_startup_script):
            raise FileNotFoundError(f"Main startup script not found at {main_startup_script}. Run bootstrap.sh first.")
        shutil.copy(main_startup_script, os.path.join(temp_dir, "start_pipecat.sh"))
        os.chmod(os.path.join(temp_dir, "start_pipecat.sh"), 0o755)


        # 2. Deploy the application with the candidate code
        logging.info(f"Deploying application job '{app_job_id}'")
        app_job_context = {
            "job_name": app_job_id,
            "service_name": service_name,
            "host_volume_source": temp_dir
        }
        app_job_spec = render_nomad_job(JOB_TEMPLATE_PATH, app_job_context)
        # Note: The original script used a global nomad_client. The lib function does too.
        from evaluation_lib import nomad_client
        nomad_client.jobs.register_job({'Job': app_job_spec})
        jobs_to_clean.append(app_job_id)

        # 3. Wait for the new service to be healthy
        if not wait_for_service_healthy(service_name, HEALTH_CHECK_RETRIES, HEALTH_CHECK_DELAY):
            raise RuntimeError("Application service failed to become healthy.")

        # 4. Run the test job
        logging.info(f"Running test job '{test_job_id}' against service '{service_name}'")
        test_job_spec = render_nomad_job(TEST_RUNNER_TEMPLATE_PATH, {})
        test_job_spec['ID'] = test_job_id
        # This assumes the test runner job has these env vars available.
        test_job_env = test_job_spec['TaskGroups'][0]['Tasks'][0]['Env']
        test_job_env['TARGET_SERVICE_URL'] = f"http://{service_name}.service.consul:8000"

        # Check if a dynamic test case path is provided via environment variable
        dynamic_test_path = os.environ.get("DYNAMIC_TEST_CASE_PATH")
        if dynamic_test_path:
            logging.info(f"Using dynamic test case from: {dynamic_test_path}")
            # The test runner is configured to look for this env var
            test_job_env['PYTEST_TARGET'] = dynamic_test_path
        else:
            # Default behavior: run the whole suite
            logging.info("No dynamic test case provided. Running default test suite.")
            test_job_env['PYTEST_TARGET'] = "/app/tests/integration/"


        nomad_client.jobs.register_job({'Job': test_job_spec})
        jobs_to_clean.append(test_job_id)

        # 5. Get test results
        results = get_test_results(test_job_id, EVALUATION_TIMEOUT_SECONDS)
        fitness = 1.0 if results.get("passed") else 0.0

        logging.info(f"Evaluation finished. Fitness: {fitness}. Details: {results.get('details')}")

        evaluation_results = {
            "fitness": fitness,
            "passed": results.get("passed"),
            "details": results.get("details"),
            "log": results.get("log", "")
        }
        return evaluation_results

    except Exception as e:
        logging.error(f"An error occurred during evaluation: {e}", exc_info=True)
        evaluation_results = {"fitness": 0.0, "error": str(e)}
        return evaluation_results
    finally:
        # Save metadata to the archive
        if 'evaluation_results' in locals():
            # Add the rationale to the results dictionary
            evaluation_results['rationale'] = rationale

            # Check for parent ID from the environment
            parent_id = os.environ.get("PARENT_AGENT_ID")
            if parent_id:
                evaluation_results["parent"] = parent_id

            with open(agent_meta_path, "w") as f:
                json.dump(evaluation_results, f, indent=2)
            logging.info(f"Saved agent metadata to {agent_meta_path}")

        # Cleanup successful jobs, leave failed ones for inspection
        cleanup(jobs_to_clean, temp_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluator.py <path_to_candidate_code_file>")
        sys.exit(1)

    code_file_path = sys.argv[1]
    with open(code_file_path, 'r') as f:
        code = f.read()

    import asyncio
    results = asyncio.run(evaluate_code(code))

    print(json.dumps(results))