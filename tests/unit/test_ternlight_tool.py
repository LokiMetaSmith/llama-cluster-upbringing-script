import pytest
import os
import sys
import json
from unittest.mock import MagicMock, patch

# Add the path to the pipecatapp directory to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/tools')))

from ternlight_tool import TernlightTool

@pytest.fixture
def mock_requests_post():
    with patch('requests.post') as mock:
        yield mock

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock:
        # Mock health check
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock.return_value = mock_resp
        yield mock

@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock:
        yield mock

def test_ternlight_tool_remote_embed(mock_requests_post, mock_requests_get):
    """Tests that TernlightTool uses the remote microservice for embedding."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
    mock_requests_post.return_value = mock_resp

    tool = TernlightTool(base_url="http://fake-service")
    result = tool.embed("test text")

    assert result == [0.1, 0.2, 0.3]
    mock_requests_post.assert_called_once()
    assert mock_requests_post.call_args[1]['json'] == {"text": "test text"}

def test_ternlight_tool_remote_similar(mock_requests_post, mock_requests_get):
    """Tests that TernlightTool uses the remote microservice for similarity search."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"results": ["doc1", "doc2"]}
    mock_requests_post.return_value = mock_resp

    tool = TernlightTool(base_url="http://fake-service")
    result = tool.similar("query", ["doc1", "doc2", "doc3"], top_k=2)

    assert result == ["doc1", "doc2"]
    mock_requests_post.assert_called_once()
    assert mock_requests_post.call_args[1]['json'] == {
        "query": "query",
        "documents": ["doc1", "doc2", "doc3"],
        "topK": 2
    }

def test_ternlight_tool_local_fallback(mock_requests_get, mock_subprocess_run):
    """Tests that TernlightTool falls back to local node execution if service is unavailable."""
    # Mock health check failure
    mock_health_resp = MagicMock()
    mock_health_resp.status_code = 503
    mock_requests_get.return_value = mock_health_resp

    # Mock subprocess output
    mock_sub_res = MagicMock()
    mock_sub_res.stdout = json.dumps({"result": [0.5, 0.6]})
    mock_subprocess_run.return_value = mock_sub_res

    tool = TernlightTool(base_url="http://broken-service")
    result = tool.embed("test text")

    assert result == [0.5, 0.6]
    mock_subprocess_run.assert_called_once()
    # Check that 'node' was called
    assert mock_subprocess_run.call_args[0][0][0] == "node"

def test_ternlight_tool_execute_entrypoint(mock_requests_post, mock_requests_get):
    """Tests the generic execute() method."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"results": ["res1"]}
    mock_requests_post.return_value = mock_resp

    tool = TernlightTool(base_url="http://fake-service")

    # Test action=similar
    args = {"action": "similar", "query": "hello", "documents": ["hi"]}
    res = tool.execute(args)
    assert "res1" in res

    # Test action=embed
    mock_resp.json.return_value = {"embedding": [1, 2]}
    args = {"action": "embed", "text": "hello"}
    res = tool.execute(args)
    assert "[1, 2]" in res
