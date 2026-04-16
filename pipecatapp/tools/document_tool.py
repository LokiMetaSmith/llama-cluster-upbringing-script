import os
import json
import sqlite3
import requests
import fitz  # PyMuPDF
import subprocess
import shutil
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import functools
from pipecatapp.utils.command_runner import CommandRunner

class DocumentBackend(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_text(self, document_identifier: str) -> str:
        pass


class PaperlessBackend(DocumentBackend):
    def __init__(self, url: str, token: str):
        self.url = url.rstrip('/')
        self.headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json; version=2"
        }

    def search(self, query: str) -> List[Dict[str, Any]]:
        try:
            response = requests.get(
                f"{self.url}/api/documents/",
                headers=self.headers,
                params={"query": query},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            results = []
            for doc in data.get('results', []):
                results.append({
                    "id": str(doc['id']),
                    "title": doc.get('title', 'Untitled'),
                    "type": "paperless",
                    "snippet": doc.get('content', '')[:200] + "..." if doc.get('content') else ""
                })
            return results
        except Exception as e:
            return [{"error": f"Failed to search Paperless: {str(e)}"}]

    def get_text(self, document_identifier: str) -> str:
        try:
            response = requests.get(
                f"{self.url}/api/documents/{document_identifier}/",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            doc = response.json()
            return doc.get('content', '')
        except Exception as e:
            return f"Error retrieving document from Paperless: {str(e)}"


class LocalDirectoryBackend(DocumentBackend):
    def __init__(self, directory: str):
        self.directory = os.path.realpath(directory)
        if not os.path.exists(self.directory):
            raise ValueError(f"Directory {self.directory} does not exist.")

    def _list_files_git(self) -> Optional[List[str]]:
        """Lists files using git ls-files if possible. Returns None if not a git repo."""
        if not shutil.which("git"):
            return None

        try:
            # Check if inside git repo
            CommandRunner.run(["git", "rev-parse", "--is-inside-work-tree"],
                           cwd=self.directory, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # git ls-files returns paths relative to cwd
            res = CommandRunner.run(["git", "ls-files"], cwd=self.directory, check=True, capture_output=True, text=True)
            files = res.stdout.splitlines()
            return files
        except Exception:
            return None

    def search(self, query: str) -> List[Dict[str, Any]]:
        results = []

        git_files = self._list_files_git()
        if git_files is not None:
            for rel_path in git_files:
                filepath = os.path.join(self.directory, rel_path)
                try:
                    text = self._extract_text(filepath)
                    if query.lower() in text.lower():
                        # Extract a snippet around the first match
                        idx = text.lower().find(query.lower())
                        start = max(0, idx - 50)
                        end = min(len(text), idx + len(query) + 50)
                        snippet = text[start:end]
                        results.append({
                            "id": filepath,
                            "title": os.path.basename(filepath),
                            "type": "local",
                            "snippet": f"...{snippet}..."
                        })
                except Exception as e:
                    # Skip files that can't be read or aren't text/PDF
                    continue
            return results

        for root, _, files in os.walk(self.directory):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    text = self._extract_text(filepath)
                    if query.lower() in text.lower():
                        # Extract a snippet around the first match
                        idx = text.lower().find(query.lower())
                        start = max(0, idx - 50)
                        end = min(len(text), idx + len(query) + 50)
                        snippet = text[start:end]
                        results.append({
                            "id": filepath,
                            "title": file,
                            "type": "local",
                            "snippet": f"...{snippet}..."
                        })
                except Exception as e:
                    # Skip files that can't be read or aren't text/PDF
                    continue
        return results

    def get_text(self, document_identifier: str) -> str:
        filepath = os.path.realpath(document_identifier)
        # Security: Check if path is within allowed directory
        try:
            common = os.path.commonpath([self.directory, filepath])
            if common != self.directory:
                return f"Error: Access denied to {filepath}"
        except ValueError:
            return f"Error: Access denied to {filepath}"

        if not os.path.exists(filepath):
            return f"Error: File {filepath} not found."

        try:
            return self._extract_text(filepath)
        except Exception as e:
            return f"Error extracting text from local file: {str(e)}"

    @functools.lru_cache(maxsize=10)
    def _extract_text(self, filepath: str) -> str:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.pdf':
            text = ""
            with fitz.open(filepath) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        elif ext in ['.txt', '.md', '.csv', '.json', '.xml']:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")


class DocumentTool:
    """A tool for retrieving and searching documents from various backends (e.g., Paperless-ngx, local directory).
    It also supports creating bookmarks/references to specific documents or text blocks.
    """
    def __init__(self, backend_config: Dict[str, Any], db_path: str = "document_bookmarks.sqlite"):
        self.name = "document_tool"
        self.description = "Search, retrieve, and bookmark text documents and PDFs for research."

        self.backend_type = backend_config.get("type")
        if self.backend_type == "paperless":
            self.backend = PaperlessBackend(backend_config["url"], backend_config["token"])
        elif self.backend_type == "local":
            self.backend = LocalDirectoryBackend(backend_config["directory"])
        else:
            raise ValueError(f"Unsupported backend type: {self.backend_type}")

        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT NOT NULL,
                document_title TEXT,
                backend_type TEXT NOT NULL,
                text_block TEXT,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def search(self, query: str) -> str:
        """Searches for documents matching the given query.

        Args:
            query (str): The keyword or phrase to search for.

        Returns:
            str: JSON string of search results (id, title, snippet).
        """
        results = self.backend.search(query)
        return json.dumps(results, indent=2)

    def get_text(self, document_id: str) -> str:
        """Retrieves the full text of a specific document.

        Args:
            document_id (str): The ID or path of the document.

        Returns:
            str: The extracted text of the document.
        """
        return self.backend.get_text(document_id)

    def add_bookmark(self, document_id: str, document_title: str, text_block: str = "", note: str = "") -> str:
        """Creates a bookmark/reference to a document or specific text block.

        Args:
            document_id (str): The ID or path of the document.
            document_title (str): Title of the document for easier reference.
            text_block (str, optional): A specific snippet or block of text from the document.
            note (str, optional): Personal notes about this bookmark.

        Returns:
            str: A confirmation message.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bookmarks (document_id, document_title, backend_type, text_block, note)
                VALUES (?, ?, ?, ?, ?)
            ''', (document_id, document_title, self.backend_type, text_block, note))
            conn.commit()
            bookmark_id = cursor.lastrowid
            conn.close()
            return f"Bookmark successfully added with ID: {bookmark_id}"
        except Exception as e:
            return f"Error adding bookmark: {str(e)}"

    def list_bookmarks(self) -> str:
        """Lists all stored bookmarks.

        Returns:
            str: JSON string of all bookmarks.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM bookmarks ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()

            bookmarks = [dict(row) for row in rows]
            return json.dumps(bookmarks, indent=2)
        except Exception as e:
            return f"Error listing bookmarks: {str(e)}"
