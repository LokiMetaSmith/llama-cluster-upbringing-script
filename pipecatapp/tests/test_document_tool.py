import os
import json
import sqlite3
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from pipecatapp.tools.document_tool import DocumentTool, PaperlessBackend, LocalDirectoryBackend

class TestDocumentTool:
    def setup_method(self):
        # Create a temporary database for testing bookmarks
        self.db_fd, self.db_path = tempfile.mkstemp()

    def teardown_method(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    @patch('pipecatapp.tools.document_tool.requests.get')
    def test_paperless_backend_search(self, mock_get):
        # Mock response from Paperless API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {"id": 1, "title": "Test Doc", "content": "This is a test content with the word research in it."}
            ]
        }
        mock_get.return_value = mock_response

        config = {
            "type": "paperless",
            "url": "http://localhost:8000",
            "token": "testtoken123"
        }
        tool = DocumentTool(backend_config=config, db_path=self.db_path)

        results_json = tool.search("research")
        results = json.loads(results_json)

        assert len(results) == 1
        assert results[0]["title"] == "Test Doc"
        assert results[0]["id"] == "1"
        assert "This is a test content" in results[0]["snippet"]

        mock_get.assert_called_with(
            "http://localhost:8000/api/documents/",
            headers={"Authorization": "Token testtoken123", "Accept": "application/json; version=2"},
            params={"query": "research"},
            timeout=10
        )

    @patch('pipecatapp.tools.document_tool.requests.get')
    def test_paperless_backend_get_text(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": "Full document content here."
        }
        mock_get.return_value = mock_response

        config = {
            "type": "paperless",
            "url": "http://localhost:8000",
            "token": "testtoken123"
        }
        tool = DocumentTool(backend_config=config, db_path=self.db_path)

        text = tool.get_text("1")
        assert text == "Full document content here."

        mock_get.assert_called_with(
            "http://localhost:8000/api/documents/1/",
            headers={"Authorization": "Token testtoken123", "Accept": "application/json; version=2"},
            timeout=10
        )

    def test_local_backend_search_and_get_text(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a sample text file
            test_file_path = os.path.join(temp_dir, "test.txt")
            with open(test_file_path, "w") as f:
                f.write("This is a local text file for testing research capabilities.")

            config = {
                "type": "local",
                "directory": temp_dir
            }
            tool = DocumentTool(backend_config=config, db_path=self.db_path)

            # Test search
            results_json = tool.search("research")
            results = json.loads(results_json)

            assert len(results) == 1
            assert results[0]["title"] == "test.txt"
            assert "testing research capabilities" in results[0]["snippet"]

            # Test get text
            text = tool.get_text(test_file_path)
            assert text == "This is a local text file for testing research capabilities."

    def test_local_backend_path_traversal(self):
         with tempfile.TemporaryDirectory() as temp_dir:
            config = {
                "type": "local",
                "directory": temp_dir
            }
            tool = DocumentTool(backend_config=config, db_path=self.db_path)

            # Attempt to access a file outside the directory
            result = tool.get_text("/etc/passwd")
            assert "Access denied" in result

    def test_bookmarks(self):
        config = {
            "type": "local",
            "directory": "/tmp"
        }
        tool = DocumentTool(backend_config=config, db_path=self.db_path)

        # Add a bookmark
        tool.add_bookmark(
            document_id="/tmp/test.pdf",
            document_title="Test PDF",
            text_block="Important concept: XYZ",
            note="Read this later"
        )

        # List bookmarks
        bookmarks_json = tool.list_bookmarks()
        bookmarks = json.loads(bookmarks_json)

        assert len(bookmarks) == 1
        assert bookmarks[0]["document_id"] == "/tmp/test.pdf"
        assert bookmarks[0]["document_title"] == "Test PDF"
        assert bookmarks[0]["backend_type"] == "local"
        assert bookmarks[0]["text_block"] == "Important concept: XYZ"
        assert bookmarks[0]["note"] == "Read this later"
