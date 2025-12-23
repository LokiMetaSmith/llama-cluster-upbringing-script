import json
import subprocess
import sys
import os
import requests
import yaml

# Global cache for LLM configuration
LLM_CONFIG = None

def load_llm_config():
    """Loads and caches the LLM configuration from the main Ansible vars file.

    This function reads `group_vars/all.yaml` to find the configuration
    for the external expert (OpenAI GPT-4), which is used for reflection.
    It caches the result in a global variable to avoid repeated file reads.

    Returns:
        dict: The configuration dictionary for the LLM, or None if the
              configuration cannot be loaded.
    """
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

def call_openai_llm(messages, reasoning_config=None):
    """Sends a request to the OpenAI Chat Completions API.

    This function constructs and sends a request to the configured OpenAI
    endpoint, handling authentication and error reporting.

    Args:
        messages (list): A list of message dictionaries conforming to the
            OpenAI API schema.
        reasoning_config (dict, optional): Configuration for reasoning tokens
            (e.g., {"effort": "high"} or {"max_tokens": 1000}).

    Returns:
        str: The JSON content of the API response as a string, or a JSON
             string containing an error message.
    """
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

    if reasoning_config:
        payload["reasoning"] = reasoning_config

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
    """Executes a tool call requested by the LLM and captures its output.

    This function acts as a dispatcher, calling the appropriate local script
    or function based on the tool name provided by the LLM.

    Args:
        tool_call (dict): A dictionary representing the tool call, containing
            'name' and 'parameters'.

    Returns:
        str: The standard output of the executed tool, or an error message.
    """
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
    """Orchestrates the LLM interaction to analyze a failure.

    This function manages the conversational loop with the LLM. It sends the
    initial diagnostic data, handles requests for tool execution, and sends
    the tool output back to the LLM until a final action is decided upon.

    Args:
        diagnostic_data (dict): A dictionary containing the initial failure
            diagnostics.

    Returns:
        dict: The final JSON object from the LLM, containing the analysis
              and the proposed action.
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
    """The main entry point for the reflection script.

    This function parses the command-line arguments to get the path to the
    diagnostic file, reads the file, and initiates the failure analysis
    process. The final proposed solution from the LLM is printed to standard
    output as a JSON string.
    """
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