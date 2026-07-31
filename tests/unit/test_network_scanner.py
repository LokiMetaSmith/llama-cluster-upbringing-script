import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock

from pipecatapp.network_scanner import get_local_ip, check_llm_service

@patch('pipecatapp.network_scanner.socket.socket')
def test_get_local_ip_success(mock_socket_class):
    # Setup mock socket instance
    mock_socket_instance = MagicMock()
    mock_socket_class.return_value = mock_socket_instance

    # Configure getsockname to return a fake local IP
    mock_socket_instance.getsockname.return_value = ('192.168.1.50', 12345)

    # Call the function
    ip = get_local_ip()

    # Verify behavior
    mock_socket_instance.connect.assert_called_once_with(('10.255.255.255', 1))
    mock_socket_instance.getsockname.assert_called_once()
    mock_socket_instance.close.assert_called_once()

    assert ip == '192.168.1.50'

@patch('pipecatapp.network_scanner.socket.socket')
def test_get_local_ip_exception(mock_socket_class):
    # Setup mock socket instance
    mock_socket_instance = MagicMock()
    mock_socket_class.return_value = mock_socket_instance

    # Configure connect to raise an exception
    mock_socket_instance.connect.side_effect = OSError("Network is unreachable")

    # Call the function
    ip = get_local_ip()

    # Verify behavior
    mock_socket_instance.connect.assert_called_once_with(('10.255.255.255', 1))
    mock_socket_instance.getsockname.assert_not_called()
    mock_socket_instance.close.assert_called_once()

    # Fallback to localhost
    assert ip == '127.0.0.1'

@pytest.fixture
def mock_open_connection():
    # Use patch to mock the function instead of trying to pass mock into asyncio.wait_for
    with patch('asyncio.wait_for', new_callable=AsyncMock) as mock_wait_for:
        reader = MagicMock()
        writer = MagicMock()
        writer.close = MagicMock()
        writer.wait_closed = AsyncMock()
        mock_wait_for.return_value = (reader, writer)

        with patch('asyncio.open_connection', new_callable=MagicMock) as mock_open_conn:
            # We don't await the return value of open_connection inside check_llm_service, wait_for does.
            # wait_for is mocked to return (reader, writer) instead of evaluating the coroutine.
            # We mock open_connection to just return None instead of a coroutine to prevent "was never awaited" warnings.
            mock_open_conn.return_value = None
            yield mock_wait_for

@pytest.fixture
def mock_httpx_client():
    with patch('pipecatapp.network_scanner.httpx.AsyncClient') as MockClient:
        mock_client_instance = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client_instance
        yield mock_client_instance

@pytest.mark.asyncio
async def test_check_llm_service_connection_timeout(mock_open_connection):
    """Test that function returns None if the initial socket connection times out."""
    mock_open_connection.side_effect = asyncio.TimeoutError()
    result = await check_llm_service('127.0.0.1', 11434)
    assert result is None

@pytest.mark.asyncio
async def test_check_llm_service_connection_refused(mock_open_connection):
    """Test that function returns None if the connection is refused."""
    mock_open_connection.side_effect = ConnectionRefusedError()
    result = await check_llm_service('127.0.0.1', 11434)
    assert result is None

@pytest.mark.asyncio
async def test_check_llm_service_ollama_success(mock_open_connection, mock_httpx_client):
    """Test successful detection of Ollama service on port 11434."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_httpx_client.get.return_value = mock_response

    result = await check_llm_service('192.168.1.100', 11434)

    assert result == 'http://192.168.1.100:11434/v1'
    mock_httpx_client.get.assert_called_once_with('http://192.168.1.100:11434/api/tags')

@pytest.mark.asyncio
async def test_check_llm_service_ollama_http_error(mock_open_connection, mock_httpx_client):
    """Test Ollama service detection failure when HTTP request fails."""
    mock_httpx_client.get.side_effect = Exception("HTTP Error")

    result = await check_llm_service('192.168.1.100', 11434)

    assert result is None

@pytest.mark.asyncio
async def test_check_llm_service_ollama_non_200(mock_open_connection, mock_httpx_client):
    """Test Ollama service detection failure when HTTP response is not 200."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_httpx_client.get.return_value = mock_response

    result = await check_llm_service('192.168.1.100', 11434)

    assert result is None

@pytest.mark.asyncio
async def test_check_llm_service_llama_cpp_v1_models_success(mock_open_connection, mock_httpx_client):
    """Test successful detection of Llama.cpp via /v1/models."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    mock_httpx_client.get.return_value = mock_response

    result = await check_llm_service('192.168.1.101', 8080)

    assert result == 'http://192.168.1.101:8080/v1'
    mock_httpx_client.get.assert_called_once_with('http://192.168.1.101:8080/v1/models')

@pytest.mark.asyncio
async def test_check_llm_service_llama_cpp_health_success(mock_open_connection, mock_httpx_client):
    """Test successful detection of Llama.cpp via /health fallback."""
    # First get (/v1/models) fails or returns non-200
    mock_v1_response = MagicMock()
    mock_v1_response.status_code = 404

    # Second get (/health) succeeds
    mock_health_response = MagicMock()
    mock_health_response.status_code = 200
    mock_health_response.headers = {}

    mock_httpx_client.get.side_effect = [mock_v1_response, mock_health_response]

    result = await check_llm_service('192.168.1.101', 8080)

    assert result == 'http://192.168.1.101:8080/v1'
    assert mock_httpx_client.get.call_count == 2

@pytest.mark.asyncio
async def test_check_llm_service_llama_cpp_exception_then_health_success(mock_open_connection, mock_httpx_client):
    """Test successful detection of Llama.cpp via /health fallback when /v1/models throws exception."""
    # Second get (/health) succeeds
    mock_health_response = MagicMock()
    mock_health_response.status_code = 200
    mock_health_response.headers = {}

    mock_httpx_client.get.side_effect = [Exception("No models endpoint"), mock_health_response]

    result = await check_llm_service('192.168.1.101', 8080)

    assert result == 'http://192.168.1.101:8080/v1'

@pytest.mark.asyncio
async def test_check_llm_service_llama_cpp_all_fail(mock_open_connection, mock_httpx_client):
    """Test failure of Llama.cpp detection when both endpoints fail."""
    mock_httpx_client.get.side_effect = Exception("Connection Refused")

    result = await check_llm_service('192.168.1.101', 8080)

    assert result is None
    assert mock_httpx_client.get.call_count == 2

@pytest.mark.asyncio
async def test_check_llm_service_llama_cpp_github_header_skipped_v1_models(mock_open_connection, mock_httpx_client):
    """Test that a 200 response with 'github' in the Server header is skipped for /v1/models."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Server": "GitHub.com"}

    mock_httpx_client.get.side_effect = [mock_response, Exception("health fails")]

    result = await check_llm_service('192.168.1.101', 8080)

    assert result is None

@pytest.mark.asyncio
async def test_check_llm_service_llama_cpp_github_header_skipped_health(mock_open_connection, mock_httpx_client):
    """Test that a 200 response with 'github' in the Server header is skipped for /health."""
    mock_response_v1 = MagicMock()
    mock_response_v1.status_code = 404

    mock_response_health = MagicMock()
    mock_response_health.status_code = 200
    mock_response_health.headers = {"x-github-request-id": "1234-github"}

    mock_httpx_client.get.side_effect = [mock_response_v1, mock_response_health]

    result = await check_llm_service('192.168.1.101', 8080)

    assert result is None
