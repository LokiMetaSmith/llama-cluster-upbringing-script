import os
import pytest
from pipecatapp.file_ingestion import LocalFileIngestor

@pytest.fixture
def temp_inbox(tmp_path):
    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    return str(inbox_dir)

@pytest.fixture
def ingestor(temp_inbox):
    return LocalFileIngestor(inbox_dir=temp_inbox)

def test_safe_path(ingestor, temp_inbox):
    safe_file = os.path.join(temp_inbox, "safe.txt")
    # File doesn't need to exist for is_safe_path, it just checks path
    assert ingestor.is_safe_path(safe_file) is True

def test_safe_path_nested(ingestor, temp_inbox):
    safe_file = os.path.join(temp_inbox, "nested", "safe.txt")
    assert ingestor.is_safe_path(safe_file) is True

def test_unsafe_path_traversal(ingestor, temp_inbox):
    # Try to traverse up
    unsafe_file = os.path.join(temp_inbox, "..", "unsafe.txt")
    assert ingestor.is_safe_path(unsafe_file) is False

def test_unsafe_path_absolute(ingestor):
    unsafe_file = "/etc/passwd"
    assert ingestor.is_safe_path(unsafe_file) is False

def test_ingest_file_safe(ingestor, temp_inbox):
    # Create a real file
    safe_file = os.path.join(temp_inbox, "safe.txt")
    with open(safe_file, "w") as f:
        f.write("test")

    assert ingestor.ingest_file(safe_file) is True

def test_ingest_file_unsafe(ingestor, temp_inbox):
    # Try to ingest a file outside the inbox
    parent_dir = os.path.dirname(temp_inbox)
    unsafe_file = os.path.join(parent_dir, "unsafe.txt")
    with open(unsafe_file, "w") as f:
        f.write("test")

    assert ingestor.ingest_file(unsafe_file) is False

def test_process_inbox(ingestor, temp_inbox):
    # Create multiple safe files
    file1 = os.path.join(temp_inbox, "file1.txt")
    file2 = os.path.join(temp_inbox, "file2.txt")
    with open(file1, "w") as f: f.write("1")
    with open(file2, "w") as f: f.write("2")

    ingested = ingestor.process_inbox()
    assert len(ingested) == 2
    assert file1 in ingested
    assert file2 in ingested
