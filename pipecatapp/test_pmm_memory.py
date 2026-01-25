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
