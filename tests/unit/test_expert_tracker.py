import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from pipecatapp.expert_tracker import ExpertTracker

@pytest.fixture
def tracker():
    return ExpertTracker()

def test_initialization(tracker):
    assert tracker.experts == {}
    assert tracker.memory_url == "http://memory-graph.service.consul:8000/sse"

def test_register_expert(tracker):
    tracker.register_expert("test_expert", "local")
    assert "test_expert" in tracker.experts

    expert = tracker.experts["test_expert"]
    assert expert["type"] == "local"
    assert expert["health"] == "unknown"
    assert expert["success_count"] == 0
    assert expert["failure_count"] == 0
    assert expert["total_latency"] == 0.0
    assert expert["average_latency"] == 0.0
    assert expert["last_seen"] == 0

def test_register_existing_expert(tracker):
    tracker.register_expert("test_expert", "local")

    # Modify it
    tracker.experts["test_expert"]["success_count"] = 5

    # Registering again should not overwrite
    tracker.register_expert("test_expert", "external")
    assert tracker.experts["test_expert"]["success_count"] == 5
    assert tracker.experts["test_expert"]["type"] == "local"

def test_record_success(tracker):
    tracker.register_expert("test_expert", "local")

    tracker.record_success("test_expert", 1.5)
    expert = tracker.experts["test_expert"]

    assert expert["health"] == "healthy"
    assert expert["success_count"] == 1
    assert expert["total_latency"] == 1.5
    assert expert["average_latency"] == 1.5
    assert expert["last_seen"] > 0

    tracker.record_success("test_expert", 2.5)
    assert expert["success_count"] == 2
    assert expert["total_latency"] == 4.0
    assert expert["average_latency"] == 2.0

def test_record_success_unregistered(tracker):
    tracker.record_success("unknown_expert", 1.0)
    assert "unknown_expert" not in tracker.experts

def test_record_failure(tracker):
    tracker.register_expert("test_expert", "local")

    tracker.record_failure("test_expert")
    expert = tracker.experts["test_expert"]

    assert expert["health"] == "unhealthy"
    assert expert["failure_count"] == 1
    assert expert["last_seen"] > 0

def test_record_failure_unregistered(tracker):
    tracker.record_failure("unknown_expert")
    assert "unknown_expert" not in tracker.experts

def test_get_metrics_for_prompt_empty(tracker):
    result = tracker.get_metrics_for_prompt()
    assert result == "No expert performance data available."

def test_get_metrics_for_prompt_populated(tracker):
    tracker.register_expert("expert_a", "local")
    tracker.register_expert("expert_b", "external")

    tracker.record_success("expert_a", 1.0)
    tracker.record_failure("expert_b")

    result = tracker.get_metrics_for_prompt()

    assert "expert_a" in result
    assert "expert_b" in result
    assert "Health: healthy" in result
    assert "Health: unhealthy" in result
    assert "Successes: 1, Failures: 0" in result
    assert "Successes: 0, Failures: 1" in result

@pytest.mark.asyncio
async def test_connect_and_store_relation_no_mcp():
    with patch("pipecatapp.expert_tracker.MCP_AVAILABLE", False):
        tracker = ExpertTracker()
        await tracker.connect_and_store_relation("source", "relation", "target")
        # Should just return early without error

@pytest.mark.asyncio
async def test_connect_and_store_relation_mcp_available():
    # Setup mocks
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    mock_session.call_tool = AsyncMock(return_value="mock_result")

    # This context manager mock is tricky, we need to mock sse_client to return a mock streams context,
    # and ClientSession to return our mock session

    class AsyncContextManagerMock:
        def __init__(self, obj):
            self.obj = obj
        async def __aenter__(self):
            return self.obj
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    mock_streams = (AsyncMock(), AsyncMock())

    with patch("pipecatapp.expert_tracker.MCP_AVAILABLE", True), \
         patch("pipecatapp.expert_tracker.sse_client", return_value=AsyncContextManagerMock(mock_streams), create=True), \
         patch("pipecatapp.expert_tracker.ClientSession", return_value=AsyncContextManagerMock(mock_session), create=True):

        tracker = ExpertTracker()
        await tracker.connect_and_store_relation("source_id", "likes", "target_id")

        mock_session.initialize.assert_awaited_once()
        mock_session.call_tool.assert_awaited_once_with("create_relationship", {
            "from_memory_id": "source_id",
            "to_memory_id": "target_id",
            "relationship_type": "likes"
        })

@pytest.mark.asyncio
async def test_connect_and_store_relation_exception(caplog):
    # Setup mock to raise exception
    class AsyncContextManagerMockError:
        async def __aenter__(self):
            raise ConnectionError("Mock connection error")
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch("pipecatapp.expert_tracker.MCP_AVAILABLE", True), \
         patch("pipecatapp.expert_tracker.sse_client", return_value=AsyncContextManagerMockError(), create=True):

        tracker = ExpertTracker()
        await tracker.connect_and_store_relation("source", "rel", "target")

        assert "Failed to store relation in memory graph" in caplog.text

def test_tracker_token_clamping():
    from pipecatapp.expert_tracker import clamp_output_tokens, OUTPUT_RESERVE_CAP

    # Under the cap
    assert clamp_output_tokens(500) == 500
    # Over the cap
    assert clamp_output_tokens(4500) == OUTPUT_RESERVE_CAP
    # Fallback
    assert clamp_output_tokens(None) == 1000


def test_utilization_caps_and_usage(tracker):
    task_id = "test-runaway-task"
    tracker.set_task_utilization_cap(task_id, 10)

    # 1. Check early usage (under 80%)
    res = tracker.record_and_check_usage(task_id, increment=5)
    assert res["status"] == "OK"
    assert res["usage"] == 5
    assert res["usage_pct"] == 50.0

    # 2. Check warning boundary (at 80%)
    res = tracker.record_and_check_usage(task_id, increment=3)
    assert res["status"] == "WARNING"
    assert res["usage"] == 8
    assert res["usage_pct"] == 80.0
    assert "Governance Warning" in res["msg"]

    # 3. Check hard-stop boundary (at 100%)
    res = tracker.record_and_check_usage(task_id, increment=2)
    assert res["status"] == "HARD_STOP"
    assert res["usage"] == 10
    assert res["usage_pct"] == 100.0
    assert "Governance Hard-Stop triggered" in res["msg"]


@pytest.mark.asyncio
async def test_enforce_governance_cap_runaway(tracker):
    task_id = "runaway-agent"
    nomad_job_id = "worker-runaway-agent"
    tracker.set_task_utilization_cap(task_id, 5)

    # Create mock swarm tool
    mock_swarm_tool = AsyncMock()
    mock_swarm_tool.kill_worker.return_value = "Successfully killed job"

    # Increment up to the 100% hard-stop threshold
    res = await tracker.enforce_governance_cap(
        task_id=task_id,
        nomad_job_id=nomad_job_id,
        swarm_tool=mock_swarm_tool,
        increment=5
    )

    assert res["status"] == "HARD_STOP"
    assert res["kill_result"] == "Successfully killed job"
    mock_swarm_tool.kill_worker.assert_called_once_with(nomad_job_id)
