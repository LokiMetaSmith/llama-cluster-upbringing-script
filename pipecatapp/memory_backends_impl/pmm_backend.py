import os
import json
import logging
import sqlite3
from typing import List, Dict, Any, Optional

from pipecatapp.memory_backends import BaseMemoryBackend
from pipecatapp.pmm_memory import PMMMemory

logger = logging.getLogger(__name__)

class PMMMemoryBackend(BaseMemoryBackend):
    """
    Persistent Mind Model (PMM) Memory Backend.
    Uses SQLite event-sourcing via PMMMemory for deterministic, immutable memory
    storage with skill and consolidation management.
    """
    def __init__(self, db_path: str = "pmm_memory.db"):
        self.pmm = PMMMemory(db_path=db_path)
        self.db_path = self.pmm.db_path
        self._init_skills_table()

    def _init_skills_table(self):
        """Initializes auxiliary tables on the PMM SQLite connection for skills and consolidations."""
        with self.pmm.conn:
            self.pmm.conn.execute("""
                CREATE TABLE IF NOT EXISTS dynamic_skills (
                    name TEXT PRIMARY KEY,
                    description TEXT NOT NULL,
                    content TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    created_at REAL DEFAULT (strftime('%s', 'now')),
                    updated_at REAL DEFAULT (strftime('%s', 'now'))
                );
            """)
            self.pmm.conn.execute("""
                CREATE TABLE IF NOT EXISTS consolidations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_ids TEXT NOT NULL,
                    summary TEXT,
                    insight TEXT,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                );
            """)

    def add(self, text: str):
        """Adds a plain text memory entry as an episodic event."""
        self.pmm.add_event_sync(kind="memory_text", content=text, meta={"type": "text"})

    def force_save(self):
        """Flushes database WAL if needed."""
        try:
            with self.pmm.conn:
                self.pmm.conn.execute("PRAGMA wal_checkpoint(PASSIVE);")
        except Exception as e:
            logger.debug(f"WAL checkpoint non-critical error: {e}")

    def search(self, query_text: str, k: int = 3) -> List[str]:
        """Simple keyword/substring search across memory text events."""
        cursor = self.pmm.conn.cursor()
        cursor.execute(
            "SELECT content FROM events WHERE kind IN ('memory_text', 'memory_item') AND content LIKE ? ORDER BY id DESC LIMIT ?",
            (f"%{query_text}%", k)
        )
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def add_memory(self, source: str, raw_text: str, summary: str | None = None,
                   entities: list | None = None, topics: list | None = None,
                   importance: int | None = None, consolidated: bool = False,
                   metadata: dict | None = None, doc_id: str | None = None) -> int:
        """Stores a structured memory item into the PMM ledger."""
        meta = {
            "source": source,
            "summary": summary,
            "entities": entities or [],
            "topics": topics or [],
            "importance": importance,
            "consolidated": consolidated,
            "metadata": metadata or {},
            "doc_id": doc_id
        }
        self.pmm.add_event_sync(kind="memory_item", content=raw_text, meta=meta)
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT last_insert_rowid()")
        row = cursor.fetchone()
        return row[0] if row else 0

    def get_memory(self, memory_id: int) -> Optional[dict]:
        """Retrieves a memory by its SQLite event id."""
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT id, content, meta FROM events WHERE id = ?", (memory_id,))
        row = cursor.fetchone()
        if not row:
            return None
        event_id, content, meta_str = row
        meta = json.loads(meta_str) if meta_str else {}
        return {
            "id": event_id,
            "source": meta.get("source"),
            "raw_text": content,
            "summary": meta.get("summary"),
            "entities": meta.get("entities"),
            "topics": meta.get("topics"),
            "importance": meta.get("importance"),
            "consolidated": meta.get("consolidated", False),
            "metadata": meta.get("metadata"),
            "doc_id": meta.get("doc_id")
        }

    def get_unconsolidated_memories(self, limit: int = 50) -> List[dict]:
        """Fetches unconsolidated memories from the ledger."""
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT id, content, meta FROM events WHERE kind = 'memory_item' ORDER BY id DESC")
        rows = cursor.fetchall()
        results = []
        for event_id, content, meta_str in rows:
            meta = json.loads(meta_str) if meta_str else {}
            if not meta.get("consolidated", False):
                results.append({
                    "id": event_id,
                    "source": meta.get("source"),
                    "raw_text": content,
                    "summary": meta.get("summary"),
                    "entities": meta.get("entities"),
                    "topics": meta.get("topics"),
                    "importance": meta.get("importance"),
                    "consolidated": False,
                    "metadata": meta.get("metadata"),
                    "doc_id": meta.get("doc_id")
                })
                if len(results) >= limit:
                    break
        return results

    def add_consolidation(self, source_ids: List[int], summary: str, insight: str | None = None) -> int:
        """Stores a consolidation entry."""
        cursor = self.pmm.conn.cursor()
        with self.pmm.conn:
            cursor.execute(
                "INSERT INTO consolidations (source_ids, summary, insight) VALUES (?, ?, ?)",
                (json.dumps(source_ids), summary, insight)
            )
            consolidation_id = cursor.lastrowid
        # Also log to PMM ledger
        self.pmm.add_event_sync(kind="memory_consolidation", content=summary, meta={
            "consolidation_id": consolidation_id,
            "source_ids": source_ids,
            "insight": insight
        })
        return consolidation_id

    def get_consolidation(self, consolidation_id: int) -> Optional[dict]:
        """Fetches a consolidation by ID."""
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT id, source_ids, summary, insight FROM consolidations WHERE id = ?", (consolidation_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "source_ids": json.loads(row[1]) if row[1] else [],
            "summary": row[2],
            "insight": row[3]
        }

    def mark_memory_consolidated(self, memory_id: int):
        """Marks a memory item as consolidated in its metadata."""
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT meta FROM events WHERE id = ?", (memory_id,))
        row = cursor.fetchone()
        if row and row[0]:
            meta = json.loads(row[0])
            meta["consolidated"] = True
            with self.pmm.conn:
                cursor.execute("UPDATE events SET meta = ? WHERE id = ?", (json.dumps(meta), memory_id))

    def add_activity(self, activity_type: str, description: str, metadata: dict | None = None) -> int:
        """Logs an activity event into the PMM ledger."""
        meta = metadata or {}
        meta["activity_type"] = activity_type
        self.pmm.add_event_sync(kind="activity", content=description, meta=meta)
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT last_insert_rowid()")
        row = cursor.fetchone()
        return row[0] if row else 0

    def get_activities(self, limit: int = 50) -> List[dict]:
        """Retrieves recent activity events."""
        cursor = self.pmm.conn.cursor()
        cursor.execute(
            "SELECT id, timestamp, content, meta FROM events WHERE kind = 'activity' ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        activities = []
        for event_id, timestamp, content, meta_str in rows:
            meta = json.loads(meta_str) if meta_str else {}
            activities.append({
                "id": event_id,
                "timestamp": timestamp,
                "activity_type": meta.get("activity_type", "unknown"),
                "description": content,
                "metadata": meta
            })
        return activities

    def save_skill(self, name: str, description: str, content: str) -> None:
        """Saves or updates a dynamic skill."""
        with self.pmm.conn:
            self.pmm.conn.execute("""
                INSERT INTO dynamic_skills (name, description, content, version, updated_at)
                VALUES (?, ?, ?, 1, strftime('%s', 'now'))
                ON CONFLICT(name) DO UPDATE SET
                    description = excluded.description,
                    content = excluded.content,
                    version = version + 1,
                    updated_at = strftime('%s', 'now')
            """, (name, description, content))

    def get_skill(self, name: str) -> Optional[dict]:
        """Retrieves a skill by name."""
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT name, description, content, version FROM dynamic_skills WHERE name = ?", (name,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "name": row[0],
            "description": row[1],
            "content": row[2],
            "version": row[3]
        }

    def list_skills(self) -> List[dict]:
        """Lists all dynamic skills."""
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT name, description, content, version FROM dynamic_skills ORDER BY name ASC")
        rows = cursor.fetchall()
        return [{"name": r[0], "description": r[1], "content": r[2], "version": r[3]} for r in rows]

    def delete_skill(self, name: str) -> bool:
        """Deletes a dynamic skill."""
        with self.pmm.conn:
            cursor = self.pmm.conn.execute("DELETE FROM dynamic_skills WHERE name = ?", (name,))
            return cursor.rowcount > 0

    def write_documents(self, documents: List[Any]) -> int:
        """Writes Haystack Document protocol items into memory."""
        count = 0
        for doc in documents:
            content = getattr(doc, "content", str(doc))
            metadata = getattr(doc, "metadata", {})
            doc_id = getattr(doc, "id", None)
            source = metadata.get("source", "document_writer")
            self.add_memory(source=source, raw_text=content, metadata=metadata, doc_id=doc_id)
            count += 1
        return count

    def filter_documents(self, filters: Dict[str, Any] = None) -> List[Any]:
        """Filters documents based on metadata criteria."""
        if not filters:
            return []
        cursor = self.pmm.conn.cursor()
        cursor.execute("SELECT id, content, meta FROM events WHERE kind = 'memory_item'")
        rows = cursor.fetchall()
        from pipecatapp.memory import Document
        docs = []
        for event_id, content, meta_str in rows:
            meta = json.loads(meta_str) if meta_str else {}
            metadata = meta.get("metadata", {})
            match = True
            for k, v in filters.items():
                if k == "source" and meta.get("source") != v:
                    match = False
                    break
                elif k in metadata and metadata[k] != v:
                    match = False
                    break
            if match:
                docs.append(Document(id=meta.get("doc_id", str(event_id)), content=content, metadata=metadata))
        return docs
