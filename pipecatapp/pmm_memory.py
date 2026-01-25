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
            events.append({
                "id": row[0],
                "timestamp": row[1],
                "kind": row[2],
                "content": row[3],
                "meta": json.loads(row[4])
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
        item['meta'] = json.loads(item['meta'])
        item['validation_results'] = json.loads(item['validation_results'])
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
            item['meta'] = json.loads(item['meta'])
            item['validation_results'] = json.loads(item['validation_results'])
            results.append(item)
        return results

    async def list_work_items(self, status: str = None, assignee_id: str = None, limit: int = 50) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.list_work_items_sync, status, assignee_id, limit)

    def get_agent_stats_sync(self, assignee_id: str) -> Dict[str, Any]:
        """Aggregates work statistics for a specific agent."""
        cursor = self.conn.cursor()

        # Count total tasks assigned
        cursor.execute("SELECT COUNT(*) FROM work_items WHERE assignee_id = ?", (assignee_id,))
        total_tasks = cursor.fetchone()[0]

        # Count successful tasks
        cursor.execute("SELECT COUNT(*) FROM work_items WHERE assignee_id = ? AND status = 'completed'", (assignee_id,))
        completed_tasks = cursor.fetchone()[0]

        # Count failed tasks
        cursor.execute("SELECT COUNT(*) FROM work_items WHERE assignee_id = ? AND status = 'failed'", (assignee_id,))
        failed_tasks = cursor.fetchone()[0]

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

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
