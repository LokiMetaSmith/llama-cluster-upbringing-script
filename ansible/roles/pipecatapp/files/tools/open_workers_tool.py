import requests
import json
import logging
import os
import uuid
from typing import Optional

class OpenWorkersTool:
    """A tool for executing JavaScript code in the OpenWorkers sandbox.

    This class interfaces with the OpenWorkers API to run untrusted
    JavaScript/TypeScript code in secure V8 isolates.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
        api_url (str): The URL of the OpenWorkers API.
        token (str): The authentication token for the API.
    """
    def __init__(self, api_url: Optional[str] = None, token: Optional[str] = None):
        """Initializes the OpenWorkersTool."""
        self.description = "Execute JavaScript code in a secure V8 isolate."
        self.name = "openworkers"

        # Default to the internal Consul service address if not provided
        self.api_url = api_url or os.getenv("OPENWORKERS_API_URL", "http://openworkers-api.service.consul:7000")
        self.token = token or os.getenv("OPENWORKERS_TOKEN", "")

    def run_javascript(self, code: str) -> str:
        """Runs a string of JavaScript code in an OpenWorkers isolate.

        Args:
            code (str): The JavaScript code to execute.

        Returns:
            str: The output from the code execution or an error message.
        """
        if not self.api_url:
            return "Error: OpenWorkers API URL is not configured."

        # Use a unique worker name to avoid collisions in a multi-agent environment
        worker_id = str(uuid.uuid4())
        worker_name = f"adhoc-runner-{worker_id}"

        try:
            # 1. Upload the script
            upload_url = f"{self.api_url}/api/workers/{worker_name}/script"
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/javascript"}
            response = requests.put(upload_url, data=code, headers=headers)

            if response.status_code not in [200, 201]:
                return f"Error uploading script: {response.status_code} - {response.text}"

            # 2. Execute the worker (via its subdomain or route)
            runner_url = os.getenv("OPENWORKERS_RUNNER_URL", "http://openworkers-runner.service.consul:8080")
            exec_headers = {"Host": f"{worker_name}.openworkers.local"}

            exec_response = requests.get(runner_url, headers=exec_headers, timeout=5)
            return exec_response.text

        except requests.exceptions.RequestException as e:
            return f"Network error communicating with OpenWorkers: {e}"
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            # 3. Clean up the worker
            try:
                delete_url = f"{self.api_url}/api/workers/{worker_name}"
                requests.delete(delete_url, headers={"Authorization": f"Bearer {self.token}"})
            except Exception:
                # Best effort cleanup, log silently in this tool context
                pass
