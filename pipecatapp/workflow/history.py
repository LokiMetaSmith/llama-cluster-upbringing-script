import sqlite3
import json
import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

class WorkflowHistory:
    """Manages the persistence of workflow execution history."""

    _initialized_paths = set()

    def __init__(self, db_path: str = "~/.config/pipecat/workflow_history.db"):
        self.db_path = os.path.abspath(os.path.expanduser(db_path))
        # Optimization: Only run _init_db (which checks filesystem/creates tables)
        # if we haven't already done so for this path in this process.
        if self.db_path not in self._initialized_paths:
            self._init_db()
            self._initialized_paths.add(self.db_path)

    def _init_db(self):
        """Initialize the SQLite database and create the table if it doesn't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
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
        conn.commit()
        conn.close()

    def save_run(self, runner_id: str, workflow_name: str, start_time: float, end_time: float, status: str, context: Dict[str, Any], error: Optional[str] = None):
        """Save a completed workflow run to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Serialize context to JSON
        final_state_json = json.dumps(context)

        cursor.execute('''
            INSERT OR REPLACE INTO workflow_runs (id, workflow_name, start_time, end_time, status, final_state, error)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (runner_id, workflow_name, start_time, end_time, status, final_state_json, error))

        conn.commit()
        conn.close()

    def get_all_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve a list of recent workflow runs (summary only)."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

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

        conn.close()
        return runs

    def get_run(self, runner_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the full details of a specific workflow run."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM workflow_runs WHERE id = ?', (runner_id,))
        row = cursor.fetchone()

        if row:
            run_data = dict(row)
            try:
                run_data["final_state"] = json.loads(run_data["final_state"])
            except (json.JSONDecodeError, TypeError):
                run_data["final_state"] = {}
            conn.close()
            return run_data

        conn.close()
        return None
