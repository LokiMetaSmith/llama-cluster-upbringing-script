import json
import os
import httpx
import logging
import uuid

class SwarmTool:
    """
    A tool that allows the agent to spawn multiple 'worker' agents to perform tasks in parallel.
    This enables the 'Frontier Agent' capability of scaling by spawning 10 versions of itself.
    """
    def __init__(self, nomad_url: str = "http://localhost:4646"):
        self.nomad_url = nomad_url
        self.logger = logging.getLogger(__name__)

    async def spawn_workers(self, tasks: list[dict], image: str = "pipecatapp:latest") -> str:
        """
        Spawns a worker agent for each task in the list.

        Args:
            tasks (list[dict]): A list of task definitions. Each dict must contain:
                - id (str): Unique identifier for the sub-task.
                - prompt (str): The instruction for the worker agent.
                - context (str): Relevant context or data.
            image (str): The Docker image to use for the worker (default: pipecatapp:latest).

        Returns:
            str: A summary of the dispatched jobs.
        """
        dispatched_ids = []
        errors = []

        async with httpx.AsyncClient() as client:
            for task in tasks:
                # Use UUID for collision-free IDs
                unique_suffix = str(uuid.uuid4())[:8]
                job_id = f"swarm-worker-{task.get('id', 'unknown')}-{unique_suffix}"

                # Construct a Nomad batch job payload
                # This explicitly runs the worker_agent.py script we just added.
                job_payload = {
                    "Job": {
                        "ID": job_id,
                        "Name": job_id,
                        "Type": "batch",
                        "Datacenters": ["dc1"],
                        "TaskGroups": [
                            {
                                "Name": "worker-group",
                                "Tasks": [
                                    {
                                        "Name": "worker-agent",
                                        "Driver": "docker",
                                        "Config": {
                                            "image": image,
                                            "command": "python",
                                            "args": ["/opt/pipecatapp/worker_agent.py"],
                                            "mounts": [
                                                {
                                                    "type": "bind",
                                                    "source": "/opt/pipecatapp",
                                                    "target": "/opt/pipecatapp",
                                                    "readonly": True
                                                }
                                            ]
                                        },
                                        "Env": {
                                            "WORKER_PROMPT": task.get("prompt"),
                                            "WORKER_CONTEXT": task.get("context", ""),
                                            "WORKER_TASK_ID": task.get("id"),
                                            "CONSUL_HTTP_ADDR": os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
                                        },
                                        "Resources": {
                                            "CPU": 500,
                                            "MemoryMB": 1024
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }

                try:
                    resp = await client.post(f"{self.nomad_url}/v1/job/{job_id}", json=job_payload)
                    resp.raise_for_status()
                    dispatched_ids.append(job_id)
                    self.logger.info(f"Dispatched swarm worker: {job_id}")
                except Exception as e:
                    error_msg = f"Failed to dispatch {job_id}: {str(e)}"
                    self.logger.error(error_msg)
                    errors.append(error_msg)

        result_msg = f"Successfully dispatched {len(dispatched_ids)} workers: {', '.join(dispatched_ids)}."
        if errors:
            result_msg += f" Errors: {'; '.join(errors)}"

        return result_msg
