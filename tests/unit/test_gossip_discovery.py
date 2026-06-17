import pytest
import asyncio
import json
from unittest.mock import MagicMock, patch
from pipecatapp.gossip_discovery import GossipDiscovery

def test_gossip_registry_register_and_get():
    gossip = GossipDiscovery(local_ip="10.0.0.1")
    gossip.register_service("rpc-main", 8080)

    # Check we can get it
    addr = gossip.get_service("rpc-main")
    assert addr is not None
    assert addr == ("10.0.0.1", 8080)

    # Check non-existent
    assert gossip.get_service("missing") is None

def test_gossip_handle_message():
    gossip = GossipDiscovery(local_ip="10.0.0.1")
    message = {
        "type": "ANNOUNCE",
        "service": "ollama",
        "ip": "10.0.0.2",
        "port": 11434
    }

    gossip._handle_message(message, ("10.0.0.2", 7946))

    addr = gossip.get_service("ollama")
    assert addr is not None
    assert addr == ("10.0.0.2", 11434)

    # Ensure it's marked as non-local
    assert gossip.services["ollama"]["local"] is False

def test_cleanup_stale_services():
    gossip = GossipDiscovery(local_ip="10.0.0.1")
    gossip.ttl = 1  # 1 second TTL

    # Add a local service (should never expire)
    gossip.register_service("local-svc", 8080)

    # Add a remote service (should expire)
    gossip.services["remote-svc"] = {
        "ip": "10.0.0.2",
        "port": 9090,
        "last_seen": 0,  # Old timestamp
        "local": False
    }

    # Before cleanup
    assert "remote-svc" in gossip.services

    # Trigger cleanup via get_service
    gossip.get_service("remote-svc")

    # After cleanup
    assert "remote-svc" not in gossip.services
    assert "local-svc" in gossip.services  # Local service remains

@pytest.mark.asyncio
async def test_gossip_broadcast_loop():
    gossip = GossipDiscovery(local_ip="10.0.0.1")
    gossip.running = True
    gossip.register_service("rpc-main", 8080)

    mock_transport = MagicMock()
    gossip.transport = mock_transport

    # Run one iteration of the loop
    with patch("asyncio.sleep", side_effect=asyncio.CancelledError):
        try:
            await gossip._broadcast_loop()
        except asyncio.CancelledError:
            pass

    # Verify sendto was called
    assert mock_transport.sendto.called
    args = mock_transport.sendto.call_args[0]

    payload = json.loads(args[0].decode('utf-8'))
    assert payload["type"] == "ANNOUNCE"
    assert payload["service"] == "rpc-main"
    assert payload["ip"] == "10.0.0.1"
    assert payload["port"] == 8080

    assert args[1][0] == "10.0.0.255"  # Broadcast IP based on /24
    assert args[1][1] == 7946
