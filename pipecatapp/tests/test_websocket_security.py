import pytest
from unittest.mock import MagicMock, patch
import sys

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
from pipecatapp.web_server import app
import pipecatapp.web_server

def test_websocket_accepts_trusted_origin():
    client = TestClient(app)
    with patch("pipecatapp.web_server.get_allowed_origins", return_value=["http://localhost"]):
        try:
            with client.websocket_connect("/ws", headers={"Origin": "http://localhost"}) as websocket:
                websocket.send_json({"type": "ping"})
        except WebSocketDisconnect:
            pytest.fail("WebSocket rejected trusted origin")

def test_websocket_rejects_untrusted_origin():
    client = TestClient(app)
    with patch("pipecatapp.web_server.get_allowed_origins", return_value=["http://localhost"]):
        with pytest.raises(WebSocketDisconnect) as excinfo:
            with client.websocket_connect("/ws", headers={"Origin": "http://evil.com"}) as websocket:
                websocket.receive_text()
        assert excinfo.value.code == 1008

def test_websocket_allows_wildcard():
    client = TestClient(app)
    with patch("pipecatapp.web_server.get_allowed_origins", return_value=["*"]):
        try:
            with client.websocket_connect("/ws", headers={"Origin": "http://evil.com"}) as websocket:
                websocket.send_json({"type": "ping"})
        except WebSocketDisconnect:
            pytest.fail("WebSocket rejected wildcard origin")

def test_websocket_default_secure_same_origin_success():
    client = TestClient(app)
    with patch("pipecatapp.web_server.get_allowed_origins", return_value=[]):
        try:
            with client.websocket_connect("/ws", headers={"Origin": "http://testserver"}) as websocket:
                websocket.send_json({"type": "ping"})
        except WebSocketDisconnect:
            pytest.fail("WebSocket rejected same-origin connection")

def test_websocket_default_secure_same_origin_failure():
    client = TestClient(app)
    with patch("pipecatapp.web_server.get_allowed_origins", return_value=[]):
        with pytest.raises(WebSocketDisconnect) as excinfo:
            with client.websocket_connect("/ws", headers={"Origin": "http://attacker.com"}) as websocket:
                websocket.receive_text()
        assert excinfo.value.code == 1008

def test_websocket_default_secure_missing_origin():
    client = TestClient(app)
    with patch("pipecatapp.web_server.get_allowed_origins", return_value=[]):
        with pytest.raises(WebSocketDisconnect) as excinfo:
            with client.websocket_connect("/ws") as websocket:
                websocket.receive_text()
        assert excinfo.value.code == 1008

