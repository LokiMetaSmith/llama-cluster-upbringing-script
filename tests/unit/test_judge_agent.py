import pytest
from unittest.mock import AsyncMock, patch
from pipecatapp.judge_agent import JudgeAgent

@pytest.fixture
def judge_agent():
    # We patch the environment variables before initializing the agent
    with patch("os.getenv", side_effect=lambda k, default=None: {
        "JUDGE_TASK_ID": "test_task_id",
        "TARGET_TASK_ID": "test_target_task_id",
        "TARGET_WORK_ITEM_ID": "test_target_work_item_id",
        "JUDGE_CRITERIA": "Test criteria"
    }.get(k, default)):
        agent = JudgeAgent()
        return agent

@pytest.mark.asyncio
async def test_report_event_no_memory_client(judge_agent):
    """Test that report_event returns early if memory_client is None."""
    judge_agent.memory_client = None
    # Should not raise an exception
    await judge_agent.report_event("test_kind", "test_content")

@pytest.mark.asyncio
async def test_report_event_with_no_meta(judge_agent):
    """Test report_event when meta is None, expecting default metadata."""
    judge_agent.memory_client = AsyncMock()

    await judge_agent.report_event("test_kind", "test_content")

    judge_agent.memory_client.add_event.assert_called_once_with(
        "test_kind",
        "test_content",
        {
            "task_id": "test_task_id",
            "agent_type": "judge",
            "target_task_id": "test_target_task_id",
            "target_work_item_id": "test_target_work_item_id"
        }
    )

@pytest.mark.asyncio
async def test_report_event_with_meta(judge_agent):
    """Test report_event with custom meta, ensuring it gets merged."""
    judge_agent.memory_client = AsyncMock()

    custom_meta = {"custom_key": "custom_value", "task_id": "will_be_overwritten"}
    await judge_agent.report_event("test_kind", "test_content", custom_meta)

    judge_agent.memory_client.add_event.assert_called_once_with(
        "test_kind",
        "test_content",
        {
            "custom_key": "custom_value",
            "task_id": "test_task_id",
            "agent_type": "judge",
            "target_task_id": "test_target_task_id",
            "target_work_item_id": "test_target_work_item_id"
        }
    )

@pytest.mark.asyncio
async def test_report_event_exception_handling(judge_agent):
    """Test that if add_event raises an exception, it propagates up."""
    judge_agent.memory_client = AsyncMock()

    class NetworkError(Exception):
        pass

    judge_agent.memory_client.add_event.side_effect = NetworkError("Connection timeout")

    with pytest.raises(NetworkError, match="Connection timeout"):
        await judge_agent.report_event("test_kind", "test_content")
