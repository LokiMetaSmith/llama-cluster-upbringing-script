import requests
import json
import logging
import os
import uuid
import random
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

        self.api_url = api_url or os.getenv("OPENWORKERS_API_URL")
        self.token = token or os.getenv("OPENWORKERS_TOKEN", "")

    def _get_service_url(self, service_name: str, fallback_url: str) -> str:
        """Discovers a service via Consul."""
        try:
            consul_host = os.getenv("CONSUL_HTTP_ADDR", "localhost:8500")
            if not consul_host.startswith("http"):
                consul_host = f"http://{consul_host}"

            response = requests.get(f"{consul_host}/v1/catalog/service/{service_name}", timeout=2)
            if response.status_code == 200:
                services = response.json()
                if services:
                    service = random.choice(services)
                    address = service.get("ServiceAddress") or service.get("Address")
                    port = service.get("ServicePort")
                    return f"http://{address}:{port}"
        except Exception as e:
            logging.warning(f"Failed to resolve {service_name} from Consul: {e}")

        return fallback_url

    def _get_api_url(self) -> str:
        if self.api_url:
            return self.api_url
        return self._get_service_url("openworkers-api", "http://openworkers-api.service.consul:7000")

    def run_javascript(self, code: str) -> str:
        """Runs a string of JavaScript code in an OpenWorkers isolate.

        Args:
            code (str): The JavaScript code to execute.

        Returns:
            str: The output from the code execution or an error message.
        """
        api_base = self._get_api_url()

        if not api_base:
             return "Error: OpenWorkers API URL could not be determined."

        # Use a unique worker name to avoid collisions in a multi-agent environment
        worker_id = str(uuid.uuid4())
        worker_name = f"adhoc-runner-{worker_id}"

        try:
            # 1. Upload the script
            upload_url = f"{api_base}/api/workers/{worker_name}/script"
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/javascript"}
            response = requests.put(upload_url, data=code, headers=headers)

            if response.status_code not in [200, 201]:
                return f"Error uploading script: {response.status_code} - {response.text}"

            # 2. Execute the worker
            runner_url = self._get_service_url("openworkers-runner", "http://openworkers-runner.service.consul:8080")

            # The Host header routes the request to the specific isolate
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
                delete_url = f"{api_base}/api/workers/{worker_name}"
                requests.delete(delete_url, headers={"Authorization": f"Bearer {self.token}"})
            except Exception:
                pass
