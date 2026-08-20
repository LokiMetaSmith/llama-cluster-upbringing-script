import pytest
import asyncio
from unittest.mock import patch, MagicMock
from pipecatapp.workflow.nodes.pi_node import PiAgentNode
from pipecatapp.workflow.context import WorkflowContext

@pytest.fixture
def workflow_context():
    context = WorkflowContext(workflow_definition={
        "name": "test_workflow",
        "nodes": [
            {
                "id": "PiExecution",
                "inputs": [
                    {"name": "prompt", "connection": {"from_node": "Input", "from_output": "user_text"}}
                ]
            }
        ]
    })
    context.set_output("Input", "user_text", "hello pi")
    return context

@pytest.mark.asyncio
@patch('shutil.which')
@patch('subprocess.run')
async def test_pi_agent_node_success(mock_run, mock_which, workflow_context):
    mock_which.return_value = "/usr/bin/pi"

    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = '{"status": "success", "response": "Hello from Pi!"}'
    mock_process.stderr = ""
    mock_run.return_value = mock_process

    node = PiAgentNode({
        "id": "PiExecution",
        "config": {"timeout": 60},
        "inputs": [{
            "name": "prompt",
            "connection": {"from_node": "Input", "from_output": "user_text"}
        }]
    })

    await node.execute(workflow_context)

    # Verify subprocess arguments
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    assert args[0] == ["/usr/bin/pi", "-p", "hello pi"]

    result = workflow_context.node_outputs["PiExecution"]["result"]
    assert 'Hello from Pi!' in result


@pytest.mark.asyncio
@patch('shutil.which')
async def test_pi_agent_node_missing_executable(mock_which, workflow_context):
    mock_which.return_value = None

    node = PiAgentNode({
        "id": "PiExecution",
        "config": {},
        "inputs": [{
            "name": "prompt",
            "connection": {"from_node": "Input", "from_output": "user_text"}
        }]
    })

    await node.execute(workflow_context)

    result = workflow_context.node_outputs["PiExecution"]["result"]
    assert "Error: 'pi' executable not found" in result


@pytest.mark.asyncio
async def test_pi_agent_node_missing_prompt():
    context = WorkflowContext(workflow_definition={
        "name": "test_workflow",
        "nodes": [
            {
                "id": "PiExecution",
                "inputs": []
            }
        ]
    })

    node = PiAgentNode({
        "id": "PiExecution",
        "config": {},
        "inputs": []
    })

    await node.execute(context)

    result = context.node_outputs["PiExecution"]["result"]
    assert "Error: 'prompt' input is required" in result
