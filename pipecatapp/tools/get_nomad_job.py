import os
import requests
import sys
import json
import re

class GetNomadJobTool:
    """A tool to retrieve a Nomad job definition by its job ID."""

    def __init__(self):
        self.name = "get_nomad_job"
        self.description = "Retrieves the JSON definition of a Nomad job on the cluster by its exact job ID."
        self.input_schema = {
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "string",
                    "description": "The exact job ID of the Nomad job to retrieve."
                }
            },
            "required": ["job_id"]
        }

    def run(self, job_id: str, **kwargs) -> str:
        """Retrieves and returns the job definition as a JSON string."""
        job_def = get_nomad_job_definition(job_id)
        if job_def:
            return json.dumps(job_def, indent=2)
        else:
            return f"Error: Could not retrieve Nomad job definition for ID: '{job_id}'."


def get_nomad_job_definition(job_id):
    """
    Retrieves the JSON definition of a Nomad job.
    """
    # Security Fix: Sentinel - Validate job_id to prevent path traversal
    if not re.match(r"^[a-zA-Z0-9_\-\.]+$", job_id):
        print(f"Error: Invalid job_id '{job_id}'. Only alphanumeric characters, dashes, underscores, and dots are allowed.", file=sys.stderr)
        return None

    nomad_addr = os.environ.get("NOMAD_ADDR", f"http://{os.getenv("CLUSTER_IP", "127.0.0.1")}:4646")
    url = f"{nomad_addr}/v1/job/{job_id}"

    try:
        # Security Fix: Sentinel - Add timeout to prevent DoS
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job definition for '{job_id}': {e}", file=sys.stderr)
        return None

def main():
    """The main entry point for the script.

    Parses command-line arguments to get the job ID, fetches the job
    definition, and prints it to standard output.
    """
    if len(sys.argv) < 2:
        print("Usage: python get_nomad_job.py <job_id>", file=sys.stderr)
        sys.exit(1)

    job_id = sys.argv[1]
    job_definition = get_nomad_job_definition(job_id)

    if job_definition:
        print(json.dumps(job_definition, indent=2))
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
