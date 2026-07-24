import sqlite3
import json
import logging
import time
from typing import List, Dict

logger = logging.getLogger(__name__)

class PdsSyncBuffer:
    """
    A local SQLite-backed buffer for AT Protocol actions to support offline-capable operations.
    Queues posts when the remote PDS is unreachable.
    """
    def __init__(self, db_path: str = "/opt/pipecatapp/atproto_buffer.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS post_queue (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL,
                        handle TEXT NOT NULL,
                        timestamp REAL NOT NULL,
                        status TEXT DEFAULT 'pending'
                    )
                ''')
                # Attempt to add handle column if it doesn't exist (for existing DBs)
                try:
                    cursor.execute('ALTER TABLE post_queue ADD COLUMN handle TEXT DEFAULT "unknown"')
                except sqlite3.OperationalError:
                    pass # Column likely already exists
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize PDS Sync Buffer DB: {e}")

    def enqueue_post(self, text: str, handle: str) -> int:
        """
        Adds a post to the sync queue under a specific handle.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO post_queue (text, handle, timestamp) VALUES (?, ?, ?)',
                    (text, handle, time.time())
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Failed to enqueue post: {e}")
            return -1

    def get_pending_posts(self, handle: str) -> List[Dict]:
        """
        Retrieves all pending posts from the queue for a specific handle.
        """
        posts = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM post_queue WHERE status = "pending" AND handle = ? ORDER BY timestamp ASC', (handle,))
                rows = cursor.fetchall()
                for row in rows:
                    posts.append(dict(row))
        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve pending posts: {e}")
        return posts

    def mark_post_synced(self, post_id: int):
        """
        Marks a post as successfully synced to the PDS.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE post_queue SET status = "synced" WHERE id = ?', (post_id,))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to mark post {post_id} as synced: {e}")
