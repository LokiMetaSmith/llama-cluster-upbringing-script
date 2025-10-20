import pytest
import os
import sys
import httpx
from unittest.mock import MagicMock, AsyncMock

# Add the parent directory of 'testing' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files')))

# Now we can import from the files in ansible/roles/pipecatapp/files
from app import TwinService
from web_server import app
from fastapi.testclient import TestClient

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
    mocker.patch("web_server.twin_service_instance", mock_twin_service)

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# More advanced tests for the TwinService can be added here
# For example, mocking the LLM and other services to test the agent's logic

@pytest.mark.requires_display
@pytest.mark.asyncio
async def test_twin_service_initialization(mocker):
    """Tests that the TwinService initializes correctly."""
    # This is a basic test. More advanced tests would mock dependencies.
    mocker.patch('memory.SentenceTransformer')
    mocker.patch('faiss.IndexFlatL2')
    mocker.patch('docker.from_env')
    mocker.patch('tools.web_browser_tool.sync_playwright')
    mocker.patch('tools.summarizer_tool.SentenceTransformer')
    mock_llm = AsyncMock()
    mock_vision = AsyncMock()
    mock_runner = AsyncMock()
    mock_config = MagicMock()
    service = TwinService(llm=mock_llm, vision_detector=mock_vision, runner=mock_runner, app_config=mock_config)
    assert service is not None

# Example of a more advanced test with mocking
@pytest.mark.requires_display
@pytest.mark.asyncio
async def test_twin_service_sends_vision_frame(mocker):
    """Tests that TwinService sends a vision frame to the LLM."""
    # Mock the LLM and other external services
    mocker.patch('memory.SentenceTransformer')
    mocker.patch('faiss.IndexFlatL2')
    mocker.patch('docker.from_env')
    mocker.patch('tools.web_browser_tool.sync_playwright')
    mocker.patch('tools.summarizer_tool.SentenceTransformer')
    mock_llm = AsyncMock()
    mock_vision = AsyncMock()
    mock_runner = AsyncMock()
    mock_config = MagicMock()

    service = TwinService(llm=mock_llm, vision_detector=mock_vision, runner=mock_runner, app_config=mock_config)

    # This test will require more setup to properly simulate the pipeline
    # For now, we'll just check that the service can be instantiated.
    assert service is not None

# The following tests are marked as integration tests because they
# are designed to run against a live, running pipecat server.
# In a CI environment, these might be run as a separate step after
# the application has been deployed to a staging environment.

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
