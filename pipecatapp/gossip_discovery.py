import asyncio
import json
import logging
import socket
import time
import hashlib
from typing import Dict, Optional, List, Tuple, Any

logger = logging.getLogger(__name__)

class SimpleBloomFilter:
    """A lightweight, dependency-free Bloom filter implementation."""
    def __init__(self, size: int = 256, hash_count: int = 3, bit_array: int = 0):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bit_array

    def add(self, item: str):
        for i in range(self.hash_count):
            digest = hashlib.sha256(f"{item}{i}".encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.size
            self.bit_array |= (1 << index)

    def check(self, item: str) -> bool:
        for i in range(self.hash_count):
            digest = hashlib.sha256(f"{item}{i}".encode('utf-8')).hexdigest()
            index = int(digest, 16) % self.size
            if (self.bit_array & (1 << index)) == 0:
                return False
        return True

    def to_hex(self) -> str:
        return hex(self.bit_array)[2:]

    @classmethod
    def from_hex(cls, hex_str: str, size: int = 256, hash_count: int = 3):
        try:
            return cls(size=size, hash_count=hash_count, bit_array=int(hex_str, 16))
        except ValueError:
            return cls(size=size, hash_count=hash_count)


class GossipDiscovery:
    """
    A lightweight UDP gossip protocol for service discovery.
    Provides a fallback when Consul/Raft is unavailable.
    """
    def __init__(self, port: int = 7946, host: str = "0.0.0.0", local_ip: Optional[str] = None):
        self.port = port
        self.host = host
        self.local_ip = local_ip or self._get_local_ip()
        self.services: Dict[str, Dict[str, Any]] = {}  # service_name -> {"ip": "1.2.3.4", "port": 8080, "last_seen": 12345}
        self.transport = None
        self.running = False
        self.ttl = 30  # seconds until a service is considered dead without heartbeat

    def _get_local_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Doesn't have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def register_service(self, service_name: str, port: int, capabilities: Optional[List[str]] = None, extensions: Optional[Dict[str, Any]] = None):
        """Registers a local service to be broadcasted, optionally with capabilities and extensible metadata payloads (GGEP-style)."""
        bloom_hex = None
        if capabilities:
            bf = SimpleBloomFilter()
            for cap in capabilities:
                bf.add(cap)
            bloom_hex = bf.to_hex()

        self.services[service_name] = {
            "ip": self.local_ip,
            "port": port,
            "last_seen": time.time(),
            "local": True,
            "bloom_filter": bloom_hex,
            "extensions": extensions or {}
        }

    def get_service(self, service_name: str) -> Optional[Tuple[str, int]]:
        """Returns the (ip, port) of a requested service, or None if not found/expired."""
        self._cleanup_stale_services()
        svc = self.services.get(service_name)
        if svc:
            return svc["ip"], svc["port"]
        return None

    def find_capable_service(self, capability: str) -> Optional[Tuple[str, int]]:
        """Finds the first service that advertises support for the given capability via its Bloom filter."""
        self._cleanup_stale_services()
        for name, data in self.services.items():
            bloom_hex = data.get("bloom_filter")
            if bloom_hex:
                bf = SimpleBloomFilter.from_hex(bloom_hex)
                if bf.check(capability):
                    return data["ip"], data["port"]
        return None

    def _cleanup_stale_services(self):
        now = time.time()
        stale_keys = []
        for name, data in self.services.items():
            if not data.get("local", False) and now - data["last_seen"] > self.ttl:
                stale_keys.append(name)

        for k in stale_keys:
            logger.info(f"Gossip: Removing stale service {k}")
            del self.services[k]

    class GossipProtocol(asyncio.DatagramProtocol):
        def __init__(self, parent):
            self.parent = parent

        def connection_made(self, transport):
            self.parent.transport = transport

        def datagram_received(self, data, addr):
            try:
                message = json.loads(data.decode('utf-8'))
                self.parent._handle_message(message, addr)
            except json.JSONDecodeError:
                pass

    def _handle_message(self, message: dict, addr: Tuple[str, int]):
        if message.get("type") == "ANNOUNCE":
            service_name = message.get("service")
            port = message.get("port")
            ip = message.get("ip", addr[0])  # Trust payload IP, or fallback to packet source
            bloom_filter = message.get("bloom_filter")
            extensions = message.get("extensions", {})

            if service_name and port:
                # Update our registry
                self.services[service_name] = {
                    "ip": ip,
                    "port": port,
                    "last_seen": time.time(),
                    "local": False,
                    "bloom_filter": bloom_filter,
                    "extensions": extensions
                }

    async def _broadcast_loop(self):
        """Periodically broadcasts local services to the subnet."""
        # Simple UDP broadcast to the local /24 subnet
        parts = self.local_ip.split('.')
        if len(parts) == 4 and self.local_ip != '127.0.0.1':
            broadcast_ip = f"{parts[0]}.{parts[1]}.{parts[2]}.255"
        else:
            broadcast_ip = "255.255.255.255"

        while self.running:
            if self.transport:
                for name, data in self.services.items():
                    if data.get("local", False):
                        msg = {
                            "type": "ANNOUNCE",
                            "service": name,
                            "ip": self.local_ip,
                            "port": data["port"]
                        }
                        if data.get("bloom_filter"):
                            msg["bloom_filter"] = data["bloom_filter"]
                        if data.get("extensions"):
                            msg["extensions"] = data["extensions"]
                        payload = json.dumps(msg).encode('utf-8')
                        try:
                            self.transport.sendto(payload, (broadcast_ip, self.port))
                        except Exception as e:
                            logger.debug(f"Gossip broadcast failed: {e}")
            await asyncio.sleep(5)  # Broadcast every 5 seconds

    async def start(self):
        """Starts the gossip UDP listener and broadcast loop."""
        if self.running:
            return

        logger.info(f"Starting Gossip Discovery on {self.host}:{self.port}")
        self.running = True
        loop = asyncio.get_running_loop()

        # We need to set SO_BROADCAST to allow sending broadcast packets
        # And SO_REUSEADDR so multiple apps on the same host can bind to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # On some systems, binding to "" or "0.0.0.0" is needed to receive broadcasts
        try:
            sock.bind((self.host, self.port))
        except OSError as e:
            logger.warning(f"Gossip failed to bind to {self.host}:{self.port}: {e}")
            self.running = False
            return

        await loop.create_datagram_endpoint(
            lambda: self.GossipProtocol(self),
            sock=sock
        )

        # Start background broadcaster
        asyncio.create_task(self._broadcast_loop())

    async def stop(self):
        self.running = False
        if self.transport:
            self.transport.close()

# Global instance for the app to use
gossip_registry = GossipDiscovery()
