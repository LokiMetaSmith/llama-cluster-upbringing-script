import os
import asyncio
import hashlib
import bisect
import yaml
import httpx
import logging
from typing import Dict, List, Optional, Any
from pipecatapp.pmm_memory import PMMMemory

class HashRing:
    """Consistent Hashing implementation with Virtual Nodes."""
    def __init__(self, shards: List[str] = None, replica_count: int = 128):
        self.replica_count = replica_count
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []
        if shards:
            for s in shards:
                self.add_shard(s)

    def _hash(self, key: str) -> int:
        """Returns the MD5 integer hash of a key."""
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_shard(self, shard: str):
        """Adds virtual nodes for a shard to the hash ring."""
        for i in range(self.replica_count):
            key = self._hash(f"{shard}:{i}")
            self.ring[key] = shard
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_shard(self, shard: str):
        """Removes all virtual nodes of a shard from the hash ring."""
        for i in range(self.replica_count):
            key = self._hash(f"{shard}:{i}")
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)

    def get_shard(self, key: str) -> Optional[str]:
        """Looks up the target shard for the given key in the ring."""
        if not self.ring:
            return None
        val_hash = self._hash(key)
        idx = bisect.bisect_right(self.sorted_keys, val_hash)
        if idx == len(self.sorted_keys):
            idx = 0
        return self.ring[self.sorted_keys[idx]]


class ShardedPMMMemoryRouter:
    """A thread-safe sharding router that routes PMMMemory calls locally or over HTTP."""
    def __init__(self, config: Any, local_node_id: Optional[str] = None):
        """
        Initializes the ShardedPMMMemoryRouter.

        Args:
            config: Can be a file path (str) or a dictionary representing the data topology.
            local_node_id: Node ID of this local instance. Defaults to NODE_ID env var or 'node_0'.
        """
        self.logger = logging.getLogger(__name__)

        if isinstance(config, str):
            with open(config, "r") as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config or {}

        self.local_node_id = local_node_id or os.environ.get("NODE_ID", "node_0")

        # Load topology/sharding configuration parameters
        sharding_section = self.config.get("sharding", {})
        self.replica_count = sharding_section.get("replica_count", 128)
        self.coordinator_node_id = sharding_section.get("coordinator_node", "node_0")
        self.nodes_config = sharding_section.get("nodes", {})
        self.api_key = sharding_section.get("api_key") or os.environ.get("PIPECAT_API_KEY", "")
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

        # Initialize consistent hashing ring
        self.hash_ring = HashRing(shards=list(self.nodes_config.keys()), replica_count=self.replica_count)

        # Pre-instantiate memory instances for any locally configured databases
        self.local_memories: Dict[str, PMMMemory] = {}
        for node_id, info in self.nodes_config.items():
            db_path = info.get("sqlite_path") or info.get("sqlite_url", "").replace("sqlite:///", "")
            if db_path:
                self.local_memories[node_id] = PMMMemory(db_path=db_path)

        # Clients for HTTP routing
        self.async_client = httpx.AsyncClient(timeout=5.0)
        self.sync_client = httpx.Client(timeout=5.0)

    def get_shard_for_session(self, session_id: str) -> str:
        """Determines the target shard node for a session key."""
        return self.hash_ring.get_shard(session_id)

    def _get_node_api_url(self, node_id: str) -> str:
        """Helper to get the API base URL of a specific node."""
        info = self.nodes_config.get(node_id, {})
        url = info.get("api_url", "")
        return url.rstrip("/")

    # -------------------------------------------------------------------------
    # Conversational Events (Sharded by Session ID)
    # -------------------------------------------------------------------------

    def add_event_sync(self, session_id: str, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> str:
        """Synchronously routes a new conversational event to its session-based shard."""
        target_node = self.get_shard_for_session(session_id)
        meta = meta or {}
        if "session_id" not in meta:
            meta["session_id"] = session_id

        if target_node in self.local_memories:
            self.local_memories[target_node].add_event_sync(kind, content, meta)
            return target_node
        else:
            api_url = self._get_node_api_url(target_node)
            try:
                resp = self.sync_client.post(
                    f"{api_url}/api/memory/sharded/events",
                    json={"session_id": session_id, "kind": kind, "content": content, "meta": meta},
                    headers=self.headers
                )
                resp.raise_for_status()
                return target_node
            except Exception as e:
                self.logger.error(f"Failed to route add_event_sync to {target_node}: {e}")
                # Fallback to local default node if remote fails
                default_node = self.coordinator_node_id
                if default_node in self.local_memories:
                    self.local_memories[default_node].add_event_sync(kind, content, meta)
                    return default_node
                raise e

    async def add_event(self, session_id: str, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> str:
        """Asynchronously routes a new conversational event to its session-based shard."""
        target_node = self.get_shard_for_session(session_id)
        meta = meta or {}
        if "session_id" not in meta:
            meta["session_id"] = session_id

        if target_node in self.local_memories:
            await self.local_memories[target_node].add_event(kind, content, meta)
            return target_node
        else:
            api_url = self._get_node_api_url(target_node)
            try:
                resp = await self.async_client.post(
                    f"{api_url}/api/memory/sharded/events",
                    json={"session_id": session_id, "kind": kind, "content": content, "meta": meta},
                    headers=self.headers
                )
                resp.raise_for_status()
                return target_node
            except Exception as e:
                self.logger.error(f"Failed to route add_event to {target_node}: {e}")
                default_node = self.coordinator_node_id
                if default_node in self.local_memories:
                    await self.local_memories[default_node].add_event(kind, content, meta)
                    return default_node
                raise e

    def get_events_sync(self, session_id: str, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Synchronously retrieves and filters events from the session's target shard."""
        target_node = self.get_shard_for_session(session_id)
        if target_node in self.local_memories:
            events = self.local_memories[target_node].get_events_sync(kind=kind, limit=limit)
            return [e for e in events if e.get("meta", {}).get("session_id") == session_id]
        else:
            api_url = self._get_node_api_url(target_node)
            try:
                params = {"session_id": session_id, "limit": limit}
                if kind:
                    params["kind"] = kind
                resp = self.sync_client.get(
                    f"{api_url}/api/memory/sharded/events",
                    params=params,
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.logger.error(f"Failed to route get_events_sync to {target_node}: {e}")
                return []

    async def get_events(self, session_id: str, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Asynchronously retrieves and filters events from the session's target shard."""
        target_node = self.get_shard_for_session(session_id)
        if target_node in self.local_memories:
            events = await self.local_memories[target_node].get_events(kind=kind, limit=limit)
            return [e for e in events if e.get("meta", {}).get("session_id") == session_id]
        else:
            api_url = self._get_node_api_url(target_node)
            try:
                params = {"session_id": session_id, "limit": limit}
                if kind:
                    params["kind"] = kind
                resp = await self.async_client.get(
                    f"{api_url}/api/memory/sharded/events",
                    params=params,
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.logger.error(f"Failed to route get_events to {target_node}: {e}")
                return []

    # -------------------------------------------------------------------------
    # Gas Town Work Ledger (Centralized on Coordinator Node)
    # -------------------------------------------------------------------------

    def create_work_item_sync(self, title: str, created_by: str, assignee_id: str = None, parent_id: str = None, meta: Dict = None) -> str:
        """Synchronously creates a new work item on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return self.local_memories[coord_node].create_work_item_sync(title, created_by, assignee_id, parent_id, meta)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = self.sync_client.post(
                    f"{api_url}/api/memory/coordinator/work_items",
                    json={"title": title, "created_by": created_by, "assignee_id": assignee_id, "parent_id": parent_id, "meta": meta},
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json().get("item_id")
            except Exception as e:
                self.logger.error(f"Failed to route create_work_item_sync to coordinator: {e}")
                return None

    async def create_work_item(self, title: str, created_by: str, assignee_id: str = None, parent_id: str = None, meta: Dict = None) -> str:
        """Asynchronously creates a new work item on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return await self.local_memories[coord_node].create_work_item(title, created_by, assignee_id, parent_id, meta)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = await self.async_client.post(
                    f"{api_url}/api/memory/coordinator/work_items",
                    json={"title": title, "created_by": created_by, "assignee_id": assignee_id, "parent_id": parent_id, "meta": meta},
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json().get("item_id")
            except Exception as e:
                self.logger.error(f"Failed to route create_work_item to coordinator: {e}")
                return None

    def update_work_item_sync(self, item_id: str, status: str = None, assignee_id: str = None, validation_results: Dict = None, meta_update: Dict = None) -> bool:
        """Synchronously updates an existing work item on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return self.local_memories[coord_node].update_work_item_sync(item_id, status, assignee_id, validation_results, meta_update)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = self.sync_client.post(
                    f"{api_url}/api/memory/coordinator/work_items/{item_id}",
                    json={"status": status, "assignee_id": assignee_id, "validation_results": validation_results, "meta_update": meta_update},
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json().get("updated", False)
            except Exception as e:
                self.logger.error(f"Failed to route update_work_item_sync to coordinator: {e}")
                return False

    async def update_work_item(self, item_id: str, status: str = None, assignee_id: str = None, validation_results: Dict = None, meta_update: Dict = None) -> bool:
        """Asynchronously updates an existing work item on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return await self.local_memories[coord_node].update_work_item(item_id, status, assignee_id, validation_results, meta_update)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = await self.async_client.post(
                    f"{api_url}/api/memory/coordinator/work_items/{item_id}",
                    json={"status": status, "assignee_id": assignee_id, "validation_results": validation_results, "meta_update": meta_update},
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json().get("updated", False)
            except Exception as e:
                self.logger.error(f"Failed to route update_work_item to coordinator: {e}")
                return False

    def get_work_item_sync(self, item_id: str) -> Optional[Dict]:
        """Synchronously retrieves a work item from the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return self.local_memories[coord_node].get_work_item_sync(item_id)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = self.sync_client.get(
                    f"{api_url}/api/memory/coordinator/work_items/{item_id}",
                    headers=self.headers
                )
                if resp.status_code == 404:
                    return None
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.logger.error(f"Failed to route get_work_item_sync from coordinator: {e}")
                return None

    async def get_work_item(self, item_id: str) -> Optional[Dict]:
        """Asynchronously retrieves a work item from the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return await self.local_memories[coord_node].get_work_item(item_id)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = await self.async_client.get(
                    f"{api_url}/api/memory/coordinator/work_items/{item_id}",
                    headers=self.headers
                )
                if resp.status_code == 404:
                    return None
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.logger.error(f"Failed to route get_work_item from coordinator: {e}")
                return None

    def list_work_items_sync(self, status: str = None, assignee_id: str = None, limit: int = 50) -> List[Dict]:
        """Synchronously lists work items from the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return self.local_memories[coord_node].list_work_items_sync(status, assignee_id, limit)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                params = {"limit": limit}
                if status: params["status"] = status
                if assignee_id: params["assignee_id"] = assignee_id
                resp = self.sync_client.get(
                    f"{api_url}/api/memory/coordinator/work_items",
                    params=params,
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.logger.error(f"Failed to route list_work_items_sync from coordinator: {e}")
                return []

    async def list_work_items(self, status: str = None, assignee_id: str = None, limit: int = 50) -> List[Dict]:
        """Asynchronously lists work items from the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return await self.local_memories[coord_node].list_work_items(status, assignee_id, limit)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                params = {"limit": limit}
                if status: params["status"] = status
                if assignee_id: params["assignee_id"] = assignee_id
                resp = await self.async_client.get(
                    f"{api_url}/api/memory/coordinator/work_items",
                    params=params,
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.logger.error(f"Failed to route list_work_items from coordinator: {e}")
                return []

    # -------------------------------------------------------------------------
    # Dead Letter Queue (DLQ) (Centralized on Coordinator Node)
    # -------------------------------------------------------------------------

    def enqueue_dlq_item_sync(self, event_type: str, payload: Dict[str, Any], error_reason: str, retry_count: int = 0) -> str:
        """Synchronously enqueues a DLQ item on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return self.local_memories[coord_node].enqueue_dlq_item_sync(event_type, payload, error_reason, retry_count)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = self.sync_client.post(
                    f"{api_url}/api/memory/coordinator/dlq",
                    json={"event_type": event_type, "payload": payload, "error_reason": error_reason, "retry_count": retry_count},
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json().get("id")
            except Exception as e:
                self.logger.error(f"Failed to route enqueue_dlq_item_sync to coordinator: {e}")
                return None

    async def enqueue_dlq_item(self, event_type: str, payload: Dict[str, Any], error_reason: str, retry_count: int = 0) -> str:
        """Asynchronously enqueues a DLQ item on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return await self.local_memories[coord_node].enqueue_dlq_item(event_type, payload, error_reason, retry_count)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = await self.async_client.post(
                    f"{api_url}/api/memory/coordinator/dlq",
                    json={"event_type": event_type, "payload": payload, "error_reason": error_reason, "retry_count": retry_count},
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json().get("id")
            except Exception as e:
                self.logger.error(f"Failed to route enqueue_dlq_item to coordinator: {e}")
                return None

    def claim_dlq_item_sync(self, worker_id: str, supported_types: List[str] = None) -> Optional[Dict]:
        """Synchronously claims a DLQ item on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return self.local_memories[coord_node].claim_dlq_item_sync(worker_id, supported_types)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = self.sync_client.post(
                    f"{api_url}/api/memory/coordinator/dlq/claim",
                    json={"worker_id": worker_id, "supported_types": supported_types},
                    headers=self.headers
                )
                if resp.status_code == 204 or not resp.content:
                    return None
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.logger.error(f"Failed to route claim_dlq_item_sync from coordinator: {e}")
                return None

    async def claim_dlq_item(self, worker_id: str, supported_types: List[str] = None) -> Optional[Dict]:
        """Asynchronously claims a DLQ item on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return await self.local_memories[coord_node].claim_dlq_item(worker_id, supported_types)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = await self.async_client.post(
                    f"{api_url}/api/memory/coordinator/dlq/claim",
                    json={"worker_id": worker_id, "supported_types": supported_types},
                    headers=self.headers
                )
                if resp.status_code == 204 or not resp.content:
                    return None
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                self.logger.error(f"Failed to route claim_dlq_item from coordinator: {e}")
                return None

    def update_dlq_item_sync(self, item_id: str, status: str, result: str = None, retry_after: float = None, increment_retry: bool = False) -> bool:
        """Synchronously updates a DLQ item's status on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return self.local_memories[coord_node].update_dlq_item_sync(item_id, status, result, retry_after, increment_retry)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = self.sync_client.post(
                    f"{api_url}/api/memory/coordinator/dlq/{item_id}",
                    json={"status": status, "result": result, "retry_after": retry_after, "increment_retry": increment_retry},
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json().get("updated", False)
            except Exception as e:
                self.logger.error(f"Failed to route update_dlq_item_sync to coordinator: {e}")
                return False

    async def update_dlq_item(self, item_id: str, status: str, result: str = None, retry_after: float = None, increment_retry: bool = False) -> bool:
        """Asynchronously updates a DLQ item's status on the centralized coordinator node."""
        coord_node = self.coordinator_node_id
        if coord_node in self.local_memories:
            return await self.local_memories[coord_node].update_dlq_item(item_id, status, result, retry_after, increment_retry)
        else:
            api_url = self._get_node_api_url(coord_node)
            try:
                resp = await self.async_client.post(
                    f"{api_url}/api/memory/coordinator/dlq/{item_id}",
                    json={"status": status, "result": result, "retry_after": retry_after, "increment_retry": increment_retry},
                    headers=self.headers
                )
                resp.raise_for_status()
                return resp.json().get("updated", False)
            except Exception as e:
                self.logger.error(f"Failed to route update_dlq_item to coordinator: {e}")
                return False

    def close(self):
        """Closes all local SQLite database connections and client pools."""
        for mem in self.local_memories.values():
            mem.close()
        self.sync_client.close()
        # To close async_client safely in sync context:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.async_client.aclose())
        except RuntimeError:
            pass
