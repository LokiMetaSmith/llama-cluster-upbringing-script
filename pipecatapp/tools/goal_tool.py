import sqlite3
import os
import time
import logging
import json
from typing import Optional

logger = logging.getLogger(__name__)

class GoalTool:
    """
    A tool that allows agents to create, read, update, and manage persistent goals.
    This gives the working model stateful control over its objectives across sessions.
    """
    def __init__(self, db_path="~/.config/pipecat/goals.db"):
        self.db_path = os.path.expanduser(db_path)
        self._ensure_db_dir()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.create_table()


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "goaltool"),
                "description": getattr(self, "description", "Tool GoalTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: create_table, get_active_goal, create_goal, get_goal, update_goal, schedule_wakeup"
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs):
        if action == "create_table":
            return getattr(self, "create_table")(**kwargs.get("kwargs", kwargs))
        if action == "get_active_goal":
            return getattr(self, "get_active_goal")(**kwargs.get("kwargs", kwargs))
        if action == "create_goal":
            return getattr(self, "create_goal")(**kwargs.get("kwargs", kwargs))
        if action == "get_goal":
            return getattr(self, "get_goal")(**kwargs.get("kwargs", kwargs))
        if action == "update_goal":
            return getattr(self, "update_goal")(**kwargs.get("kwargs", kwargs))
        if action == "schedule_wakeup":
            return getattr(self, "schedule_wakeup")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"

    def _ensure_db_dir(self):
        directory = os.path.dirname(self.db_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                logger.error(f"Could not create directory for goals DB: {e}")

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    objective TEXT NOT NULL,
                    status TEXT NOT NULL,
                    budget INTEGER,
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL
                )
            """)
            # Wakeup schedules
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wakeups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    resume_time INTEGER NOT NULL,
                    context TEXT
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error creating goals table: {e}")

    def get_active_goal(self, task_id: str) -> Optional[dict]:
        """Internal helper to get an active goal for a task."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM goals
                WHERE task_id = ? AND status = 'active'
                ORDER BY updated_at DESC LIMIT 1
            """, (task_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching active goal: {e}")
            return None

    def create_goal(self, task_id: str, objective: str, budget: int = None) -> str:
        """
        Creates a new active goal for the current task.
        """
        # Close existing active goals for this task
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE goals SET status = 'abandoned' WHERE task_id = ? AND status = 'active'", (task_id,))

            now = int(time.time() * 1000)
            cursor.execute("""
                INSERT INTO goals (task_id, objective, status, budget, created_at, updated_at)
                VALUES (?, ?, 'active', ?, ?, ?)
            """, (task_id, objective, budget, now, now))
            self.conn.commit()
            return f"Successfully created new goal for task {task_id}: {objective}"
        except sqlite3.Error as e:
            logger.error(f"Error creating goal: {e}")
            return f"Error creating goal: {e}"

    def get_goal(self, task_id: str) -> str:
        """
        Retrieves the currently active goal for the task.
        """
        goal = self.get_active_goal(task_id)
        if goal:
            return json.dumps(goal)
        return "No active goal found for this task."

    def update_goal(self, task_id: str, status: str) -> str:
        """
        Updates the status of the currently active goal.
        Valid statuses: 'active', 'completed', 'failed', 'abandoned'.
        """
        try:
            cursor = self.conn.cursor()
            now = int(time.time() * 1000)
            cursor.execute("""
                UPDATE goals
                SET status = ?, updated_at = ?
                WHERE task_id = ? AND status = 'active'
            """, (status, now, task_id))
            if cursor.rowcount > 0:
                self.conn.commit()
                return f"Successfully updated active goal for task {task_id} to status: {status}"
            else:
                return f"No active goal found for task {task_id} to update."
        except sqlite3.Error as e:
            logger.error(f"Error updating goal: {e}")
            return f"Error updating goal: {e}"

    def schedule_wakeup(self, task_id: str, delay_seconds: int, context: str = "") -> str:
        """
        Allows the agent to yield execution and explicitly schedule a resumption.
        Useful for waiting on long-running processes (strategic pause).
        """
        try:
            cursor = self.conn.cursor()
            resume_time = int(time.time()) + delay_seconds
            cursor.execute("""
                INSERT INTO wakeups (task_id, resume_time, context)
                VALUES (?, ?, ?)
            """, (task_id, resume_time, context))
            self.conn.commit()
            return f"Wakeup scheduled for {delay_seconds} seconds from now. You can safely stop here."
        except sqlite3.Error as e:
            logger.error(f"Error scheduling wakeup: {e}")
            return f"Error scheduling wakeup: {e}"

    def run(self, action: str, task_id: str, objective: str = "", status: str = "", budget: int = None, delay_seconds: int = 0, context: str = "") -> str:
        """
        Main entry point for the tool.
        """
        if action == "create_goal":
            if not objective:
                return "Error: objective is required to create a goal."
            return self.create_goal(task_id, objective, budget)
        elif action == "get_goal":
            return self.get_goal(task_id)
        elif action == "update_goal":
            if not status:
                return "Error: status is required to update a goal."
            return self.update_goal(task_id, status)
        elif action == "schedule_wakeup":
            if delay_seconds <= 0:
                return "Error: delay_seconds must be positive to schedule a wakeup."
            return self.schedule_wakeup(task_id, delay_seconds, context)
        else:
            return f"Error: unknown action '{action}'. Valid actions are create_goal, get_goal, update_goal, schedule_wakeup."
