import os
import asyncio
import logging
import httpx
from pipecatapp.net_utils import format_url

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("app-health-monitor")

class AppHealthMonitor:
    """Background service that periodically checks the health of installed community container apps

    via Consul and Nomad APIs, triggering automatic Ansible reconciliation if an app becomes degraded.
    """
    def __init__(self, interval: int = 300):
        self.interval = interval
        self.cluster_ip = os.getenv("CLUSTER_IP", "127.0.0.1")
        self.consul_url = format_url("http", os.getenv("CONSUL_HOST", self.cluster_ip), 8500)
        self.nomad_url = format_url("http", os.getenv("NOMAD_HOST", self.cluster_ip), 4646)
        self.is_running = False

    async def check_and_reconcile(self):
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                # Query installed jobs from Nomad
                res = await client.get(f"{self.nomad_url}/v1/jobs")
                if res.status_code != 200:
                    return

                jobs = res.json()
                for job in jobs:
                    job_id = job.get("ID", "")
                    status = job.get("Status", "")

                    if status == "dead" or status == "degraded":
                        logger.warning(f"Community app '{job_id}' is {status}. Triggering self-healing reconciliation...")
                        await self.trigger_reconciliation(job_id)

            except Exception as e:
                logger.error(f"Error checking app health: {e}")

    async def trigger_reconciliation(self, app_id: str):
        cmd = [
            "uvx", "--from", "ansible-core", "ansible-playbook",
            "-i", "localhost,", "-c", "local",
            "playbooks/deploy_community_app.yaml",
            "-e", f"app_name={app_id}"
        ]
        try:
            proc = await asyncio.create_subprocess_exec(*cmd)
            await proc.communicate()
            logger.info(f"Reconciliation trigger finished for {app_id} with returncode {proc.returncode}")
        except Exception as e:
            logger.error(f"Failed to execute self-healing playbook for {app_id}: {e}")

    async def start_loop(self):
        self.is_running = True
        logger.info(f"AppHealthMonitor started with check interval {self.interval}s")
        while self.is_running:
            await self.check_and_reconcile()
            await asyncio.sleep(self.interval)

if __name__ == "__main__":
    monitor = AppHealthMonitor(interval=60)
    asyncio.run(monitor.start_loop())
