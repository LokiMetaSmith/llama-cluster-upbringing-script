import sqlite3
import json
import logging
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class ExecutionHistory:
    def __init__(self, db_path: str = "execution_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS executions (
                        execution_id TEXT PRIMARY KEY,
                        code_hash TEXT NOT NULL,
                        language TEXT NOT NULL,
                        libraries_hash TEXT NOT NULL,
                        code TEXT NOT NULL,
                        libraries TEXT,
                        stdout TEXT,
                        stderr TEXT,
                        exit_code INTEGER,
                        status TEXT NOT NULL,
                        duration_ms INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        error TEXT
                    )
                """)
                # Create index for idempotency lookups
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_idempotency
                    ON executions(code_hash, language, libraries_hash, status)
                """)
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to initialize execution history DB: {e}")

    def _compute_hash(self, content: Any) -> str:
        if isinstance(content, list):
            content = json.dumps(sorted(content))
        elif not isinstance(content, str):
            content = str(content)
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def record_execution(self, execution_id: str, code: str, language: str,
                        libraries: Optional[List[str]], status: str,
                        stdout: str = "", stderr: str = "", exit_code: Optional[int] = None,
                        duration_ms: Optional[int] = None, error: Optional[str] = None):
        code_hash = self._compute_hash(code)
        libraries_hash = self._compute_hash(libraries or [])
        libraries_json = json.dumps(libraries) if libraries else None

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO executions (
                        execution_id, code_hash, language, libraries_hash, code,
                        libraries, stdout, stderr, exit_code, status, duration_ms, error
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    execution_id, code_hash, language, libraries_hash, code,
                    libraries_json, stdout, stderr, exit_code, status, duration_ms, error
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to record execution {execution_id}: {e}")

    def get_cached_result(self, code: str, language: str, libraries: Optional[List[str]]) -> Optional[Dict[str, Any]]:
        code_hash = self._compute_hash(code)
        libraries_hash = self._compute_hash(libraries or [])

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT stdout, stderr, exit_code, status, error, duration_ms
                    FROM executions
                    WHERE code_hash = ? AND language = ? AND libraries_hash = ? AND status = 'success'
                    ORDER BY created_at DESC LIMIT 1
                """, (code_hash, language, libraries_hash))

                row = cursor.fetchone()
                if row:
                    return dict(row)
        except Exception as e:
            logger.error(f"Failed to fetch cached execution: {e}")

        return None

    def get_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM executions WHERE execution_id = ?", (execution_id,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
        except Exception as e:
            logger.error(f"Failed to fetch execution {execution_id}: {e}")

        return None
