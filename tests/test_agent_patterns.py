import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os
import asyncio
import sqlite3

# Mock agent_factory first
mock_agent_factory = MagicMock()
sys.modules["agent_factory"] = mock_agent_factory

# Mock tools
sys.modules["tools.swarm_tool"] = MagicMock()
sys.modules["tools.skill_tool"] = MagicMock()

# Now import modules
from pipecatapp.manager_agent import ManagerAgent
from pipecatapp.technician_agent import TechnicianAgent
from pipecatapp.durable_execution import DurableExecutionEngine, InvocationStatus

@pytest.mark.asyncio
async def test_manager_agent_map_reduce():
    """Test the Manager Agent's Map-Reduce logic."""
    with patch("pipecatapp.manager_agent.httpx.AsyncClient") as mock_httpx_cls, \
         patch("pipecatapp.manager_agent.httpx.get") as mock_get:
        
        # Mocks
        mock_client = AsyncMock()
        mock_httpx_cls.return_value.__aenter__.return_value = mock_client
        
        # Mock synchronous get for discovery
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"ServiceAddress": "localhost", "ServicePort": 1234}]

        # Mock LLM Response (Sync object)
        mock_response_llm = MagicMock()
        mock_response_llm.raise_for_status.return_value = None
        mock_response_llm.json.side_effect = [
            {"choices": [{"message": {"content": '[{"id": "t1", "prompt": "do 1", "context": ""}, {"id": "t2", "prompt": "do 2", "context": ""}]'}}]}, # Map
            {"choices": [{"message": {"content": "Final Report: All done."}}]} # Aggregate
        ]
        mock_client.post.return_value = mock_response_llm
        
        # Mock Memory Polling Response (Sync object)
        mock_response_mem = MagicMock()
        mock_response_mem.status_code = 200
        mock_response_mem.json.side_effect = [
            [], # Call 1: No results
            [ # Call 2: Results arrive
                {"kind": "worker_result", "meta": {"task_id": "t1"}, "content": "Done T1"},
                {"kind": "worker_result", "meta": {"task_id": "t2"}, "content": "Done T2"}
            ]
        ]
        mock_client.get.return_value = mock_response_mem
        
        # Initialize
        os.environ["MANAGER_PROMPT"] = "Big Task"
        agent = ManagerAgent()
        
        # Mock SwarmTool inside the agent instance
        # Use AsyncMock for async methods
        mock_swarm = MagicMock()
        mock_swarm.spawn_workers = AsyncMock(return_value="Dispatched")
        
        with patch("pipecatapp.manager_agent.SwarmTool", return_value=mock_swarm):
            await agent.run()
        
        # Assertions
        mock_swarm.spawn_workers.assert_called_once()
        args = mock_swarm.spawn_workers.call_args[0][0]
        assert len(args) == 2
        assert args[0]['id'] == "t1"

@pytest.mark.asyncio
async def test_durable_technician():
    """Test that TechnicianAgent uses Durable Execution."""
    db_path = "/tmp/test_durable.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    os.environ["WORKER_TASK_ID"] = "test-task-123"
    
    # We need to mock create_tools again like in the previous test
    mock_agent_factory.create_tools.return_value = {}

    with patch("pipecatapp.technician_agent.requests"), \
         patch("pipecatapp.technician_agent.httpx.AsyncClient") as mock_httpx_cls:
             
        mock_client = AsyncMock()
        mock_httpx_cls.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"choices": [{"message": {"content": "Plan"}}]}
        mock_client.post.return_value = mock_response

        agent = TechnicianAgent()
        agent.llm_base_url = "http://mock" # Manually set so call_llm proceeds
        agent.durable_engine = DurableExecutionEngine(db_path=db_path)
        
        # Execute the durable step
        print("Executing phase_1_plan...")
        await agent.phase_1_plan()
        
        # Debug DB
        cursor = agent.durable_engine.conn.cursor()
        cursor.execute("SELECT * FROM execution_log")
        rows = cursor.fetchall()
        print(f"DB Content ({len(rows)} rows):")
        for row in rows:
            print(row)

        # Check DB
        inv = agent.durable_engine.get_invocation("test-task-123", 0) # seq 0
        assert inv is not None, f"Invocation seq 0 not found. DB has {len(rows)} rows."
        assert inv['status'] == InvocationStatus.COMPLETE
        assert inv['return_value'] == "Plan"
        
        # Re-run to verify caching (idempotency)
        mock_client.post.reset_mock()
        agent.step_counter = 0
        
        cached_result = await agent.phase_1_plan()
        
        assert cached_result == "Plan"
        mock_client.post.assert_not_called() # Should use cache

if __name__ == "__main__":
    asyncio.run(test_manager_agent_map_reduce())
    asyncio.run(test_durable_technician())
