import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch
from command_deck.scripts.benchmark_personaplex_latency import LatencyBenchmarker

@pytest.mark.asyncio
async def test_latency_benchmarker(capsys):
    benchmarker = LatencyBenchmarker(uri="ws://test:8080/stream", iterations=5)

    mock_websocket = AsyncMock()

    # Simulate a fast response for the recv call
    async def mock_recv():
        await asyncio.sleep(0.05) # Simulate 50ms network/processing delay
        return json.dumps({"type": "audio", "data": "dummyhex"})

    mock_websocket.recv.side_effect = mock_recv

    class MockConnectContextManager:
        async def __aenter__(self):
            return mock_websocket

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch('websockets.connect', return_value=MockConnectContextManager()):
        await benchmarker.run_benchmark()

    # Verify the stats were recorded
    assert len(benchmarker.latencies) == 5

    # Check that latencies reflect the mock delay (should be slightly above 50ms)
    for lat in benchmarker.latencies:
        assert 45.0 <= lat <= 150.0

    captured = capsys.readouterr()
    assert "Status: PASS" in captured.out
    assert "p95:" in captured.out

@pytest.mark.asyncio
async def test_latency_benchmarker_timeout(capsys):
    benchmarker = LatencyBenchmarker(uri="ws://test:8080/stream", iterations=2, timeout=0.1)

    mock_websocket = AsyncMock()

    # Simulate a slow response that causes a timeout
    async def mock_recv_slow():
        await asyncio.sleep(0.2)
        return json.dumps({"type": "audio", "data": "dummyhex"})

    mock_websocket.recv.side_effect = mock_recv_slow

    class MockConnectContextManager:
        async def __aenter__(self):
            return mock_websocket

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch('websockets.connect', return_value=MockConnectContextManager()):
        await benchmarker.run_benchmark()

    assert len(benchmarker.latencies) == 0
    captured = capsys.readouterr()
    assert "Timeout after" in captured.out
    assert "No successful iterations" in captured.out
