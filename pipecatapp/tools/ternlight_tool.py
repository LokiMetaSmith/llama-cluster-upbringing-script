import os
import json
import logging
import requests
import subprocess
from typing import Optional, List, Union, Dict, Any

class TernlightTool:
    """
    TernlightTool: A lightweight embedding and similarity search tool.
    Powered by Ternlight (7MB ternary model).

    It can run as a remote microservice (via Consul) or as a local Node.js subprocess.
    """
    def __init__(self, base_url: Optional[str] = None):
        self.name = "ternlight"
        self.description = (
            "Lightweight semantic search and text embedding tool. "
            "Extremely fast and low-resource. "
            "Use it for quick document lookup or finding similar strings."
        )
        # Default to the Consul Service Mesh address
        self.base_url = (base_url or os.getenv("TERNLIGHT_SERVICE_URL", "http://ternlight-service.service.consul:8000")).rstrip('/')

        # Paths for local fallback
        self.local_js_path = os.path.join(os.path.dirname(__file__), "../services/ternlight/ternlight_server.js")
        self._is_service_available = None

    def _check_service(self) -> bool:
        """Checks if the remote microservice is healthy."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=1)
            return response.status_code == 200
        except Exception:
            return False

    def embed(self, text: str) -> Union[List[float], str]:
        """Generates an embedding for the given text."""
        if self._is_service_available is None:
            self._is_service_available = self._check_service()

        if self._is_service_available:
            try:
                response = requests.post(f"{self.base_url}/embed", json={"text": text}, timeout=5)
                response.raise_for_status()
                return response.json().get("embedding")
            except Exception as e:
                logging.error(f"Ternlight remote embed failed: {e}")
                # Fall through to local fallback

        return self._local_execute("embed", {"text": text})

    def similar(self, query: str, documents: List[Union[str, Dict[str, Any]]], top_k: int = 5) -> Union[List[Any], str]:
        """Finds documents similar to the query."""
        if self._is_service_available is None:
            self._is_service_available = self._check_service()

        if self._is_service_available:
            try:
                response = requests.post(
                    f"{self.base_url}/similar",
                    json={"query": query, "documents": documents, "topK": top_k},
                    timeout=10
                )
                response.raise_for_status()
                return response.json().get("results")
            except Exception as e:
                logging.error(f"Ternlight remote similar failed: {e}")
                # Fall through to local fallback

        return self._local_execute("similar", {"query": query, "documents": documents, "topK": top_k})

    def _local_execute(self, action: str, data: Dict[str, Any]) -> Any:
        """Fallback to local node execution if the microservice is down."""
        # This requires node and @ternlight/base to be installed on the worker node.
        # We use a simple CLI wrapper or call the JS file with a special flag if we had one.
        # For simplicity in this implementation, we will try to call a small JS snippet.

        js_code = f"""
const {{ embed, similar }} = require('@ternlight/base');
const data = {json.dumps(data)};
(async () => {{
    try {{
        if ("{action}" === "embed") {{
            const res = await embed(data.text);
            console.log(JSON.stringify({{result: res}}));
        }} else if ("{action}" === "similar") {{
            const res = await similar(data.query, data.documents, {{ topK: data.topK || 5 }});
            console.log(JSON.stringify({{result: res}}));
        }}
    }} catch (e) {{
        console.error(e);
        process.exit(1);
    }}
}})();
"""
        try:
            result = subprocess.run(
                ["node", "-e", js_code],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout).get("result")
        except Exception as e:
            logging.error(f"Ternlight local fallback failed: {e}")
            return f"Error: Ternlight tool unavailable (remote and local failed). {e}"

    def execute(self, arguments: Dict[str, Any] = None) -> str:
        """Standard tool execution entry point."""
        if not arguments:
            return "Error: Ternlight tool requires arguments."

        action = arguments.get("action", "similar")
        if action == "embed":
            text = arguments.get("text")
            if not text:
                return "Error: 'text' is required for embed action."
            res = self.embed(text)
            return json.dumps(res) if isinstance(res, list) else res

        elif action == "similar":
            query = arguments.get("query")
            documents = arguments.get("documents")
            if not query or not documents:
                return "Error: 'query' and 'documents' are required for similar action."
            top_k = arguments.get("top_k", 5)
            res = self.similar(query, documents, top_k)
            return json.dumps(res) if isinstance(res, list) else res

        else:
            return f"Error: Unknown action '{action}' for Ternlight tool."
