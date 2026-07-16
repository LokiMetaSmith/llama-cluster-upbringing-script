import pytest
import os
import asyncio
import tempfile
from typing import Dict, Any

from pipecatapp.sharded_router import HashRing, ShardedPMMMemoryRouter
from pipecatapp.pmm_memory import PMMMemory

def test_hash_ring_consistent_mapping():
    """Tests basic HashRing addition, removal, and consistent lookup mapping."""
    shards = ["node_0", "node_1", "node_2"]
    ring = HashRing(shards=shards, replica_count=10)

    # Verify exact consistency
    for key in ["session_abc", "session_def", "user_123", "task_999"]:
        target1 = ring.get_shard(key)
        target2 = ring.get_shard(key)
        assert target1 is not None
        assert target1 in shards
        assert target1 == target2  # Consistent lookup

    # Verify distribution properties (at least more than 1 shard mapped to keys)
    mapped_shards = set()
    for i in range(100):
        mapped_shards.add(ring.get_shard(f"session_key_{i}"))
    assert len(mapped_shards) > 1


def test_hash_ring_removal():
    """Tests that removing a shard from the HashRing stops key mapping to it."""
    shards = ["node_a", "node_b"]
    ring = HashRing(shards=shards, replica_count=5)

    # Count how many of 50 keys map to node_b
    mapped_to_b = 0
    for i in range(50):
        if ring.get_shard(f"key_{i}") == "node_b":
            mapped_to_b += 1

    assert mapped_to_b > 0

    # Remove node_b
    ring.remove_shard("node_b")

    # Ensure no keys map to node_b anymore
    for i in range(50):
        assert ring.get_shard(f"key_{i}") == "node_a"


@pytest.fixture
def temp_sharded_router_and_files():
    """Fixture that provisions temporary SQLite databases and a routing configuration."""
    temp_dir = tempfile.TemporaryDirectory()
    db_path_0 = os.path.join(temp_dir.name, "node_0.db")
    db_path_1 = os.path.join(temp_dir.name, "node_1.db")
    db_path_2 = os.path.join(temp_dir.name, "node_2.db")

    config = {
        "sharding": {
            "algorithm": "consistent_hash",
            "replica_count": 64,
            "coordinator_node": "node_0",
            "nodes": {
                "node_0": {"sqlite_path": db_path_0},
                "node_1": {"sqlite_path": db_path_1},
                "node_2": {"sqlite_path": db_path_2}
            }
        }
    }

    router = ShardedPMMMemoryRouter(config=config, local_node_id="node_0")

    yield router, db_path_0, db_path_1, db_path_2

    # Cleanup
    router.close()
    temp_dir.cleanup()


def test_sharded_events_routing(temp_sharded_router_and_files):
    """Tests that conversational events are sharded and routed based on session_id."""
    router, db_path_0, db_path_1, db_path_2 = temp_sharded_router_and_files

    # Route a series of events across different sessions
    sessions = ["sess_0", "sess_1", "sess_2", "sess_3", "sess_4"]
    routed_nodes = {}

    for sess in sessions:
        node = router.add_event_sync(session_id=sess, kind="user_message", content=f"Hello from {sess}")
        routed_nodes[sess] = node
        assert node in ["node_0", "node_1", "node_2"]

    # Verify that the events exist ONLY on their respective shard databases
    for sess, node in routed_nodes.items():
        # Retrieve through router
        retrieved = router.get_events_sync(session_id=sess, limit=5)
        assert len(retrieved) == 1
        assert retrieved[0]["content"] == f"Hello from {sess}"
        assert retrieved[0]["meta"]["session_id"] == sess

        # Access the underlying PMMMemory object directly to confirm isolation
        for other_node, pmm in router.local_memories.items():
            direct_events = pmm.get_events_sync(limit=10)
            direct_sessions = [e["meta"].get("session_id") for e in direct_events if "session_id" in e.get("meta", {})]
            if other_node == node:
                assert sess in direct_sessions
            else:
                assert sess not in direct_sessions


@pytest.mark.asyncio
async def test_sharded_events_routing_async(temp_sharded_router_and_files):
    """Tests asynchronous event routing intercepts."""
    router, _, _, _ = temp_sharded_router_and_files

    session_id = "async_sess_123"
    target_node = router.get_shard_for_session(session_id)

    await router.add_event(session_id=session_id, kind="assistant_message", content="Async Hello!")

    # Retrieve async
    retrieved = await router.get_events(session_id=session_id)
    assert len(retrieved) == 1
    assert retrieved[0]["content"] == "Async Hello!"
    assert retrieved[0]["meta"]["session_id"] == session_id


def test_two_tier_ledger_consensus(temp_sharded_router_and_files):
    """
    Tests that work items and DLQ entries are centralized entirely on the
    coordinator node (node_0), guaranteeing global consensus and transactional consistency,
    even if events are sharded.
    """
    router, db_path_0, db_path_1, db_path_2 = temp_sharded_router_and_files

    # Create tasks via the sharded router
    task_id_1 = router.create_work_item_sync(title="Fix core mesh", created_by="manager_agent")
    task_id_2 = router.create_work_item_sync(title="Optimize memory routing", created_by="technician_agent")

    # Enqueue a DLQ item
    dlq_id = router.enqueue_dlq_item_sync(event_type="agent_alert", payload={"alert": "OOM_WARN"}, error_reason="RAM > 90%")

    assert task_id_1 is not None
    assert task_id_2 is not None
    assert dlq_id is not None

    # Verify the coordinator shard (node_0) has the work items and DLQ entries
    coord_items = router.local_memories["node_0"].list_work_items_sync()
    assert len(coord_items) == 2
    coord_titles = [item["title"] for item in coord_items]
    assert "Fix core mesh" in coord_titles
    assert "Optimize memory routing" in coord_titles

    claimed_dlq = router.claim_dlq_item_sync(worker_id="worker_a", supported_types=["agent_alert"])
    assert claimed_dlq is not None
    assert claimed_dlq["id"] == dlq_id
    assert claimed_dlq["payload"]["alert"] == "OOM_WARN"

    # Verify that node_1 and node_2 databases are completely EMPTY of tasks and DLQ items
    for other_node in ["node_1", "node_2"]:
        other_items = router.local_memories[other_node].list_work_items_sync()
        assert len(other_items) == 0

        other_claimed = router.local_memories[other_node].claim_dlq_item_sync(worker_id="worker_a")
        assert other_claimed is None


@pytest.mark.asyncio
async def test_two_tier_ledger_consensus_async(temp_sharded_router_and_files):
    """Tests asynchronous task and DLQ intercepts on the coordinator node."""
    router, _, _, _ = temp_sharded_router_and_files

    # Create work item async
    item_id = await router.create_work_item(title="Async Task", created_by="manager_agent")
    assert item_id is not None

    # Get work item async
    item = await router.get_work_item(item_id)
    assert item is not None
    assert item["title"] == "Async Task"

    # List async
    items = await router.list_work_items()
    assert len(items) == 1
    assert items[0]["id"] == item_id

    # Update work item async
    updated = await router.update_work_item(item_id, status="completed")
    assert updated is True

    item_updated = await router.get_work_item(item_id)
    assert item_updated["status"] == "completed"

    # DLQ async
    dlq_id = await router.enqueue_dlq_item(event_type="test_event", payload={"foo": "bar"}, error_reason="test")
    assert dlq_id is not None

    claimed = await router.claim_dlq_item(worker_id="async_worker")
    assert claimed is not None
    assert claimed["id"] == dlq_id

    updated_dlq = await router.update_dlq_item(dlq_id, status="RESOLVED")
    assert updated_dlq is True
