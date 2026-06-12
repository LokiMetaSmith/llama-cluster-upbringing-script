import requests
import json
import logging
import os
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class HelixClient:
    def __init__(self, url=None):
        self.url = url or os.getenv("HELIX_URL", "http://localhost:6969/v1/query")

    def _post(self, payload: dict) -> dict:
        try:
            resp = requests.post(self.url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"HelixDB Request Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response text: {e.response.text}")
            return {}

    def execute_ast(self, queries: List[dict], parameters: dict = None, parameter_types: dict = None, returns: List[str] = None, request_type: str = "write") -> dict:
        payload = {
            "request_type": request_type,
            "query": {
                "queries": queries,
                "returns": returns or []
            }
        }
        if parameters:
            payload["parameters"] = parameters
        if parameter_types:
            payload["parameter_types"] = parameter_types

        return self._post(payload)
