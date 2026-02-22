import json
import os
import time
import uuid
import logging
import asyncio
import shutil
import tempfile
import subprocess
import shlex
import httpx
from typing import List, Dict, Any, Optional
from tools.swarm_tool import SwarmTool

class ExperimentTool:
    """
    A tool that orchestrates A/B testing or parallel experiments for code generation.
    It spawns multiple Worker Agents, collects their solutions, runs them in a sandbox
    against a verification command, and reports the best result.
    """
    def __init__(self, event_bus_url: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        # Try to find Event Bus URL from env if not provided
        if not event_bus_url:
            host = os.getenv("EVENT_BUS_HOST", "localhost")
            port = os.getenv("EVENT_BUS_PORT", "8000")
            # In some setups, service name might be needed, but we default to direct address
            self.event_bus_url = f"http://{host}:{port}"
        else:
            self.event_bus_url = event_bus_url

        self.swarm_tool = SwarmTool()

    async def run(self, task_description: str, test_command: str, variants: List[str] = [], num_workers: int = 5, timeout_seconds: int = 300) -> str:
        """
        Runs the experiment.

        Args:
            task_description (str): The main task instruction.
            test_command (str): Shell command to verify the solution (e.g., 'pytest tests/test_app.py').
            variants (List[str]): Optional list of specific prompts/strategies to try. If provided, num_workers is ignored (one per variant).
            num_workers (int): Number of parallel workers if variants are not provided.
            timeout_seconds (int): Max time to wait for results.

        Returns:
            str: JSON summary of the experiment results.
        """
        experiment_id = str(uuid.uuid4())[:8]
        self.logger.info(f"Starting Experiment {experiment_id}")

        # 1. Prepare Tasks
        tasks = []
        if variants:
            for i, variant in enumerate(variants):
                tasks.append({
                    "id": f"{experiment_id}-v{i}",
                    "prompt": f"{task_description}\n\nStrategy: {variant}",
                    "context": "Experiment Mode"
                })
        else:
            for i in range(num_workers):
                tasks.append({
                    "id": f"{experiment_id}-w{i}",
                    "prompt": task_description,
                    "context": f"Experiment Worker {i}"
                })

        # 2. Spawn Workers
        swarm_resp = await self.swarm_tool.spawn_workers(tasks)
        try:
            swarm_data = json.loads(swarm_resp)
            job_ids = swarm_data.get("job_ids", [])
        except:
            return f"Error spawning workers: {swarm_resp}"

        if not job_ids:
            return "Failed to spawn any workers."

        self.logger.info(f"Waiting for results from {len(job_ids)} workers...")

        # 3. Collect Results (Polling)
        results = {}
        start_time = time.time()

        while len(results) < len(job_ids) and (time.time() - start_time) < timeout_seconds:
            # Poll the Event Bus for results
            # We look for 'worker_result' events where meta.task_id is in our list
            try:
                # Assuming /events returns recent events.
                # Ideally we filter by task_id but the simple API might just return list.
                # We'll fetch tasks specific endpoint if available, or just all recent events.
                # The memory said: GET /tasks/{task_id} exists.

                for task in tasks:
                    t_id = task["id"]
                    if t_id in results:
                        continue

                    async with httpx.AsyncClient() as client:
                        try:
                            resp = await client.get(f"{self.event_bus_url}/tasks/{t_id}")
                            if resp.status_code == 200:
                                events = resp.json()
                                # Look for worker_result
                                for evt in events:
                                    if evt.get("kind") == "worker_result":
                                        results[t_id] = evt
                                        break
                        except Exception as e:
                            self.logger.warning(f"Error polling task {t_id}: {e}")

            except Exception as e:
                self.logger.error(f"Polling loop error: {e}")

            if len(results) < len(job_ids):
                await asyncio.sleep(5)

        # 4. Evaluate Results
        eval_report = []
        best_candidate = None

        # Optimization: Create a source snapshot once to avoid repeatedly copying thousands of files.
        # This significantly reduces syscall overhead as per https://modulovalue.com/blog/syscall-overhead-tar-gz-io-performance/
        snapshot_path = self._create_snapshot("/opt/pipecatapp")

        try:
            for t_id, evt in results.items():
                content = evt.get("content", "")

                # Extract artifact from content
                # Content might be "Tool submit_solution output: {...}" or just the JSON if the worker returned it directly.
                # We need to parse it.
                artifact = self._extract_artifact(content)

                if not artifact:
                    eval_report.append({
                        "task_id": t_id,
                        "status": "malformed_output",
                        "details": "Could not find valid solution artifact."
                    })
                    continue

                # Run Sandbox Eval
                score_data = self._run_sandbox_eval(artifact, test_command, snapshot_path)

                result_entry = {
                    "task_id": t_id,
                    "status": "evaluated",
                    "passed": score_data["passed"],
                    "output": score_data["output"],
                    "artifact": artifact
                }
                eval_report.append(result_entry)

                if score_data["passed"]:
                    # Simple logic: First passing result is best (or could look for fastest/cleanest)
                    if not best_candidate:
                        best_candidate = result_entry
        finally:
            if snapshot_path and os.path.exists(snapshot_path):
                os.remove(snapshot_path)

        # 5. Cleanup Workers (Optional, Swarm might auto-cleanup or we leave them for debug)
        # for jid in job_ids:
        #    await self.swarm_tool.kill_worker(jid)

        summary = {
            "experiment_id": experiment_id,
            "total_workers": len(job_ids),
            "completed": len(results),
            "winner": best_candidate,
            "details": eval_report
        }

        return json.dumps(summary, indent=2)

    def _validate_path(self, root_dir: str, filepath: str) -> str:
        """Ensures the filepath is within the root directory."""
        root_dir = os.path.abspath(root_dir)

        # Handle absolute paths by stripping leading slash
        # This treats /etc/passwd as relative to root_dir
        if os.path.isabs(filepath):
            filepath = filepath.lstrip(os.sep)

        full_path = os.path.join(root_dir, filepath)
        full_path = os.path.abspath(full_path)

        try:
            common = os.path.commonpath([root_dir, full_path])
        except ValueError:
            common = ""

        if common != root_dir:
            raise ValueError(f"Access denied: {filepath} is outside the sandbox.")

        return full_path

    def _create_snapshot(self, src_dir: str) -> Optional[str]:
        """Creates a tar snapshot of the source directory to speed up sandbox creation."""
        if not os.path.exists(src_dir):
            return None

        try:
            fd, archive_path = tempfile.mkstemp(suffix=".tar")
            os.close(fd)

            # Create tarball using system tar for speed and efficient syscall usage
            # Exclude .git, __pycache__, node_modules, *.pyc
            cmd = [
                "tar",
                "-cf", archive_path,
                "-C", src_dir,
                "--exclude", ".git",
                "--exclude", "__pycache__",
                "--exclude", "node_modules",
                "--exclude", "*.pyc",
                "."
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return archive_path
        except Exception as e:
            self.logger.error(f"Failed to create snapshot: {e}")
            if 'archive_path' in locals() and os.path.exists(archive_path):
                os.remove(archive_path)
            return None

    def _extract_artifact(self, content: str) -> Optional[Dict]:
        """Parses the content to find the JSON artifact."""
        try:
            # Check if content is already the tool output string
            if "Tool submit_solution output:" in content:
                json_part = content.split("Tool submit_solution output:", 1)[1].strip()
                return json.loads(json_part)

            # Or scan for JSON structure directly
            if '"type": "solution_artifact"' in content:
                # Find start/end braces
                start = content.find('{')
                end = content.rfind('}') + 1
                return json.loads(content[start:end])

        except Exception as e:
            self.logger.warning(f"Failed to parse artifact: {e}")
        return None

    def _run_sandbox_eval(self, artifact: Dict, test_command: str, snapshot_path: Optional[str] = None) -> Dict:
        """Runs the artifact in a temp sandbox against the test command."""

        # Create temp dir
        temp_dir = tempfile.mkdtemp(prefix="pipecat_exp_")

        try:
            # Populate Sandbox
            if snapshot_path and os.path.exists(snapshot_path):
                 # Fast path: Extract tarball
                 # This avoids thousands of open/read/write/close syscalls
                 cmd = ["tar", "-xf", snapshot_path, "-C", temp_dir]
                 subprocess.run(cmd, check=True, capture_output=True)
            else:
                 # Fallback: Copy Codebase (Assume /opt/pipecatapp is source)
                 src_dir = "/opt/pipecatapp"
                 if not os.path.exists(src_dir):
                     return {"passed": False, "output": "Source directory /opt/pipecatapp not found"}

                 # Copy relevant files
                 # We use ignore_patterns to skip .git, __pycache__
                 shutil.copytree(src_dir, temp_dir, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns('.git', '__pycache__', 'node_modules', '*.pyc'))

            # Apply Artifact
            file_path = artifact.get("file_path", "solution.py")
            try:
                full_path = self._validate_path(temp_dir, file_path)
            except ValueError as e:
                return {"passed": False, "output": f"Security Error: {e}"}

            # Ensure directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            content = artifact.get("content", "")
            # Security Fix: Sentinel - Prevent DoS via large file
            if len(content) > 1024 * 1024:  # 1MB limit
                return {"passed": False, "output": "Security Error: Artifact too large (>1MB)."}

            with open(full_path, 'w') as f:
                f.write(content)

            # Run Command
            # we need to set PYTHONPATH if running python tests
            env = os.environ.copy()
            env["PYTHONPATH"] = temp_dir

            # Security Fix: Sentinel - Use shell=False and split args to prevent command injection
            cmd_args = shlex.split(test_command)

            result = subprocess.run(
                cmd_args,
                cwd=temp_dir,
                shell=False,
                capture_output=True,
                text=True,
                timeout=60,
                env=env
            )

            passed = (result.returncode == 0)
            return {
                "passed": passed,
                "output": result.stdout + "\n" + result.stderr
            }

        except Exception as e:
            return {"passed": False, "output": f"Sandbox error: {str(e)}"}
        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
