import sqlite3
import json
import time
import hashlib
import asyncio
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
        self.db_path = db_path
        self.conn = self._init_db()

    def _init_db(self):
        """Initializes the SQLite database and creates the events table."""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
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

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
