import json
import subprocess
import sys
import os
import requests
import yaml

# Global cache for LLM configuration
LLM_CONFIG = None

def load_llm_config():
    """Loads LLM configuration from group_vars/all.yaml and caches it."""
    global LLM_CONFIG
    if LLM_CONFIG:
        return LLM_CONFIG

    config_path = os.path.join(os.path.dirname(__file__), '..', 'group_vars/all.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            LLM_CONFIG = config['external_experts_config']['openai_gpt4']
            # Also load the plaintext key from the same file as a fallback
            LLM_CONFIG['api_key_plaintext'] = config.get('openai_api_key')
            return LLM_CONFIG
    except (IOError, yaml.YAMLError, KeyError) as e:
        print(f"Error loading LLM config from {config_path}: {e}", file=sys.stderr)
        return None

def call_openai_llm(messages):
    """Makes a real API call to the OpenAI chat completions endpoint."""
    config = load_llm_config()
    if not config:
        return json.dumps({"analysis": "LLM configuration is missing or invalid.", "action": "error", "parameters": {}})

    api_key = os.environ.get(config['api_key_env'])
    if not api_key or "your_openai_api_key_here" in api_key:
        api_key = config.get('api_key_plaintext')

    if not api_key or "your_openai_api_key_here" in api_key:
        error_msg = f"API key not found in env var {config['api_key_env']} or in group_vars/all.yaml."
        print(error_msg, file=sys.stderr)
        return json.dumps({"analysis": error_msg, "action": "error", "parameters": {}})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": config['model'],
        "messages": messages,
        "response_format": {"type": "json_object"},
        "temperature": 0.2, # Lower temperature for more deterministic, factual responses
    }

    endpoint = f"{config['base_url'].rstrip('/')}/chat/completions"

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        response_data = response.json()
        content_str = response_data['choices'][0]['message']['content']
        return content_str
    except requests.exceptions.RequestException as e:
        error_msg = f"Error calling OpenAI API: {e}"
        print(error_msg, file=sys.stderr)
        return json.dumps({"analysis": error_msg, "action": "error", "parameters": {}})
    except (KeyError, IndexError) as e:
        error_msg = f"Error parsing OpenAI API response: {e}"
        print(error_msg, file=sys.stderr)
        return json.dumps({"analysis": error_msg, "action": "error", "parameters": {}})

def run_tool(tool_call):
    """Executes a tool call requested by the LLM."""
    tool_name = tool_call.get("name")
    params = tool_call.get("parameters")

    if tool_name == "get_nomad_job":
        job_id = params.get("job_id")
        # Ensure the path is relative to the project root
        script_path = os.path.join(os.path.dirname(__file__), '..', 'ansible/roles/pipecatapp/files/tools/get_nomad_job.py')
        try:
            command = ["python", script_path, job_id]
            result = subprocess.run(command, capture_output=True, text=True, check=True, cwd=os.path.join(os.path.dirname(__file__), '..'))
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            stderr = e.stderr if hasattr(e, 'stderr') else '(no stderr)'
            return f"Error running tool {tool_name}: {e}\n{stderr}"

    return "Error: Unknown tool requested."

def analyze_failure_with_llm(diagnostic_data):
    """
    Analyzes a job failure by making real API calls to an LLM,
    including handling tool use by maintaining a message history.
    """
    system_prompt = """
    You are an expert system administrator specializing in Nomad cluster operations. Your task is to analyze a failed job's diagnostic data and determine a course of action.
    Your response MUST be a single, valid JSON object.

    1. If you need more information, respond with a `tool_call` object.
       Example: `{"tool_call": {"name": "get_nomad_job", "parameters": {"job_id": "the-job-id"}}}`

    2. If you have enough information, respond with a final `action` object.
       Example: `{"analysis": "The job failed due to an OOM error.", "action": "increase_memory", "parameters": {"job_id": "the-job-id", "memory_mb": 512}}`

    Available tools:
    - `get_nomad_job`: Retrieves the full job specification. Use this for suspected configuration issues (e.g., memory).

    Available actions:
    - `restart`: A generic restart. Parameters: `job_id`.
    - `increase_memory`: For OOM errors. Parameters: `job_id`, `memory_mb`. Double the previous value if possible.
    - `error`: If you cannot determine a cause.
    """

    user_prompt = f"""
    A Nomad job with ID '{diagnostic_data.get("job_id")}' has failed.
    Diagnostic information:
    {json.dumps(diagnostic_data, indent=2)}
    Please analyze this failure and respond in the specified JSON format.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    llm_response_str = call_openai_llm(messages)
    llm_response = json.loads(llm_response_str)

    if "tool_call" in llm_response:
        messages.append({"role": "assistant", "content": llm_response_str})

        tool_call = llm_response.get("tool_call")
        print(f"--- LLM requested tool: {tool_call.get('name')} with params {tool_call.get('parameters')} ---", file=sys.stderr)

        tool_output = run_tool(tool_call)

        tool_response_prompt = f"Tool `{tool_call.get('name')}` output:\n{tool_output}"
        messages.append({"role": "user", "content": tool_response_prompt})

        final_response_str = call_openai_llm(messages)
        return json.loads(final_response_str)

    return llm_response

def main():
    if len(sys.argv) < 2:
        print("Usage: python reflect.py <path_to_diagnostic_file>", file=sys.stderr)
        sys.exit(1)

    diagnostic_file_path = sys.argv[1]

    try:
        with open(diagnostic_file_path, 'r') as f:
            diagnostic_data = json.load(f)

        solution = analyze_failure_with_llm(diagnostic_data)
        print(json.dumps(solution, indent=2))

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing diagnostic file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()