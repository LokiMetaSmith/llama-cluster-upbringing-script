import hashlib
import asyncio
import time
import json
import uuid
from typing import Dict, Any, Optional, List
from pipecatapp.pmm_memory import PMMMemory

class ShardedPMMMemory:
    """A proxy router wrapper that shards PMMMemory across multiple SQLite databases.

    This class provides the exact same interface as `PMMMemory` but acts as an
    intelligent database proxy router. It hashes a key to select the shard
    for write operations and point queries, while scatter-gathering for scans.

    Attributes:
        shards (List[PMMMemory]): The list of PMMMemory database shards.
        num_shards (int): The total number of configured shards.
    """
    def __init__(self, db_paths: List[str]):
        """Initializes the ShardedPMMMemory proxy.

        Args:
            db_paths (List[str]): List of paths for each SQLite shard.
        """
        if not db_paths:
            raise ValueError("Must specify at least one database path for sharding.")
        self.shards = [PMMMemory(db_path=path) for path in db_paths]
        self.num_shards = len(db_paths)

    def _get_shard_index(self, routing_key: str) -> int:
        """Determines the target shard index by hashing the key.

        Args:
            routing_key (str): The routing key to hash.

        Returns:
            int: The index of the target shard.
        """
        hasher = hashlib.md5(routing_key.encode("utf-8"))
        return int(hasher.hexdigest(), 16) % self.num_shards

    def _get_shard_for_event(self, kind: str, meta: Optional[Dict[str, Any]]) -> PMMMemory:
        """Returns the appropriate shard for an event based on metadata or kind."""
        meta = meta or {}
        # Try routing by session_id, task_id, or kind
        routing_key = meta.get("session_id") or meta.get("task_id") or kind
        idx = self._get_shard_index(routing_key)
        return self.shards[idx]

    def _get_shard_for_id(self, item_id: str) -> PMMMemory:
        """Returns the appropriate shard based on a unique identifier."""
        idx = self._get_shard_index(item_id)
        return self.shards[idx]

    # -------------------------------------------------------------------------
    # Event Sourcing Methods
    # -------------------------------------------------------------------------

    def add_event_sync(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Adds an event to the selected shard synchronously."""
        shard = self._get_shard_for_event(kind, meta)
        shard.add_event_sync(kind, content, meta)

    async def add_event(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Adds an event to the selected shard asynchronously."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.add_event_sync, kind, content, meta)

    def get_events_sync(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves events from all shards, merges and sorts them, and limits the result.

        This uses a scatter-gather approach across all shards.
        """
        all_events = []
        for shard in self.shards:
            events = shard.get_events_sync(kind=kind, limit=limit)
            all_events.extend(events)

        # Merge and sort by timestamp, then limit
        all_events.sort(key=lambda x: x["timestamp"])
        return all_events[-limit:]

    async def get_events(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves and merges events from all shards asynchronously."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_events_sync, kind, limit)

    # -------------------------------------------------------------------------
    # Gas Town Work Ledger Methods
    # -------------------------------------------------------------------------

    def create_work_item_sync(self, title: str, created_by: str, assignee_id: str = None, parent_id: str = None, meta: Dict = None) -> str:
        """Creates a new work item on a dynamically chosen shard based on title/creator hash."""
        # Route by generated UUID first or a hash of the title + creator
        # We can generate the short ID upfront to route it consistently
        item_id = str(self._mock_uuid if hasattr(self, '_mock_uuid') else uuid_8_hex())
        shard = self._get_shard_for_id(item_id)

        # We must override the internal PMMMemory id generation to ensure it matches our shard route
        # Since standard create_work_item generates its own uuid inside PMMMemory, we'll implement it here or inject it.
        # Let's write directly to the db or override the method.
        # PMMMemory.create_work_item_sync accepts ID generation internally. Let's do a direct insert or hack.
        # Since we want to use the standard PMMMemory instance, let's inject it via meta or mock uuid, or do a direct insert.
        # Wait, the PMMMemory.create_work_item_sync has:
        # item_id = str(uuid.uuid4())[:8]
        # Since it generates its own UUID, if we call it, the resulting item is placed in whatever shard we called it on.
        # But wait! If we let it generate the ID, how do we know which shard it went to?
        # A clean way is to generate the item_id first, and have a modified insert on PMMMemory or write a custom insert.
        # Let's inspect PMMMemory's create_work_item_sync structure.
        # If we can't change PMMMemory, we can write a helper on PMMMemory or just perform the database insert directly in ShardedPMMMemory.
        # Let's look: PMMMemory has `self.conn` which we can use directly!
        timestamp = time.time()
        meta = meta or {}

        cursor = shard.conn.cursor()
        cursor.execute("""
            INSERT INTO work_items (id, title, status, assignee_id, created_by, created_at, updated_at, parent_id, meta, validation_results)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (item_id, title, "open", assignee_id, created_by, timestamp, timestamp, parent_id, json.dumps(meta), json.dumps({})))
        shard.conn.commit()

        shard.add_event_sync("work_item_created", f"Created work item {item_id}: {title}", {"work_item_id": item_id, "creator": created_by})
        return item_id

    async def create_work_item(self, title: str, created_by: str, assignee_id: str = None, parent_id: str = None, meta: Dict = None) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.create_work_item_sync, title, created_by, assignee_id, parent_id, meta)

    def update_work_item_sync(self, item_id: str, status: str = None, assignee_id: str = None, validation_results: Dict = None, meta_update: Dict = None) -> bool:
        """Updates a work item in the corresponding shard."""
        shard = self._get_shard_for_id(item_id)
        return shard.update_work_item_sync(item_id, status, assignee_id, validation_results, meta_update)

    async def update_work_item(self, item_id: str, status: str = None, assignee_id: str = None, validation_results: Dict = None, meta_update: Dict = None) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.update_work_item_sync, item_id, status, assignee_id, validation_results, meta_update)

    def get_work_item_sync(self, item_id: str) -> Optional[Dict]:
        """Retrieves a work item from its corresponding shard."""
        shard = self._get_shard_for_id(item_id)
        return shard.get_work_item_sync(item_id)

    async def get_work_item(self, item_id: str) -> Optional[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_work_item_sync, item_id)

    def list_work_items_sync(self, status: str = None, assignee_id: str = None, limit: int = 50) -> List[Dict]:
        """Scatter-gathers work items across all shards."""
        all_items = []
        for shard in self.shards:
            items = shard.list_work_items_sync(status=status, assignee_id=assignee_id, limit=limit)
            all_items.extend(items)

        # Sort by created_at desc
        all_items.sort(key=lambda x: x["created_at"], reverse=True)
        return all_items[:limit]

    async def list_work_items(self, status: str = None, assignee_id: str = None, limit: int = 50) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.list_work_items_sync, status, assignee_id, limit)

    def sync_work_items_sync(self, remote_items: List[Dict]) -> List[Dict]:
        """Syncs work items by routing each remote item to its matching shard."""
        synced = []
        # Group remote items by their sharded destination
        shard_groups = {i: [] for i in range(self.num_shards)}
        for item in remote_items:
            idx = self._get_shard_index(item["id"])
            shard_groups[idx].append(item)

        for idx, items in shard_groups.items():
            if items:
                res = self.shards[idx].sync_work_items_sync(items)
                synced.extend(res)
        return synced

    async def sync_work_items(self, remote_items: List[Dict]) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.sync_work_items_sync, remote_items)

    def get_work_items_since_sync(self, since_timestamp: float) -> List[Dict]:
        """Scatter-gathers updated work items since timestamp."""
        all_items = []
        for shard in self.shards:
            all_items.extend(shard.get_work_items_since_sync(since_timestamp))
        return all_items

    async def get_work_items_since(self, since_timestamp: float) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_work_items_since_sync, since_timestamp)

    def get_agent_stats_sync(self, assignee_id: str) -> Dict[str, Any]:
        """Aggregates work stats for a given assignee across all shards."""
        total_tasks = 0
        completed_tasks = 0
        failed_tasks = 0

        for shard in self.shards:
            stats = shard.get_agent_stats_sync(assignee_id)
            total_tasks += stats["total_tasks"]
            completed_tasks += stats["completed_tasks"]
            failed_tasks += stats["failed_tasks"]

        success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

        return {
            "assignee_id": assignee_id,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": round(success_rate, 2)
        }

    async def get_agent_stats(self, assignee_id: str) -> Dict[str, Any]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_agent_stats_sync, assignee_id)

    # -------------------------------------------------------------------------
    # Dead Letter Queue (DLQ) Methods
    # -------------------------------------------------------------------------

    def enqueue_dlq_item_sync(self, event_type: str, payload: Dict[str, Any], error_reason: str, retry_count: int = 0) -> str:
        """Enqueues failed task on shard based on a generated UUID."""
        item_id = str(hashlib.md5(f"{event_type}-{time.time()}".encode("utf-8")).hexdigest())[:8]
        shard = self._get_shard_for_id(item_id)

        # Use database connection to insert with custom id to match routing route
        timestamp = time.time()
        cursor = shard.conn.cursor()
        cursor.execute("""
            INSERT INTO dlq (id, event_type, payload, error_reason, status, retry_count, retry_after, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (item_id, event_type, json.dumps(payload), error_reason, "PENDING", retry_count, timestamp, timestamp, timestamp))
        shard.conn.commit()
        return item_id

    async def enqueue_dlq_item(self, event_type: str, payload: Dict[str, Any], error_reason: str, retry_count: int = 0) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.enqueue_dlq_item_sync, event_type, payload, error_reason, retry_count)

    def claim_dlq_item_sync(self, worker_id: str, supported_types: List[str] = None) -> Optional[Dict]:
        """Claim next DLQ item in a round-robin or sequential search across shards."""
        for shard in self.shards:
            item = shard.claim_dlq_item_sync(worker_id, supported_types)
            if item:
                return item
        return None

    async def claim_dlq_item(self, worker_id: str, supported_types: List[str] = None) -> Optional[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.claim_dlq_item_sync, worker_id, supported_types)

    def update_dlq_item_sync(self, item_id: str, status: str, result: str = None, retry_after: float = None, increment_retry: bool = False) -> bool:
        """Updates a DLQ item in its matching shard."""
        shard = self._get_shard_for_id(item_id)
        return shard.update_dlq_item_sync(item_id, status, result, retry_after, increment_retry)

    async def update_dlq_item(self, item_id: str, status: str, result: str = None, retry_after: float = None, increment_retry: bool = False) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.update_dlq_item_sync, item_id, status, result, retry_after, increment_retry)

    def close(self):
        """Closes all shards."""
        for shard in self.shards:
            shard.close()


def uuid_8_hex() -> str:
    return str(uuid.uuid4())[:8]
