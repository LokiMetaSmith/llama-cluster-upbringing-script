import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class PdsSyncBuffer:
    """
    A local, persistent queue (SQLite-backed) for caching ATProto actions.
    Ensures that agents can publish states/posts even when offline, providing
    eventual consistency to the remote PDS once network connectivity is restored.
    """
    def __init__(self, db_path: str = "atproto_sync_buffer.sqlite"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Returns a connection tailored to the DB path, handling :memory: correctly."""
        # For :memory: databases, check_same_thread must be False for tests if shared across threads,
        # but :memory: creates a new DB per connection unless using URI.
        # Actually, if db_path is :memory:, we should store the connection in self
        # so it's not destroyed when the connection is closed.

        # We will use file-based databases in production, but support memory for testing
        if self.db_path == ':memory:':
            if not hasattr(self, '_mem_conn'):
                self._mem_conn = sqlite3.connect(':memory:', check_same_thread=False)
            return self._mem_conn
        else:
            return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        """Initializes the SQLite database and creates the queue table."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS atproto_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    error_msg TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            if self.db_path != ':memory:':
                conn.close()
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize PdsSyncBuffer DB: {e}")

    def add_event(self, action: str, payload: Dict[str, Any]) -> int:
        """
        Adds an ATProto action to the sync buffer queue.

        Args:
            action (str): The action to perform (e.g., 'send_post').
            payload (dict): The arguments/data for the action.

        Returns:
            int: The ID of the inserted event, or -1 if failed.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO atproto_events (action, payload, status) VALUES (?, ?, ?)",
                (action, json.dumps(payload), 'pending')
            )
            conn.commit()
            last_id = cursor.lastrowid
            if self.db_path != ':memory:':
                conn.close()
            return last_id
        except sqlite3.Error as e:
            logger.error(f"Failed to add event to PdsSyncBuffer: {e}")
            return -1

    def get_pending_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieves a list of pending events from the queue.

        Args:
            limit (int): The maximum number of events to retrieve.

        Returns:
            List[dict]: A list of event dictionaries.
        """
        events = []
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM atproto_events WHERE status = 'pending' ORDER BY created_at ASC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            for row in rows:
                events.append({
                    "id": row["id"],
                    "action": row["action"],
                    "payload": json.loads(row["payload"]),
                    "status": row["status"],
                    "created_at": row["created_at"]
                })
            if self.db_path != ':memory:':
                conn.close()
        except sqlite3.Error as e:
            logger.error(f"Failed to get pending events from PdsSyncBuffer: {e}")
        return events

    def mark_event_completed(self, event_id: int):
        """Marks an event as successfully completed."""
        self._update_event_status(event_id, 'completed')

    def mark_event_failed(self, event_id: int, error_msg: str):
        """Marks an event as failed (it will not be retried automatically)."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE atproto_events SET status = ?, error_msg = ? WHERE id = ?",
                ('failed', error_msg, event_id)
            )
            conn.commit()
            if self.db_path != ':memory:':
                conn.close()
        except sqlite3.Error as e:
            logger.error(f"Failed to mark event {event_id} as failed: {e}")

    def _update_event_status(self, event_id: int, status: str):
        """Internal helper to update the status of an event."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE atproto_events SET status = ? WHERE id = ?",
                (status, event_id)
            )
            conn.commit()
            if self.db_path != ':memory:':
                conn.close()
        except sqlite3.Error as e:
            logger.error(f"Failed to update event {event_id} status to {status}: {e}")
