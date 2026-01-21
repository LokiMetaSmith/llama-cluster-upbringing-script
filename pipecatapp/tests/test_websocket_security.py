import sys
from unittest.mock import MagicMock

# Mock out heavy dependencies that cause timeouts during import
sys.modules["workflow.runner"] = MagicMock()
sys.modules["workflow.history"] = MagicMock()
sys.modules["workflow"] = MagicMock()
sys.modules["pipecat"] = MagicMock()
sys.modules["pipecat.services.openai.llm"] = MagicMock()
sys.modules["ultralytics"] = MagicMock()
sys.modules["faster_whisper"] = MagicMock()
sys.modules["piper"] = MagicMock()
sys.modules["piper.voice"] = MagicMock()
sys.modules["consul"] = MagicMock()
sys.modules["consul.aio"] = MagicMock()

from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from web_server import app
import pytest
from unittest.mock import patch

client = TestClient(app)

def test_websocket_accepts_trusted_origin():
    """
    Test that the WebSocket accepts connections from trusted origins.
    """
    # We patch the 'allowed_origins' list that we will access in the endpoint
    with patch("web_server.allowed_origins", ["http://localhost"]):
        try:
            with client.websocket_connect("/ws", headers={"Origin": "http://localhost"}) as websocket:
                # Send a message to verify connection is open
                websocket.send_json({"type": "ping"})
        except WebSocketDisconnect:
            pytest.fail("WebSocket rejected trusted origin")

def test_websocket_rejects_untrusted_origin():
    """
    Test that the WebSocket rejects connections from untrusted origins.
    This simulates a Cross-Site WebSocket Hijacking attempt.
    """
    with patch("web_server.allowed_origins", ["http://localhost"]):
        with pytest.raises(WebSocketDisconnect) as excinfo:
            with client.websocket_connect("/ws", headers={"Origin": "http://evil.com"}) as websocket:
                websocket.receive_text()

        # Verify the close code is 1008 (Policy Violation)
        assert excinfo.value.code == 1008

def test_websocket_allows_wildcard():
    """
    Test that the WebSocket accepts all origins if configured with wildcard '*'.
    """
    with patch("web_server.allowed_origins", ["*"]):
         with client.websocket_connect("/ws", headers={"Origin": "http://evil.com"}) as websocket:
             pass
