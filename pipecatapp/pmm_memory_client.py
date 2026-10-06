import asyncio
import httpx
import logging
import os
import time
from typing import Optional, Dict, Any, List

class PMMMemoryClient:
    """
    A client for the remote PMM Memory Service with automatic circuit breaker
    and graceful fallback to local SQLite PMMMemory store.
    Implements the same interface as the local PMMMemory class but over HTTP.
    """
    def __init__(
        self,
        base_url: Optional[str] = None,
        fallback_to_local: bool = True,
        db_path: Optional[str] = None,
        cooldown_seconds: float = 60.0
    ):
        if base_url is None:
            base_url = f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8000"
        self.base_url = base_url.rstrip("/")
        self.fallback_to_local = fallback_to_local
        self.db_path = db_path or os.getenv("PMM_DB_PATH", "~/.config/pipecat/pypicat_memory.db")
        self.logger = logging.getLogger(__name__)
        self._local_memory = None
        self._is_available = True
        self._last_failure_time = 0.0
        self._cooldown_seconds = cooldown_seconds
        self._timeout = httpx.Timeout(connect=2.0, read=5.0, write=5.0, pool=2.0)

    def _get_local_memory(self):
        """Lazily instantiates the fallback local PMMMemory to respect memory budget."""
        if not self.fallback_to_local:
            return None
        if self._local_memory is None:
            try:
                from pipecatapp.pmm_memory import PMMMemory
                self._local_memory = PMMMemory(db_path=self.db_path)
            except Exception as e:
                self.logger.error(f"Failed to initialize fallback local PMMMemory: {e}")
        return self._local_memory

    def _should_try_remote(self) -> bool:
        """Determines if a remote HTTP call should be attempted based on circuit breaker state."""
        if self._is_available:
            return True
        if time.time() - self._last_failure_time < self._cooldown_seconds:
            return False
        return True

    def _handle_remote_success(self):
        """Handles successful remote communication, clearing the circuit breaker."""
        if not self._is_available:
            self.logger.info(f"Remote memory service at {self.base_url} is reachable again.")
            self._is_available = True

    def _handle_remote_failure(self, error: Exception, operation: str):
        """Trips the circuit breaker and logs gracefully without terminal flooding."""
        now = time.time()
        was_available = self._is_available
        self._is_available = False
        self._last_failure_time = now

        if was_available:
            if self.fallback_to_local:
                self.logger.warning(
                    f"Remote memory service at {self.base_url} is unreachable during {operation}: {error}. "
                    f"Falling back to local SQLite memory ({self.db_path}) with {self._cooldown_seconds:.0f}s cooldown."
                )
            else:
                self.logger.warning(
                    f"Remote memory service at {self.base_url} is unreachable during {operation}: {error}. "
                    f"Entering {self._cooldown_seconds:.0f}s cooldown."
                )
        else:
            self.logger.debug(f"Remote memory service still unreachable during {operation}: {error}")

    def add_event_sync(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None, provenance: Optional[Dict[str, Any]] = None) -> None:
        """Adds a new event to the remote memory ledger synchronously (with local fallback)."""
        if self._should_try_remote():
            url = f"{self.base_url}/events"
            payload = {
                "kind": kind,
                "content": content,
                "meta": meta or {}
            }
            if provenance:
                payload["provenance"] = provenance
            try:
                with httpx.Client(timeout=self._timeout) as client:
                    resp = client.post(url, json=payload)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return
            except Exception as e:
                self._handle_remote_failure(e, "add_event_sync")

        local = self._get_local_memory()
        if local:
            local.add_event_sync(kind, content, meta=meta, provenance=provenance)

    async def add_event(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None, provenance: Optional[Dict[str, Any]] = None) -> None:
        """Adds a new event to the remote memory ledger asynchronously (with local fallback)."""
        if self._should_try_remote():
            url = f"{self.base_url}/events"
            payload = {
                "kind": kind,
                "content": content,
                "meta": meta or {}
            }
            if provenance:
                payload["provenance"] = provenance
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.post(url, json=payload)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return
            except Exception as e:
                self._handle_remote_failure(e, "add_event")

        local = self._get_local_memory()
        if local:
            await local.add_event(kind, content, meta=meta, provenance=provenance)

    def get_events_sync(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves events from the remote memory ledger synchronously (with local fallback)."""
        if self._should_try_remote():
            url = f"{self.base_url}/events"
            params = {"limit": limit}
            if kind:
                params["kind"] = kind
            try:
                with httpx.Client(timeout=self._timeout) as client:
                    resp = client.get(url, params=params)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()
            except Exception as e:
                self._handle_remote_failure(e, "get_events_sync")

        local = self._get_local_memory()
        if local:
            return local.get_events_sync(kind=kind, limit=limit)
        return []

    async def get_events(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves events from the remote memory ledger asynchronously (with local fallback)."""
        if self._should_try_remote():
            url = f"{self.base_url}/events"
            params = {"limit": limit}
            if kind:
                params["kind"] = kind
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url, params=params)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()
            except Exception as e:
                self._handle_remote_failure(e, "get_events")

        local = self._get_local_memory()
        if local:
            return await local.get_events(kind=kind, limit=limit)
        return []

    # -------------------------------------------------------------------------
    # Gas Town Work Ledger Client Methods
    # -------------------------------------------------------------------------

    async def create_work_item(self, title: str, created_by: str, assignee_id: str | None = None, parent_id: str | None = None, meta: Dict = None) -> Optional[str]:
        if self._should_try_remote():
            url = f"{self.base_url}/work_items"
            payload = {
                "title": title,
                "created_by": created_by,
                "assignee_id": assignee_id,
                "parent_id": parent_id,
                "meta": meta or {}
            }
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.post(url, json=payload)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()["work_item_id"]
            except Exception as e:
                self._handle_remote_failure(e, "create_work_item")

        local = self._get_local_memory()
        if local:
            return await local.create_work_item(title, created_by, assignee_id=assignee_id, parent_id=parent_id, meta=meta)
        return None

    async def update_work_item(self, item_id: str, status: str | None = None, assignee_id: str | None = None, validation_results: Dict = None, meta_update: Dict = None) -> bool:
        if self._should_try_remote():
            url = f"{self.base_url}/work_items/{item_id}"
            payload = {}
            if status: payload["status"] = status
            if assignee_id: payload["assignee_id"] = assignee_id
            if validation_results: payload["validation_results"] = validation_results
            if meta_update: payload["meta_update"] = meta_update

            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.patch(url, json=payload)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return True
            except Exception as e:
                self._handle_remote_failure(e, f"update_work_item {item_id}")

        local = self._get_local_memory()
        if local:
            return await local.update_work_item(item_id, status=status, assignee_id=assignee_id, validation_results=validation_results, meta_update=meta_update)
        return False

    async def get_work_item(self, item_id: str) -> Optional[Dict]:
        if self._should_try_remote():
            url = f"{self.base_url}/work_items/{item_id}"
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url)
                    if resp.status_code == 404:
                        return None
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()
            except Exception as e:
                self._handle_remote_failure(e, f"get_work_item {item_id}")

        local = self._get_local_memory()
        if local:
            return await local.get_work_item(item_id)
        return None

    async def list_work_items(self, status: str | None = None, assignee_id: str | None = None, limit: int = 50) -> List[Dict]:
        if self._should_try_remote():
            url = f"{self.base_url}/work_items"
            params = {"limit": limit}
            if status: params["status"] = status
            if assignee_id: params["assignee_id"] = assignee_id

            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url, params=params)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()
            except Exception as e:
                self._handle_remote_failure(e, "list_work_items")

        local = self._get_local_memory()
        if local:
            return await local.list_work_items(status=status, assignee_id=assignee_id, limit=limit)
        return []

    async def get_agent_stats(self, agent_id: str) -> Dict[str, Any]:
        """Retrieves performance statistics for a given agent."""
        if self._should_try_remote():
            url = f"{self.base_url}/agents/{agent_id}/stats"
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()
            except Exception as e:
                self._handle_remote_failure(e, f"get_agent_stats {agent_id}")

        local = self._get_local_memory()
        if local:
            return await local.get_agent_stats(agent_id)
        return {}

    # -------------------------------------------------------------------------
    # DLQ Client Methods
    # -------------------------------------------------------------------------

    async def enqueue_dlq_item(self, event_type: str, payload: Dict[str, Any], error_reason: str, retry_count: int = 0) -> Optional[str]:
        if self._should_try_remote():
            url = f"{self.base_url}/dlq"
            payload_data = {
                "event_type": event_type,
                "payload": payload,
                "error_reason": error_reason,
                "retry_count": retry_count
            }
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.post(url, json=payload_data)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()["dlq_item_id"]
            except Exception as e:
                self._handle_remote_failure(e, "enqueue_dlq_item")

        local = self._get_local_memory()
        if local:
            return await local.enqueue_dlq_item(event_type, payload, error_reason, retry_count)
        return None

    async def claim_dlq_item(self, worker_id: str, supported_types: List[str] = None) -> Optional[Dict]:
        if self._should_try_remote():
            url = f"{self.base_url}/dlq/claim"
            payload = {
                "worker_id": worker_id,
                "supported_types": supported_types
            }
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.post(url, json=payload)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()
            except Exception as e:
                self._handle_remote_failure(e, "claim_dlq_item")

        local = self._get_local_memory()
        if local:
            return await local.claim_dlq_item(worker_id, supported_types)
        return None

    async def update_dlq_item(self, item_id: str, status: str, result: str | None = None, retry_after: float | None = None, increment_retry: bool = False) -> bool:
        if self._should_try_remote():
            url = f"{self.base_url}/dlq/{item_id}"
            payload = {
                "status": status,
                "result": result,
                "retry_after": retry_after,
                "increment_retry": increment_retry
            }
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.patch(url, json=payload)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return True
            except Exception as e:
                self._handle_remote_failure(e, f"update_dlq_item {item_id}")

        local = self._get_local_memory()
        if local:
            return await local.update_dlq_item(item_id, status, result=result, retry_after=retry_after, increment_retry=increment_retry)
        return False

    def get_work_items_since_sync(self, since: float = 0.0) -> List[Dict]:
        if self._should_try_remote():
            url = f"{self.base_url}/work_items/sync"
            try:
                with httpx.Client(timeout=self._timeout) as client:
                    resp = client.get(url, params={"since": since})
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()
            except Exception as e:
                self._handle_remote_failure(e, f"get_work_items_since_sync {since}")

        local = self._get_local_memory()
        if local:
            return local.get_work_items_since_sync(since)
        return []

    async def get_work_items_since(self, since: float = 0.0) -> List[Dict]:
        if self._should_try_remote():
            url = f"{self.base_url}/work_items/sync"
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url, params={"since": since})
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return resp.json()
            except Exception as e:
                self._handle_remote_failure(e, f"get_work_items_since {since}")

        local = self._get_local_memory()
        if local:
            return await local.get_work_items_since(since)
        return []

    def push_work_items_sync(self, items: List[Dict]) -> bool:
        if self._should_try_remote():
            url = f"{self.base_url}/work_items/sync"
            try:
                with httpx.Client(timeout=self._timeout) as client:
                    resp = client.post(url, json=items)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return True
            except Exception as e:
                self._handle_remote_failure(e, "push_work_items_sync")

        local = self._get_local_memory()
        if local:
            local.sync_work_items_sync(items)
            return True
        return False

    async def push_work_items(self, items: List[Dict]) -> bool:
        if self._should_try_remote():
            url = f"{self.base_url}/work_items/sync"
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.post(url, json=items)
                    resp.raise_for_status()
                    self._handle_remote_success()
                    return True
            except Exception as e:
                self._handle_remote_failure(e, "push_work_items")

        local = self._get_local_memory()
        if local:
            await local.sync_work_items(items)
            return True
        return False

    def close(self):
        """Closes any underlying local database connections."""
        if self._local_memory is not None:
            try:
                self._local_memory.close()
            except Exception:
                pass
            self._local_memory = None
