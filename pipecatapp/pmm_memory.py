import sqlite3
import json
import time
import hashlib
import asyncio
import os
import uuid
from typing import Dict, Any, Optional, List

class PMMMemory:
    """A memory store based on the Persistent Mind Model's event-sourcing.

    This class implements a deterministic, event-sourced cognitive architecture
    for persistent AI memory. It uses a SQLite database as an append-only
    ledger for events.

    Attributes:
        db_path (str): The path to the SQLite database file.
        conn: The database connection object.
    """
    def __init__(self, db_path: str = "pmm_memory.db"):
        """Initializes the PMMMemory store.

        Args:
            db_path (str, optional): The path to the SQLite database file.
                Defaults to "pmm_memory.db".
        """
        self.db_path = os.path.expanduser(db_path)
        # Ensure the directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self.conn = self._init_db()

    def _init_db(self):
        """Initializes the SQLite database and creates the events table."""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                kind TEXT,
                content TEXT,
                meta TEXT,
                prev_hash TEXT,
                hash TEXT UNIQUE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_kind ON events(kind);")

        # Gas Town Work Ledger (Beads) Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS work_items (
                id TEXT PRIMARY KEY,
                title TEXT,
                status TEXT,
                assignee_id TEXT,
                created_by TEXT,
                created_at REAL,
                updated_at REAL,
                parent_id TEXT,
                meta TEXT,
                validation_results TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_work_items_status ON work_items(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_work_items_assignee ON work_items(assignee_id);")
        # Bolt ⚡ Optimization: Index created_at for faster sorting
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_work_items_created_at ON work_items(created_at);")
        # Bolt ⚡ Optimization: Composite index for agent stats
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_work_items_assignee_status ON work_items(assignee_id, status);")

        # DLQ Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dlq (
                id TEXT PRIMARY KEY,
                event_type TEXT,
                payload TEXT,
                error_reason TEXT,
                status TEXT,
                retry_count INTEGER,
                retry_after REAL,
                created_at REAL,
                updated_at REAL,
                locked_by TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_dlq_status ON dlq(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_dlq_event_type ON dlq(event_type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_dlq_retry_after ON dlq(retry_after);")

        conn.commit()
        return conn

    def _get_last_hash(self) -> Optional[str]:
        """Retrieves the hash of the most recent event in the ledger.

        Returns:
            The hash of the last event, or None if the ledger is empty.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT hash FROM events ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        return result[0] if result else None

    def _calculate_hash(self, timestamp: float, kind: str, content: str, meta: Dict[str, Any], prev_hash: Optional[str]) -> str:
        """Calculates the SHA-256 hash for a new event.

        Args:
            timestamp (float): The event's timestamp.
            kind (str): The type of the event.
            content (str): The main content of the event.
            meta (Dict[str, Any]): a JSON-serializable dictionary of metadata.
            prev_hash (Optional[str]): The hash of the previous event.

        Returns:
            The calculated hex digest of the hash.
        """
        hasher = hashlib.sha256()
        payload = {
            "timestamp": timestamp,
            "kind": kind,
            "content": content,
            "meta": meta,
            "prev_hash": prev_hash,
        }
        hasher.update(json.dumps(payload, sort_keys=True).encode('utf-8'))
        return hasher.hexdigest()

    def add_event_sync(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Adds a new event to the memory ledger synchronously.

        Args:
            kind (str): The type of event (e.g., 'user_message', 'assistant_message').
            content (str): The content of the event.
            meta (Optional[Dict[str, Any]], optional): Additional metadata.
                Defaults to None.
        """
        meta = meta or {}
        timestamp = time.time()
        prev_hash = self._get_last_hash()
        event_hash = self._calculate_hash(timestamp, kind, content, meta, prev_hash)

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO events (timestamp, kind, content, meta, prev_hash, hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, kind, content, json.dumps(meta), prev_hash, event_hash))
        self.conn.commit()

    async def add_event(self, kind: str, content: str, meta: Optional[Dict[str, Any]] = None) -> None:
        """Adds a new event to the memory ledger asynchronously.

        Args:
            kind (str): The type of event (e.g., 'user_message', 'assistant_message').
            content (str): The content of the event.
            meta (Optional[Dict[str, Any]], optional): Additional metadata.
                Defaults to None.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.add_event_sync, kind, content, meta)

    def get_events_sync(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves the most recent events from the ledger synchronously.

        Args:
            kind (Optional[str], optional): The type of events to retrieve.
                If None, retrieves all kinds. Defaults to None.
            limit (int, optional): The maximum number of events to retrieve.
                Defaults to 10.

        Returns:
            A list of dictionaries, where each dictionary represents an event.
        """
        cursor = self.conn.cursor()
        if kind:
            cursor.execute("SELECT id, timestamp, kind, content, meta FROM events WHERE kind = ? ORDER BY id DESC LIMIT ?", (kind, limit))
        else:
            cursor.execute("SELECT id, timestamp, kind, content, meta FROM events ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        events = []
        for row in rows:
            meta = json.loads(row[4]) if row[4] else {}
            events.append({
                "id": row[0],
                "timestamp": row[1],
                "kind": row[2],
                "content": row[3],
                "meta": meta
            })
        return list(reversed(events))

    async def get_events(self, kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves the most recent events from the ledger asynchronously.

        Args:
            kind (Optional[str], optional): The type of events to retrieve.
                If None, retrieves all kinds. Defaults to None.
            limit (int, optional): The maximum number of events to retrieve.
                Defaults to 10.

        Returns:
            A list of dictionaries, where each dictionary represents an event.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_events_sync, kind, limit)

    # -------------------------------------------------------------------------
    # Gas Town Work Ledger Methods
    # -------------------------------------------------------------------------

    def create_work_item_sync(self, title: str, created_by: str, assignee_id: str = None, parent_id: str = None, meta: Dict = None) -> str:
        """Creates a new work item in the ledger."""
        item_id = str(uuid.uuid4())[:8] # Short ID like 'a1b2c3d4'
        timestamp = time.time()
        meta = meta or {}

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO work_items (id, title, status, assignee_id, created_by, created_at, updated_at, parent_id, meta, validation_results)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (item_id, title, "open", assignee_id, created_by, timestamp, timestamp, parent_id, json.dumps(meta), json.dumps({})))
        self.conn.commit()

        # Also log as an event for audit trail
        self.add_event_sync("work_item_created", f"Created work item {item_id}: {title}", {"work_item_id": item_id, "creator": created_by})

        return item_id

    async def create_work_item(self, title: str, created_by: str, assignee_id: str = None, parent_id: str = None, meta: Dict = None) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.create_work_item_sync, title, created_by, assignee_id, parent_id, meta)

    def update_work_item_sync(self, item_id: str, status: str = None, assignee_id: str = None, validation_results: Dict = None, meta_update: Dict = None) -> bool:
        """Updates an existing work item."""
        cursor = self.conn.cursor()

        # Build update query dynamically
        updates = ["updated_at = ?"]
        params = [time.time()]

        if status:
            updates.append("status = ?")
            params.append(status)
        if assignee_id:
            updates.append("assignee_id = ?")
            params.append(assignee_id)
        if validation_results:
            updates.append("validation_results = ?")
            params.append(json.dumps(validation_results))

        # Fetch existing meta to merge if needed, or simple overwrite?
        # For simplicity, we'll fetch-merge-update if meta_update is present
        if meta_update:
            cursor.execute("SELECT meta FROM work_items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            if not row:
                return False
            current_meta = json.loads(row[0])
            current_meta.update(meta_update)
            updates.append("meta = ?")
            params.append(json.dumps(current_meta))

        params.append(item_id)

        sql = f"UPDATE work_items SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, params)
        self.conn.commit()

        if cursor.rowcount > 0:
            self.add_event_sync("work_item_updated", f"Updated work item {item_id}", {"updates": updates})
            return True
        return False

    async def update_work_item(self, item_id: str, status: str = None, assignee_id: str = None, validation_results: Dict = None, meta_update: Dict = None) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.update_work_item_sync, item_id, status, assignee_id, validation_results, meta_update)

    def get_work_item_sync(self, item_id: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM work_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            return None

        # Map columns to dict
        columns = [description[0] for description in cursor.description]
        item = dict(zip(columns, row))
        item['meta'] = json.loads(item['meta']) if item['meta'] else {}
        item['validation_results'] = json.loads(item['validation_results']) if item['validation_results'] else {}
        return item

    async def get_work_item(self, item_id: str) -> Optional[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.get_work_item_sync, item_id)

    def list_work_items_sync(self, status: str = None, assignee_id: str = None, limit: int = 50) -> List[Dict]:
        cursor = self.conn.cursor()
        query = "SELECT * FROM work_items"
        conditions = []
        params = []

        if status:
            conditions.append("status = ?")
            params.append(status)
        if assignee_id:
            conditions.append("assignee_id = ?")
            params.append(assignee_id)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]
        results = []
        for row in rows:
            item = dict(zip(columns, row))
            item['meta'] = json.loads(item['meta']) if item['meta'] else {}
            item['validation_results'] = json.loads(item['validation_results']) if item['validation_results'] else {}
            results.append(item)
        return results

    async def list_work_items(self, status: str = None, assignee_id: str = None, limit: int = 50) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.list_work_items_sync, status, assignee_id, limit)

    def get_agent_stats_sync(self, assignee_id: str) -> Dict[str, Any]:
        """Aggregates work statistics for a specific agent."""
        cursor = self.conn.cursor()

        # Bolt ⚡ Optimization: Use a single query for all stats to reduce overhead
        cursor.execute("""
            SELECT
                COUNT(*),
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END),
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END)
            FROM work_items
            WHERE assignee_id = ?
        """, (assignee_id,))

        row = cursor.fetchone()

        total_tasks = row[0]
        # SQLite SUM() can return None if there are no rows, but since we count(*), if count is 0, sums are None.
        completed_tasks = row[1] if row[1] is not None else 0
        failed_tasks = row[2] if row[2] is not None else 0

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
        """Enqueues a failed event into the Dead Letter Queue."""
        item_id = str(uuid.uuid4())
        timestamp = time.time()
        retry_after = timestamp

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO dlq (id, event_type, payload, error_reason, status, retry_count, retry_after, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (item_id, event_type, json.dumps(payload), error_reason, "PENDING", retry_count, retry_after, timestamp, timestamp))
        self.conn.commit()
        return item_id

    async def enqueue_dlq_item(self, event_type: str, payload: Dict[str, Any], error_reason: str, retry_count: int = 0) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.enqueue_dlq_item_sync, event_type, payload, error_reason, retry_count)

    def claim_dlq_item_sync(self, worker_id: str, supported_types: List[str] = None) -> Optional[Dict]:
        """Atomically claims a PENDING DLQ item for processing."""
        cursor = self.conn.cursor()
        now = time.time()

        # Build query filters
        type_filter = ""
        params = [now]
        if supported_types:
            placeholders = ",".join("?" * len(supported_types))
            type_filter = f"AND event_type IN ({placeholders})"
            params.extend(supported_types)

        # Retry loop for optimistic concurrency (simulating SKIP LOCKED)
        for _ in range(3):
            # 1. Find a candidate
            query = f"""
                SELECT id FROM dlq
                WHERE status = 'PENDING'
                  AND retry_after <= ?
                  {type_filter}
                ORDER BY created_at ASC
                LIMIT 1
            """
            cursor.execute(query, params)
            row = cursor.fetchone()

            if not row:
                return None # Queue empty

            item_id = row[0]

            # 2. Try to lock it
            update_query = """
                UPDATE dlq
                SET status = 'PROCESSING', locked_by = ?, updated_at = ?
                WHERE id = ? AND status = 'PENDING'
            """
            cursor.execute(update_query, (worker_id, now, item_id))
            self.conn.commit()

            if cursor.rowcount == 1:
                # Successfully claimed
                cursor.execute("SELECT * FROM dlq WHERE id = ?", (item_id,))
                row = cursor.fetchone()
                columns = [description[0] for description in cursor.description]
                item = dict(zip(columns, row))
                item['payload'] = json.loads(item['payload']) if item['payload'] else {}
                return item
            else:
                # Race condition: someone else claimed it, loop again
                continue

        return None

    async def claim_dlq_item(self, worker_id: str, supported_types: List[str] = None) -> Optional[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.claim_dlq_item_sync, worker_id, supported_types)

    def update_dlq_item_sync(self, item_id: str, status: str, result: str = None, retry_after: float = None, increment_retry: bool = False) -> bool:
        """Updates the status of a DLQ item."""
        cursor = self.conn.cursor()
        now = time.time()

        updates = ["status = ?", "updated_at = ?", "locked_by = NULL"]
        params = [status, now]

        if increment_retry:
             updates.append("retry_count = retry_count + 1")

        if retry_after is not None:
            updates.append("retry_after = ?")
            params.append(retry_after)

        if result:
             updates.append("error_reason = ?")
             params.append(result)

        params.append(item_id)

        sql = f"UPDATE dlq SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor.rowcount > 0

    async def update_dlq_item(self, item_id: str, status: str, result: str = None, retry_after: float = None, increment_retry: bool = False) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.update_dlq_item_sync, item_id, status, result, retry_after, increment_retry)

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
