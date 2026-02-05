import os
import requests
import logging
from typing import Optional, List, Any
from workflow.nodes.tool_nodes import ToolBase

class MKV_Tool(ToolBase):
    """
    A tool for interacting with the Minikeyvalue (MKV) distributed object store.
    """

    def __init__(self, master_url: str = "http://mkv-master.service.consul:3000"):
        super().__init__()
        self.master_url = os.getenv("MKV_MASTER_URL", master_url)
        # Handle localhost fallback if consul DNS not working/testing
        if "localhost" in self.master_url and "CONSUL_HTTP_ADDR" not in os.environ:
             # If running locally without full dns, try 127.0.0.1
             pass

    def get_tool_info(self):
        return {
            "name": "mkv_store",
            "description": "Store and retrieve large data/objects from the distributed Minikeyvalue store.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["get", "put", "delete", "list"],
                        "description": "The action to perform."
                    },
                    "key": {
                        "type": "string",
                        "description": "The key (filename) to operate on."
                    },
                    "value": {
                        "type": "string",
                        "description": "The content to store (for 'put' action)."
                    },
                    "prefix": {
                        "type": "string",
                        "description": "The prefix to list keys for (for 'list' action)."
                    }
                },
                "required": ["action"]
            }
        }

    async def execute(self, action: str, key: str = "", value: str = "", prefix: str = "") -> str:
        try:
            if action == "put":
                if not key or not value:
                    return "Error: 'key' and 'value' are required for 'put'."
                # MKV PUT is just a PUT request to master/{key}
                resp = requests.put(f"{self.master_url}/{key}", data=value)
                if resp.status_code in [200, 201]:
                    return f"Successfully stored key '{key}'."
                else:
                    return f"Failed to store key '{key}': {resp.status_code} - {resp.text}"

            elif action == "get":
                if not key:
                    return "Error: 'key' is required for 'get'."
                resp = requests.get(f"{self.master_url}/{key}")
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code == 404:
                    return "Key not found."
                else:
                    return f"Error retrieving key: {resp.status_code}"

            elif action == "delete":
                if not key:
                    return "Error: 'key' is required for 'delete'."
                resp = requests.delete(f"{self.master_url}/{key}")
                if resp.status_code == 204:
                    return f"Successfully deleted '{key}'."
                else:
                    return f"Failed to delete '{key}': {resp.status_code}"

            elif action == "list":
                url = f"{self.master_url}/{prefix}?list"
                resp = requests.get(url)
                if resp.status_code == 200:
                    try:
                        keys = resp.json()
                        return f"Keys: {', '.join(keys)}"
                    except:
                        return f"Keys: {resp.text}"
                else:
                    return f"Error listing keys: {resp.status_code}"

            else:
                return f"Unknown action: {action}"

        except Exception as e:
            logging.error(f"MKV Tool Error: {e}")
            return f"Error executing MKV operation: {str(e)}"
