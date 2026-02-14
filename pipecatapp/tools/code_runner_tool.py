import abc
import docker
import logging
import os
import tempfile
import time
import uuid
import requests
import base64
from llm_sandbox import SandboxSession
from typing import List, Optional
from .dependency_scanner_tool import DependencyScannerTool

class SandboxExecutor(abc.ABC):
    """Abstract base class for sandbox execution strategies."""

    @abc.abstractmethod
    def execute(self, code: str, language: str = "python", libraries: Optional[List[str]] = None) -> str:
        pass

class DockerSandboxExecutor(SandboxExecutor):
    """Executes code using local Docker containers (via docker-py or llm-sandbox)."""

    def __init__(self):
        self.image = "python:3.9-slim"
        self.scanner = DependencyScannerTool()
        try:
            self.client = docker.from_env()
        except Exception as e:
            logging.warning(f"Failed to initialize Docker client for CodeRunnerTool: {e}")
            self.client = None

    def execute(self, code: str, language: str = "python", libraries: Optional[List[str]] = None) -> str:
        """Executes code using llm-sandbox for robust multi-language support."""
        if libraries is None:
            libraries = []

        # Dependency Intelligence Check
        if language == "python" and libraries:
            for lib in libraries:
                if '==' in lib:
                    name, version = lib.split('==', 1)
                else:
                    name, version = lib, None

                scan_result = self.scanner.scan_package(name, version)
                if "UNSAFE" in scan_result:
                    return f"Operation blocked by security policy. Vulnerability detected in dependency '{lib}':\n{scan_result}"

        try:
            with SandboxSession(lang=language) as session:
                result = session.run(code, libraries=libraries)
                if result.exit_code == 0:
                    output = result.stdout
                else:
                    output = f"Exit Code: {result.exit_code}\n---STDERR---\n{result.stderr}\n---STDOUT---\n{result.stdout}"

                if result.plots:
                    output += "\n\nGenerated plots are available."

                return output
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def execute_simple_python(self, code: str) -> str:
        """Runs simple Python code using raw docker-py for speed/legacy support."""
        if not self.client:
            return "Error: Docker execution is not available (Docker client failed to initialize)."

        try:
            # Use TemporaryDirectory for better isolation than mounting /tmp
            with tempfile.TemporaryDirectory() as temp_dir:
                script_name = "script.py"
                host_script_path = os.path.join(temp_dir, script_name)

                with open(host_script_path, "w") as f:
                    f.write(code)

                # Mount the temp dir to /code
                volumes = {temp_dir: {'bind': '/code', 'mode': 'ro'}}

                container = self.client.containers.run(
                    self.image,
                    command=["python", f"/code/{script_name}"],
                    volumes=volumes,
                    working_dir="/code",
                    network_mode="none",  # Security: No internet access
                    mem_limit="128m",     # Security: Limit memory
                    cpu_period=100000,
                    cpu_quota=50000,      # Security: Limit CPU (50%)
                    pids_limit=20,        # Security: Limit processes
                    remove=True,
                    stderr=True,
                    stdout=True
                )

                output = container.decode('utf-8')
                return output

        except docker.errors.ImageNotFound:
            return f"Error: The Docker image '{self.image}' was not found. Please pull it first."
        except Exception as e:
            return f"An error occurred: {e}"

class NomadSandboxExecutor(SandboxExecutor):
    """Executes code by dispatching ephemeral Nomad batch jobs."""

    def __init__(self):
        self.nomad_url = os.environ.get("NOMAD_ADDR", "http://localhost:4646")
        self.token = os.environ.get("NOMAD_TOKEN")
        self.timeout = 300 # 5 minutes timeout for job execution
        self.headers = {"X-Nomad-Token": self.token} if self.token else {}

    def execute(self, code: str, language: str = "python", libraries: Optional[List[str]] = None) -> str:
        if language != "python":
            return "Error: Nomad executor currently only supports Python."
        if libraries:
             return "Error: Nomad executor currently does not support dynamic library installation. Use Docker executor or pre-built images."

        job_id = f"sandbox-{uuid.uuid4()}"
        logging.info(f"Dispatching Nomad sandbox job: {job_id}")

        # Security Enhancement: Base64 encode the code to prevent Nomad Template Injection
        code_b64 = base64.b64encode(code.encode('utf-8')).decode('utf-8')

        # Construct Job JSON
        job_payload = {
            "Job": {
                "ID": job_id,
                "Name": job_id,
                "Type": "batch",
                "Datacenters": ["dc1"],
                "TaskGroups": [
                    {
                        "Name": "sandbox",
                        "Count": 1,
                        "RestartPolicy": {
                            "Attempts": 0,
                            "Mode": "fail"
                        },
                        "Tasks": [
                            {
                                "Name": "execution",
                                "Driver": "docker",
                                "Config": {
                                    "image": "python:3.9-slim",
                                    "command": "/bin/sh",
                                    # Decode base64 to script.py and then execute it
                                    "args": [
                                        "-c",
                                        "python3 -c 'import base64; open(\"/local/script.py\", \"wb\").write(base64.b64decode(open(\"/local/script.b64\", \"rb\").read()))' && python3 /local/script.py"
                                    ],
                                    "network_mode": "none"
                                },
                                "Resources": {
                                    "CPU": 100,
                                    "MemoryMB": 128
                                },
                                "Templates": [
                                    {
                                        "EmbeddedTmpl": code_b64,
                                        "DestPath": "local/script.b64",
                                        "ChangeMode": "noop"
                                        # Removed LeftDelim/RightDelim as base64 is safe with default {{ }}
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }

        try:
            # 1. Register Job
            reg_resp = requests.post(f"{self.nomad_url}/v1/jobs", json=job_payload, headers=self.headers, timeout=10)
            reg_resp.raise_for_status()

            # 2. Wait for Allocation
            alloc_id = None
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                try:
                    allocs_resp = requests.get(f"{self.nomad_url}/v1/job/{job_id}/allocations", headers=self.headers, timeout=10)
                    allocs_resp.raise_for_status()
                    allocs = allocs_resp.json()

                    if allocs:
                        # Sort by CreateTime desc to get latest
                        allocs.sort(key=lambda x: x.get('CreateTime', 0), reverse=True)
                        latest_alloc = allocs[0]
                        alloc_id = latest_alloc['ID']
                        client_status = latest_alloc.get('ClientStatus')

                        if client_status in ['complete', 'failed']:
                            break
                except Exception as e:
                    logging.warning(f"Error polling allocations for job {job_id}: {e}")

                time.sleep(1)

            if not alloc_id:
                return "Error: Nomad job timed out waiting for allocation."

            # 3. Retrieve Logs
            try:
                # Re-fetch alloc to get NodeID/Address
                alloc_detail = requests.get(f"{self.nomad_url}/v1/allocation/{alloc_id}", headers=self.headers, timeout=10).json()
                node_id = alloc_detail.get("NodeID")
                # We can find the Node address from /v1/node/:node_id
                node_detail = requests.get(f"{self.nomad_url}/v1/node/{node_id}", headers=self.headers, timeout=10).json()
                node_addr = node_detail.get("HTTPAddr")
                # This is likely the internal IP.

                logs = ""
                for log_type in ["stdout", "stderr"]:
                    # Using the node address directly
                    try:
                        log_url = f"http://{node_addr}/v1/client/fs/logs/{alloc_id}?task=execution&type={log_type}&plain=true"
                        log_resp = requests.get(log_url, headers=self.headers, timeout=10)
                        if log_resp.status_code == 200:
                            content = log_resp.text
                            if content:
                                logs += f"---{log_type.upper()}---\n{content}\n"
                    except Exception as e:
                        logs += f"Error fetching {log_type}: {e}\n"

                return logs.strip()
            except Exception as e:
                return f"Error retrieving logs for job {job_id}: {e}"

        except Exception as e:
            return f"Nomad execution error: {e}"
        finally:
            # 4. Cleanup
            try:
                requests.delete(f"{self.nomad_url}/v1/job/{job_id}?purge=true", headers=self.headers, timeout=10)
            except:
                pass

class CodeRunnerTool:
    """A tool for executing Python code in a sandboxed environment (Docker or Nomad).

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self):
        """Initializes the CodeRunnerTool."""
        self.description = "Execute Python code in a sandboxed Docker container."
        self.name = "code_runner"

        # Determine executor mode: 'docker' (default) or 'nomad'
        # Can be overridden by env var SANDBOX_EXECUTOR
        self.mode = os.environ.get("SANDBOX_EXECUTOR", "docker").lower()

        if self.mode == "nomad":
            self.executor = NomadSandboxExecutor()
            logging.info("CodeRunnerTool initialized in NOMAD mode.")
        elif self.mode == "hybrid":
            self.executor = NomadSandboxExecutor()
            self.fast_executor = DockerSandboxExecutor()
            logging.info("CodeRunnerTool initialized in HYBRID mode.")
        else:
            self.executor = DockerSandboxExecutor()
            logging.info("CodeRunnerTool initialized in DOCKER mode.")

    def run_python_code(self, code: str) -> str:
        """Runs a string of Python code and returns the output.

        Preserves legacy behavior for Docker mode (simple execution).
        """
        if self.mode == "hybrid" and hasattr(self, 'fast_executor'):
            if self.fast_executor.client:
                 return self.fast_executor.execute_simple_python(code)
            logging.warning("Local Docker client unavailable in hybrid mode. Falling back to Nomad.")
            return self.executor.execute(code, language="python")

        if isinstance(self.executor, DockerSandboxExecutor):
            return self.executor.execute_simple_python(code)

        return self.executor.execute(code, language="python")

    def run_code_in_sandbox(
        self,
        code: str,
        language: str = "python",
        libraries: Optional[List[str]] = None
    ) -> str:
        """Runs code in a secure sandbox, with support for multiple languages."""
        return self.executor.execute(code, language, libraries)
