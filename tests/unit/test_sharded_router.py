import pytest
import os
import asyncio
import tempfile
import httpx
from typing import Dict, Any
from unittest.mock import MagicMock

from pipecatapp.sharded_router import HashRing, ShardedPMMMemoryRouter
from pipecatapp.pmm_memory import PMMMemory

# Standard imports for FastAPI Testing
from fastapi.testclient import TestClient
from pipecatapp.web_server import app
try:
    from api_keys import get_api_key
except ImportError:
    from pipecatapp.api_keys import get_api_key

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
                "node_0": {"sqlite_path": db_path_0, "api_url": "http://10.0.0.0:8000"},
                "node_1": {"sqlite_path": db_path_1, "api_url": "http://10.0.0.1:8000"},
                "node_2": {"sqlite_path": db_path_2, "api_url": "http://10.0.0.2:8000"}
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


# -------------------------------------------------------------------------
# HTTP Mesh Integration & FastAPI Web Endpoint Tests
# -------------------------------------------------------------------------

@pytest.fixture
def mock_httpx_mesh(monkeypatch):
    """
    Patches httpx.Client and httpx.AsyncClient to route remote shard requests
    directly through FastAPI's TestClient, simulating a multi-node mesh network.
    """
    client = TestClient(app)

    # Override FastAPI auth dependency
    app.dependency_overrides[get_api_key] = lambda: "test-key"

    original_post = httpx.Client.post
    original_get = httpx.Client.get
    original_post_async = httpx.AsyncClient.post
    original_get_async = httpx.AsyncClient.get

    def mock_post(self_client, url, *args, **kwargs):
        url_str = str(url)
        if "10.0." in url_str:
            # Extract path: e.g. "http://10.0.0.1:8000/api/memory/sharded/events" -> "/api/memory/sharded/events"
            path = "/" + url_str.split(":8000/")[-1]
            json_data = kwargs.get("json")
            headers = kwargs.get("headers", {})
            resp = client.post(path, json=json_data, headers=headers)

            mock_resp = MagicMock()
            mock_resp.status_code = resp.status_code
            mock_resp.json.return_value = resp.json() if resp.status_code != 204 else {}
            mock_resp.content = resp.content
            mock_resp.raise_for_status = MagicMock()
            return mock_resp
        else:
            return original_post(self_client, url, *args, **kwargs)

    def mock_get(self_client, url, *args, **kwargs):
        url_str = str(url)
        if "10.0." in url_str:
            path = "/" + url_str.split(":8000/")[-1]
            params = kwargs.get("params")
            headers = kwargs.get("headers", {})
            resp = client.get(path, params=params, headers=headers)

            mock_resp = MagicMock()
            mock_resp.status_code = resp.status_code
            mock_resp.json.return_value = resp.json()
            mock_resp.content = resp.content
            mock_resp.raise_for_status = MagicMock()
            return mock_resp
        else:
            return original_get(self_client, url, *args, **kwargs)

    async def mock_post_async(self_client, url, *args, **kwargs):
        url_str = str(url)
        if "10.0." in url_str:
            # Re-use sync helper for simple test execution
            return mock_post(None, url, *args, **kwargs)
        else:
            return await original_post_async(self_client, url, *args, **kwargs)

    async def mock_get_async(self_client, url, *args, **kwargs):
        url_str = str(url)
        if "10.0." in url_str:
            return mock_get(None, url, *args, **kwargs)
        else:
            return await original_get_async(self_client, url, *args, **kwargs)

    # Patch sync client methods
    monkeypatch.setattr(httpx.Client, "post", mock_post)
    monkeypatch.setattr(httpx.Client, "get", mock_get)
    # Patch async client methods
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post_async)
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get_async)

    yield client

    # Cleanup dependency override
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_http_mesh_routing_and_endpoints(mock_httpx_mesh, monkeypatch):
    """
    Tests actual async and sync HTTP mesh routing through FastAPI Web Server endpoints.
    Configures node_0 as a direct local database, and node_1 as a remote HTTP node,
    showing how writes are successfully proxied, dispatched, authenticated, and serialized.
    """
    temp_dir = tempfile.TemporaryDirectory()
    db_path_0 = os.path.join(temp_dir.name, "node_0.db")

    # node_0 is a local DB shard; node_1 is a remote HTTP API node (no local sqlite_path!)
    config = {
        "sharding": {
            "algorithm": "consistent_hash",
            "replica_count": 64,
            "coordinator_node": "node_0",
            "api_key": "test-key",
            "nodes": {
                "node_0": {"sqlite_path": db_path_0, "api_url": "http://10.0.0.0:8000"},
                "node_1": {"api_url": "http://10.0.0.1:8000"}  # remote only!
            }
        }
    }

    router = ShardedPMMMemoryRouter(config=config, local_node_id="node_0")

    # Store router in fastapi app state so endpoints can see it
    app.state.memory_router = router

    try:
        # 1. Test GET /api/memory/sharded/status Endpoint (Category C)
        client = mock_httpx_mesh
        headers = {"Authorization": "Bearer test-key"}
        status_resp = client.get("/api/memory/sharded/status", headers=headers)
        assert status_resp.status_code == 200
        assert status_resp.json()["enabled"] is True
        assert status_resp.json()["local_node_id"] == "node_0"
        assert "node_1" in status_resp.json()["shards"]
        assert "node_1" not in status_resp.json()["local_databases"] # isolated database local db checks

        # 2. Test GET /api/memory/sharded/lookup Endpoint (Category C)
        lookup_resp = client.get("/api/memory/sharded/lookup?key=session_abc", headers=headers)
        assert lookup_resp.status_code == 200
        assert "target_node" in lookup_resp.json()

        # 3. Test Routing conversational events to a REMOTE node over HTTP (Category A)
        # Find a session ID that consistent-hashes to node_1 (the remote shard)
        remote_sess = None
        for i in range(100):
            sess_candidate = f"sess_{i}"
            if router.get_shard_for_session(sess_candidate) == "node_1":
                remote_sess = sess_candidate
                break

        assert remote_sess is not None, "Failed to find session hashing to node_1"

        # Write event asynchronously. Since node_1 is remote, router will issue an HTTP POST to node_1.
        # This HTTP call is intercepted by our patched httpx, routed to FastAPI, which processes it
        # on the "server" node (node_0, since the server has local_node_id='node_0' and is sharded).
        # On the server side, it is written to the local node_0 database!
        target_node = await router.add_event(session_id=remote_sess, kind="user_message", content="Hello remote!")
        assert target_node == "node_1"

        # Verify that node_0's local sqlite db indeed received the event from the API write call
        local_db_events = router.local_memories["node_0"].get_events_sync()
        assert len(local_db_events) == 1
        assert local_db_events[0]["content"] == "Hello remote!"
        assert local_db_events[0]["meta"]["session_id"] == remote_sess

        # 4. Test Reading sharded events from a remote node over HTTP
        # Let's perform a GET call through the router to node_1's API
        retrieved = await router.get_events(session_id=remote_sess)
        assert len(retrieved) == 1
        assert retrieved[0]["content"] == "Hello remote!"

        # 5. Test Coordinator work items API calls over HTTP (Category B)
        # To simulate a worker node calling the coordinator node (node_0), we temporarily set local_node_id="node_1"
        # (meaning we act as the worker, and coordinator is remote node_0)
        worker_router = ShardedPMMMemoryRouter(config=config, local_node_id="node_1")
        # Keep app state memory_router pointing to the server router (node_0)

        # Write task from the worker. Since coord_node (node_0) is not in worker_router's local_memories,
        # it will make an HTTP call to the coordinator node's endpoint.
        task_id = await worker_router.create_work_item(title="Mesh Task", created_by="worker_node_1")
        assert task_id is not None

        # Verify coordinator actually stored it
        task = await router.local_memories["node_0"].get_work_item(task_id)
        assert task is not None
        assert task["title"] == "Mesh Task"
        assert task["created_by"] == "worker_node_1"

        # Update task over HTTP
        updated = await worker_router.update_work_item(task_id, status="completed")
        assert updated is True

        task_updated = await router.local_memories["node_0"].get_work_item(task_id)
        assert task_updated["status"] == "completed"

        # List tasks over HTTP
        tasks_list = await worker_router.list_work_items()
        assert len(tasks_list) == 1
        assert tasks_list[0]["id"] == task_id

    finally:
        app.state.memory_router = None
        router.close()
        temp_dir.cleanup()
