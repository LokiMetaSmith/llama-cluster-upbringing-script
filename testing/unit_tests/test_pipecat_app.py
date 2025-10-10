import pytest
import httpx
import requests
from unittest.mock import MagicMock, patch

# Due to the file location, we need to add the role's files directory to the path
# to ensure that modules like `memory` and `tools` can be imported by `app`.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles/pipecatapp/files')))

from app import TwinService

@pytest.fixture
def mock_app_config():
    """Provides a mock application configuration."""
    return {
        "consul_host": "localhost",
        "consul_port": 8500,
        "external_experts_config": {
            "openai_gpt4": {
                "base_url": "https://api.openai.com/v1",
                "api_key_env": "OPENAI_API_KEY",
                "model": "gpt-4-turbo"
            }
        }
    }

@pytest.fixture
def twin_service(mock_app_config):
    """Provides an instance of TwinService with mocked dependencies."""
    mock_llm = MagicMock()
    mock_vision_detector = MagicMock()
    mock_runner = MagicMock()
    mock_approval_queue = MagicMock()

    # When importing app, its global logger is initialized. We need to prevent
    # it from trying to access the event loop during test setup.
    # We also mock dependencies with external requirements (filesystem, docker, playwright).
    with patch('app.WebSocketLogHandler.emit'), \
         patch('app.MemoryStore'), \
         patch('app.CodeRunnerTool'), \
         patch('app.WebBrowserTool'):
        service = TwinService(
            llm=mock_llm,
            vision_detector=mock_vision_detector,
            runner=mock_runner,
            app_config=mock_app_config,
            approval_queue=mock_approval_queue
        )
    return service

class TestTwinService:
    """Unit tests for the TwinService class."""

    def test_get_discovered_experts_successful(self, twin_service):
        """
        Tests that get_discovered_experts correctly merges experts from the
        config and from a successful Consul API call.
        """
        # Mock the response from Consul
        mock_consul_response = {
            "llamacpp-rpc-main": {
                "Tags": ["llm"]
            },
            "llamacpp-rpc-coding": {
                "Tags": ["llm", "expert", "coding"]
            },
            "some-other-service": {
                "Tags": ["web"]
            }
        }

        with patch('requests.get') as mock_get:
            # Configure the mock to return a successful response with our test data
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_consul_response
            mock_get.return_value = mock_response

            # Call the method under test
            experts = twin_service.get_discovered_experts()

            # Assertions
            # It should call the correct Consul endpoint
            mock_get.assert_called_once_with("http://localhost:8500/v1/catalog/services")

            # The final list should be sorted and contain experts from all sources
            expected_experts = sorted(["openai_gpt4", "main", "coding"])
            assert experts == expected_experts

    def test_get_discovered_experts_consul_error(self, twin_service):
        """
        Tests that get_discovered_experts returns only the configured experts
        when there is an error connecting to Consul.
        """
        with patch('requests.get') as mock_get:
            # Configure the mock to raise a requests connection error
            mock_get.side_effect = requests.exceptions.RequestException("Connection failed")

            # Call the method under test
            experts = twin_service.get_discovered_experts()

            # Assertions
            # It should still return the expert from the initial config
            assert experts == ["openai_gpt4"]
            # It should have attempted to connect to Consul
            mock_get.assert_called_once()

# We keep the old health check tests but convert them to pytest style
# These act more like integration tests as they require a running server.
@pytest.mark.integration
@pytest.mark.asyncio
async def test_health_check_is_healthy():
    """Tests that the /health endpoint returns a 200 OK status."""
    host = os.environ.get("PIPECAT_HOST", "127.0.0.1")
    base_url = f"http://{host}:8000"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{base_url}/health", timeout=5)
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
        except httpx.ConnectError as e:
            pytest.fail(f"Could not connect to the pipecat server at {base_url}. Is it running? Error: {e}")

@pytest.mark.integration
@pytest.mark.asyncio
async def test_main_page_loads():
    """Tests that the main page ('/') loads correctly."""
    host = os.environ.get("PIPECAT_HOST", "127.0.0.1")
    base_url = f"http://{host}:8000"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, timeout=5)
            assert response.status_code == 200
            assert "Mission Control" in response.text
        except httpx.ConnectError as e:
            pytest.fail(f"Could not connect to the pipecat server at {base_url}. Is it running? Error: {e}")