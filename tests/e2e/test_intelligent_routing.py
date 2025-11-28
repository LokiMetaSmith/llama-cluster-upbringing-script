import pytest
import json
import os
from unittest.mock import MagicMock, patch

# Add the app directory to the path to allow imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docker/pipecatapp')))

from app import TwinService, TranscriptionFrame
from pipecat.frames.frames import StartFrame

# Mock LLM service that returns a predictable response
class MockLLM:
    def __init__(self, response_text):
        self.response_text = response_text
        self.last_prompt = None

    async def process_text(self, prompt: str) -> str:
        # The presence of the expert's name in the prompt can be used to verify
        # that the correct context (including performance metrics) was passed.
        self.last_prompt = prompt
        return self.response_text

@pytest.fixture
def twin_service_fixture():
    """Sets up a TwinService instance for testing intelligent routing."""
    # 1. Configure mock external expert
    external_expert_name = "mock_openai"
    external_config = {
        external_expert_name: {
            "base_url": "http://mock-openai-api.test/v1",
            "api_key_env": "MOCK_OPENAI_API_KEY"
        }
    }
    os.environ["MOCK_OPENAI_API_KEY"] = "test-key"

    # 2. Mock the runner and vision detector
    mock_runner = MagicMock()
    mock_vision = MagicMock()

    # 3. Mock the primary router LLM to control its "decision"
    # We'll make it decide to route to our mock external expert.
    mock_router_llm = MockLLM(
        json.dumps({
            "tool": "route_to_expert",
            "args": {"expert": external_expert_name, "query": "what is the weather?"}
        })
    )

    # 4. Use unittest.mock.patch to mock dependencies that access the filesystem or network
    with patch('app.requests.get') as mock_get, \
         patch('app.MemoryStore', MagicMock()), \
         patch('app.CodeRunnerTool', MagicMock()), \
         patch('app.WebBrowserTool', MagicMock()):

        # Mock the response from Consul for discovering local experts
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "llama-api-local_expert": ["tag"],
            "consul": []
        }
        mock_get.return_value = mock_response

        # 5. Initialize TwinService with all the mocks
        service = TwinService(
            llm=mock_router_llm,
            vision_detector=mock_vision,
            runner=mock_runner,
            external_experts_config=external_config
        )
        # Since MemoryStore is now a MagicMock, we need to configure its methods if they are called.
        service.long_term_memory.search.return_value = "No relevant long-term memories found."
        yield service, mock_router_llm, external_expert_name

@pytest.mark.asyncio
async def test_discovers_all_experts(twin_service_fixture):
    """Verify that both local and external experts are discovered."""
    service, _, _ = twin_service_fixture
    experts = service.get_discovered_experts()
    assert "local_expert" in experts
    assert "mock_openai" in experts
    assert len(experts) == 2

@pytest.mark.asyncio
async def test_routing_to_external_expert_and_tracking(twin_service_fixture):
    """Verify that the service can route to an external expert and track its performance."""
    service, router_llm, expert_name = twin_service_fixture

    # Mock the external API call itself
    with patch('llm_clients.requests.post') as mock_post:
        mock_api_response = MagicMock()
        mock_api_response.status_code = 200
        mock_api_response.json.return_value = {
            "choices": [{"message": {"content": "The weather is sunny."}}]
        }
        mock_post.return_value = mock_api_response

        # Initialize the service with a StartFrame, which is required by pipecat processors
        await service.process_frame(StartFrame(), "down")

        # This frame simulates a user asking a question
        user_input_frame = TranscriptionFrame(text="what is the weather?", user_id="test_user", timestamp="time")

        # Process the frame
        await service.process_frame(user_input_frame, "down")

        # 1. Verify the router was called
        assert router_llm.last_prompt is not None

        # 2. Verify the external API was called
        mock_post.assert_called_once()

        # 3. Verify the tracker recorded a success for the correct expert
        expert_metrics = service.expert_tracker.experts[expert_name]
        assert expert_metrics["success_count"] == 1
        assert expert_metrics["failure_count"] == 0
        assert expert_metrics["average_latency"] > 0
        assert expert_metrics["health"] == "healthy"

@pytest.mark.asyncio
async def test_system_prompt_includes_metrics(twin_service_fixture):
    """Verify that the system prompt is correctly updated with performance data."""
    service, _, expert_name = twin_service_fixture

    # Manually record some data to test the prompt formatting
    service.expert_tracker.record_success(expert_name, 0.75)
    service.expert_tracker.record_failure("local_expert")

    # Get the system prompt
    system_prompt = service.get_system_prompt("router")

    # Check that the metrics are present and formatted correctly
    assert f"Expert: {expert_name}" in system_prompt
    assert "Type: external" in system_prompt
    assert "Health: healthy" in system_prompt
    assert "Average Latency: 0.75s" in system_prompt

    assert "Expert: local_expert" in system_prompt
    assert "Type: local" in system_prompt
    assert "Health: unhealthy" in system_prompt
    assert "Failures: 1" in system_prompt