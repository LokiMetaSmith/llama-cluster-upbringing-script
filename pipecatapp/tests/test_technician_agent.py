import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
import json
import sys
import os

# Ensure the pipecatapp directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp')))

# Mock agent_factory to avoid heavy dependency imports
mock_agent_factory = MagicMock()
sys.modules["agent_factory"] = mock_agent_factory

from technician_agent import TechnicianAgent

@pytest.fixture
def mock_agent():
    def mock_getenv(key, default=None):
        if key == "MAX_STEPS":
            return "15"
        return "dummy"

    with patch("technician_agent.os.getenv", side_effect=mock_getenv):
        agent = TechnicianAgent()
        agent.prompt = "Test prompt"
        agent.context = "Test context"
        agent.memory_client = MagicMock()
        # Mock async methods on memory_client
        agent.memory_client.create_work_item = AsyncMock(return_value="dummy_work_item_id")
        agent.memory_client.update_work_item = AsyncMock()

        agent.report_event = AsyncMock()
        agent.tools = {}
        # Mocking llm call
        agent.call_llm = AsyncMock()

        return agent

@pytest.mark.asyncio
async def test_phase_1_plan(mock_agent):
    mock_agent.call_llm.return_value = "1. Step 1\n2. Step 2"
    plan = await mock_agent.phase_1_plan.__wrapped__(mock_agent)
    assert plan == "1. Step 1\n2. Step 2"
    mock_agent.call_llm.assert_called_once()
    mock_agent.report_event.assert_called_with("technician_plan", plan)

@pytest.mark.asyncio
async def test_phase_2_execute_success(mock_agent):
    # Mock LLM output to indicate final answer on the first step
    mock_agent.call_llm.return_value = "FINAL_ANSWER: I have finished."

    # We must patch execute_step since it has @durable_step which breaks our simple tests
    original_execute_step = mock_agent.execute_step.__wrapped__

    async def side_effect(*args, **kwargs):
        return await original_execute_step(mock_agent, *args, **kwargs)

    mock_agent.execute_step = AsyncMock(side_effect=side_effect)

    plan = "1. Step 1\n2. Step 2"
    result = await mock_agent.phase_2_execute(plan)

    assert result == "I have finished."

@pytest.mark.asyncio
async def test_phase_2_execute_with_tool_call(mock_agent):
    # Mock a tool call then a final answer
    mock_agent.call_llm.side_effect = [
        '{"tool": "dummy_tool", "args": {"arg1": "val1"}}',
        'FINAL_ANSWER: Done.'
    ]

    dummy_tool = MagicMock()
    dummy_tool.run = MagicMock(return_value="tool_output")
    mock_agent.tools = {"dummy_tool": dummy_tool}

    # We must patch execute_step since it has @durable_step which breaks our simple tests
    original_execute_step = mock_agent.execute_step.__wrapped__

    async def side_effect(*args, **kwargs):
        return await original_execute_step(mock_agent, *args, **kwargs)

    mock_agent.execute_step = AsyncMock(side_effect=side_effect)

    plan = "1. Step 1\n2. Step 2"
    result = await mock_agent.phase_2_execute(plan)

    assert result == "Done."
    assert mock_agent.call_llm.call_count == 2
    dummy_tool.run.assert_called_once_with(arg1="val1")
    # Verify the tool output was added to messages
    assert any("tool_output" in msg.get("content", "") for msg in mock_agent.messages)

@pytest.mark.asyncio
async def test_phase_3_reflect(mock_agent):
    mock_agent.call_llm.return_value = "Yes, satisfactory."

    result = "Some execution result"

    reflection = await mock_agent.phase_3_reflect.__wrapped__(mock_agent, result)

    assert reflection == "Yes, satisfactory."
    mock_agent.call_llm.assert_called_once()
