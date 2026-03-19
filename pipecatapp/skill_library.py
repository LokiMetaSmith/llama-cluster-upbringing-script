import json
import os
import logging
import sqlite3

logger = logging.getLogger("SkillLibrary")

class SkillLibrary:
    """A simple file-based skill library for persisting successful agent task steps."""
    def __init__(self, db_path="skills.sqlite"):
        self.db_path = db_path
        self._init_sqlite()

    def _init_sqlite(self):
        """Initializes the SQLite database and schema."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def save_skill(self, name: str, description: str, content: str) -> bool:
        """Saves a skill to the database. Updates if it already exists."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO skills (name, description, content)
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    description=excluded.description,
                    content=excluded.content
            ''', (name, description, content))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save skill '{name}': {e}")
            return False

    def search_skills(self, query: str) -> list[dict]:
        """Searches skills matching the query in name or description."""
        try:
            cursor = self.conn.cursor()
            # simple LIKE search
            search_pattern = f"%{query}%"
            cursor.execute('''
                SELECT name, description, content FROM skills
                WHERE name LIKE ? OR description LIKE ? OR content LIKE ?
            ''', (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to search skills for query '{query}': {e}")
            return []

    def get_skill(self, name: str) -> dict:
        """Retrieves a specific skill by name."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT name, description, content FROM skills
                WHERE name = ?
            ''', (name,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve skill '{name}': {e}")
            return None
