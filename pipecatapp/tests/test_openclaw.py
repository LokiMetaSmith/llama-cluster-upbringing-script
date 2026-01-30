import pytest
import asyncio
import json
from unittest.mock import MagicMock, AsyncMock, patch
from integrations.openclaw import OpenClawClient
from tools.openclaw_tool import OpenClawTool

@pytest.mark.asyncio
async def test_openclaw_client_handshake_and_send():
    # Mock WebSocket connection
    mock_ws = MagicMock()

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

    incoming_queue = asyncio.Queue()

    async def mock_iter():
        while True:
            msg = await incoming_queue.get()
            if msg is None: break
            yield msg

    mock_ws.__aiter__.side_effect = mock_iter

    # Intercept send to respond
    async def mock_send(msg_str):
        msg = json.loads(msg_str)
        if msg['type'] == 'req':
            if msg['method'] == 'connect':
                # Respond with hello-ok
                # Note: real server echoes ID, but our client logic for handshake just checks for payload type
                await incoming_queue.put(hello_ok_msg)
            elif msg['method'] == 'message.send':
                # Respond with success and matching ID
                resp = send_response_msg_template.copy()
                resp['id'] = msg['id']
                await incoming_queue.put(json.dumps(resp))

    mock_ws.send = AsyncMock(side_effect=mock_send)
    mock_ws.close = AsyncMock()

    # Initial challenge (pushed immediately upon connect)
    await incoming_queue.put(challenge_msg)

    with patch('websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = mock_ws
        client = OpenClawClient("ws://test")

        # Test Connect
        await client.connect()
        assert client._connected
        assert client._handshake_complete.is_set()

        # Test Send Message
        res = await client.send_message("123", "hello")
        assert res['ok'] is True
        assert res['payload']['id'] == "msg_123"

        # Verify connect request params
        calls = mock_ws.send.call_args_list
        # calls[0] should be connect request
        connect_req = json.loads(calls[0][0][0])
        assert connect_req['method'] == 'connect'
        assert connect_req['params']['role'] == 'operator'

        # calls[1] should be message.send
        send_req = json.loads(calls[1][0][0])
        assert send_req['method'] == 'message.send'
        assert send_req['params']['target'] == '123'
        assert send_req['params']['message'] == 'hello'

        # Clean up
        await incoming_queue.put(None) # Stop iterator
        await client.disconnect()

@pytest.mark.asyncio
async def test_openclaw_tool():
    # Similar setup but testing the tool wrapper
    with patch('integrations.openclaw.OpenClawClient.connect', new_callable=AsyncMock) as mock_connect, \
         patch('integrations.openclaw.OpenClawClient.send_message', new_callable=AsyncMock) as mock_send:

        tool = OpenClawTool("ws://test")

        mock_send.return_value = {"ok": True, "payload": {"id": "msg_123"}}

        result = await tool.send_message("123", "hi")

        mock_connect.assert_called_once()
        mock_send.assert_called_once_with("123", "hi", None)
        assert "Message sent successfully" in result
