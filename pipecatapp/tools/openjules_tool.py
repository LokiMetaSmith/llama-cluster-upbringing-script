import os
import logging
import ipaddress
import urllib.parse
from typing import Dict, Any, Optional
import httpx

class OpenJulesTool:
    """A tool for interacting with the OpenJules autonomous sandboxed coding agent service.

    OpenJules provides Docker-in-Docker isolated agent execution with the
    Propose-Probe-Compose adaptive harness, coordinated via Keystone Polyphony
    and reconciled via Zero Point Modulator (ZPM).
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        bearer_token: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.name = "openjules"
        self.description = (
            "Delegate autonomous coding, bug fixing, and test repair tasks to the "
            "sandboxed OpenJules agent service."
        )
        self.base_url = (
            base_url
            or os.getenv("OPENJULES_URL")
            or os.getenv("OPENJULES_API_URL")
            or "http://127.0.0.1:8000"
        ).rstrip("/")
        self.bearer_token = bearer_token or os.getenv("OPENJULES_WORKER_TOKEN")
        self.timeout = timeout

    def _validate_url(self, url: str) -> bool:
        """Validate destination URL to prevent SSRF while allowing legitimate cluster endpoints."""
        try:
            parsed = urllib.parse.urlparse(url)
            if parsed.scheme not in ("http", "https"):
                return False
            if not parsed.hostname:
                return False
            # Block obvious cloud metadata IPs
            if parsed.hostname in ("169.254.169.254", "metadata.google.internal"):
                return False
            return True
        except Exception:
            return False

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": [
                                "submit_task",
                                "capabilities",
                                "list_workers",
                                "observe_worker",
                                "drain_worker",
                                "stop_worker",
                                "health"
                            ],
                            "description": "Action to perform on OpenJules service."
                        },
                        "task": {
                            "type": "string",
                            "description": "Task description, bug report, or instruction for the coding agent."
                        },
                        "repository": {
                            "type": "string",
                            "description": "Repository identifier (e.g. 'github:owner/repo' or 'owner/repo')."
                        },
                        "deployment_id": {
                            "type": "string",
                            "description": "Deployment identifier (e.g. 'llama-cluster-zpm')."
                        },
                        "profile": {
                            "type": "string",
                            "description": "Approved runtime execution profile (e.g. 'approved-coding')."
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID for observe, drain, or stop operations."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def get_info(self) -> Dict[str, Any]:
        return self.get_schema()["function"]

    async def run(
        self,
        task: str,
        repository: Optional[str] = None,
        deployment_id: Optional[str] = None,
        profile: str = "approved-coding",
    ) -> str:
        """Convenience runner for direct task execution."""
        return await self.execute_async(
            "submit_task",
            task=task,
            repository=repository or "local/repo",
            deployment_id=deployment_id or "default",
            profile=profile,
        )

    def execute(self, action: str, **kwargs: Any) -> Any:
        """Synchronous entry point that runs the async implementation safely."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(asyncio.run, self.execute_async(action, **kwargs))
                    return future.result()
            return loop.run_until_complete(self.execute_async(action, **kwargs))
        except RuntimeError:
            return asyncio.run(self.execute_async(action, **kwargs))

    async def execute_async(self, action: str, **kwargs: Any) -> str:
        """Execute OpenJules operations asynchronously."""
        if not self._validate_url(self.base_url):
            return f"Error: Invalid or rejected base URL: {self.base_url}"

        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if action == "health":
                    url = f"{self.base_url}/health"
                    res = await client.get(url)
                    return f"Health: {res.status_code} - {res.text}"

                elif action == "capabilities":
                    deployment_id = kwargs.get("deployment_id", "default")
                    repository = kwargs.get("repository", "default")
                    profile = kwargs.get("profile", "approved-coding")
                    url = (
                        f"{self.base_url}/api/workers/capabilities"
                        f"?deployment_id={urllib.parse.quote(deployment_id)}"
                        f"&repository={urllib.parse.quote(repository)}"
                        f"&profile={urllib.parse.quote(profile)}"
                    )
                    res = await client.get(url, headers=headers)
                    return res.text

                elif action == "submit_task":
                    task = kwargs.get("task")
                    if not task:
                        return "Error: 'task' parameter is required for submit_task."
                    repository = kwargs.get("repository", "default")
                    deployment_id = kwargs.get("deployment_id", "default")
                    profile = kwargs.get("profile", "approved-coding")

                    # Primary path: OpenJules worker ensure or webhook task
                    payload = {
                        "schema_version": 1,
                        "task": task,
                        "deployment_id": deployment_id,
                        "repository": repository,
                        "profile": profile,
                    }
                    url = f"{self.base_url}/api/workers/ensure"
                    res = await client.post(url, headers=headers, json=payload)
                    if res.status_code in (200, 201, 202):
                        return f"OpenJules task successfully submitted: {res.text}"
                    # Fallback to general task endpoint if ensure is not ready
                    fallback_url = f"{self.base_url}/api/task"
                    fallback_res = await client.post(fallback_url, headers=headers, json=payload)
                    return f"OpenJules task response: {fallback_res.status_code} - {fallback_res.text}"

                elif action == "list_workers":
                    deployment_id = kwargs.get("deployment_id", "default")
                    repository = kwargs.get("repository", "default")
                    url = (
                        f"{self.base_url}/api/workers"
                        f"?deployment_id={urllib.parse.quote(deployment_id)}"
                        f"&repository={urllib.parse.quote(repository)}"
                    )
                    res = await client.get(url, headers=headers)
                    return res.text

                elif action == "observe_worker":
                    worker_id = kwargs.get("worker_id")
                    if not worker_id:
                        return "Error: 'worker_id' parameter is required for observe_worker."
                    deployment_id = kwargs.get("deployment_id", "default")
                    repository = kwargs.get("repository", "default")
                    url = (
                        f"{self.base_url}/api/workers/{urllib.parse.quote(worker_id)}"
                        f"?deployment_id={urllib.parse.quote(deployment_id)}"
                        f"&repository={urllib.parse.quote(repository)}"
                    )
                    res = await client.get(url, headers=headers)
                    return res.text

                elif action == "drain_worker":
                    worker_id = kwargs.get("worker_id")
                    if not worker_id:
                        return "Error: 'worker_id' parameter is required for drain_worker."
                    url = f"{self.base_url}/api/workers/{urllib.parse.quote(worker_id)}/drain"
                    res = await client.post(url, headers=headers, json=kwargs)
                    return f"Drain worker {worker_id}: {res.status_code} - {res.text}"

                elif action == "stop_worker":
                    worker_id = kwargs.get("worker_id")
                    if not worker_id:
                        return "Error: 'worker_id' parameter is required for stop_worker."
                    url = f"{self.base_url}/api/workers/{urllib.parse.quote(worker_id)}/stop"
                    res = await client.post(url, headers=headers, json=kwargs)
                    return f"Stop worker {worker_id}: {res.status_code} - {res.text}"

                else:
                    return f"Error: Unknown action '{action}'"

        except httpx.HTTPError as e:
            logging.error(f"HTTP error communicating with OpenJules: {e}")
            return f"HTTP error communicating with OpenJules: {str(e)}"
        except Exception as e:
            logging.error(f"Error executing OpenJules action: {e}")
            return f"Error executing OpenJules action: {str(e)}"
