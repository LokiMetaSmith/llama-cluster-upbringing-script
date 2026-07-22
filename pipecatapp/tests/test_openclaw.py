import pytest
import asyncio
import json
from unittest.mock import MagicMock, AsyncMock, patch
from integrations.openclaw import OpenClawClient
from pipecatapp.tools.openclaw_tool import OpenClawTool

@pytest.mark.asyncio
async def test_openclaw_client_handshake_and_send():
    # Setup messages
    challenge_msg = json.dumps({
        "type": "event",
        "event": "connect.challenge",
        "payload": {"nonce": "12345", "ts": 123456789}
    })

    hello_ok_msg = json.dumps({
        "type": "res",
        "id": "mock_id",
        "ok": True,
        "payload": {"type": "hello-ok"}
    })

    send_response_msg_template = {
        "type": "res",
        "ok": True,
        "payload": {"id": "msg_123"}
    }

    class MockWebSocket:
        def __init__(self):
            self.incoming = asyncio.Queue()
            self.sent = []

        async def close(self):
            pass

        async def __aiter__(self):
            while True:
                msg = await self.incoming.get()
                if msg is None:
                    break
                yield msg

        async def send(self, msg_str):
            self.sent.append(msg_str)
            msg = json.loads(msg_str)
            if msg['type'] == 'req':
                if msg['method'] == 'connect':
                    await self.incoming.put(hello_ok_msg)
                elif msg['method'] == 'message.send':
                    resp = send_response_msg_template.copy()
                    resp['id'] = msg['id']
                    await self.incoming.put(json.dumps(resp))

    mock_ws = MockWebSocket()
    await mock_ws.incoming.put(challenge_msg)


    class AsyncContextManagerMock:
        def __await__(self):
            async def get_ws():
                return mock_ws
            return get_ws().__await__()

        async def __aenter__(self):
            return mock_ws

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    def mock_connect_sync(*args, **kwargs):
        return AsyncContextManagerMock()

    with patch('websockets.connect', side_effect=mock_connect_sync) as mock_connect:
        client = OpenClawClient("ws://test")
        await client.connect()

        assert client._connected
        assert client._handshake_complete.is_set()

        # Test Send Message
        res = await client.send_message("123", "hello")
        assert res['ok'] is True
        assert res['payload']['id'] == "msg_123"

        # Verify connect request params
        connect_req = json.loads(mock_ws.sent[0])
        assert connect_req['method'] == 'connect'
        assert connect_req['params']['role'] == 'operator'

        send_req = json.loads(mock_ws.sent[1])
        assert send_req['method'] == 'message.send'
        assert send_req['params']['target'] == '123'
        assert send_req['params']['message'] == 'hello'

        # Clean up
        await mock_ws.incoming.put(None)
        await client.disconnect()

@pytest.mark.asyncio
async def test_openclaw_tool():
    tool = OpenClawTool("ws://test")
    tool.client = MagicMock()
    tool.client.connect = AsyncMock()
    tool.client.send_message = AsyncMock(return_value={"ok": True, "payload": {"id": "msg_123"}})

    result = await tool.send_message("123", "hi")

    tool.client.connect.assert_called_once()
    tool.client.send_message.assert_called_once_with("123", "hi", None)
    assert "Message sent successfully" in result