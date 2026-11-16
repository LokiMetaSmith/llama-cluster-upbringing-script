import os
import subprocess
import json
from typing import Dict, Any, Optional
from pipecatapp.utils.command_runner import CommandRunner

class PolyphonyTool:
    """
    A tool for interacting with the Keystone Polyphony Swarm.
    Agents can use this tool to broadcast thoughts, ping other nodes, acquire baton locks,
    or manage swarm tasks.
    """

    def __init__(self, cli_path: str = "modules/keystone-polyphony/polyphony", swarm_key: Optional[str] = None):
        self.cli_path = cli_path
        self.swarm_key = swarm_key or os.environ.get("SWARM_KEY", "KEYSTONE-POLYPHONY-LOCAL")
        self.name = "polyphony_tool"
        self.description = "Interact with the Keystone Polyphony swarm to share thoughts, acquire baton locks, and manage tasks."

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "polyphony_tool"),
                "description": getattr(self, "description", "Tool PolyphonyTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": [
                                "share", "ping", "task_list", "task_add", "task_claim",
                                "task_complete", "baton_acquire", "baton_release", "status", "get_info"
                            ],
                            "description": "The polyphony action to perform."
                        },
                        "thought": {
                            "type": "string",
                            "description": "The thought to share (for 'share' action)."
                        },
                        "node_id": {
                            "type": "string",
                            "description": "The target node ID (for 'ping' action)."
                        },
                        "message": {
                            "type": "string",
                            "description": "The message to send (for 'ping' action)."
                        },
                        "title": {
                            "type": "string",
                            "description": "The task title (for 'task_add' action)."
                        },
                        "description": {
                            "type": "string",
                            "description": "The task description (for 'task_add' action)."
                        },
                        "priority": {
                            "type": "string",
                            "description": "The task priority (for 'task_add' action)."
                        },
                        "task_id": {
                            "type": "string",
                            "description": "The task ID (for 'task_claim' and 'task_complete' actions)."
                        },
                        "resource": {
                            "type": "string",
                            "description": "The resource or filepath to lock/unlock (for 'baton_acquire' and 'baton_release')."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs: Any) -> Any:
        """
        Executes a Polyphony CLI command or internal query.

        Args:
            action: The polyphony action to take (e.g. "share", "ping", "task_list", "task_add", "baton_acquire", "baton_release", "status")
            kwargs: Parameters for the action.
        """
        if action == "get_info":
            return self.get_info()

        env = os.environ.copy()
        env["SWARM_KEY"] = self.swarm_key

        try:
            if action == "share":
                thought = kwargs.get("thought")
                if not thought:
                    return "Error: 'thought' parameter is required for share action."
                return self._run_cmd(["share", thought], env)

            elif action == "ping":
                node_id = kwargs.get("node_id")
                message = kwargs.get("message")
                if not node_id or not message:
                    return "Error: 'node_id' and 'message' parameters are required for ping action."
                return self._run_cmd(["ping", node_id, message], env)

            elif action == "task_list":
                return self._run_cmd(["task", "list"], env)

            elif action == "task_add":
                title = kwargs.get("title")
                description = kwargs.get("description", "")
                priority = kwargs.get("priority", "medium")
                if not title:
                    return "Error: 'title' parameter is required for task_add action."
                return self._run_cmd(["task", "add", title, description, priority], env)

            elif action == "task_claim":
                task_id = kwargs.get("task_id")
                if not task_id:
                    return "Error: 'task_id' parameter is required for task_claim action."
                return self._run_cmd(["task", "claim", task_id], env)

            elif action == "task_complete":
                task_id = kwargs.get("task_id")
                if not task_id:
                    return "Error: 'task_id' parameter is required for task_complete action."
                return self._run_cmd(["task", "complete", task_id], env)

            elif action == "baton_acquire":
                resource = kwargs.get("resource") or kwargs.get("filepath")
                if not resource:
                    return "Error: 'resource' or 'filepath' parameter is required for baton_acquire action."
                return self._run_cmd(["baton", "acquire", resource], env)

            elif action == "baton_release":
                resource = kwargs.get("resource") or kwargs.get("filepath")
                if not resource:
                    return "Error: 'resource' or 'filepath' parameter is required for baton_release action."
                return self._run_cmd(["baton", "release", resource], env)

            elif action == "status":
                return self._run_cmd(["status"], env)

            else:
                return f"Error: Unknown action '{action}'"

        except Exception as e:
            return f"Error executing polyphony command: {str(e)}"

    def _run_cmd(self, args: list[str], env: dict) -> str:
        if not os.path.exists(self.cli_path):
            return f"Error: Polyphony CLI not found at {self.cli_path}. Are you running this in the project root?"

        cmd = [self.cli_path] + args
        result = CommandRunner.run(
            cmd,
            env=env,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"Command failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        return result.stdout or "Success"

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": "polyphony_tool",
            "description": "Interact with the Keystone Polyphony swarm to share thoughts, check status, acquire baton locks, and manage tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": [
                            "share", "ping", "task_list", "task_add", "task_claim",
                            "task_complete", "baton_acquire", "baton_release", "status"
                        ],
                        "description": "The polyphony action to perform."
                    },
                    "thought": {
                        "type": "string",
                        "description": "The thought to share (for 'share' action)."
                    },
                    "node_id": {
                        "type": "string",
                        "description": "The target node ID (for 'ping' action)."
                    },
                    "message": {
                        "type": "string",
                        "description": "The message to send (for 'ping' action)."
                    },
                    "title": {
                        "type": "string",
                        "description": "The task title (for 'task_add' action)."
                    },
                    "description": {
                        "type": "string",
                        "description": "The task description (for 'task_add' action)."
                    },
                    "priority": {
                        "type": "string",
                        "description": "The task priority (for 'task_add' action)."
                    },
                    "task_id": {
                        "type": "string",
                        "description": "The task ID (for 'task_claim' and 'task_complete' actions)."
                    },
                    "resource": {
                        "type": "string",
                        "description": "The resource or filepath to lock/unlock (for 'baton_acquire' and 'baton_release')."
                    }
                },
                "required": ["action"]
            }
        }
