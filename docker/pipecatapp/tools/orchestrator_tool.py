import httpx
import os

class OrchestratorTool:
    def __init__(self):
        self.world_model_url = os.getenv("WORLD_MODEL_URL", "http://localhost:8000")

    def dispatch_job(self, model_name: str, prompt: str, cpu: int = 1000, memory: int = 4096, gpu_count: int = 1):
        """Dispatches a Nomad batch job to run a model with the given prompt and resources."""
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
                    },
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return f"Error dispatching job: {e.response.text}"
