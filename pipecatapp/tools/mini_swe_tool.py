"""
Tool wrapper around mini-swe-agent for task delegation.
"""

import os
from typing import Dict, Any, Optional
try:
    from pipecatapp.services.mini_swe_service import MiniSWEService
except ImportError:
    MiniSWEService = None

class MiniSWEAgentTool:
    """
    Tool allowing pipecatapp agents to delegate coding, fixing, and repository tasks
    to mini-swe-agent with optional Docker sandboxing or Local execution.
    """

    def __init__(self, service: Optional[Any] = None):
        self.name = "mini_swe_agent"
        self.description = (
            "Executes software engineering, debugging, and bash code tasks using mini-swe-agent. "
            "Requires a 'task' string argument. Accepts 'environment_type' ('docker' or 'local') and 'cwd'."
        )
        if service is not None:
            self.service = service
        elif MiniSWEService is not None:
            try:
                self.service = MiniSWEService()
            except Exception:
                self.service = None
        else:
            self.service = None

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The detailed description of the software engineering or debugging task."
                        },
                        "environment_type": {
                            "type": "string",
                            "enum": ["docker", "local"],
                            "description": "Execution environment. Default is 'docker' for sandboxed execution."
                        },
                        "cwd": {
                            "type": "string",
                            "description": "Working directory for task execution."
                        }
                    },
                    "required": ["task"]
                }
            }
        }

    def execute(self, action: Optional[str] = None, task: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        task_str = task or kwargs.get("task") or action
        if not task_str:
            return {"status": "error", "error": "Parameter 'task' is required."}

        if not self.service:
            return {"status": "error", "error": "MiniSWEService is not available or minisweagent is not installed."}

        env_type = kwargs.get("environment_type", "docker")
        cwd = kwargs.get("cwd")

        return self.service.run_task(
            task=task_str,
            cwd=cwd,
            environment_type=env_type,
        )

    def run(self, task: str, environment_type: str = "docker", cwd: Optional[str] = None) -> Dict[str, Any]:
        return self.execute(task=task, environment_type=environment_type, cwd=cwd)
