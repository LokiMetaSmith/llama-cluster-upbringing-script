import sqlite3
import json
import os
import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime

class WorkflowHistory:
    """Manages the persistence of workflow execution history.

    Bolt ⚡ Optimization:
    - Implements Singleton pattern to avoid repeated object creation.
    - Uses a persistent SQLite connection with WAL mode for better concurrency.
    - Uses threading.Lock to ensure thread-safe writes on the shared connection.
    """

    _instances = {}
    _instances_lock = threading.Lock()

    def __new__(cls, db_path: str = "~/.config/pipecat/workflow_history.db"):
        path = os.path.abspath(os.path.expanduser(db_path))
        with cls._instances_lock:
            if path not in cls._instances:
                instance = super(WorkflowHistory, cls).__new__(cls)
                cls._instances[path] = instance
                # Initialize the instance here, protected by the class lock
                instance.db_path = path
                instance.lock = threading.Lock()
                instance._init_db()
            return cls._instances[path]

    def __init__(self, db_path: str = "~/.config/pipecat/workflow_history.db"):
        # Initialization is handled in __new__ to ensure thread safety
        pass

    def _init_db(self):
        """Initialize the SQLite database and create the table if it doesn't exist."""
        # This is called inside __new__ under the class lock, so it's safe.
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        # Bolt ⚡ Optimization: Keep connection open and use WAL mode
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row # Set row_factory globally
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")

        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_runs (
                id TEXT PRIMARY KEY,
                workflow_name TEXT,
                start_time REAL,
                end_time REAL,
                status TEXT,
                final_state TEXT,
                error TEXT
            )
        ''')
        self.conn.commit()

    def save_run(self, runner_id: str, workflow_name: str, start_time: float, end_time: float, status: str, context: Dict[str, Any], error: Optional[str] = None):
        """Save a completed workflow run to the database."""
        # Serialize context to JSON outside the lock to minimize lock holding time
        final_state_json = json.dumps(context)

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO workflow_runs (id, workflow_name, start_time, end_time, status, final_state, error)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (runner_id, workflow_name, start_time, end_time, status, final_state_json, error))
            self.conn.commit()

    def get_all_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve a list of recent workflow runs (summary only)."""
        # SQLite's internal mutex protects the connection object itself.
        # We create a new cursor which is thread-local.
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT id, workflow_name, start_time, end_time, status, error
            FROM workflow_runs
            ORDER BY start_time DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        runs = []
        for row in rows:
            runs.append({
                "id": row["id"],
                "workflow_name": row["workflow_name"],
                "start_time": row["start_time"],
                "end_time": row["end_time"],
                "status": row["status"],
                "error": row["error"],
                "duration": row["end_time"] - row["start_time"] if row["end_time"] and row["start_time"] else 0
            })

        return runs

    def get_run(self, runner_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the full details of a specific workflow run."""
        cursor = self.conn.cursor()

        cursor.execute('SELECT * FROM workflow_runs WHERE id = ?', (runner_id,))
        row = cursor.fetchone()

        if row:
            run_data = dict(row)
            try:
                run_data["final_state"] = json.loads(run_data["final_state"])
            except (json.JSONDecodeError, TypeError):
                run_data["final_state"] = {}
            return run_data

        return None

    def close(self):
        """Explicitly close the database connection."""
        with self.lock:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
                del self.conn
