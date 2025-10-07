import os
import sys
import json
import uuid
import shutil
import time
import nomad
import jinja2
import requests
import logging

# --- Configuration ---
NOMAD_ADDR = os.environ.get("NOMAD_ADDR", "http://127.0.0.1:4646")
CONSUL_ADDR = os.environ.get("CONSUL_ADDR", "http://127.0.0.1:8500")
JOB_TEMPLATE_PATH = "ansible/roles/pipecatapp/templates/pipecatapp.nomad.j2"
TEST_RUNNER_TEMPLATE_PATH = "ansible/jobs/test-runner.nomad.j2"
APP_SOURCE_DIR = "ansible/roles/pipecatapp/files"
EVALUATION_TIMEOUT_SECONDS = 300  # 5 minutes
HEALTH_CHECK_RETRIES = 60
HEALTH_CHECK_DELAY = 5

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Nomad Client ---
nomad_client = nomad.Nomad(address=NOMAD_ADDR)

def render_nomad_job(template_path: str, context: dict) -> dict:
    """Renders a Jinja2 Nomad job template."""
    template_dir, template_name = os.path.split(template_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    rendered_job_hcl = template.render(context)
    return nomad_client.jobs.parse(rendered_job_hcl)

def wait_for_service_healthy(service_name: str, retries: int, delay: int) -> bool:
    """Waits for a Consul service to become healthy."""
    logging.info(f"Waiting for service '{service_name}' to become healthy...")
    for i in range(retries):
        try:
            url = f"{CONSUL_ADDR}/v1/health/service/{service_name}"
            response = requests.get(url)
            response.raise_for_status()
            health_data = response.json()

            if health_data and all(
                check['Status'] == 'passing'
                for entry in health_data
                for check in entry['Checks']
            ):
                logging.info(f"Service '{service_name}' is healthy.")
                return True
        except requests.RequestException as e:
            logging.warning(f"Consul request failed: {e}. Retrying...")
        except (KeyError, IndexError):
            logging.warning(f"Service '{service_name}' not yet registered or has no checks. Retrying...")

        time.sleep(delay)

    logging.error(f"Timeout: Service '{service_name}' did not become healthy after {retries * delay} seconds.")
    return False

def get_test_results(job_id: str) -> dict:
    """Monitors a Nomad batch job and retrieves its final logs."""
    try:
        # Wait for the job to complete
        nomad_client.job.monitor(job_id, timeout=EVALUATION_TIMEOUT_SECONDS)

        # Get the allocation for the completed job
        allocs = nomad_client.job.get_allocations(job_id)
        if not allocs:
            raise RuntimeError(f"No allocations found for job '{job_id}'")

        # Assuming one allocation for this batch job
        alloc_id = allocs[0]['ID']

        # Get logs
        logs = nomad_client.allocation.logs(alloc_id, task="run-tests", stderr=True, plain=True)

        # Simple check for pytest summary
        if "failed" in logs or "error" in logs:
            return {"passed": False, "details": "Pytest reported failures or errors.", "log": logs}
        elif "passed" in logs:
            return {"passed": True, "details": "Pytest reported all tests passed.", "log": logs}
        else:
            return {"passed": False, "details": "Could not determine test outcome from logs.", "log": logs}

    except Exception as e:
        logging.error(f"Error getting test results for job '{job_id}': {e}")
        return {"passed": False, "details": str(e)}


def cleanup(job_ids: list, temp_dir: str):
    """Stops Nomad jobs and removes the temporary directory."""
    for job_id in job_ids:
        try:
            logging.info(f"Cleaning up Nomad job '{job_id}'...")
            nomad_client.job.deregister(job_id, purge=True)
        except Exception as e:
            logging.error(f"Failed to cleanup Nomad job '{job_id}': {e}")

    if os.path.exists(temp_dir):
        logging.info(f"Removing temporary directory '{temp_dir}'...")
        shutil.rmtree(temp_dir)


async def evaluate_code(candidate_code: str) -> dict:
    """
    Evaluates candidate Python code by deploying it in an isolated Nomad
    environment and running integration tests against it.
    """
    eval_id = str(uuid.uuid4())[:8]
    temp_dir = f"/tmp/eval-{eval_id}"
    app_job_id = f"pipecat-app-eval-{eval_id}"
    service_name = f"prima-api-eval-{eval_id}"
    test_job_id = f"test-runner-eval-{eval_id}"

    jobs_to_clean = []

    try:
        # 1. Setup temporary directory with candidate code
        logging.info(f"Creating temporary directory: {temp_dir}")
        shutil.copytree(APP_SOURCE_DIR, temp_dir)
        with open(os.path.join(temp_dir, "app.py"), "w") as f:
            f.write(candidate_code)

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
        nomad_client.jobs.register_job({'Job': app_job_spec})
        jobs_to_clean.append(app_job_id)

        # 3. Wait for the new service to be healthy
        if not wait_for_service_healthy(service_name, HEALTH_CHECK_RETRIES, HEALTH_CHECK_DELAY):
            raise RuntimeError("Application service failed to become healthy.")

        # 4. Run the test job
        logging.info(f"Running test job '{test_job_id}' against service '{service_name}'")
        # The test runner template doesn't need context, but we need to give it a unique ID
        test_job_spec = render_nomad_job(TEST_RUNNER_TEMPLATE_PATH, {})
        test_job_spec['ID'] = test_job_id
        test_job_spec['TaskGroups'][0]['Tasks'][0]['Env']['TARGET_SERVICE_URL'] = f"http://{service_name}.service.consul:8000"

        nomad_client.jobs.register_job({'Job': test_job_spec})
        jobs_to_clean.append(test_job_id)

        # 5. Get test results
        results = get_test_results(test_job_id)
        fitness = 1.0 if results.get("passed") else 0.0

        logging.info(f"Evaluation finished. Fitness: {fitness}. Details: {results.get('details')}")

        return {
            "fitness": fitness,
            "passed": results.get("passed"),
            "details": results.get("details"),
            "log": results.get("log", "")
        }

    except Exception as e:
        logging.error(f"An error occurred during evaluation: {e}", exc_info=True)
        return {"fitness": 0.0, "error": str(e)}
    finally:
        # Cleanup successful jobs, leave failed ones for inspection
        cleanup(jobs_to_clean, temp_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluator.py <path_to_candidate_code_file>")
        sys.exit(1)

    code_file_path = sys.argv[1]
    with open(code_file_path, 'r') as f:
        code = f.read()

    # openevolve runs async, so we need a loop to run our main function
    import asyncio
    results = asyncio.run(evaluate_code(code))

    # The openevolve library expects a JSON object printed to stdout
    print(json.dumps(results))