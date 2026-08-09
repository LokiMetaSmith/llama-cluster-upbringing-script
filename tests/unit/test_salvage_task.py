import pytest
import sqlite3
import pickle
import os
from scripts.salvage_task import extract_partial_work

@pytest.fixture
def mock_db_path(tmp_path):
    """Creates a temporary SQLite database populated with test data for execution_log."""
    db_file = tmp_path / "durable_execution_test.db"
    db_path = str(db_file)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the table schema as expected by extract_partial_work
    cursor.execute("""
        CREATE TABLE execution_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flowId TEXT,
            step_sequence INTEGER,
            status TEXT,
            step_name TEXT,
            return_value BLOB,
            internal_context BLOB
        )
    """)

    # Pre-pickled valid data
    valid_ret_1 = pickle.dumps({"result": "success", "count": 1})
    valid_ctx_1 = pickle.dumps({"messages": [{"role": "user", "content": "hello"}]})

    valid_ret_2 = pickle.dumps("final result")
    valid_ctx_2 = pickle.dumps({"messages": [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "hi"}]})

    # Corrupted / Unpickleable data (just random bytes)
    bad_blob = b'\x00\xff\x00\xffnot a pickle string'

    data_to_insert = [
        # Happy Path: Task 'task_1', two COMPLETE steps
        ("task_1", 1, "COMPLETE", "step_one", valid_ret_1, valid_ctx_1),
        ("task_1", 2, "COMPLETE", "step_two", valid_ret_2, valid_ctx_2),

        # Ignored Status: PENDING step, should not be extracted
        ("task_1", 3, "PENDING", "step_three", None, None),

        # Corrupted Data: Task 'task_bad', COMPLETE but unpickleable
        ("task_bad", 1, "COMPLETE", "step_bad", bad_blob, bad_blob),

        # Null Blobs: Task 'task_null', COMPLETE but null blobs
        ("task_null", 1, "COMPLETE", "step_null", None, None)
    ]

    cursor.executemany("""
        INSERT INTO execution_log (flowId, step_sequence, status, step_name, return_value, internal_context)
        VALUES (?, ?, ?, ?, ?, ?)
    """, data_to_insert)

    conn.commit()
    conn.close()

    return db_path

def test_extract_partial_work_happy_path(mock_db_path):
    """Tests that extract_partial_work correctly extracts and unpickles valid steps."""
    steps, last_context = extract_partial_work(mock_db_path, "task_1")

    assert len(steps) == 2

    assert steps[0]["sequence"] == 1
    assert steps[0]["name"] == "step_one"
    assert steps[0]["return_value"] == {"result": "success", "count": 1}

    assert steps[1]["sequence"] == 2
    assert steps[1]["name"] == "step_two"
    assert steps[1]["return_value"] == "final result"

    # last_context should be from the final COMPLETE step extracted
    assert last_context == {"messages": [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "hi"}]}

def test_extract_partial_work_unpickleable(mock_db_path):
    """Tests that unpickleable blobs are handled gracefully."""
    steps, last_context = extract_partial_work(mock_db_path, "task_bad")

    assert len(steps) == 1
    assert steps[0]["sequence"] == 1
    assert steps[0]["name"] == "step_bad"
    assert steps[0]["return_value"] == "<unpickleable>"

    assert last_context is None

def test_extract_partial_work_null_blobs(mock_db_path):
    """Tests that null (None) blobs in DB are handled gracefully."""
    steps, last_context = extract_partial_work(mock_db_path, "task_null")

    assert len(steps) == 1
    assert steps[0]["sequence"] == 1
    assert steps[0]["name"] == "step_null"
    assert steps[0]["return_value"] is None

    assert last_context is None

def test_extract_partial_work_no_results(mock_db_path):
    """Tests that querying for a non-existent task returns empty results."""
    steps, last_context = extract_partial_work(mock_db_path, "task_nonexistent")

    assert len(steps) == 0
    assert steps == []
    assert last_context is None
