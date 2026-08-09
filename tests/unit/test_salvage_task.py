import sqlite3
import os
import pytest

from scripts.salvage_task import find_stalled_tasks

def setup_db(db_path, records):
    """Helper to setup a temporary database with specific records."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE execution_log (
            flowId TEXT,
            step_sequence INTEGER,
            status TEXT,
            step_name TEXT,
            return_value BLOB,
            internal_context BLOB
        )
    """)
    if records:
        cursor.executemany(
            "INSERT INTO execution_log (flowId, step_sequence, status) VALUES (?, ?, ?)",
            records
        )
    conn.commit()
    conn.close()

def test_find_stalled_tasks_no_db(tmp_path):
    db_path = str(tmp_path / "nonexistent.db")
    result = find_stalled_tasks(db_path)
    assert result == []

def test_find_stalled_tasks_empty_db(tmp_path):
    db_path = str(tmp_path / "empty.db")
    setup_db(db_path, [])
    result = find_stalled_tasks(db_path)
    assert result == []

def test_find_stalled_tasks_completed_tasks(tmp_path):
    db_path = str(tmp_path / "completed.db")
    records = [
        ("task1", 1, "COMPLETE"),
        ("task1", 2, "COMPLETE"),
        ("task2", 1, "COMPLETE")
    ]
    setup_db(db_path, records)
    result = find_stalled_tasks(db_path)
    assert result == []

def test_find_stalled_tasks_pending_tasks(tmp_path):
    db_path = str(tmp_path / "pending.db")
    records = [
        ("task1", 1, "COMPLETE"),
        ("task1", 2, "PENDING"),
        ("task2", 1, "COMPLETE"),
        ("task3", 1, "PENDING")
    ]
    setup_db(db_path, records)
    result = find_stalled_tasks(db_path)
    assert set(result) == {"task1", "task3"}

def test_find_stalled_tasks_mixed_tasks(tmp_path):
    db_path = str(tmp_path / "mixed.db")
    # task1: latest is COMPLETE
    # task2: latest is PENDING
    records = [
        ("task1", 1, "COMPLETE"),
        ("task1", 2, "PENDING"),
        ("task1", 3, "COMPLETE"),
        ("task2", 1, "COMPLETE"),
        ("task2", 2, "PENDING")
    ]
    setup_db(db_path, records)
    result = find_stalled_tasks(db_path)
    assert result == ["task2"]
