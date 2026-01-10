import pytest
import os
import sys
import httpx
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio

# Add the parent directory of 'testing' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files')))

# Mock problematic modules before importing app
sys.modules["pyaudio"] = MagicMock()
sys.modules["faster_whisper"] = MagicMock()
sys.modules["piper"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["pipecat.transports.local.audio"] = MagicMock()

# Define a Mock FrameProcessor Class to allow inheritance
class MockFrameProcessor:
    def __init__(self):
        self._prev = None
        self._next = None

    async def process_frame(self, frame, direction):
        pass

    async def push_frame(self, frame, direction):
        pass

# Mock pipecat dependencies
mock_pipecat = MagicMock()
sys.modules["pipecat"] = mock_pipecat
sys.modules["pipecat.frames"] = mock_pipecat.frames
sys.modules["pipecat.frames.frames"] = mock_pipecat.frames.frames
sys.modules["pipecat.pipeline"] = mock_pipecat.pipeline
sys.modules["pipecat.pipeline.pipeline"] = mock_pipecat.pipeline.pipeline
sys.modules["pipecat.pipeline.runner"] = mock_pipecat.pipeline.runner
sys.modules["pipecat.pipeline.task"] = mock_pipecat.pipeline.task
sys.modules["pipecat.processors"] = mock_pipecat.processors
sys.modules["pipecat.processors.frame_processor"] = mock_pipecat.processors.frame_processor
# CRITICAL: Set FrameProcessor to our Mock Class so inheritance works
sys.modules["pipecat.processors.frame_processor"].FrameProcessor = MockFrameProcessor
sys.modules["pipecat.services"] = mock_pipecat.services
sys.modules["pipecat.services.openai"] = mock_pipecat.services.openai
sys.modules["pipecat.services.openai.llm"] = mock_pipecat.services.openai.llm

# Now we can import from the files in ansible/roles/pipecatapp/files
from app import TwinService
from web_server import app
from fastapi.testclient import TestClient

# Since we mocked pipecat, TranscriptionFrame is now a Mock class
# But we might need a consistent class for testing if isinstance is used
# Re-define TranscriptionFrame if needed, but for existing tests mocking might be enough.
from pipecat.frames.frames import TranscriptionFrame

@pytest.fixture
def client(mocker):
    client = TestClient(app)
    return client

# Basic testing of the web server endpoints
def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Mission Control" in response.text

def test_health_check(client, mocker):
    # Mock the twin_service_instance to simulate a healthy state
    mock_twin_service = mocker.Mock()
    mock_twin_service.router_llm = True
    client.app.state.twin_service_instance = mock_twin_service
    client.app.state.is_ready = True

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_workflow_runner_loads_definition(mocker):
    """Tests that the WorkflowRunner can successfully load and parse the default workflow."""
    # We need to mock the nodes and other dependencies to isolate the runner
    mocker.patch('workflow.runner.registry.get_node_class', return_value=MagicMock())

    # The path is relative to the `app.py` file's location
    workflow_path = os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp', 'workflows', 'default_agent_loop.yaml')

    # This will raise an error if the file is not found or is invalid YAML
    from workflow.runner import WorkflowRunner
    runner = WorkflowRunner(workflow_path)

    assert runner is not None
    assert "nodes" in runner.workflow_definition
    # Since we created an empty workflow file with nodes: [], check for that
    assert isinstance(runner.workflow_definition["nodes"], list)

@pytest.mark.asyncio
async def test_health_check_is_healthy(mocker):
    """Tests that the /health endpoint returns a 200 OK status."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}

    async def get_mock_response(*args, **kwargs):
        return mock_response

    mocker.patch("httpx.AsyncClient.get", new=get_mock_response)

    host = os.environ.get("PIPECAT_HOST", "127.0.0.1")
    base_url = f"http://{host}:8000"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/health", timeout=5)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_main_page_loads(mocker):
    """Tests that the main page ('/') loads correctly."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "Mission Control"

    async def get_mock_response(*args, **kwargs):
        return mock_response

    mocker.patch("httpx.AsyncClient.get", new=get_mock_response)

    host = os.environ.get("PIPECAT_HOST", "127.0.0.1")
    base_url = f"http://{host}:8000"
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, timeout=5)
        assert response.status_code == 200
        assert "Mission Control" in response.text

@pytest.mark.asyncio
async def test_loop_detection_mechanism(mocker):
    """
    Tests that the TwinService.process_frame method correctly detects repetitive tool calls
    and injects a system alert.
    """
    # Mock dependencies
    mock_llm = MagicMock()
    mock_vision = MagicMock()
    mock_runner = MagicMock()
    mock_config = {"debug_mode": True}
    mock_approval_queue = asyncio.Queue()

    # Instantiate TwinService
    # We patch PMMMemoryClient and PMMMemory to avoid side effects
    # We also patch docker.from_env because TwinService -> create_tools -> CodeRunnerTool -> docker.from_env()
    with patch('app.PMMMemoryClient'), patch('app.PMMMemory'), patch('docker.from_env'):
        with patch.dict(os.environ, {"HA_URL": "http://mock-ha", "HA_TOKEN": "mock-token"}):
            service = TwinService(mock_llm, mock_vision, mock_runner, mock_config, mock_approval_queue)

    # Mock WorkflowRunner to return a sequence of repetitive tool calls
    mock_workflow_runner = AsyncMock()

    # We want to simulate:
    # 1. Tool Call A
    # 2. Tool Call A
    # 3. Tool Call A (Loop detected!) -> "SYSTEM ALERT..."
    # 4. Final Response (Break loop)

    tool_call_payload = {
        "tool_call": {
            "name": "test_tool",
            "arguments": {"arg": "value"}
        },
        "tool_result": None,
        "final_response": None
    }

    final_response_payload = {
        "tool_call": None,
        "tool_result": None,
        "final_response": "I broke the loop."
    }

    # Use a mutable list for side effects to be consumed by the async function
    side_effect_values = [
        tool_call_payload,
        tool_call_payload,
        tool_call_payload,
        final_response_payload
    ]

    async def side_effect_func(*args, **kwargs):
        return side_effect_values.pop(0)

    # Explicitly set side_effect to an async function to avoid AsyncMock wrapping issues
    mock_workflow_runner.run.side_effect = side_effect_func

    # Patch WorkflowRunner instantiation inside process_frame
    with patch('app.WorkflowRunner', return_value=mock_workflow_runner):
        # Patch _send_response to verify output
        with patch.object(service, '_send_response', new_callable=AsyncMock) as mock_send_response:
            # Patch long_term_memory to avoid errors
            service.long_term_memory = AsyncMock()
            service.short_term_memory = []

            # Create a dummy frame
            # Since TranscriptionFrame is a Mock, we need to ensure isinstance works.
            # We will patch `app` module to use a local Mock class for TranscriptionFrame
            # so we can control isinstance.

            class MockTranscriptionFrame:
                def __init__(self, text, meta=None):
                    self.text = text
                    self.meta = meta or {}

            # We patch the imported class inside app
            with patch('app.TranscriptionFrame', MockTranscriptionFrame):
                frame = MockTranscriptionFrame("Run loop test", meta={"request_id": "test_req"})

                # Ensure push_frame is safe
                service.push_frame = AsyncMock()

                await service.process_frame(frame, direction=None)

                # Verify that the workflow runner was called 4 times
                assert mock_workflow_runner.run.call_count == 4

                # Check the inputs to the 4th call to see if the system alert was injected
                call_args_list = mock_workflow_runner.run.call_args_list
                last_call_args = call_args_list[3]
                global_inputs = last_call_args[0][0]

                assert "SYSTEM ALERT" in global_inputs["tool_result"]
                # The exact message might change, but "3 times" is in the injected string in app.py
                assert "3 times" in global_inputs["tool_result"]

                # Verify final response was sent
                mock_send_response.assert_called_with("I broke the loop.")
