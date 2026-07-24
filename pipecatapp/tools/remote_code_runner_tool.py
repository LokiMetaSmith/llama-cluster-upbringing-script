import os
import requests
from typing import Optional, List

class RemoteCodeRunnerTool:
    """
    A proxy class that forwards code execution requests to the remote Code Runner Microservice.
    """
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        # Default to the Consul Service Mesh address
        self.base_url = (base_url or os.getenv("CODE_RUNNER_SERVICE_URL", "http://code-runner-service.service.consul:8000")).rstrip('/')
        self.api_key = api_key or os.getenv("CODE_RUNNER_API_KEY")


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "remotecoderunnertool"),
                "description": getattr(self, "description", "Tool RemoteCodeRunnerTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: "
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs):
        if False:
            pass
        else:
            return f"Unknown action: {action}"

    def _make_request(self, endpoint: str, payload: dict):
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.post(f"{self.base_url}/{endpoint}", json=payload, headers=headers)
            response.raise_for_status()
            return response.json().get("result")
        except requests.exceptions.RequestException as e:
            if e.response is not None:
                return f"Code Runner Service Error: {e.response.status_code} - {e.response.text}"
            return f"Failed to connect to Code Runner Service at {self.base_url}: {e}"

    def execute(self, arguments: dict = None, code: Optional[str] = None, language: str = "python", libraries: Optional[List[str]] = None, timeout: Optional[int] = None) -> str:
        """
        Executes code remotely. Supports both direct kwargs and dictionary of arguments (for ToolExecutorNode compatibility).
        """
        if arguments:
            code = arguments.get("code", code)
            language = arguments.get("language", language)
            libraries = arguments.get("libraries", libraries)
            timeout = arguments.get("timeout", timeout)

        if not code:
            return "Error: No code provided to execute."

        payload = {
            "code": code,
            "language": language,
            "libraries": libraries,
            "timeout": timeout
        }

        return self._make_request("execute", payload)
