import httpx
import os
import logging
import asyncio
import concurrent.futures
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OrchestratorTool:
    def __init__(self, world_model=None):
        self.world_model = world_model
        if self.world_model is None:
            self.world_model_url = os.getenv("WORLD_MODEL_URL", f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8000")

    def dispatch_job(self, model_name: str, prompt: str, cpu: int = 1000, memory: int = 4096, gpu_count: int = 1, context: str = ""):
        """Dispatches a Nomad batch job to run a model with the given prompt, resources, and optional context."""
        if self.world_model is not None and hasattr(self.world_model, 'dispatch_job'):
            # Tools need to return a sync value. dispatch_job in world model is async.
            try:
                # Check if we are running in an event loop
                asyncio.get_running_loop()
                # Run the coroutine in another thread to avoid blocking or 'Event loop is running' errors
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self.world_model.dispatch_job(model_name, prompt, cpu, memory, gpu_count, context))
                    return future.result()
            except RuntimeError:
                # No event loop, we can use asyncio.run directly
                return asyncio.run(self.world_model.dispatch_job(model_name, prompt, cpu, memory, gpu_count, context))

        with httpx.Client() as client:
            try:
                response = client.post(
                    f"{self.world_model_url}/dispatch-job",
                    json={
                        "model_name": model_name,
                        "prompt": prompt,
                        "cpu": cpu,
                        "memory": memory,
                        "gpu_count": gpu_count,
                        "context": context,
                    },
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return f"Error dispatching job: {e.response.text}"
