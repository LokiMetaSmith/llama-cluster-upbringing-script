import pytest
import os
import sqlite3
import json
import time
from pipecatapp.pmm_memory import PMMMemory

DB_PATH = "test_unit_pmm.db"

@pytest.fixture
def memory():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except:
            pass
    mem = PMMMemory(db_path=DB_PATH)
    yield mem
    mem.close()
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except:
            pass

def test_dlq_lifecycle(memory):
    # Enqueue
    item_id = memory.enqueue_dlq_item_sync(
        event_type="error",
        payload={"a": 1},
        error_reason="fail"
    )
    assert item_id is not None

    # Claim - success
    item = memory.claim_dlq_item_sync(worker_id="w1", supported_types=["error"])
    assert item is not None
    assert item['id'] == item_id
    assert item['status'] == 'PROCESSING'
    assert item['locked_by'] == 'w1'

    # Claim - empty/locked
    item2 = memory.claim_dlq_item_sync(worker_id="w2", supported_types=["error"])
    assert item2 is None

    # Update
    success = memory.update_dlq_item_sync(item_id, status="SUCCEEDED")
    assert success

    # Verify
    cursor = memory.conn.cursor()
    cursor.execute("SELECT status FROM dlq WHERE id = ?", (item_id,))
    assert cursor.fetchone()[0] == 'SUCCEEDED'

def test_dlq_filtering(memory):
    memory.enqueue_dlq_item_sync("typeA", {}, "err")
    memory.enqueue_dlq_item_sync("typeB", {}, "err")

    # Claim only typeA
    item = memory.claim_dlq_item_sync("w1", supported_types=["typeA"])
    assert item['event_type'] == "typeA"

    # Claim only typeB
    item = memory.claim_dlq_item_sync("w1", supported_types=["typeB"])
    assert item['event_type'] == "typeB"

def test_dlq_retry_mechanics(memory):
    # Test retry logic: Transient error should allow retries
    item_id = memory.enqueue_dlq_item_sync("typeA", {}, "err")

    # Claim
    item = memory.claim_dlq_item_sync("w1")
    assert item is not None
    assert item['retry_count'] == 0

    # Update to PENDING with retry count increment
    memory.update_dlq_item_sync(item_id, status="PENDING", result="transient error", increment_retry=True)

    # Verify retry count increased and status is PENDING
    cursor = memory.conn.cursor()
    cursor.execute("SELECT retry_count, status FROM dlq WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    assert row[0] == 1
    assert row[1] == 'PENDING'

    # Claim again
    item_retry = memory.claim_dlq_item_sync("w2")
    assert item_retry is not None
    assert item_retry['id'] == item_id

def test_sync_work_items_sync(memory):
    # Setup initial remote items
    now = time.time()
    remote_items = [
        {
            'id': 'item_1',
            'title': 'Task 1',
            'status': 'open',
            'assignee_id': 'agent_1',
            'created_by': 'user_1',
            'created_at': now,
            'updated_at': now,
            'parent_id': None,
            'meta': {},
            'validation_results': {}
        },
        {
            'id': 'item_2',
            'title': 'Task 2',
            'status': 'open',
            'assignee_id': 'agent_2',
            'created_by': 'user_2',
            'created_at': now,
            'updated_at': now,
            'parent_id': None,
            'meta': {},
            'validation_results': {}
        }
    ]

    # First sync (inserts)
    merged = memory.sync_work_items_sync(remote_items)
    assert len(merged) == 2
    assert {m['id'] for m in merged} == {'item_1', 'item_2'}

    # Verify database contents
    item1 = memory.get_work_item_sync('item_1')
    assert item1 is not None
    assert item1['title'] == 'Task 1'

    # Second sync with older update (no-op) and newer update
    remote_updates = [
        {
            'id': 'item_1',
            'title': 'Task 1 Older',
            'status': 'open',
            'assignee_id': 'agent_1',
            'created_by': 'user_1',
            'created_at': now,
            'updated_at': now - 10.0, # older, should not update
            'parent_id': None,
            'meta': {},
            'validation_results': {}
        },
        {
            'id': 'item_2',
            'title': 'Task 2 Newer',
            'status': 'completed',
            'assignee_id': 'agent_2',
            'created_by': 'user_2',
            'created_at': now,
            'updated_at': now + 10.0, # newer, should update
            'parent_id': None,
            'meta': {},
            'validation_results': {}
        }
    ]

    merged2 = memory.sync_work_items_sync(remote_updates)
    assert len(merged2) == 1
    assert merged2[0]['id'] == 'item_2'
    assert merged2[0]['title'] == 'Task 2 Newer'

    # Verify db state
    item1_after = memory.get_work_item_sync('item_1')
    assert item1_after['title'] == 'Task 1' # remained unchanged

    item2_after = memory.get_work_item_sync('item_2')
    assert item2_after['title'] == 'Task 2 Newer'
    assert item2_after['status'] == 'completed'

    # Sync with duplicate item IDs in the list
    duplicate_items = [
        {
            'id': 'item_3',
            'title': 'Task 3 Initial',
            'status': 'open',
            'assignee_id': 'agent_3',
            'created_by': 'user_3',
            'created_at': now,
            'updated_at': now,
            'parent_id': None,
            'meta': {},
            'validation_results': {}
        },
        {
            'id': 'item_3',
            'title': 'Task 3 Updated',
            'status': 'in_progress',
            'assignee_id': 'agent_3',
            'created_by': 'user_3',
            'created_at': now,
            'updated_at': now + 5.0,
            'parent_id': None,
            'meta': {},
            'validation_results': {}
        }
    ]

    merged3 = memory.sync_work_items_sync(duplicate_items)
    assert len(merged3) == 2
    assert merged3[0]['title'] == 'Task 3 Initial'
    assert merged3[1]['title'] == 'Task 3 Updated'

    item3_after = memory.get_work_item_sync('item_3')
    assert item3_after['title'] == 'Task 3 Updated'
    assert item3_after['status'] == 'in_progress'
