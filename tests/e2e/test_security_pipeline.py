import os
import sys
import pytest
import asyncio
from unittest.mock import MagicMock, patch

# Mock out heavy tools package completely
sys.modules['pipecatapp.tools'] = MagicMock()
sys.modules['tools'] = MagicMock()
sys.modules['agent_factory'] = MagicMock()
sys.modules['tools.submit_solution_tool'] = MagicMock()
sys.modules['pmm_memory_client'] = MagicMock()
sys.modules['durable_execution'] = MagicMock()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/tools')))
# Load the security_remediation_tool directly from file path
import importlib.util
spec = importlib.util.spec_from_file_location("security_remediation_tool", os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/tools/security_remediation_tool.py')))
security_remediation_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(security_remediation_tool)
SecurityRemediationTool = security_remediation_tool.SecurityRemediationTool

@pytest.fixture
def remediation_tool():
    return SecurityRemediationTool()

def test_security_remediation_tool_success(remediation_tool):
    """Test that the tool correctly calls the nomad CLI for valid inputs."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="Allocation 1234abcd stopped", returncode=0)

        result = remediation_tool.run(action="stop_allocation", target="1234abcd")

        mock_run.assert_called_once_with(["nomad", "alloc", "stop", "1234abcd"], capture_output=True, text=True, check=True)
        assert "Successfully stopped allocation" in result

def test_security_remediation_tool_invalid_format(remediation_tool):
    """Test that the tool blocks shell injections/invalid IDs."""
    with patch("subprocess.run") as mock_run:
        result = remediation_tool.run(action="stop_allocation", target="1234; rm -rf /")

        mock_run.assert_not_called()
        assert "Error: Invalid allocation ID format" in result

def test_security_remediation_tool_unsupported_action(remediation_tool):
    """Test that the tool blocks unsupported actions to enforce least privilege."""
    with patch("subprocess.run") as mock_run:
        result = remediation_tool.run(action="delete_node", target="worker-1")

        mock_run.assert_not_called()
        assert "Error: Unsupported action" in result


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp')))
spec = importlib.util.spec_from_file_location("worker_agent", os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/worker_agent.py')))
worker_agent = importlib.util.module_from_spec(spec)
# mock out durable execution decorator
worker_agent.durable_step = lambda f: f
spec.loader.exec_module(worker_agent)
WorkerAgent = worker_agent.WorkerAgent

@pytest.mark.asyncio
async def test_worker_agent_security_injection():
    """Test that the WorkerAgent properly buffers and injects high-severity alerts."""

    agent = WorkerAgent()
    # Mock setup
    agent.mqtt_client = MagicMock()
    agent.messages = [{"role": "system", "content": "You are a worker."}]
    agent.last_heartbeat_time = 9999999999 # Future, so heartbeat timeout doesn't trigger

    # Simulate receiving an MQTT alert
    agent.pending_alerts.append({
        "severity": "high",
        "message": "Suspicious payload exec( detected."
    })

    agent.inject_pending_alerts()

    assert len(agent.messages) == 2
    assert agent.messages[-1]["role"] == "user"
    assert "URGENT SYSTEM SECURITY ALERT: Suspicious payload exec( detected" in agent.messages[-1]["content"]
    assert "You MUST use your security_remediation tool" in agent.messages[-1]["content"]
    assert len(agent.pending_alerts) == 0

@pytest.mark.asyncio
async def test_worker_agent_heartbeat_timeout():
    """Test that the WorkerAgent injects a warning if the heartbeat is missed."""
    import time

    agent = WorkerAgent()
    agent.mqtt_client = MagicMock()
    agent.messages = []
    # Set last heartbeat to 100 seconds ago (threshold is 90)
    agent.last_heartbeat_time = time.time() - 100

    agent.inject_pending_alerts()

    assert len(agent.messages) == 1
    assert "URGENT: Security Agent heartbeat lost" in agent.messages[0]["content"]
    # Check that time was reset to prevent spam
    assert time.time() - agent.last_heartbeat_time < 5
