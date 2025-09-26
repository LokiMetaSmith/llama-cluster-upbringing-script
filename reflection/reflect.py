import json
import sys

def analyze_failure_with_llm(diagnostic_data):
    """
    Simulates a call to an LLM for failure analysis.
    In a real implementation, this would involve constructing a detailed prompt
    and making an API call to a service like a prima-expert.
    """
    # For now, use a simple, rule-based approach as a placeholder.
    # This can be expanded with more sophisticated rules.
    logs = diagnostic_data.get("logs", {})
    stderr = logs.get("stderr", "").lower()

    if "out of memory" in stderr:
        return {
            "analysis": "The job failed due to an out-of-memory error.",
            "action": "increase_memory",
            "parameters": {"job_id": diagnostic_data.get("job_id"), "memory_mb": 512}
        }

    if "exit code 1" in diagnostic_data.get("status", "").lower():
        return {
            "analysis": "The job exited with a non-zero exit code, suggesting a runtime error.",
            "action": "restart",
            "parameters": {"job_id": diagnostic_data.get("job_id")}
        }

    # Default action if no specific cause is found
    return {
        "analysis": "The cause of failure could not be determined from the logs. A restart is recommended as a first step.",
        "action": "restart",
        "parameters": {"job_id": diagnostic_data.get("job_id")}
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python reflect.py <path_to_diagnostic_file>")
        sys.exit(1)

    diagnostic_file_path = sys.argv[1]

    try:
        with open(diagnostic_file_path, 'r') as f:
            diagnostic_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing diagnostic file: {e}")
        sys.exit(1)

    # Get the proposed solution from the simulated LLM
    solution = analyze_failure_with_llm(diagnostic_data)

    # Print the solution as a JSON object for the next playbook to consume
    print(json.dumps(solution, indent=2))

if __name__ == "__main__":
    main()