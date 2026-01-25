import os
import sys
import logging
import time
import asyncio
import requests
from pmm_memory_client import PMMMemoryClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JanitorAgent")

class JanitorAgent:
    def __init__(self):
        self.worker_id = f"janitor_{os.getpid()}"
        self.memory_url = None
        self.memory_client = None
        self.running = True
        self.supported_types = ["llm_failure", "test_failure", "app_crash"]

    def discover_services(self):
        """Discovers Memory Service via Consul or Environment."""
        consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")

        # Try direct env var first (useful for testing)
        if os.getenv("MEMORY_SERVICE_URL"):
             self.memory_url = os.getenv("MEMORY_SERVICE_URL")
             self.memory_client = PMMMemoryClient(base_url=self.memory_url)
             logger.info(f"Using configured Memory Service at {self.memory_url}")
             return

        try:
            resp = requests.get(f"{consul_addr}/v1/catalog/service/memory-service")
            if resp.status_code == 200:
                services = resp.json()
                if services:
                    svc = services[0]
                    addr = svc.get("ServiceAddress", "localhost")
                    port = svc.get("ServicePort", 8000)
                    self.memory_url = f"http://{addr}:{port}"
                    self.memory_client = PMMMemoryClient(base_url=self.memory_url)
                    logger.info(f"Discovered Memory Service at {self.memory_url}")
        except Exception as e:
            logger.warning(f"Failed to discover services: {e}")

    async def process_item(self, item: dict):
        """Simulates processing of a DLQ item."""
        logger.info(f"Processing DLQ Item: {item['id']} ({item['event_type']})")

        # Check retry limit
        if item.get("retry_count", 0) > 3:
            logger.warning(f"Item {item['id']} exceeded max retries. Marking FAILED.")
            await self.memory_client.update_dlq_item(
                item_id=item['id'],
                status="FAILED",
                result="Max retries exceeded"
            )
            return

        # Simulate work
        await asyncio.sleep(1)

        # Simple logic: succeed unless the payload says 'force_fail'
        payload = item.get("payload", {})
        if payload.get("force_fail"):
            logger.warning(f"Item {item['id']} forced to fail.")
            # Mark as PENDING for retry, increment count
            await self.memory_client.update_dlq_item(
                item_id=item['id'],
                status="PENDING",
                result="Forced failure for testing",
                retry_after=time.time() + 2, # Retry in 2 seconds for test speed
                increment_retry=True
            )
        else:
            logger.info(f"Item {item['id']} processed successfully.")
            await self.memory_client.update_dlq_item(
                item_id=item['id'],
                status="SUCCEEDED",
                result="Janitor cleaned up the mess."
            )

    async def run(self):
        logger.info(f"Janitor Agent {self.worker_id} starting...")
        self.discover_services()

        if not self.memory_client:
            logger.error("Could not connect to Memory Service. Exiting.")
            return

        while self.running:
            try:
                item = await self.memory_client.claim_dlq_item(
                    worker_id=self.worker_id,
                    supported_types=self.supported_types
                )

                if item:
                    await self.process_item(item)
                else:
                    # No work, sleep
                    await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(5)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    agent = JanitorAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("Janitor stopping...")
