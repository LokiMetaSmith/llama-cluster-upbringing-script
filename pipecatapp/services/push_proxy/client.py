import asyncio
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PushProxyClient:
    def __init__(self, proxy_host: str, proxy_port: int, worker_id: str, local_service_port: int = 4646):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.worker_id = worker_id
        self.local_service_port = local_service_port # E.g., local Nomad client port

    async def connect_and_serve(self):
        while True:
            try:
                logger.info(f"Connecting to proxy at {self.proxy_host}:{self.proxy_port}...")
                reader, writer = await asyncio.open_connection(self.proxy_host, self.proxy_port)

                # Send handshake
                writer.write(f"{self.worker_id}\n".encode())
                await writer.drain()

                # Read response
                response = await reader.read(1024)
                response_str = response.decode().strip()
                if response_str.startswith("OK:"):
                    assigned_port = int(response_str.split(":")[1])
                    logger.info(f"Connected! Proxy is forwarding traffic on port {assigned_port} to us.")
                else:
                    logger.error(f"Unexpected proxy response: {response_str}")
                    writer.close()
                    await asyncio.sleep(5)
                    continue

                # Now wait for incoming traffic from the proxy, and forward it to our local service
                while True:
                    data = await reader.read(4096)
                    if not data:
                        logger.warning("Connection to proxy closed by server.")
                        break

                    # We got a connection/data from the proxy. Forward it to local Nomad
                    logger.info(f"Received {len(data)} bytes from proxy, forwarding to local port {self.local_service_port}")
                    try:
                        local_reader, local_writer = await asyncio.open_connection("127.0.0.1", self.local_service_port)
                        local_writer.write(data)
                        await local_writer.drain()

                        # Read response from local service and send back to proxy
                        async def forward_local_to_proxy(l_reader, p_writer):
                            try:
                                while True:
                                    local_data = await l_reader.read(4096)
                                    if not local_data:
                                        break
                                    p_writer.write(local_data)
                                    await p_writer.drain()
                            except Exception as e:
                                logger.error(f"Error forwarding local to proxy: {e}")
                            finally:
                                p_writer.close()

                        asyncio.create_task(forward_local_to_proxy(local_reader, writer))

                    except Exception as e:
                        logger.error(f"Failed to connect to local service on port {self.local_service_port}: {e}")

            except ConnectionRefusedError:
                logger.error("Connection refused. Retrying in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Connection error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push Proxy Client for NAT Traversal")
    parser.add_argument("--proxy-host", required=True, help="IP or hostname of the push proxy server")
    parser.add_argument("--proxy-port", type=int, default=9000, help="Port of the push proxy server")
    parser.add_argument("--worker-id", required=True, help="Unique ID for this worker")
    parser.add_argument("--local-port", type=int, default=4646, help="Local port to forward traffic to (e.g., 4646 for Nomad)")
    args = parser.parse_args()

    client = PushProxyClient(proxy_host=args.proxy_host, proxy_port=args.proxy_port, worker_id=args.worker_id, local_service_port=args.local_port)
    asyncio.run(client.connect_and_serve())
