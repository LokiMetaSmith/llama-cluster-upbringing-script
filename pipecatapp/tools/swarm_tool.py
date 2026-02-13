import json
import os
import httpx
import logging
import uuid
import asyncio
import time

class SwarmTool:
    """
    A tool that allows the agent to spawn multiple 'worker' agents to perform tasks in parallel.
    This enables the 'Frontier Agent' capability of scaling by spawning 10 versions of itself.
    """
    def __init__(self, nomad_url: str = "http://localhost:4646", memory_client=None):
        self.nomad_url = nomad_url
        self.memory_client = memory_client
        self.logger = logging.getLogger(__name__)

    async def spawn_workers(self, tasks: list[dict], image: str = "pipecatapp:latest", agent_type: str = "worker") -> str:
        """
        Spawns a worker agent for each task in the list.

        Args:
            tasks (list[dict]): A list of task definitions. Each dict must contain:
                - id (str): Unique identifier for the sub-task.
                - prompt (str): The instruction for the worker agent.
                - context (str): Relevant context or data.
            image (str): The Docker image to use for the worker (default: pipecatapp:latest).
            agent_type (str): The type of agent to spawn. Options: 'worker' (simple), 'technician' (advanced).

        Returns:
            str: A JSON string summary of the dispatched jobs, including a list of 'task_ids'.
        """
        dispatched_ids = []
        task_ids = []
        errors = []
        
        # Determine script based on agent_type
        script_path = "/opt/pipecatapp/worker_agent.py"
        if agent_type == "technician":
            script_path = "/opt/pipecatapp/technician_agent.py"

        async with httpx.AsyncClient() as client:
            for task in tasks:
                t_id = task.get('id', 'unknown')
                task_ids.append(t_id)

                # Use UUID for collision-free IDs
                unique_suffix = str(uuid.uuid4())[:8]
                job_id = f"swarm-{agent_type}-{t_id}-{unique_suffix}"

                # Construct a Nomad batch job payload
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
                                            "args": [script_path],
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
                                            "WORKER_TASK_ID": t_id,
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

        result = {
            "job_ids": dispatched_ids,
            "task_ids": task_ids,
            "message": f"Successfully dispatched {len(dispatched_ids)} workers.",
            "errors": errors
        }

        return json.dumps(result)

    async def wait_for_results(self, task_ids: list[str], timeout: int = 600, poll_interval: int = 5) -> str:
        """
        Waits for the specified tasks to complete and returns their results.

        Args:
            task_ids (list[str]): List of task IDs to wait for.
            timeout (int): Max wait time in seconds (default: 600).
            poll_interval (int): Seconds to wait between polls (default: 5).

        Returns:
            str: JSON string containing a dictionary of task_id -> result content.
        """
        if not self.memory_client:
            return json.dumps({"error": "Memory client not initialized in SwarmTool. Cannot wait for results."})

        results = {}
        start_time = time.time()

        self.logger.info(f"Waiting for results from tasks: {task_ids}")

        while len(results) < len(task_ids):
            if time.time() - start_time > timeout:
                remaining = list(set(task_ids) - set(results.keys()))
                self.logger.warning(f"Timeout waiting for tasks: {remaining}")
                break

            try:
                # Poll memory for results
                events = await self.memory_client.get_events(limit=100)

                for event in events:
                    kind = event.get("kind")
                    meta = event.get("meta", {})
                    t_id = meta.get("task_id")

                    if kind == "worker_result" and t_id in task_ids:
                        if t_id not in results:
                            results[t_id] = event.get("content")
                            self.logger.info(f"Received result for task {t_id}")

            except Exception as e:
                self.logger.error(f"Error polling memory: {e}")
                await asyncio.sleep(poll_interval)

            if len(results) == len(task_ids):
                break

            await asyncio.sleep(poll_interval)

        return json.dumps({
            "status": "complete" if len(results) == len(task_ids) else "partial",
            "results": results,
            "missing": list(set(task_ids) - set(results.keys()))
        })

    async def kill_worker(self, job_id: str) -> str:
        """Kills a specific worker job."""
        async with httpx.AsyncClient() as client:
            try:
                # Use query param purge=true to clean up immediately
                resp = await client.delete(f"{self.nomad_url}/v1/job/{job_id}?purge=true")
                resp.raise_for_status()
                return f"Successfully killed worker: {job_id}"
            except Exception as e:
                return f"Failed to kill worker {job_id}: {str(e)}"
