import asyncio
import logging
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
            import json
            import base64

            # Dispatch a parameterized Nomad job specifically configured for user resource environments
            # Passing vector_store and other attributes via Meta blocks allows the Nomad template to mount them
            async with httpx.AsyncClient(timeout=10.0) as client:
                job_id = f"user-llm"
                url = f"{self.nomad_api_url}/v1/job/{job_id}/dispatch"

                dispatch_payload = {
                    "Meta": {
                        "user_id": user.username,
                        "vector_store_path": vector_store or "",
                        "target_gpu_node": target_node,
                        "models": ",".join(resource_config.get("models", []))
                    }
                }

                # In parameterized jobs, we can pass arbitrary opaque data in Payload, Base64 encoded
                # We'll pass the full user attributes just in case the job needs them
                payload_str = json.dumps(user.attributes)
                payload_b64 = base64.b64encode(payload_str.encode()).decode()
                dispatch_payload["Payload"] = payload_b64

                response = await client.post(url, json=dispatch_payload)
                response.raise_for_status()

                res_data = response.json()
                logger.info(f"Successfully dispatched Nomad job for {user.username}. DispatchedJobID: {res_data.get('DispatchedJobID')}")

        except httpx.HTTPStatusError as e:
            # Handle cases where the parameterized job doesn't exist yet
            if e.response.status_code == 404:
                logger.warning(f"Parameterized Nomad job '{job_id}' not found. Ensure the template is deployed.")
            else:
                logger.error(f"HTTP error communicating with Nomad API: {e} - {e.response.text}")
        except Exception as e:
            logger.error(f"Error communicating with Nomad API: {e}")

    async def issue_ephemeral_credentials(self, user: AuthentikUser, public_key: str = ""):
        """
        Interacts with Vault or local CA to issue short-lived SSH credentials.
        Since public keys are typically required for signing, this might be fetched from Authentik attributes or a local store.
        """
        logger.info(f"Issuing ephemeral credentials for {user.username}")

        # If public key isn't provided, see if it exists in the user's Authentik attributes
        pub_key_to_sign = public_key or user.attributes.get("ssh_public_key")

        if not pub_key_to_sign:
            logger.warning(f"No SSH public key available to sign for user {user.username}. Skipping Vault cert issuance.")
            return

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Typically, Vault SSH secrets engine is mounted at /v1/ssh
                # and you sign client keys against a specific role (e.g. 'local-user')
                vault_role = "local-user"
                url = f"{self.vault_api_url}/v1/ssh/sign/{vault_role}"

                # In a real environment, you'd also pass X-Vault-Token for auth
                headers = {}
                vault_token = user.attributes.get("vault_token") # Or perhaps a service token
                if vault_token:
                    headers["X-Vault-Token"] = vault_token
                else:
                    logger.warning("No Vault token provided. Request may fail if unauthenticated access is disabled.")

                data = {
                    "public_key": pub_key_to_sign,
                    "valid_principals": user.username,
                    # e.g. valid for 1 hour
                    "ttl": "1h",
                    "extensions": {
                        "permit-pty": "",
                        "permit-port-forwarding": ""
                    }
                }

                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()

                res_data = response.json()
                signed_cert = res_data.get("data", {}).get("signed_key")

                if signed_cert:
                    logger.info(f"Successfully generated signed SSH certificate for {user.username}")
                    # In a fully integrated system, you might push this cert back to the user via an out-of-band channel
                    # or drop it into a secure distributed store (like Consul KV under their namespace)
                else:
                    logger.warning(f"Vault responded successfully but no signed_key found in payload for {user.username}")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error communicating with Vault API: {e} - {e.response.text}")
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
