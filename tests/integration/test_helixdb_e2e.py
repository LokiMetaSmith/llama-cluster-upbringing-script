import pytest
import os
import json
from unittest.mock import patch, MagicMock

# E2E test simulating inserting a node via the MCP service tools
# and retrieving it via the HelixBackend.

from pipecatapp.memory_graph_service.helix_server import store_memory
from pipecatapp.memory_backends_impl.helix_backend import HelixMemoryBackend

@pytest.mark.asyncio
@patch('pipecatapp.memory_graph_service.helix_server.httpx.AsyncClient.post')
@patch('pipecatapp.memory_backends_impl.helix_client.requests.post')
async def test_helixdb_e2e_insert_and_retrieve(mock_sync_post, mock_async_post):
    # Setup mock for MCP insert
    mock_async_resp = MagicMock()
    mock_async_resp.json.return_value = {"mem": [{"title": "E2E Test Node", "content": "This is a test node"}]}
    mock_async_resp.raise_for_status.return_value = None
    mock_async_post.return_value = mock_async_resp

    # 1. Insert via the MCP tool
    result_msg = await store_memory(
        content="This is a test node",
        memory_type="test",
        title="E2E Test Node",
        tags=["e2e", "test"],
        importance=0.9
    )

    assert result_msg == "Stored memory: E2E Test Node"
    mock_async_post.assert_called_once()

    # Extract the payload that was sent
    mcp_payload = mock_async_post.call_args.kwargs['json']
    assert mcp_payload["request_type"] == "write"
    add_node = mcp_payload["query"]["queries"][0]["Query"]["steps"][0]["AddN"]
    assert add_node["label"] == "MemoryGraphNode"

    # Setup mock for Backend retrieve
    mock_sync_resp = MagicMock()
    # HelixBackend search expects an array of dicts with 'text' under the 'results' key
    mock_sync_resp.json.return_value = {"results": [{"text": "This is a test node"}]}
    mock_sync_resp.raise_for_status.return_value = None
    mock_sync_post.return_value = mock_sync_resp

    # 2. Retrieve via Backend
    backend = HelixMemoryBackend()
    results = backend.search("query string doesn't matter for mock", k=1)

    assert len(results) == 1
    assert results[0] == "This is a test node"
    mock_sync_post.assert_called_once()

    backend_payload = mock_sync_post.call_args.kwargs['json']
    assert backend_payload["request_type"] == "read"
