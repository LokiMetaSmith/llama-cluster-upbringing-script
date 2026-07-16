import pytest
import os
import time
from pipecatapp.sharded_pmm_memory import ShardedPMMMemory

SHARDS_PATHS = ["test_shard_0.db", "test_shard_1.db", "test_shard_2.db"]

@pytest.fixture
def sharded_memory():
    # Clean up old shard files
    for path in SHARDS_PATHS:
        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass

    sm = ShardedPMMMemory(db_paths=SHARDS_PATHS)
    yield sm
    sm.close()

    # Clean up files afterwards
    for path in SHARDS_PATHS:
        if os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass

def test_sharding_distribution(sharded_memory):
    # Verify shard indexing
    idx_a = sharded_memory._get_shard_index("keyA")
    idx_b = sharded_memory._get_shard_index("keyB")
    assert 0 <= idx_a < 3
    assert 0 <= idx_b < 3

    # Add different events and check that they go to the correct shards
    sharded_memory.add_event_sync("user_message", "Hello Shard A", meta={"session_id": "session1"})
    sharded_memory.add_event_sync("user_message", "Hello Shard B", meta={"session_id": "session2"})
    sharded_memory.add_event_sync("user_message", "Hello Shard C", meta={"session_id": "session3"})

    # Check total events retrieved via scatter-gather
    events = sharded_memory.get_events_sync(limit=10)
    assert len(events) == 3
    assert all("Hello Shard" in e["content"] for e in events)

def test_work_item_lifecycle(sharded_memory):
    # Create work item
    item_id = sharded_memory.create_work_item_sync(
        title="Deploy Sharded DB Proxy",
        created_by="Jules",
        assignee_id="AgentZero",
        meta={"priority": "high"}
    )
    assert len(item_id) == 8

    # Retrieve work item via point-read routing
    item = sharded_memory.get_work_item_sync(item_id)
    assert item is not None
    assert item["id"] == item_id
    assert item["title"] == "Deploy Sharded DB Proxy"
    assert item["status"] == "open"
    assert item["meta"]["priority"] == "high"

    # Update work item
    success = sharded_memory.update_work_item_sync(item_id, status="completed", meta_update={"done": True})
    assert success

    # Verify updated state
    updated_item = sharded_memory.get_work_item_sync(item_id)
    assert updated_item["status"] == "completed"
    assert updated_item["meta"]["done"] is True

    # List work items (scatter-gather)
    items_list = sharded_memory.list_work_items_sync()
    assert len(items_list) == 1
    assert items_list[0]["id"] == item_id

def test_agent_stats_aggregation(sharded_memory):
    # Create multiple work items across potentially different shards
    for i in range(5):
        sharded_memory.create_work_item_sync(
            title=f"Subtask {i}",
            created_by="Jules",
            assignee_id="WorkerAgent"
        )

    # Let's mark 2 as completed and 1 as failed
    items = sharded_memory.list_work_items_sync(assignee_id="WorkerAgent")
    assert len(items) == 5

    sharded_memory.update_work_item_sync(items[0]["id"], status="completed")
    sharded_memory.update_work_item_sync(items[1]["id"], status="completed")
    sharded_memory.update_work_item_sync(items[2]["id"], status="failed")

    # Get aggregated stats
    stats = sharded_memory.get_agent_stats_sync("WorkerAgent")
    assert stats["total_tasks"] == 5
    assert stats["completed_tasks"] == 2
    assert stats["failed_tasks"] == 1
    assert stats["success_rate"] == 40.0

def test_dlq_sharded_lifecycle(sharded_memory):
    # Enqueue DLQ item
    item_id = sharded_memory.enqueue_dlq_item_sync(
        event_type="network_error",
        payload={"url": "http://[::1]:8080"},
        error_reason="connection refused"
    )
    assert len(item_id) == 8

    # Claim DLQ item
    item = sharded_memory.claim_dlq_item_sync(worker_id="worker_9", supported_types=["network_error"])
    assert item is not None
    assert item["id"] == item_id
    assert item["status"] == "PROCESSING"
    assert item["locked_by"] == "worker_9"

    # Claim - none available
    empty_item = sharded_memory.claim_dlq_item_sync(worker_id="worker_10")
    assert empty_item is None

    # Update DLQ item
    success = sharded_memory.update_dlq_item_sync(item_id, status="SUCCEEDED")
    assert success
