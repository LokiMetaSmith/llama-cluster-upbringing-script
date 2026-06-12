import os
import requests
import json
from typing import Optional

class RemoteRAGTool:
    """
    A proxy class that forwards RAG method calls to the remote RAG Microservice.
    """
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        # Default to the Consul Service Mesh address
        self.base_url = (base_url or os.getenv("RAG_SERVICE_URL", "http://rag-service.service.consul:8000")).rstrip('/')
        self.api_key = api_key or os.getenv("RAG_SERVICE_API_KEY")

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
                return f"RAG Service Error: {e.response.status_code} - {e.response.text}"
            return f"Failed to connect to RAG Service at {self.base_url}: {e}"

    def add_document(self, filepath: str) -> str:
        return self._make_request("add_document", {"filepath": filepath})

    def search(self, query: str, k: int = 5) -> str:
        return self._make_request("search", {"query": query, "k": k})

    def scan_directory(self, directory: str) -> str:
        return self._make_request("scan_directory", {"directory": directory})

    # The executor expects an `execute` method for generic tool routing
    def execute(self, arguments: dict = None) -> str:
        """
        Executes the RAG tool remotely.
        Expects a dictionary with 'action' (search, add_document, scan_directory)
        and relevant parameters.
        """
        if not arguments:
            return "Error: RAG tool requires arguments."

        action = arguments.get("action")
        if not action:
            # Default to search if just given a query
            if "query" in arguments:
                return self.search(arguments["query"], arguments.get("k", 5))
            return "Error: RAG tool requires an 'action' (search, add_document, scan_directory) or 'query'."

        if action == "search":
            if "query" not in arguments:
                return "Error: 'query' argument is required for search action."
            return self.search(arguments["query"], arguments.get("k", 5))
        elif action == "add_document":
            if "filepath" not in arguments:
                return "Error: 'filepath' argument is required for add_document action."
            return self.add_document(arguments["filepath"])
        elif action == "scan_directory":
            if "directory" not in arguments:
                return "Error: 'directory' argument is required for scan_directory action."
            return self.scan_directory(arguments["directory"])
        else:
            return f"Error: Unknown action '{action}' for RAG tool."
