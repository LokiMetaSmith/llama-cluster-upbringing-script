import argparse
import json
import os
import subprocess
import sys
import yaml
import requests

LLM_CONFIG = None

def load_llm_config():
    """Loads the specific LLM configuration for the Adaptation Agent."""
    global LLM_CONFIG
    if LLM_CONFIG:
        return LLM_CONFIG

    config_path = os.path.join(os.path.dirname(__file__), '..', 'group_vars/all.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        # The agent definition specifies a Groq model. We assume its config is here.
        LLM_CONFIG = config['external_experts_config']['groq_llama3_70b']
        LLM_CONFIG['api_key_plaintext'] = config.get('groq_api_key')
        return LLM_CONFIG
    except (IOError, yaml.YAMLError, KeyError) as e:
        print(f"Error loading LLM config: {e}", file=sys.stderr)
        return None

def call_llm_for_test_case(diagnostic_data):
    """Calls the configured LLM to generate a structured test case."""
    config = load_llm_config()
    if not config:
        return None

    api_key = os.environ.get(config.get('api_key_env', 'GROQ_API_KEY'), config.get('api_key_plaintext'))
    if not api_key or "your_groq_api_key_here" in api_key:
        print("Error: Groq API key not found.", file=sys.stderr)
        return None

    system_prompt = """
    You are an expert in software testing and root cause analysis. Your task is to analyze a failed job's diagnostic data and generate a single, specific, and reproducible test case in YAML format.

    The test case should be structured to run within our integration test framework. The goal is to create a test that will fail in the same way as the provided diagnostics, thus proving that a future code change has fixed the root cause.

    Analyze the provided logs, job status, and job specification. Form a hypothesis about the root cause. Then, construct a series of steps that will reliably trigger the failure.

    Your response MUST be a single, valid YAML document. Do not add any explanations, apologies, or markdown formatting. The YAML should represent a list of tests, even if you only generate one.

    Example of a good response:
    ```yaml
    tests:
      - name: test_reproduce_oom_on_large_input
        description: "Verify that the application handles large text inputs without crashing, which was the suspected cause of the failure in job my-job-123."
        steps:
          - action: send_message
            payload:
              message: "Summarize this 10,000-word document: [very long text...]"
          - action: expect_response
            payload:
              constraints:
                - does_not_contain_error
                - has_word_count_less_than: 200
    ```
    """

    user_prompt = f"""
    A Nomad job with ID '{diagnostic_data.get("job_id", "N/A")}' has failed.
    Here is the diagnostic information:
    {json.dumps(diagnostic_data, indent=2)}

    Please generate a YAML test case to reproduce this failure.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config['model'],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7, # As specified in the agent definition
        "top_p": 0.9,
    }
    endpoint = f"{config['base_url'].rstrip('/')}/chat/completions"

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=180)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        # The LLM might still wrap the output in markdown, so we extract it.
        if "```yaml" in content:
            content = content.split("```yaml\n")[1].split("```")[0]
        return content
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {e}", file=sys.stderr)
    except (KeyError, IndexError) as e:
        print(f"Error parsing LLM response: {e}", file=sys.stderr)
    return None

def main():
    """Main entry point for the adaptation manager."""
    parser = argparse.ArgumentParser(description="Orchestrates the self-adaptation loop.")
    parser.add_argument("diagnostics_file", type=str, help="Path to the JSON diagnostics file.")
    args = parser.parse_args()

    try:
        with open(args.diagnostics_file, 'r') as f:
            diagnostics = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading diagnostics file: {e}", file=sys.stderr)
        sys.exit(1)

    print("--- Generating test case via LLM... ---")
    test_case_yaml = call_llm_for_test_case(diagnostics)

    if not test_case_yaml:
        print("Error: LLM failed to generate a test case.", file=sys.stderr)
        sys.exit(1)

    test_case_path = f"/tmp/test_case_{os.path.basename(args.diagnostics_file)}.yaml"
    try:
        with open(test_case_path, 'w') as f:
            f.write(test_case_yaml)
        print(f"--- Generated new test case: {test_case_path} ---")
        print(test_case_yaml)
    except IOError as e:
        print(f"Error writing test case file: {e}", file=sys.stderr)
        sys.exit(1)

    evolve_script_path = "prompt_engineering/evolve.py"
    command = ["python", evolve_script_path, "--test-case", test_case_path]
    print(f"--- Invoking evolution script: {' '.join(command)} ---")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running evolution script:", file=sys.stderr)
        print(result.stdout, file=sys.stdout)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    print(result.stdout)
    print("--- Evolution process completed successfully. ---")

if __name__ == "__main__":
    main()
