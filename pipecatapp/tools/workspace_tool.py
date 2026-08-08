# ruff: noqa: BLE001, S110, ASYNC230
# ruff: noqa: BLE001, S110, ASYNC230
# ruff: noqa: BLE001, S110, ASYNC230
import asyncio
import base64
import logging
import os
import tempfile
import time
import uuid

import aiofiles
import aiohttp

import docker

# Import LiminalMesh
# Assuming PYTHONPATH is configured correctly by the runner
try:
    from liminal_bridge.mesh import LiminalMesh
except ImportError:
    logging.getLogger(__name__).warning("Could not import LiminalMesh. WorkspaceTool will fall back to local mock storage.")
    LiminalMesh = None

class WorkspaceTool:
    """
    A tool to manage a durable workspace that agents can use to share state
    and files across multiple execution steps, using LiminalMesh as the CRDT backend.
    """
    def __init__(self):
        self.name = "workspace"
        self.description = (
            "An advanced escalation path tool that provides a durable shared filesystem (Workspace) "
            "and execution environment across multiple agent steps. Use this to maintain state, "
            "write files, and execute code against those files using Docker, Nomad, or Bare Metal backends."
        )
        # In-memory mapping of workspace_id -> local temporary directory path
        self.active_workspaces: dict[str, str] = {}

        # LiminalMesh instance (we instantiate it if available)
        # Note: In a real cluster environment, secrets and db paths would be injected.
        self.mesh = None
        if LiminalMesh is not None:
            # We initialize a mesh instance for this node's workspace operations.
            # Using in-memory DB for tool instance if not specified,
            # though it should ideally connect to the node's shared mesh.
            db_path = os.environ.get("LIMINAL_DB_PATH", "workspace_liminal.db")
            secret = os.environ.get("SWARM_KEY", "default-workspace-secret")
            identity = os.environ.get("IDENTITY_PATH", "workspace_identity.pem")
            try:
                self.mesh = LiminalMesh(secret_key=secret, db_path=db_path, identity_path=identity)
            except Exception as e:
                logging.getLogger(__name__).info(f"Failed to initialize LiminalMesh for WorkspaceTool: {e}")
                self.mesh = None

        # Initialize Docker client
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            logging.getLogger(__name__).warning(f"Failed to initialize Docker client in WorkspaceTool: {e}")
            self.docker_client = None

        self.nomad_url = os.environ.get("NOMAD_ADDR", f"http://{os.environ.get('CLUSTER_IP', '127.0.0.1')}:4646")
        self.nomad_token = os.environ.get("NOMAD_TOKEN")
        self.nomad_headers = {"X-Nomad-Token": self.nomad_token} if self.nomad_token else {}
        self._aiohttp_session = None

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
                            "description": "The action to perform: init_workspace, list_files, fetch_file, save_file, acquire_lock, release_lock, execute_code."
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    async def execute(self, action: str, **kwargs) -> str:
        actual_kwargs = kwargs.get("kwargs", kwargs)

        if action == "init_workspace":
            return await self.init_workspace(**actual_kwargs)
        elif action == "list_files":
            return await self.list_files(**actual_kwargs)
        elif action == "fetch_file":
            return await self.fetch_file(**actual_kwargs)
        elif action == "save_file":
            return await self.save_file(**actual_kwargs)
        elif action == "acquire_lock":
            return await self.acquire_lock(**actual_kwargs)
        elif action == "release_lock":
            return await self.release_lock(**actual_kwargs)
        elif action == "execute_code":
            return await self.execute_code(**actual_kwargs)
        else:
            return f"Error: Unknown action '{action}'."

    async def init_workspace(self, workspace_id: str) -> str:
        """Initializes the local workspace directory and pulls latest state from LiminalMesh."""
        if workspace_id not in self.active_workspaces:
            temp_dir = tempfile.mkdtemp(prefix=f"workspace_{workspace_id}_")
            self.active_workspaces[workspace_id] = temp_dir

        local_dir = self.active_workspaces[workspace_id]

        # Pull files from LiminalMesh CRDTs
        if self.mesh:
            all_kv = self.mesh.get_all_kv()
            prefix = f"workspace:{workspace_id}:file:"

            for key, crdt_obj in all_kv.items():
                if key.startswith(prefix):
                    rel_path = key[len(prefix):]
                    file_content = crdt_obj.value()

                    full_path = os.path.join(local_dir, rel_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)

                    try:
                        # Attempt to decode base64 if it's binary data
                        try:
                            decoded = base64.b64decode(file_content).decode('utf-8')
                            async with aiofiles.open(full_path, "w") as f:
                                await f.write(decoded)
                        except UnicodeDecodeError:
                            # It's actual binary data
                            async with aiofiles.open(full_path, "wb") as f:
                                await f.write(base64.b64decode(file_content))
                        except Exception:
                            # Fallback if it wasn't even base64 (legacy data)
                            async with aiofiles.open(full_path, "w") as f:
                                await f.write(str(file_content))
                    except Exception as e:
                        logging.getLogger(__name__).info(f"Error writing pulled file {rel_path}: {e}")

        return f"Workspace '{workspace_id}' initialized at local directory."

    async def list_files(self, workspace_id: str) -> str:
        """Lists all files in the materialized local workspace directory."""
        if workspace_id not in self.active_workspaces:
            return f"Error: Workspace '{workspace_id}' is not initialized. Run init_workspace first."

        local_dir = self.active_workspaces[workspace_id]
        file_list = []
        for root, _, files in os.walk(local_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, local_dir)
                file_list.append(rel_path)

        if not file_list:
            return "Workspace is empty."

        return "\n".join(file_list)

    async def fetch_file(self, workspace_id: str, filepath: str) -> str:
        """Reads a file from the materialized local workspace."""
        if workspace_id not in self.active_workspaces:
            return f"Error: Workspace '{workspace_id}' is not initialized. Run init_workspace first."

        local_dir = self.active_workspaces[workspace_id]
        full_path = os.path.join(local_dir, filepath)

        # Security check to prevent path traversal
        if os.path.commonpath([os.path.abspath(local_dir), os.path.abspath(full_path)]) != os.path.abspath(local_dir):
            return "Error: Access denied. Path traversal detected."

        if not os.path.exists(full_path):
            return f"Error: File '{filepath}' does not exist in workspace '{workspace_id}'."

        try:
            async with aiofiles.open(full_path, "r") as f:
                return await f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    async def save_file(self, workspace_id: str, filepath: str, content: str) -> str:
        """Saves a file locally AND pushes it to LiminalMesh CRDT."""
        if workspace_id not in self.active_workspaces:
            return f"Error: Workspace '{workspace_id}' is not initialized. Run init_workspace first."

        local_dir = self.active_workspaces[workspace_id]
        full_path = os.path.join(local_dir, filepath)

        if os.path.commonpath([os.path.abspath(local_dir), os.path.abspath(full_path)]) != os.path.abspath(local_dir):
            return "Error: Access denied. Path traversal detected."

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            async with aiofiles.open(full_path, "w") as f:
                await f.write(content)
        except Exception as e:
            return f"Error writing file locally: {e}"

        # Push to LiminalMesh
        if self.mesh:
            try:
                crdt_key = f"workspace:{workspace_id}:file:{filepath}"
                encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                await self.mesh.update_kv(crdt_key, encoded_content, urgency="high")
            except Exception as e:
                logging.getLogger(__name__).info(f"Error syncing file {filepath} to LiminalMesh: {e}")
                return f"File saved locally, but failed to sync to mesh: {e}"

        return f"Successfully saved file '{filepath}' to workspace '{workspace_id}'."

    async def acquire_lock(self, workspace_id: str, filepath: str) -> str:
        """Acquires a granular lock on a file using LiminalMesh."""
        if not self.mesh:
            return "LiminalMesh not available for locking."

        lock_key = f"workspace:{workspace_id}:lock:{filepath}"
        try:
            # Check if locked
            existing_lock = self.mesh.get_kv(lock_key)
            if existing_lock and existing_lock.value() == "locked":
                return f"Error: File '{filepath}' is already locked by another agent."

            await self.mesh.update_kv(lock_key, "locked", urgency="high")
            return f"Lock acquired for '{filepath}'."
        except Exception as e:
            return f"Error acquiring lock: {e}"

    async def release_lock(self, workspace_id: str, filepath: str) -> str:
        """Releases a granular lock on a file using LiminalMesh."""
        if not self.mesh:
            return "LiminalMesh not available for locking."

        lock_key = f"workspace:{workspace_id}:lock:{filepath}"
        try:
            await self.mesh.update_kv(lock_key, "unlocked", urgency="high")
            return f"Lock released for '{filepath}'."
        except Exception as e:
            return f"Error releasing lock: {e}"

    def _get_session(self) -> aiohttp.ClientSession:
        if not self._aiohttp_session:
            self._aiohttp_session = aiohttp.ClientSession()
        return self._aiohttp_session

    async def execute_code(self, workspace_id: str, backend: str, code: str, language: str = "python", timeout: int = 60) -> str:
        """Executes code against the materialized workspace directory using the specified backend."""
        if workspace_id not in self.active_workspaces:
            return f"Error: Workspace '{workspace_id}' is not initialized. Run init_workspace first."

        local_dir = self.active_workspaces[workspace_id]

        # Write the execution script to the workspace
        script_name = f"exec_{uuid.uuid4().hex[:8]}.py" if language == "python" else f"exec_{uuid.uuid4().hex[:8]}.sh"
        script_path = os.path.join(local_dir, script_name)

        async with aiofiles.open(script_path, "w") as f:
            await f.write(code)

        try:
            if backend == "bare_metal":
                output = await self._execute_bare_metal(local_dir, script_name, language, timeout)
            elif backend == "docker":
                output = await self._execute_docker(local_dir, script_name, language, timeout)
            elif backend == "nomad":
                output = await self._execute_nomad(workspace_id, local_dir, script_name, language, timeout)
            else:
                return f"Error: Unknown backend '{backend}'. Supported: bare_metal, docker, nomad."

            # Sync back changes to LiminalMesh
            # Note: For Nomad, if it executed remotely without LiminalMesh inside the job,
            # the local directory won't have the changes made by the remote job.
            # In a production environment with unified_fs, the local_dir would be on the shared mount.
            if self.mesh:
                for root, _, files in os.walk(local_dir):
                    for file in files:
                        if file == script_name:
                            continue # Skip the execution script itself

                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, local_dir)

                        try:
                            with open(full_path, "rb") as f:
                                file_content = f.read()

                            encoded_content = base64.b64encode(file_content).decode('utf-8')
                            crdt_key = f"workspace:{workspace_id}:file:{rel_path}"

                            existing = self.mesh.get_kv(crdt_key)
                            if not existing or existing.value() != encoded_content:
                                await self.mesh.update_kv(crdt_key, encoded_content, urgency="high")
                        except Exception as e:
                            logging.getLogger(__name__).info(f"Failed to sync modified file {rel_path} after execution: {e}")

            return output
        finally:
            # Clean up the execution script
            if os.path.exists(script_path):
                os.remove(script_path)

    async def _execute_bare_metal(self, cwd: str, script_name: str, language: str, timeout: int) -> str:
        """Executes code directly on the host machine using subprocess, with strict constraints."""
        cmd = ["python3", script_name] if language == "python" else ["sh", script_name]

        try:
            # Create a process group so we can reliably kill children
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=(os.name == 'posix')
            )

            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                output = stdout.decode()
                if stderr:
                    output += f"\n---STDERR---\n{stderr.decode()}"

                return output if output else "Execution completed with no output."

            except asyncio.TimeoutError:
                # Terminate the process group
                if os.name == 'posix':
                    import signal
                    try:
                        pgid = os.getpgid(process.pid)
                        os.killpg(pgid, signal.SIGTERM)
                        await asyncio.sleep(1) # Give it a moment to gracefully exit
                        try:
                            os.killpg(pgid, 0) # Check if still alive
                            os.killpg(pgid, signal.SIGKILL) # Force kill
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:
                    process.terminate()

                try:
                    await asyncio.wait_for(process.communicate(), timeout=5.0)
                except Exception:
                    pass
                return f"Error: Execution timed out after {timeout} seconds."

        except Exception as e:
            return f"Bare metal execution error: {e}"

    async def _execute_docker(self, cwd: str, script_name: str, language: str, timeout: int) -> str:
        """Executes code in a local Docker container mounting the workspace."""
        if not self.docker_client:
            return "Error: Docker client not available."

        image = "python:3.9-slim" if language == "python" else "alpine:latest"
        cmd = f"python3 /workspace/{script_name}" if language == "python" else f"sh /workspace/{script_name}"

        container = None
        try:
            # Make sure we use absolute path for mounting
            abs_cwd = os.path.abspath(cwd)

            container = self.docker_client.containers.run(
                image,
                command=cmd,
                volumes={abs_cwd: {'bind': '/workspace', 'mode': 'rw'}},
                working_dir="/workspace",
                detach=True,
                mem_limit="256m",
                cpu_quota=50000,
                pids_limit=50,
                network_mode="none"
            )

            start_time = time.time()
            while time.time() - start_time < timeout:
                container.reload()
                if container.status != 'running':
                    break
                await asyncio.sleep(0.5)

            if container.status == 'running':
                container.kill()
                return f"Error: Docker execution timed out after {timeout} seconds."

            return container.logs().decode('utf-8')

        except Exception as e:
            return f"Docker execution error: {e}"
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:
                    pass

    async def _execute_nomad(self, workspace_id: str, cwd: str, script_name: str, language: str, timeout: int) -> str:
        """
        Executes code by dispatching a Nomad job.
        For true distributed durability, we'd mount the shared IPFS or sync via LiminalMesh directly in the job.
        For simplicity here, we inject the script and fetch results similar to CodeRunnerTool.
        """
        job_id = f"ws-exec-{workspace_id}-{uuid.uuid4().hex[:8]}"

        # Read the script code
        async with aiofiles.open(os.path.join(cwd, script_name), "r") as f:
            code = await f.read()

        code_b64 = base64.b64encode(code.encode('utf-8')).decode('utf-8')

        image = "python:3.9-slim" if language == "python" else "alpine:latest"
        exec_cmd = "python3 /local/script.py" if language == "python" else "sh /local/script.py"
        prep_cmd = "python3 -c 'import base64; open(\"/local/script.py\", \"wb\").write(base64.b64decode(open(\"/local/script.b64\", \"rb\").read()))'"

        full_cmd = f"{prep_cmd} && {exec_cmd}"

        job_payload = {
            "Job": {
                "ID": job_id,
                "Name": job_id,
                "Type": "batch",
                "Datacenters": ["dc1"],
                "TaskGroups": [
                    {
                        "Name": "workspace-exec",
                        "Count": 1,
                        "RestartPolicy": {"Attempts": 0, "Mode": "fail"},
                        "Tasks": [
                            {
                                "Name": "execution",
                                "Driver": "docker",
                                "Config": {
                                    "image": image,
                                    "command": "/bin/sh",
                                    "args": ["-c", full_cmd],
                                    "network_mode": "none"
                                },
                                "Resources": {"CPU": 100, "MemoryMB": 256},
                                "Templates": [
                                    {
                                        "EmbeddedTmpl": code_b64,
                                        "DestPath": "local/script.b64",
                                        "ChangeMode": "noop"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }

        session = self._get_session()
        try:
            async with session.post(f"{self.nomad_url}/v1/jobs", json=job_payload, headers=self.nomad_headers, timeout=10) as reg_resp:
                if reg_resp.status != 200:
                    return f"Error registering Nomad job: {await reg_resp.text()}"

            alloc_id = None
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    async with session.get(f"{self.nomad_url}/v1/job/{job_id}/allocations", headers=self.nomad_headers, timeout=10) as allocs_resp:
                        allocs = await allocs_resp.json()
                        if allocs:
                            allocs.sort(key=lambda x: x.get('CreateTime', 0), reverse=True)
                            latest = allocs[0]
                            alloc_id = latest['ID']
                            if latest.get('ClientStatus') in ['complete', 'failed']:
                                break
                except Exception:
                    pass
                await asyncio.sleep(1)

            if not alloc_id:
                return "Error: Nomad job timed out waiting for allocation."

            # Fetch logs
            try:
                async with session.get(f"{self.nomad_url}/v1/allocation/{alloc_id}", headers=self.nomad_headers, timeout=10) as alloc_detail_resp:
                    alloc_detail = await alloc_detail_resp.json()
                node_id = alloc_detail.get("NodeID")
                async with session.get(f"{self.nomad_url}/v1/node/{node_id}", headers=self.nomad_headers, timeout=10) as node_detail_resp:
                    node_detail = await node_detail_resp.json()
                node_addr = node_detail.get("HTTPAddr")

                logs = ""
                for log_type in ["stdout", "stderr"]:
                    try:
                        log_url = f"http://{node_addr}/v1/client/fs/logs/{alloc_id}?task=execution&type={log_type}&plain=true"
                        async with session.get(log_url, headers=self.nomad_headers, timeout=10) as log_resp:
                            if log_resp.status == 200:
                                content = await log_resp.text()
                                if content:
                                    logs += f"---{log_type.upper()}---\n{content}\n"
                    except Exception:
                        pass
                return logs.strip() if logs.strip() else "Execution completed with no output."
            except Exception as e:
                return f"Error retrieving logs for job {job_id}: {e}"
        except Exception as e:
            return f"Nomad execution error: {e}"
        finally:
            try:
                async with session.delete(f"{self.nomad_url}/v1/job/{job_id}?purge=true", headers=self.nomad_headers, timeout=10) as _:
                    pass
            except Exception:
                pass
