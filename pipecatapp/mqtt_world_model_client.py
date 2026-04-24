import httpx
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MQTTWorldModelClient:
    """
    Client for interacting with the distributed MQTT-based World Model Service.
    """
    def __init__(self):
        self.world_model_url = os.getenv("WORLD_MODEL_URL", f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8000")

    def get_state(self) -> Dict[str, Any]:
        """Fetches the state from the external service."""
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.world_model_url}/state")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching state from world model: {e.response.text}")
            return {}
        except Exception as e:
            logger.error(f"Error connecting to world model at {self.world_model_url}: {e}")
            return {}

    async def dispatch_job(self, model_name: str, prompt: str, cpu: int = 1000, memory: int = 4096, gpu_count: int = 1, context: str = "") -> Any:
        """Dispatches a Nomad batch job via the external service."""
        url = f"{self.world_model_url}/dispatch-job"
        payload = {
            "model_name": model_name,
            "prompt": prompt,
            "cpu": cpu,
            "memory": memory,
            "gpu_count": gpu_count,
            "context": context,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error dispatching job: {e.response.text}")
                return {"error": e.response.text}
            except Exception as e:
                logger.error(f"Error connecting to world model at {self.world_model_url}: {e}")
                return {"error": str(e)}
