import abc
import docker
import logging
import os
import tempfile
import time
import uuid
import requests
import base64
import multiprocessing
from llm_sandbox import SandboxSession
from typing import List, Optional
from .dependency_scanner_tool import DependencyScannerTool

# Security: Limit the maximum size of the code payload to prevent DoS attacks
# especially against Nomad templates which might expand significantly or cause OOM.
MAX_CODE_LENGTH = 100000

class SandboxExecutor(abc.ABC):
    """Abstract base class for sandbox execution strategies."""

    @abc.abstractmethod
    def execute(self, code: str, language: str = "python", libraries: Optional[List[str]] = None, timeout: Optional[int] = None) -> str:
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

    def execute(self, code: str, language: str = "python", libraries: Optional[List[str]] = None, timeout: Optional[int] = None) -> str:
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

        import multiprocessing

        job_timeout = timeout if timeout is not None else 30

        import sys

        def _run_sandbox(q, c, l, lang):
            import signal
            # Signal handler to ensure graceful context manager exit on SIGTERM
            class TimeoutException(Exception): pass
            def sigterm_handler(signum, frame):
                raise TimeoutException("Timed out")
            signal.signal(signal.SIGTERM, sigterm_handler)

            try:
                with SandboxSession(lang=lang) as session:
                    res = session.run(c, libraries=l)
                    q.put((res.exit_code, res.stdout, res.stderr, res.plots))
            except TimeoutException:
                q.put("TIMEOUT")
            except Exception as e:
                q.put(e)

        try:
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=_run_sandbox, args=(q, code, libraries, language))
            p.start()
            p.join(job_timeout)

            if p.is_alive():
                p.terminate()
                p.join()
                return f"Error: Execution timed out after {job_timeout} seconds."

            if not q.empty():
                res = q.get()
                if res == "TIMEOUT":
                    return f"Error: Execution timed out after {job_timeout} seconds."
                if isinstance(res, Exception):
                    raise res
                exit_code, stdout, stderr, plots = res

                if exit_code == 0:
                    output = stdout
                else:
                    output = f"Exit Code: {exit_code}\n---STDERR---\n{stderr}\n---STDOUT---\n{stdout}"

                if plots:
                    output += "\n\nGenerated plots are available."

                return output
            else:
                return "Error: Sandbox execution failed to return a result."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def execute_simple_python(self, code: str, timeout: Optional[int] = None) -> str:
        """Runs simple Python code using raw docker-py for speed/legacy support."""
        if not self.client:
            return "Error: Docker execution is not available (Docker client failed to initialize)."

        container = None
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
                    detach=True,          # Security: Run in background to support timeout
                    stderr=True,
                    stdout=True
                )

                job_timeout = timeout if timeout is not None else 30
                # Security: Implement timeout mechanism to prevent DoS via infinite loops
                start_time = time.time()
                while time.time() - start_time < job_timeout:
                    container.reload()
                    if container.status != 'running':
                        break
                    time.sleep(0.5)

                if container.status == 'running':
                    container.kill()
                    return f"Error: Execution timed out after {job_timeout} seconds."

                output = container.logs().decode('utf-8')
                return output

        except docker.errors.ImageNotFound:
            return f"Error: The Docker image '{self.image}' was not found. Please pull it first."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:
                    pass

class NomadSandboxExecutor(SandboxExecutor):
    """Executes code by dispatching ephemeral Nomad batch jobs."""

    def __init__(self):
        self.nomad_url = os.environ.get("NOMAD_ADDR", "http://localhost:4646")
        self.token = os.environ.get("NOMAD_TOKEN")
        self.default_timeout = 300 # 5 minutes default timeout for job execution
        self.headers = {"X-Nomad-Token": self.token} if self.token else {}

    def execute(self, code: str, language: str = "python", libraries: Optional[List[str]] = None, timeout: Optional[int] = None) -> str:
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

        job_timeout = timeout if timeout is not None else self.default_timeout

        try:
            # 1. Register Job
            reg_resp = requests.post(f"{self.nomad_url}/v1/jobs", json=job_payload, headers=self.headers, timeout=10)
            reg_resp.raise_for_status()

            # 2. Wait for Allocation
            alloc_id = None
            start_time = time.time()
            while time.time() - start_time < job_timeout:
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
        self.description = (
            "Execute Python code in a sandboxed Docker/Nomad container. "
            "Use this tool as an executable oracle to test snippets before modifying host files. "
            "Dependencies can be specified in the `libraries` argument (e.g., `['requests==2.31.0']`). "
            "The tool validates dependencies against an OSV vulnerability scanner. "
            "A timeout is enforced to prevent infinite loops."
        )
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

    def run_python_code(self, code: str, timeout: Optional[int] = None) -> str:
        """Runs a string of Python code and returns the output.

        Args:
            code (str): The Python code to execute.
            timeout (int, optional): The maximum execution time in seconds. Defaults to 30.

        Preserves legacy behavior for Docker mode (simple execution).
        """
        if len(code) > MAX_CODE_LENGTH:
            return f"Error: Code length exceeds the maximum limit of {MAX_CODE_LENGTH} characters."

        if self.mode == "hybrid" and hasattr(self, 'fast_executor'):
            if self.fast_executor.client:
                 return self.fast_executor.execute_simple_python(code, timeout=timeout)
            logging.warning("Local Docker client unavailable in hybrid mode. Falling back to Nomad.")
            return self.executor.execute(code, language="python", timeout=timeout)

        if isinstance(self.executor, DockerSandboxExecutor):
            return self.executor.execute_simple_python(code, timeout=timeout)

        return self.executor.execute(code, language="python", timeout=timeout)

    def run_code_in_sandbox(
        self,
        code: str,
        language: str = "python",
        libraries: Optional[List[str]] = None,
        timeout: Optional[int] = None
    ) -> str:
        """Runs code in a secure sandbox, with support for multiple languages.

        Args:
            code (str): The code to execute.
            language (str, optional): The programming language (e.g., 'python', 'nodejs'). Defaults to 'python'.
            libraries (List[str], optional): A list of library dependencies to install before running.
            timeout (int, optional): The maximum execution time in seconds. Defaults to 30 for Docker and 300 for Nomad.
        """
        if len(code) > MAX_CODE_LENGTH:
            return f"Error: Code length exceeds the maximum limit of {MAX_CODE_LENGTH} characters."

        return self.executor.execute(code, language, libraries, timeout)
