import logging
import os
import subprocess
from typing import Optional, Dict, Any
from .code_runner_tool import ApptainerSandboxExecutor

class HermesTool:
    """A tool for interfacing with external Hermes Agent and running HPC tasks in Apptainer sandboxes.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """

    def __init__(self, sif_image: Optional[str] = None, workspace_dir: Optional[str] = None):
        self.description = (
            "Interface with external Hermes Agent and execute HPC tasks using "
            "Singularity/Apptainer sandboxed containers."
        )
        self.name = "hermes_tool"
        self.executor = ApptainerSandboxExecutor(
            sif_image=sif_image,
            workspace_dir=workspace_dir
        )

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "hermes_tool"),
                "description": getattr(self, "description", "Tool HermesTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: run_hermes_cmd, run_apptainer_task"
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs):
        kw = kwargs.get("kwargs", kwargs)
        if action == "run_hermes_cmd":
            return self.run_hermes_cmd(**kw)
        elif action == "run_apptainer_task":
            return self.run_apptainer_task(**kw)
        else:
            return f"Unknown action: {action}"

    def run_hermes_cmd(self, command: str, timeout: int = 60) -> str:
        """Executes a Hermes CLI command inside the Apptainer sandbox.

        Args:
            command (str): The Hermes agent command to execute (e.g., 'hermes run ...').
            timeout (int, optional): Execution timeout in seconds. Defaults to 60.

        Returns:
            str: Output of the command execution.
        """
        full_cmd = f"hermes {command}" if not command.startswith("hermes") else command
        res = self.executor.run_command(full_cmd, timeout=timeout)
        if res["exit_code"] == 0:
            return res["stdout"]
        err = res["stderr"] or res["stdout"]
        return f"Hermes Command Failed (Exit Code {res['exit_code']}):\n{err}"

    def run_apptainer_task(self, command: str, timeout: int = 60) -> str:
        """Executes an arbitrary command/script inside the Singularity/Apptainer HPC sandbox.

        Args:
            command (str): Shell command to execute inside the container.
            timeout (int, optional): Execution timeout in seconds. Defaults to 60.

        Returns:
            str: Standard output or error output from the container run.
        """
        res = self.executor.run_command(command, timeout=timeout)
        if res["exit_code"] == 0:
            return res["stdout"]
        err = res["stderr"] or res["stdout"]
        return f"Apptainer Task Failed (Exit Code {res['exit_code']}):\n{err}"
