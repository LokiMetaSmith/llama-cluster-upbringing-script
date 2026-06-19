import asyncio
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PushProxyServer:
    def __init__(self, bind_host: str = "0.0.0.0", bind_port: int = 9000, tunnel_port_start: int = 10000):
        self.bind_host = bind_host
        self.bind_port = bind_port
        self.tunnel_port_start = tunnel_port_start
        self.active_workers = {}
        self.next_tunnel_port = self.tunnel_port_start

    async def handle_worker_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logger.info(f"New worker connection from {addr}")

        # Basic handshake: worker sends its ID
        try:
            data = await reader.read(1024)
            worker_id = data.decode().strip()
            if not worker_id:
                logger.warning("Empty worker ID, closing.")
                writer.close()
                return
        except Exception as e:
            logger.error(f"Error during handshake: {e}")
            writer.close()
            return

        tunnel_port = self.next_tunnel_port
        self.next_tunnel_port += 1

        self.active_workers[worker_id] = {
            'reader': reader,
            'writer': writer,
            'tunnel_port': tunnel_port
        }

        logger.info(f"Worker {worker_id} registered. Assigning tunnel port {tunnel_port}")
        writer.write(f"OK:{tunnel_port}\n".encode())
        await writer.drain()

        # Start a local server on the tunnel port to forward traffic TO the worker
        tunnel_server = await asyncio.start_server(
            lambda r, w: self.handle_tunnel_connection(r, w, worker_id),
            self.bind_host, tunnel_port
        )
        self.active_workers[worker_id]['server'] = tunnel_server

        try:
            # Keep connection alive and handle traffic from worker
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                # In a real implementation, this would route responses back to the correct client connection
                # For this PoC, we just log it or handle simple keepalives
                pass
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Worker {worker_id} connection error: {e}")
        finally:
            logger.info(f"Worker {worker_id} disconnected.")
            writer.close()
            if worker_id in self.active_workers:
                self.active_workers[worker_id]['server'].close()
                del self.active_workers[worker_id]

    async def handle_tunnel_connection(self, client_reader, client_writer, worker_id):
        # Someone connected to the tunnel port (e.g. Nomad server trying to reach the worker)
        logger.info(f"New connection on tunnel for worker {worker_id}")

        worker_conn = self.active_workers.get(worker_id)
        if not worker_conn:
            logger.error(f"Worker {worker_id} not found!")
            client_writer.close()
            return

        worker_writer = worker_conn['writer']
        worker_reader = worker_conn['reader']

        # Forward traffic. Note: A real implementation requires multiplexing (like yamux or ssh channels)
        # because multiple clients might use the same tunnel port, or the worker might send unsolicited data.
        # This simple PoC just forwards bytes back and forth for a single connection.

        async def forward(src, dst):
            try:
                while True:
                    data = await src.read(4096)
                    if not data:
                        break
                    dst.write(data)
                    await dst.drain()
            except Exception:
                pass
            finally:
                dst.close()

        await asyncio.gather(
            forward(client_reader, worker_writer),
            forward(worker_reader, client_writer)
        )

    async def start(self):
        server = await asyncio.start_server(self.handle_worker_connection, self.bind_host, self.bind_port)
        addr = server.sockets[0].getsockname()
        logger.info(f"Push Proxy Server listening on {addr}")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push Proxy Server for NAT Traversal")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=9000, help="Bind port for workers")
    args = parser.parse_args()

    proxy = PushProxyServer(bind_host=args.host, bind_port=args.port)
    asyncio.run(proxy.start())
