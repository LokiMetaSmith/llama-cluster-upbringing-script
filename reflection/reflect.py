import json
import subprocess
import sys
import os

def call_prima_expert_llm(prompt, context=None):
    """
    Simulates a call to a prima-expert LLM.
    In a real implementation, this would be an API call.
    This simulation models the LLM's reasoning process, including tool use.
    """
    # Simulate LLM reasoning for tool use. If the logs mention "out of memory",
    # the LLM should decide it needs to see the job's current configuration.
    if "out of memory" in prompt.lower() and context is None:
        try:
            # In a real scenario, the LLM would extract the job_id from the structured prompt.
            # Here, we extract it from the diagnostic data embedded in the prompt string.
            data_start = prompt.find('{')
            data_end = prompt.rfind('}') + 1
            diag_data = json.loads(prompt[data_start:data_end])
            job_id = diag_data.get("job_id")

            # The LLM responds with a request to call a tool.
            return json.dumps({
                "thought": "The logs indicate an 'out of memory' error. To suggest a new memory value, I must first inspect the job's current memory allocation. I will use the get_nomad_job tool.",
                "tool_call": {
                    "name": "get_nomad_job",
                    "parameters": {"job_id": job_id}
                }
            })
        except (json.JSONDecodeError, KeyError):
            # Fallback if parsing fails.
            pass

    # Simulate LLM response after receiving the tool's output (the job spec).
    if context and '"TaskGroups"' in context: # A simple check to see if the context is a Nomad job spec.
        job_spec = json.loads(context)
        job_id = job_spec.get("ID")
        try:
            # Find the memory allocation and suggest a new, larger value.
            current_memory = job_spec.get("TaskGroups", [{}])[0].get("Tasks", [{}])[0].get("Resources", {}).get("MemoryMB", 256)
            new_memory = current_memory * 2  # Double the memory as a simple heuristic.
            return json.dumps({
                "analysis": f"The job failed due to an OOM error. The current memory allocation is {current_memory}MB. Proposing an increase to {new_memory}MB.",
                "action": "increase_memory",
                "parameters": {"job_id": job_id, "memory_mb": new_memory}
            })
        except (IndexError, KeyError):
             # Fallback if the job spec is malformed.
             pass

    # Default action: If no specific rules match, recommend a restart.
    try:
        data_start = prompt.find('{')
        data_end = prompt.rfind('}') + 1
        diag_data = json.loads(prompt[data_start:data_end])
        job_id = diag_data.get("job_id")
        return json.dumps({
            "analysis": "The specific cause of failure could not be determined. A restart is recommended as a general first-step solution.",
            "action": "restart",
            "parameters": {"job_id": job_id}
        })
    except (json.JSONDecodeError, KeyError):
        return json.dumps({
            "analysis": "Could not parse the diagnostic data.",
            "action": "error",
            "parameters": {}
        })

def run_tool(tool_call):
    """Executes a tool call requested by the LLM."""
    tool_name = tool_call.get("name")
    params = tool_call.get("parameters")

    if tool_name == "get_nomad_job":
        job_id = params.get("job_id")
        script_path = "ansible/roles/pipecatapp/files/tools/get_nomad_job.py"
        try:
            command = ["python", script_path, job_id]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            return f"Error running tool {tool_name}: {e}\n{e.stderr if hasattr(e, 'stderr') else ''}"

    return "Error: Unknown tool requested."

def analyze_failure_with_llm(diagnostic_data):
    """
    Analyzes a job failure by making simulated calls to an LLM,
    including handling tool use.
    """
    # 1. Construct the initial prompt for the LLM.
    prompt = f"""
    A Nomad job with ID '{diagnostic_data.get("job_id")}' has failed.
    Diagnostic information:
    {json.dumps(diagnostic_data, indent=2)}

    Analyze the failure and propose a solution as a JSON object with 'action' and 'parameters'.
    Available actions: 'restart', 'increase_memory'.

    You can use tools to gather more information. To use a tool, respond with a 'tool_call' JSON object.
    Available tools:
    - `get_nomad_job`: Retrieves the full job specification.
    """

    # 2. First call to the LLM.
    # The diagnostic data is passed as context for the simulation's initial routing.
    llm_response_str = call_prima_expert_llm(prompt, context=None)
    llm_response = json.loads(llm_response_str)

    # 3. Check if the LLM responded with a tool call.
    if "tool_call" in llm_response:
        tool_call = llm_response.get("tool_call")
        print(f"--- LLM requested tool: {tool_call.get('name')} with params {tool_call.get('parameters')} ---", file=sys.stderr)

        # 4. Execute the tool.
        tool_output = run_tool(tool_call)

        # 5. Second call to the LLM, providing the tool's output as context.
        new_prompt = f"""
        Continuing the analysis for job '{diagnostic_data.get("job_id")}'.
        You requested to run the tool `{tool_call.get('name')}`. Here is its output:
        {tool_output}

        Based on this new information, provide your final analysis and healing action.
        """
        final_response_str = call_prima_expert_llm(new_prompt, context=tool_output)
        return json.loads(final_response_str)

    # 6. If no tool was needed, return the initial response.
    return llm_response

def main():
    if len(sys.argv) < 2:
        print("Usage: python reflect.py <path_to_diagnostic_file>", file=sys.stderr)
        sys.exit(1)

    diagnostic_file_path = sys.argv[1]

    try:
        with open(diagnostic_file_path, 'r') as f:
            diagnostic_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing diagnostic file: {e}", file=sys.stderr)
        sys.exit(1)

    # Get the proposed solution from the LLM analysis flow.
    solution = analyze_failure_with_llm(diagnostic_data)

    # Print the final solution for the Ansible playbook to consume.
    print(json.dumps(solution, indent=2))

if __name__ == "__main__":
    main()