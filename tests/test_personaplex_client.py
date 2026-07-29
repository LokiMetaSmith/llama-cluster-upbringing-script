import pytest
import asyncio
import json
import binascii
from unittest.mock import AsyncMock, patch

from pipecatapp.persona_plex.state_adapter import StateAdapter
from command_deck.scripts.personaplex_client import PersonaPlexClient

def test_state_adapter_json():
    adapter = StateAdapter()
    json_state = '{"npc": {"name": "Omar Torres", "health": 100}, "location": "Tavern"}'
    flattened = adapter.flatten_state(json_state)
    assert "npc: name: Omar Torres. health: 100. location: Tavern" in flattened

def test_state_adapter_xml():
    adapter = StateAdapter()
    xml_state = '<state><npc name="Omar Torres"><health>100</health></npc><location>Tavern</location></state>'
    flattened = adapter.flatten_state(xml_state)
    assert "name: Omar Torres" in flattened
    assert "health: 100" in flattened
    assert "location: Tavern" in flattened

@pytest.mark.asyncio
async def test_personaplex_client():
    client = PersonaPlexClient(uri="ws://test:8080/stream", use_mock=True)

    # Mock the websocket
    mock_websocket = AsyncMock()

    # Setup recv to return a simulated response then raise exception to break loop
    simulated_pcm = b'\x00' * 1024 * 2
    simulated_hex = binascii.hexlify(simulated_pcm).decode('utf-8')
    mock_websocket.recv.side_effect = [
        json.dumps({"type": "audio", "data": simulated_hex}),
        Exception("Stop receiving")
    ]

    # Mock websockets.connect to yield the mock_websocket
    class MockConnectContextManager:
        async def __aenter__(self):
            return mock_websocket

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch('websockets.connect', return_value=MockConnectContextManager()):
        # Run for a short time
        task = asyncio.create_task(client.start())
        await asyncio.sleep(0.1)
        client.stop()
        await task

        # Verify that send was called
        mock_websocket.send.assert_called()
        args, _ = mock_websocket.send.call_args
        sent_data = json.loads(args[0])
        assert sent_data["type"] == "audio"
        assert "data" in sent_data
