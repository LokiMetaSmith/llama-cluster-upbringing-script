import httpx
import logging
from typing import Optional, Dict, Any, List
import os

class PMMMemoryClient:
    """
    A client for the remote PMM Memory Service.
    Implements the same interface as the local PMMMemory class but over HTTP.
    """
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.logger = logging.getLogger(__name__)

    def add_event(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Adds a new event to the remote memory ledger."""
        url = f"{self.base_url}/events"
        payload = {
            "kind": kind,
            "content": content,
            "meta": meta or {}
        }
        try:
            with httpx.Client() as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to add event to memory service: {e}")

    def get_events(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves events from the remote memory ledger."""
        url = f"{self.base_url}/events"
        params = {"limit": limit}
        if kind:
            params["kind"] = kind

        try:
            with httpx.Client() as client:
                resp = client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            self.logger.error(f"Failed to get events from memory service: {e}")
            return []

    def close(self):
        """No-op for HTTP client, but kept for interface compatibility."""
        pass
