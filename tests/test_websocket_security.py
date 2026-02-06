
import pytest
import sys
import os
from unittest.mock import MagicMock, AsyncMock

# 1. Setup mocks for heavy dependencies BEFORE importing web_server
sys.modules['pipecat.services.openai.llm'] = MagicMock()
sys.modules['pipecat'] = MagicMock()
sys.modules['ultralytics'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['faiss'] = MagicMock()
sys.modules['faster_whisper'] = MagicMock()
sys.modules['piper'] = MagicMock()
sys.modules['RealtimeSTT'] = MagicMock()
# Mock workflow runner to prevent it from trying to load nodes/files
sys.modules['workflow.runner'] = MagicMock()
sys.modules['workflow.nodes'] = MagicMock()

# Add pipecatapp to path so we can import web_server
sys.path.insert(0, os.path.abspath("pipecatapp"))

# Now import web_server
import web_server
from fastapi.testclient import TestClient

# Mock the asyncio queue
web_server.text_message_queue = AsyncMock()
web_server.approval_queue = AsyncMock()

client = TestClient(web_server.app)

def test_websocket_ssrf_vulnerability():
    """
    Test that sending a 'response_url' in a user message via WebSocket
    is STRIPPED or rejected.
    """
    print(f"Queue object: {web_server.text_message_queue}")

    # Need to pass Origin header to pass security checks in websocket_endpoint
    with client.websocket_connect("/ws", headers={"Origin": "http://testserver"}) as websocket:
        # 1. Send malicious payload
        payload = {
            "type": "user_message",
            "text": "Hello Agent",
            "response_url": "http://evil.com/callback", # <-- Vulnerability
            "request_id": "12345"
        }
        websocket.send_json(payload)

        # 2. Check what was put into the queue
        # TestClient interacts with the app. We verify if the mock was called.

        if web_server.text_message_queue.put.call_count == 0:
            print("Queue put was not called yet.")
            # This is strange. Maybe exceptions occurred?
            return

        args, _ = web_server.text_message_queue.put.call_args
        message = args[0]

        print(f"DEBUG: Message in queue: {message}")

        # Assertions
        assert message["text"] == "Hello Agent"

        if "response_url" in message:
             print("VULNERABILITY CONFIRMED: response_url is present in the queued message.")
        else:
             print("SECURE: response_url was stripped.")

        # For the purpose of the test suite (once fixed), we want to assert it is NOT present.
        assert "response_url" not in message, "response_url should be stripped from WebSocket messages to prevent SSRF"
