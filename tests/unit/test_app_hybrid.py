import pytest
import os
import sys
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files')))

# Mock problematic modules before importing app
sys.modules["pyaudio"] = MagicMock()
sys.modules["faster_whisper"] = MagicMock()
sys.modules["piper"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["pipecat.transports.local.audio"] = MagicMock()

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

class MockFrameProcessor:
    def __init__(self):
        self._prev = None
        self._next = None

    async def process_frame(self, frame, direction):
        raise NotImplementedError

    async def push_frame(self, frame, direction):
        raise NotImplementedError

sys.modules["pipecat.processors.frame_processor"].FrameProcessor = MockFrameProcessor
sys.modules["pipecat.processors.frame_processor"].FrameProcessor.push_frame = AsyncMock()
sys.modules["pipecat.processors.frame_processor"].FrameProcessor.process_frame = AsyncMock()

sys.modules["pipecat.services"] = mock_pipecat.services
sys.modules["pipecat.services.openai"] = mock_pipecat.services.openai
sys.modules["pipecat.services.openai.llm"] = mock_pipecat.services.openai.llm

from pipecatapp.app import discover_services, TwinService

@pytest.mark.asyncio
async def test_discover_services_monolith_mode():
    """Test 'Monolith Mode' (override URL present).
    Should return the override URL without calling Consul.
    """
    with patch.dict(os.environ, {"LLAMA_API_URL_OVERRIDE": "http://localhost:8080"}):
        # We don't mock scan_network_for_llms or httpx, because it should return early
        result = await discover_services(["llama-api-main"], "http://localhost:8500", delay=0.1)
        assert result == "http://localhost:8080"

@pytest.mark.asyncio
async def test_discover_services_distributed_mode_failure(mocker):
    """Test 'Distributed Mode' (no override URL).
    Verify App fails if Consul/Remote LLM is missing.
    """
    # Force httpx.AsyncClient.get to throw an exception or return non-200
    mock_get = AsyncMock()
    mock_get.return_value.status_code = 500
    mocker.patch("httpx.AsyncClient.get", mock_get)

    # Mock fallback to also return None
    mocker.patch("pipecatapp.app.scan_network_for_llms", new_callable=AsyncMock, return_value=None)

    with patch.dict(os.environ, {}, clear=True):
        # With clear=True, there are no overrides
        # We expect it to loop forever if it doesn't find a service.
        # So we patch asyncio.sleep to raise an exception to break the loop,
        # or we just let it try once if we modify it.
        # Let's break the loop
        mocker.patch("asyncio.sleep", side_effect=Exception("Break loop"))

        with pytest.raises(Exception, match="Break loop"):
            await discover_services(["llama-api-main"], "http://localhost:8500", delay=0.1)

@pytest.mark.asyncio
async def test_monolith_mode_answers_hello(mocker):
    """Test 'Monolith Mode': Mock network/Consul, verify App can answer "Hello" using only local classes."""
    # Ensure network doesn't work to prove it's using local mock
    mock_get = AsyncMock(side_effect=Exception("Network call forbidden"))
    mocker.patch("httpx.AsyncClient.get", mock_get)

    mock_llm = AsyncMock()
    mock_vision = AsyncMock()
    mock_runner = AsyncMock()
    mock_config = {"debug_mode": True}

    mock_workflow_runner = MagicMock()

    # Mock workflow run to simulate answering "Hello" locally
    final_response_payload = {
        "tool_call": None,
        "tool_result": None,
        "final_response": "Hello"
    }
    mock_workflow_runner.run = AsyncMock(return_value=final_response_payload)

    with patch('app.PMMMemoryClient'), patch('app.PMMMemory'), patch('tools.code_runner_tool.docker.from_env', create=True), patch('tools.skill_builder_tool.MemoryStore'):
        with patch.dict(os.environ, {"HA_URL": "http://mock-ha", "HA_TOKEN": "mock-token", "LLAMA_API_URL_OVERRIDE": "http://localhost:8080"}):
            service = TwinService(mock_llm, mock_vision, mock_runner, mock_config, asyncio.Queue())

    with patch('pipecatapp.app.WorkflowRunner', return_value=mock_workflow_runner), patch('pipecatapp.web_server.manager.broadcast', new_callable=AsyncMock):
        with patch.object(service, '_send_response', new_callable=AsyncMock) as mock_send_response:
            service.long_term_memory = MagicMock()
            service.long_term_memory.add_event = AsyncMock()
            service.short_term_memory = []

            class MockTranscriptionFrame:
                def __init__(self, text, meta=None):
                    self.text = text
                    self.meta = meta or {}

            with patch('pipecatapp.app.TranscriptionFrame', MockTranscriptionFrame):
                frame = MockTranscriptionFrame("Say hello", meta={"request_id": "test_req"})

                service.push_frame = AsyncMock()

                await service.process_frame(frame, direction=None)

                # Verify local workflow logic responded with "Hello"
                mock_send_response.assert_called_with("Hello")
                # Since LLAMA_API_URL_OVERRIDE is set, the network should not have been called
                mock_get.assert_not_called()
