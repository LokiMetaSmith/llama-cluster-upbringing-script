import sys
from unittest.mock import MagicMock

# Dynamic mock for missing imports during test collection to avoid importing heavy dependencies
class MockModule(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

# Mock packages that might not be fully installed in the test environment
for mod in [
    'extism', 'aiohttp', 'fitz', 'consul', 'consul2', 'prometheus_client',
    'redis', 'torch', 'torchvision', 'ultralytics', 'sentence_transformers',
    'transformers', 'chromadb', 'atproto', 'autoloop', 'watchdog', 'tree_sitter',
    'tree-sitter', 'llm_sandbox', 'opencode_ai', 'llmrouter_lib', 'rank_bm25',
    'podman', 'tenacity', 'backon', 'fastapi', 'uvicorn', 'websockets', 'wikipedia'
]:
    sys.modules[mod] = MockModule()

import os
import sqlite3
import tempfile
import pytest
from pipecatapp.tools.schema_mapper_tool import SchemaMapperTool

class TestSchemaMapperTool:
    def setup_method(self):
        # Create a temp directory for DB files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_store.db")
        self._setup_test_db(self.db_path)

    def teardown_method(self):
        self.temp_dir.cleanup()

    def _setup_test_db(self, db_path):
        """Creates a sample SQLite database with tables, data, and keys."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Table 1: Users
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Table 2: Products
        cursor.execute("""
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL DEFAULT 0.0
            );
        """)

        # Table 3: Orders (Declared Foreign Key to users, but NOT products)
        cursor.execute("""
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)

        # Insert some dummy records
        cursor.execute("INSERT INTO users (username, email) VALUES ('alice', 'alice@test.com');")
        cursor.execute("INSERT INTO users (username, email) VALUES ('bob', 'bob@test.com');")

        cursor.execute("INSERT INTO products (name, price) VALUES ('Widget A', 10.99);")
        cursor.execute("INSERT INTO products (name, price) VALUES ('Widget B', 24.50);")

        cursor.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (1, 1, 2);")
        cursor.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (2, 2, 1);")

        conn.commit()
        conn.close()

    def test_direct_db_path_mapping(self):
        """Tests that SchemaMapperTool correctly profiles a targeted SQLite database."""
        tool = SchemaMapperTool()
        report = tool.execute({"db_path": self.db_path, "sample_rows": 2})

        # Check title and basic metadata
        assert "# Database Profile: `test_store.db`" in report
        assert "users" in report
        assert "products" in report
        assert "orders" in report

        # Check row count reflections
        assert "**Row Count:** 2" in report

        # Check column reflections
        assert "username" in report
        assert "quantity" in report
        assert "Widget A" in report

        # Check relationship/join analysis
        # 1. Declared Foreign Key user_id -> users
        assert "`orders` ➔ `users` (via `user_id` ➔ `id`, source: declared foreign key)" in report
        # 2. Heuristic Foreign Key product_id -> products (which has PK product_id)
        assert "`orders` ➔ `products`" in report
        assert "product_id" in report

    def test_auto_discovery(self):
        """Tests that SchemaMapperTool auto-discovers databases in a directory structure."""
        tool = SchemaMapperTool()
        # Scan the temp directory
        report = tool.execute({"scan_dir": self.temp_dir.name})

        assert "# Database Profile: `test_store.db`" in report
        assert "Discovered Tables:" in report

    def test_no_databases_found(self):
        """Tests tool response when scanning a directory with no databases."""
        tool = SchemaMapperTool()
        empty_dir = tempfile.mkdtemp()
        try:
            report = tool.execute({"scan_dir": empty_dir})
            assert "No SQLite database files" in report
        finally:
            os.rmdir(empty_dir)

    def test_nonexistent_direct_path(self):
        """Tests tool response for a non-existent direct database path."""
        tool = SchemaMapperTool()
        report = tool.execute({"db_path": "non_existent_file.db"})
        assert "Error: Database file not found at path" in report

    def test_empty_database(self):
        """Tests profiling an empty database with no tables."""
        empty_db_path = os.path.join(self.temp_dir.name, "empty.db")
        # Create empty file
        conn = sqlite3.connect(empty_db_path)
        conn.close()

        tool = SchemaMapperTool()
        report = tool.execute({"db_path": empty_db_path})

        assert "empty.db" in report
        assert "The database has no user-defined tables." in report
