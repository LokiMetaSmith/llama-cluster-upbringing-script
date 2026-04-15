import pytest
import os
import json
import sqlite3
from unittest.mock import patch, MagicMock

# mock fitz before import
import sys
sys.modules['fitz'] = MagicMock()
sys.modules['requests'] = MagicMock()

from pipecatapp.tools.document_tool import DocumentTool, LocalDirectoryBackend, PaperlessBackend

def test_paperless_backend():
    backend = PaperlessBackend("http://mock-paperless", "token")

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": [{"id": 1, "title": "Doc", "content": "Text"}]}
        mock_get.return_value = mock_response

        res = backend.search("query")
        assert len(res) == 1
        assert res[0]["title"] == "Doc"

def test_local_directory_backend(tmp_path):
    d = tmp_path / "docs"
    d.mkdir()
    f = d / "test.txt"
    f.write_text("hello world")

    backend = LocalDirectoryBackend(str(d))
    res = backend.search("hello")
    assert len(res) == 1
    assert "test.txt" in res[0]["title"]

    text = backend.get_text(str(f))
    assert text == "hello world"

def test_document_tool_initialization_local(tmp_path):
    db_path = tmp_path / "test.db"
    tool = DocumentTool({"type": "local", "directory": str(tmp_path)}, db_path=str(db_path))
    assert tool.name == "document_tool"
    assert tool.backend_type == "local"

def test_document_tool_bookmarks(tmp_path):
    db_path = tmp_path / "test.db"
    tool = DocumentTool({"type": "local", "directory": str(tmp_path)}, db_path=str(db_path))

    res = tool.add_bookmark("doc1", "Doc 1", "block", "note")
    assert "Bookmark successfully added" in res

    bookmarks_json = tool.list_bookmarks()
    bookmarks = json.loads(bookmarks_json)
    assert len(bookmarks) == 1
    assert bookmarks[0]["document_id"] == "doc1"
