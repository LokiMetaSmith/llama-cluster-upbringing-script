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
    Test that the WebSocket accepts connections from trusted origins when explicitly configured.
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
    Test that the WebSocket rejects connections from untrusted origins when explicitly configured.
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
    Test that the WebSocket accepts all origins if EXPLICITLY configured with wildcard '*'.
    """
    with patch("web_server.allowed_origins", ["*"]):
         with client.websocket_connect("/ws", headers={"Origin": "http://evil.com"}) as websocket:
             pass

def test_websocket_default_secure_same_origin_success():
    """
    Test that the WebSocket accepts Same-Origin connections when allowed_origins is empty (default strict mode).
    """
    # Simulate default behavior (allowed_origins = [])
    with patch("web_server.allowed_origins", []):
         # TestClient uses 'testserver' as Host by default.
         # So we set Origin to match it.
         with client.websocket_connect("/ws", headers={"Origin": "http://testserver"}) as websocket:
             websocket.send_json({"type": "ping"})

def test_websocket_default_secure_same_origin_failure():
    """
    Test that the WebSocket rejects Cross-Origin connections when allowed_origins is empty (default strict mode).
    """
    # Simulate default behavior (allowed_origins = [])
    with patch("web_server.allowed_origins", []):
         with pytest.raises(WebSocketDisconnect) as excinfo:
             # Origin does NOT match Host (testserver)
             with client.websocket_connect("/ws", headers={"Origin": "http://attacker.com"}) as websocket:
                 websocket.receive_text()

         # Verify the close code is 1008 (Policy Violation)
         assert excinfo.value.code == 1008

def test_websocket_default_secure_missing_origin():
    """
    Test that the WebSocket rejects connections without Origin header when in default strict mode.
    """
    with patch("web_server.allowed_origins", []):
         with pytest.raises(WebSocketDisconnect) as excinfo:
             # No Origin header
             with client.websocket_connect("/ws") as websocket:
                 websocket.receive_text()

         # Verify the close code is 1008 (Policy Violation)
         assert excinfo.value.code == 1008
