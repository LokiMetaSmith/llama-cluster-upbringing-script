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

    def add_event_sync(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Adds a new event to the remote memory ledger synchronously."""
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

    async def add_event(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Adds a new event to the remote memory ledger asynchronously."""
        url = f"{self.base_url}/events"
        payload = {
            "kind": kind,
            "content": content,
            "meta": meta or {}
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to add event to memory service: {e}")

    def get_events_sync(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves events from the remote memory ledger synchronously."""
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

    async def get_events(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves events from the remote memory ledger asynchronously."""
        url = f"{self.base_url}/events"
        params = {"limit": limit}
        if kind:
            params["kind"] = kind

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            self.logger.error(f"Failed to get events from memory service: {e}")
            return []

    # -------------------------------------------------------------------------
    # Gas Town Work Ledger Client Methods
    # -------------------------------------------------------------------------

    async def create_work_item(self, title: str, created_by: str, assignee_id: str = None, parent_id: str = None, meta: Dict = None) -> str:
        url = f"{self.base_url}/work_items"
        payload = {
            "title": title,
            "created_by": created_by,
            "assignee_id": assignee_id,
            "parent_id": parent_id,
            "meta": meta or {}
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                return resp.json()["work_item_id"]
        except Exception as e:
            self.logger.error(f"Failed to create work item: {e}")
            return None

    async def update_work_item(self, item_id: str, status: str = None, assignee_id: str = None, validation_results: Dict = None, meta_update: Dict = None) -> bool:
        url = f"{self.base_url}/work_items/{item_id}"
        payload = {}
        if status: payload["status"] = status
        if assignee_id: payload["assignee_id"] = assignee_id
        if validation_results: payload["validation_results"] = validation_results
        if meta_update: payload["meta_update"] = meta_update

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.patch(url, json=payload)
                resp.raise_for_status()
                return True
        except Exception as e:
            self.logger.error(f"Failed to update work item {item_id}: {e}")
            return False

    async def get_work_item(self, item_id: str) -> Optional[Dict]:
        url = f"{self.base_url}/work_items/{item_id}"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                if resp.status_code == 404:
                    return None
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            self.logger.error(f"Failed to get work item {item_id}: {e}")
            return None

    async def list_work_items(self, status: str = None, assignee_id: str = None, limit: int = 50) -> List[Dict]:
        url = f"{self.base_url}/work_items"
        params = {"limit": limit}
        if status: params["status"] = status
        if assignee_id: params["assignee_id"] = assignee_id

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            self.logger.error(f"Failed to list work items: {e}")
            return []

    async def get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """Retrieves performance statistics for a given agent."""
        url = f"{self.base_url}/agents/{agent_id}/stats"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            self.logger.error(f"Failed to get stats for agent {agent_id}: {e}")
            return {}

    def close(self):
        """No-op for HTTP client, but kept for interface compatibility."""
        pass
