import os
import requests
import json
from typing import Optional

class RemoteToolProxy:
    """
    A proxy class that forwards tool method calls to a remote Tool Server.
    """
    def __init__(self, tool_name: str, base_url: str, api_key: Optional[str] = None):
        self.tool_name = tool_name
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv("TOOL_SERVER_API_KEY")

    def __getattr__(self, name):
        """
        Catches any method call and forwards it to the remote server.
        """
        def method(*args, **kwargs):
            # The Tool Server expects arguments to be passed as keyword arguments in the 'args' dict.
            # We strictly enforce kwargs for remote tools to match the schema.
            if args:
                 raise ValueError(f"RemoteToolProxy for {self.tool_name} only supports keyword arguments.")

            payload = {
                "tool": self.tool_name,
                "method": name,
                "args": kwargs
            }

            headers = {
                "Content-Type": "application/json"
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            try:
                response = requests.post(f"{self.base_url}/run_tool/", json=payload, headers=headers)
                response.raise_for_status()
                return response.json().get("result")
            except requests.exceptions.RequestException as e:
                # Capture and re-raise or handle gracefully
                raise RuntimeError(f"Remote tool execution failed for {self.tool_name}.{name}: {e}")

        return method
