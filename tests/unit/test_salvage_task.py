import sys
import os
import sqlite3
import pytest

from scripts.salvage_task import find_stalled_tasks
# Add scripts directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))

from salvage_task import synthesize_summary, find_stalled_tasks

# ==========================================
# Tests for synthesize_summary
# ==========================================

def test_synthesize_summary_empty():
    assert synthesize_summary([], None) == "No completed steps found."
    assert synthesize_summary(None, {}) == "No completed steps found."

def test_synthesize_summary_standard_steps():
    completed_steps = [
        {"sequence": 1, "name": "step1", "return_value": "success"},
        {"sequence": 2, "name": "step2", "return_value": {"key": "value"}},
    ]
    summary = synthesize_summary(completed_steps, None)
    assert "### Executed Steps" in summary
    assert "- Step 1 (step1):" in summary
    assert "Result: success" in summary
    assert "- Step 2 (step2):" in summary
    assert "Result: {'key': 'value'}" in summary

def test_synthesize_summary_truncate_long_return_value():
    long_ret_val = "A" * 250
    completed_steps = [
        {"sequence": 1, "name": "step_long", "return_value": long_ret_val},
    ]
    summary = synthesize_summary(completed_steps, None)

    assert "Result: " + ("A" * 200) + "..." in summary
    # 200 As + "..." = 203 chars, plus "  Result: " prefix + \n suffix
    # So the total printed string is bounded
    assert len(summary) < 300

def test_synthesize_summary_with_context_messages():
    completed_steps = [{"sequence": 1, "name": "step1", "return_value": "done"}]
    last_context = {
        "messages": [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "world"},
        ]
    }
    summary = synthesize_summary(completed_steps, last_context)

    assert "### Final Conversation Context" in summary
    assert "- user: hello" in summary
    assert "- assistant: world" in summary

def test_synthesize_summary_truncate_long_message_content():
    completed_steps = [{"sequence": 1, "name": "step1", "return_value": "done"}]
    long_msg = "B" * 200
    last_context = {
        "messages": [
            {"role": "user", "content": long_msg},
        ]
    }
    summary = synthesize_summary(completed_steps, last_context)

    assert "- user: " + ("B" * 150) + "..." in summary

def test_synthesize_summary_slice_last_3_messages():
    completed_steps = [{"sequence": 1, "name": "step1", "return_value": "done"}]
    last_context = {
        "messages": [
            {"role": "user", "content": "msg1"},
            {"role": "assistant", "content": "msg2"},
            {"role": "user", "content": "msg3"},
            {"role": "assistant", "content": "msg4"},
            {"role": "user", "content": "msg5"},
        ]
    }
    summary = synthesize_summary(completed_steps, last_context)

    # msg1 and msg2 should be dropped
    assert "msg1" not in summary
    assert "msg2" not in summary

    # msg3, msg4, and msg5 should be included
    assert "msg3" in summary
    assert "msg4" in summary
    assert "msg5" in summary

def test_synthesize_summary_missing_message_keys():
    completed_steps = [{"sequence": 1, "name": "step1", "return_value": "done"}]
    last_context = {
        "messages": [
            # missing role
            {"content": "something"},
            # missing content
            {"role": "user"},
        ]
    }
    summary = synthesize_summary(completed_steps, last_context)

    assert "- unknown: something" in summary
    assert "- user: " in summary # content defaults to empty string

# ==========================================
# Tests for find_stalled_tasks
# ==========================================

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

# ==========================================
# Tests for extract_partial_work
# ==========================================

import pickle

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

    # Note: Use `execution_log` so it correctly mimics original tables
    cursor.executemany("""
        INSERT INTO execution_log (flowId, step_sequence, status, step_name, return_value, internal_context)
        VALUES (?, ?, ?, ?, ?, ?)
    """, data_to_insert)

    conn.commit()
    conn.close()

    return db_path

def test_extract_partial_work_happy_path(mock_db_path):
    """Tests that extract_partial_work correctly extracts and unpickles valid steps."""
    from scripts.salvage_task import extract_partial_work
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
    from scripts.salvage_task import extract_partial_work
    steps, last_context = extract_partial_work(mock_db_path, "task_bad")

    assert len(steps) == 1
    assert steps[0]["sequence"] == 1
    assert steps[0]["name"] == "step_bad"
    assert steps[0]["return_value"] == "<unpickleable>"

    assert last_context is None

def test_extract_partial_work_null_blobs(mock_db_path):
    """Tests that null (None) blobs in DB are handled gracefully."""
    from scripts.salvage_task import extract_partial_work
    steps, last_context = extract_partial_work(mock_db_path, "task_null")

    assert len(steps) == 1
    assert steps[0]["sequence"] == 1
    assert steps[0]["name"] == "step_null"
    assert steps[0]["return_value"] is None

    assert last_context is None

def test_extract_partial_work_no_results(mock_db_path):
    """Tests that querying for a non-existent task returns empty results."""
    from scripts.salvage_task import extract_partial_work
    steps, last_context = extract_partial_work(mock_db_path, "task_nonexistent")

    assert len(steps) == 0
    assert steps == []
    assert last_context is None
