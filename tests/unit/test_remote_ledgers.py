import pytest
import time
import json
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Assuming pipecatapp is in PYTHONPATH
from pipecatapp.pmm_memory import PMMMemory
from pipecatapp.pmm_memory_client import PMMMemoryClient

@pytest.fixture
def memory_db(tmp_path):
    db_path = tmp_path / "test_memory.db"
    mem = PMMMemory(db_path=str(db_path))
    yield mem
    mem.close()

def test_merge_logic(memory_db):
    """Test the PMMMemory.sync_work_items_sync logic"""
    # 1. Create a local item
    t1 = time.time()
    local_id = memory_db.create_work_item_sync(title="Local Item", created_by="user1")

    local_item = memory_db.get_work_item_sync(local_id)
    assert local_item is not None

    # 2. Sync a remote item that is NEW
    t2 = t1 + 10
    remote_new_item = {
        "id": "remote_id_1",
        "title": "Remote Item",
        "status": "open",
        "assignee_id": None,
        "created_by": "user2",
        "created_at": t2,
        "updated_at": t2,
        "parent_id": None,
        "meta": {"remote": True},
        "validation_results": {}
    }

    merged = memory_db.sync_work_items_sync([remote_new_item])
    assert len(merged) == 1

    fetched_remote = memory_db.get_work_item_sync("remote_id_1")
    assert fetched_remote is not None
    assert fetched_remote["title"] == "Remote Item"

    # 3. Sync an update to the local item
    t3 = t1 + 20
    remote_update_local = dict(local_item)
    remote_update_local["status"] = "in_progress"
    remote_update_local["updated_at"] = t3

    merged = memory_db.sync_work_items_sync([remote_update_local])
    assert len(merged) == 1

    fetched_local = memory_db.get_work_item_sync(local_id)
    assert fetched_local["status"] == "in_progress"
    assert fetched_local["updated_at"] == t3

    # 4. Sync an OLDER update to the local item (should be ignored)
    t4 = t1 + 5
    stale_update = dict(local_item)
    stale_update["status"] = "done"
    stale_update["updated_at"] = t4

    merged = memory_db.sync_work_items_sync([stale_update])
    assert len(merged) == 0  # Should not be updated

    fetched_local_again = memory_db.get_work_item_sync(local_id)
    assert fetched_local_again["status"] == "in_progress"  # Still in progress





from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_client_push_pull():
    client = PMMMemoryClient(base_url="http://fake-url:8000")

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = MockClient.return_value
        mock_client_instance.__aenter__.return_value = mock_client_instance

        mock_resp = MagicMock()
        mock_resp.json.return_value = [{"id": "item1"}]
        mock_resp.raise_for_status.return_value = None

        async def mock_get(*args, **kwargs):
            return mock_resp

        mock_client_instance.get = mock_get

        items = await client.get_work_items_since(0.0)
        assert len(items) == 1
        assert items[0]["id"] == "item1"

        async def mock_post(*args, **kwargs):
            return mock_resp

        mock_client_instance.post = mock_post

        success = await client.push_work_items([{"id": "item1"}])
        assert success is True
