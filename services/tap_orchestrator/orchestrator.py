import asyncio
import logging
import subprocess
import shlex
import httpx
from typing import Optional, Dict, Any
from config import settings
from models import AuthentikUser

logger = logging.getLogger(__name__)

class ClusterOrchestrator:
    def __init__(self):
        self.nomad_api_url = settings.nomad_api_url.rstrip('/')
        self.vault_api_url = settings.vault_api_url.rstrip('/')
        # Don't use a shared http_client for all requests because we want these to be transient

    async def wake_node(self, mac_address: str, ipmi_host: Optional[str] = None):
        """
        Sends a WOL packet or IPMI command to wake a node.
        """
        logger.info(f"Attempting to wake node with MAC: {mac_address}")
        try:
            # 1. Try Wake-on-LAN first
            process = await asyncio.create_subprocess_exec(
                "wakeonlan", mac_address,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                logger.info(f"WOL command successful for {mac_address}")
            else:
                logger.warning(f"WOL command failed: {stderr.decode()}")

            # 2. Try IPMI if configured
            if ipmi_host:
                logger.info(f"Attempting IPMI power on for {ipmi_host}")
                # This is a placeholder for actual IPMI creds, typically loaded from secrets
                # cmd = f"ipmitool -I lanplus -H {ipmi_host} -U admin -P admin power on"
                # For safety, we just log it in this implementation unless specific creds are provided
                pass

        except Exception as e:
            logger.error(f"Error executing wake command: {e}")

    async def allocate_user_resources(self, user: AuthentikUser, resource_config: Dict[str, Any]):
        """
        Interacts with Nomad to allocate resources/mounts for the user.
        """
        target_node = resource_config.get("gpu_node")
        vector_store = user.attributes.get("vector_store_path")

        logger.info(f"Allocating cluster resources for {user.username} on node {target_node}")

        if not target_node:
            logger.warning(f"No target node specified for user {user.username}")
            return

        try:
            # Example API call to Nomad to trigger a parameterized job or update an allocation
            # For demonstration, we'll hit a dummy endpoint or use a dry-run log
            async with httpx.AsyncClient() as client:
                # url = f"{self.nomad_api_url}/v1/job/user-llm-{user.username}/dispatch"
                # payload = {"Payload": b64encode(json.dumps({"vector_store": vector_store}).encode()).decode()}
                # response = await client.post(url, json=payload)
                logger.info(f"[Dry Run] Nomad dispatch for {user.username} to {target_node} with vector_store={vector_store}")

        except Exception as e:
            logger.error(f"Error communicating with Nomad API: {e}")

    async def issue_ephemeral_credentials(self, user: AuthentikUser):
        """
        Interacts with Vault or local CA to issue short-lived SSH credentials.
        """
        logger.info(f"Issuing ephemeral credentials for {user.username}")
        try:
            async with httpx.AsyncClient() as client:
                # url = f"{self.vault_api_url}/v1/ssh/sign/local-user"
                # data = {"public_key": "...", "valid_principals": user.username}
                # response = await client.post(url, json=data)
                logger.info(f"[Dry Run] Vault SSH cert request for {user.username}")
        except Exception as e:
            logger.error(f"Error communicating with Vault API: {e}")

    async def execute_hot_load(self, user: AuthentikUser):
        """
        Main orchestration sequence.
        """
        resource_map = settings.cluster_resource_map
        user_config = resource_map.get(user.username, {})

        if not user_config:
            logger.warning(f"No cluster resource map found for user {user.username}")

        mac_addr = user_config.get("mac_address")
        if mac_addr:
            await self.wake_node(mac_addr, user_config.get("ipmi_host"))

        await self.allocate_user_resources(user, user_config)
        await self.issue_ephemeral_credentials(user)

cluster_orchestrator = ClusterOrchestrator()
