import os
import shutil
import subprocess
import json
import logging
from typing import Dict, Any, List, Optional
from pipecatapp.utils.command_runner import CommandRunner

class OpenShellTool:
    """
    A tool for creating, managing, and inspecting NVIDIA OpenShell sandboxes
    and evaluating security policies via OpenShell CLI / SDK.
    """

    def __init__(self):
        self.name = "openshell"
        self.description = (
            "Interface for NVIDIA OpenShell: manages agent runtime sandboxes, executes code in isolated environments, "
            "and inspects/proves security policies (Advisor and Prover)."
        )
        self.cli_binary = shutil.which("openshell") or "openshell"

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
                            "description": "The action to perform. Options: create_sandbox, list_sandboxes, destroy_sandbox, execute_command, check_policy, get_status"
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Arguments for the action (e.g. name, image, command, policy_path)."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def _run_cli(self, args: List[str], timeout: int = 30) -> Dict[str, Any]:
        """Runs the openshell CLI command and returns parsed JSON or raw output."""
        if not shutil.which("openshell"):
            # Simulation fallback if openshell CLI is not installed on host
            return self._simulate_cli(args)

        cmd = [self.cli_binary] + args
        try:
            res = CommandRunner.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
            if res.returncode == 0:
                output = res.stdout.strip()
                try:
                    parsed = json.loads(output)
                    return {"success": True, "data": parsed, "raw": output}
                except json.JSONDecodeError:
                    return {"success": True, "output": output}
            else:
                return {
                    "success": False,
                    "error": res.stderr.strip() or res.stdout.strip() or f"Command failed with exit code {res.returncode}",
                    "returncode": res.returncode
                }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"OpenShell command timed out after {timeout} seconds."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _simulate_cli(self, args: List[str]) -> Dict[str, Any]:
        """Fallback simulation for testing or environments where openshell CLI is not installed."""
        cmd_str = " ".join(args)
        if "sandbox create" in cmd_str:
            name = args[args.index("--name") + 1] if "--name" in args else "demo"
            return {"success": True, "simulated": True, "data": {"sandbox_id": f"sbx-{name}", "status": "created", "name": name}}
        elif "sandbox list" in cmd_str:
            return {"success": True, "simulated": True, "data": [{"id": "sbx-demo", "name": "demo", "status": "running"}]}
        elif "sandbox destroy" in cmd_str:
            return {"success": True, "simulated": True, "data": {"status": "destroyed"}}
        elif "policy prover" in cmd_str or "policy check" in cmd_str or "policy advisor" in cmd_str:
            return {"success": True, "simulated": True, "data": {"policy_status": "verified", "risks_found": [], "allowed": True}}
        elif "exec" in cmd_str or "run" in cmd_str:
            return {"success": True, "simulated": True, "output": "Simulated OpenShell execution completed successfully."}
        else:
            return {"success": True, "simulated": True, "output": f"Simulated OpenShell action: {cmd_str}"}

    def create_sandbox(self, name: str = "demo", image: str = "ubuntu:22.04", policy: Optional[str] = None) -> Dict[str, Any]:
        """Creates a new isolated OpenShell sandbox."""
        args = ["sandbox", "create", "--name", name, "--image", image]
        if policy:
            args.extend(["--policy", policy])
        return self._run_cli(args)

    def list_sandboxes(self) -> Dict[str, Any]:
        """Lists active OpenShell sandboxes."""
        return self._run_cli(["sandbox", "list", "--json"])

    def destroy_sandbox(self, name: str) -> Dict[str, Any]:
        """Destroys an existing OpenShell sandbox."""
        return self._run_cli(["sandbox", "destroy", name])

    def execute_command(self, sandbox_name: str, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Executes a command inside an OpenShell sandbox."""
        return self._run_cli(["sandbox", "exec", sandbox_name, "--", command], timeout=timeout)

    def check_policy(self, policy_path: str, mode: str = "prove") -> Dict[str, Any]:
        """Checks or proves policy safety using OpenShell Prover/Advisor."""
        if mode == "advise":
            return self._run_cli(["policy", "advisor", policy_path, "--json"])
        return self._run_cli(["policy", "prover", policy_path, "--json"])

    def get_status(self) -> Dict[str, Any]:
        """Gets the status of the local OpenShell gateway/daemon."""
        return self._run_cli(["status", "--json"])

    def execute(self, action: str, **kwargs) -> Any:
        # Handle nested kwargs parameter if passed via get_schema format
        params = kwargs.get("kwargs", kwargs)

        actions = {
            "create_sandbox": lambda: self.create_sandbox(
                name=params.get("name", "demo"),
                image=params.get("image", "ubuntu:22.04"),
                policy=params.get("policy")
            ),
            "list_sandboxes": lambda: self.list_sandboxes(),
            "destroy_sandbox": lambda: self.destroy_sandbox(name=params.get("name", "demo")),
            "execute_command": lambda: self.execute_command(
                sandbox_name=params.get("sandbox_name", params.get("name", "demo")),
                command=params.get("command", "echo hello"),
                timeout=params.get("timeout", 30)
            ),
            "check_policy": lambda: self.check_policy(
                policy_path=params.get("policy_path", "policy.yaml"),
                mode=params.get("mode", "prove")
            ),
            "get_status": lambda: self.get_status()
        }

        if action in actions:
            return actions[action]()
        return {"success": False, "error": f"Unknown action: '{action}'. Available actions: {list(actions.keys())}"}
