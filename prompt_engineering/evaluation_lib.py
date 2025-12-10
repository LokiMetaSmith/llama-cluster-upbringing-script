# This file will contain the reusable functions for evaluating code.
import os
import time
import logging
import shutil
import re
import jinja2
import nomad
import requests

# --- Configuration ---
NOMAD_ADDR = os.environ.get("NOMAD_ADDR", "http://127.0.0.1:4646")
CONSUL_ADDR = os.environ.get("CONSUL_ADDR", "http://127.0.0.1:8500")

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Nomad Client ---
nomad_client = nomad.Nomad(address=NOMAD_ADDR)


def render_nomad_job(template_path: str, context: dict) -> dict:
    """Renders a Jinja2 Nomad job template into a Python dictionary.

    This function takes a path to a Jinja2 template for a Nomad job and a
    context dictionary, renders the template, and then uses the Nomad HTTP API
    to parse the resulting HCL into a dictionary that can be used to register
    the job.

    Args:
        template_path (str): The file path to the Jinja2 Nomad job template.
        context (dict): A dictionary of variables to render in the template.

    Returns:
        dict: The parsed Nomad job specification as a dictionary.
    """
    template_dir, template_name = os.path.split(template_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    rendered_job_hcl = template.render(context)
    return nomad_client.jobs.parse(rendered_job_hcl)


def wait_for_service_healthy(service_name: str, retries: int, delay: int) -> bool:
    """Periodically queries Consul until a service is reported as healthy.

    This function polls the Consul health API for a given service name, waiting
    for all its health checks to pass.

    Args:
        service_name (str): The name of the service registered in Consul.
        retries (int): The maximum number of times to check for health.
        delay (int): The number of seconds to wait between retries.

    Returns:
        bool: True if the service becomes healthy, False if the timeout is
              reached.
    """
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


def get_test_results(job_id: str, evaluation_timeout_seconds: int) -> dict:
    """Monitors a Nomad batch job and retrieves its final logs with granular stats."""
    try:
        # Wait for the job to complete
        nomad_client.job.monitor(job_id, timeout=evaluation_timeout_seconds)

        # Get the allocation for the completed job
        allocs = nomad_client.job.get_allocations(job_id)
        if not allocs:
            raise RuntimeError(f"No allocations found for job '{job_id}'")

        # Assuming one allocation for this batch job
        alloc_id = allocs[0]['ID']

        # Get logs
        logs = nomad_client.allocation.logs(alloc_id, task="run-tests", stderr=True, plain=True)

        # Parse pytest summary for granular stats
        # Find all blocks of === ... === and look for the last one with status keywords
        matches = re.findall(r'={3,} (.*?) ={3,}', logs, re.DOTALL)
        passed = 0
        failed = 0
        errors = 0

        summary = None
        for m in reversed(matches):
            if "passed" in m or "failed" in m or "error" in m or "skipped" in m:
                summary = m
                break

        if summary:
            # Extract passed
            m_passed = re.search(r'(\d+) passed', summary)
            if m_passed:
                passed = int(m_passed.group(1))

            # Extract failed
            m_failed = re.search(r'(\d+) failed', summary)
            if m_failed:
                failed = int(m_failed.group(1))

            # Extract errors (treat as failures)
            m_errors = re.search(r'(\d+) error', summary)
            if m_errors:
                errors = int(m_errors.group(1))

        total = passed + failed + errors
        is_passed = (total > 0 and failed == 0 and errors == 0)

        details = f"Tests: {passed}/{total} passed."
        if failed > 0 or errors > 0:
            details += f" ({failed} failed, {errors} errors)"

        if not summary and "passed" not in logs and "failed" not in logs:
             # Fallback if no summary found (e.g. critical crash before tests ran)
             return {"passed": False, "details": "Could not determine test outcome from logs.", "log": logs, "stats": (0, 0, 0)}

        return {
            "passed": is_passed,
            "details": details,
            "log": logs,
            "stats": (passed, failed, errors)
        }

    except Exception as e:
        logging.error(f"Error getting test results for job '{job_id}': {e}")
        return {"passed": False, "details": str(e), "stats": (0, 0, 0)}


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