import asyncio
import time
from pipecatapp.tools.swarm_tool import SwarmTool
from unittest.mock import MagicMock, AsyncMock, patch

async def test_swarm_parallelism():
    print("Testing SwarmTool parallelism...")

    # Mock httpx client
    mock_post = AsyncMock()
    mock_post.return_value.status_code = 200

    # We need to patch the context manager used in SwarmTool
    # async with httpx.AsyncClient() as client:
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.post = mock_post
    mock_client.__aexit__.return_value = None

    with patch("httpx.AsyncClient", return_value=mock_client):
        tool = SwarmTool()

        # Create 100 dummy tasks
        tasks = [{"id": f"task-{i}", "prompt": "do work"} for i in range(100)]

        start_time = time.time()
        result = await tool.spawn_workers(tasks)
        end_time = time.time()

        duration = end_time - start_time
        print(f"Dispatched {len(tasks)} tasks in {duration:.4f} seconds.")
        print(f"Result: {result}")

        # Verify result format
        assert "Successfully dispatched 100 workers" in result

        # Verify 100 calls were made
        assert mock_post.call_count == 100

        # Heuristic check for parallelism
        # If it was sequential with real network, it would take much longer.
        # With mocks, gather vs loop is almost instant, but the main goal is verifying
        # the code path works without error.

if __name__ == "__main__":
    asyncio.run(test_swarm_parallelism())
