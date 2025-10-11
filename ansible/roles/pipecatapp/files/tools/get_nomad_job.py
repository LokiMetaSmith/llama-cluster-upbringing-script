import os
import requests
import sys
import json

def get_nomad_job_definition(job_id):
    """
    Retrieves the JSON definition of a Nomad job.
    """
    nomad_addr = os.environ.get("NOMAD_ADDR", "http://localhost:4646")
    url = f"{nomad_addr}/v1/job/{job_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job definition for '{job_id}': {e}", file=sys.stderr)
        return None

def main():
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