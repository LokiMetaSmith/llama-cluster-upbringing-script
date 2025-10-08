import argparse
import os

# The template is based on the one defined in prompt_engineering/agents/EVALUATOR_GENERATOR.md
EVALUATOR_TEMPLATE = """\
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

# --- GENERATED CONFIGURATION ---
APP_JOB_TEMPLATE_PATH = "{app_job_template_path}"
TEST_RUNNER_JOB_TEMPLATE_PATH = "{test_runner_job_template_path}"
APP_SOURCE_DIR = "{app_source_dir}"
TARGET_CODE_FILE = "{target_code_file}"
AUXILIARY_STARTUP_SCRIPT = {auxiliary_startup_script}


# --- STATIC CONFIGURATION ---
EVALUATION_TIMEOUT_SECONDS = 300
HEALTH_CHECK_RETRIES = 60
HEALTH_CHECK_DELAY = 5
LOG_LEVEL = logging.INFO

# --- Logging ---
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')


async def evaluate_code(candidate_code: str) -> dict:
    \"\"\"
    Evaluates candidate Python code by deploying it in an isolated Nomad
    environment and running integration tests against it.
    \"\"\"
    eval_id = str(uuid.uuid4())[:8]
    temp_dir = f"/tmp/eval-{{eval_id}}"
    app_job_id = f"app-eval-{{eval_id}}"
    service_name = f"service-eval-{{eval_id}}"
    test_job_id = f"test-runner-eval-{{eval_id}}"
    jobs_to_clean = []

    try:
        # 1. Setup temporary directory
        logging.info(f"Creating temporary directory: {{temp_dir}}")
        shutil.copytree(APP_SOURCE_DIR, temp_dir)
        with open(os.path.join(temp_dir, TARGET_CODE_FILE), "w") as f:
            f.write(candidate_code)

        if AUXILIARY_STARTUP_SCRIPT and os.path.exists(AUXILIARY_STARTUP_SCRIPT):
            dest_script_path = os.path.join(temp_dir, os.path.basename(AUXILIARY_STARTUP_SCRIPT))
            shutil.copy(AUXILIARY_STARTUP_SCRIPT, dest_script_path)
            os.chmod(dest_script_path, 0o755)

        # 2. Deploy the application
        logging.info(f"Deploying application job '{{app_job_id}}'")
        app_job_context = {{
            "job_name": app_job_id,
            "service_name": service_name,
            "host_volume_source": temp_dir
        }}
        app_job_spec = render_nomad_job(APP_JOB_TEMPLATE_PATH, app_job_context)
        nomad_client.jobs.register_job({{'Job': app_job_spec}})
        jobs_to_clean.append(app_job_id)

        # 3. Wait for the service to be healthy
        if not wait_for_service_healthy(service_name, HEALTH_CHECK_RETRIES, HEALTH_CHECK_DELAY):
            raise RuntimeError(f"Application service '{{service_name}}' failed to become healthy.")

        # 4. Run the test job
        logging.info(f"Running test job '{{test_job_id}}' against service '{{service_name}}'")
        test_job_spec = render_nomad_job(TEST_RUNNER_JOB_TEMPLATE_PATH, {{}})
        test_job_spec['ID'] = test_job_id
        test_job_spec['TaskGroups'][0]['Tasks'][0]['Env']['TARGET_SERVICE_URL'] = f"http://{{service_name}}.service.consul:8000"
        nomad_client.jobs.register_job({{'Job': test_job_spec}})
        jobs_to_clean.append(test_job_id)

        # 5. Get test results
        results = get_test_results(test_job_id, EVALUATION_TIMEOUT_SECONDS)
        fitness = 1.0 if results.get("passed") else 0.0
        logging.info(f"Evaluation finished. Fitness: {{fitness}}. Details: {{results.get('details')}}")
        results["fitness"] = fitness
        return results

    except Exception as e:
        logging.error(f"An error occurred during evaluation: {{e}}", exc_info=True)
        return {{"fitness": 0.0, "error": str(e)}}
    finally:
        cleanup(jobs_to_clean, temp_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {{sys.argv[0]}} <path_to_candidate_code_file>")
        sys.exit(1)

    code_file_path = sys.argv[1]
    with open(code_file_path, 'r') as f:
        code = f.read()

    results = asyncio.run(evaluate_code(code))
    print(json.dumps(results, indent=2))
"""

def main():
    parser = argparse.ArgumentParser(
        description="Generate a custom evaluator script for openevolve.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--app-job-template",
        required=True,
        help="Path to the application's Nomad job template (.j2)."
    )
    parser.add_argument(
        "--test-runner-job-template",
        required=True,
        help="Path to the test runner's Nomad job template (.j2)."
    )
    parser.add_argument(
        "--app-source-dir",
        required=True,
        help="Path to the directory containing the application's source code."
    )
    parser.add_argument(
        "--target-code-file",
        required=True,
        help="The specific file within the app-source-dir that openevolve will modify."
    )
    parser.add_argument(
        "--aux-startup-script",
        default=None,
        help="Optional path to an auxiliary startup script to be copied into the temp directory."
    )
    parser.add_argument(
        "--output-path",
        required=True,
        help="Path to save the generated evaluator script (e.g., 'prompt_engineering/generated_evaluators/eval_app.py')."
    )

    args = parser.parse_args()

    # Format the auxiliary script path as a Python string literal, or 'None'
    aux_script_repr = f"'{args.aux_startup_script}'" if args.aux_startup_script else "None"

    # Generate the script content
    script_content = EVALUATOR_TEMPLATE.format(
        app_job_template_path=args.app_job_template,
        test_runner_job_template_path=args.test_runner_job_template,
        app_source_dir=args.app_source_dir,
        target_code_file=args.target_code_file,
        auxiliary_startup_script=aux_script_repr,
    )

    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(args.output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the generated script
    with open(args.output_path, "w") as f:
        f.write(script_content)

    print(f"Successfully generated evaluator script at: {args.output_path}")


if __name__ == "__main__":
    main()