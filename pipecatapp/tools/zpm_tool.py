import os
import sys
import json
import logging
from typing import Dict, Any, Optional
from pipecatapp.utils.command_runner import CommandRunner

class ZeroPointModulatorTool:
    """A tool for managing repository enrollment and worker capacity reconciliation via ZPM.

    Zero Point Modulator (ZPM) coordinates the desired worker capacity across
    repositories, bridges OpenJules container execution with Keystone Polyphony
    task authority, and performs resilient reconciliation without erasing pending tasks.
    """

    def __init__(
        self,
        state_file: Optional[str] = None,
        deployment_id: Optional[str] = None,
        provider_config: Optional[str] = None,
        zpm_module_path: Optional[str] = None,
        root_dir: Optional[str] = None,
    ):
        self.name = "zpm_tool"
        self.description = (
            "Manage repository enrollment, worker capacity, and reconciliation "
            "for the distributed LLM coding system using Zero Point Modulator (ZPM)."
        )
        self.root_dir = os.path.realpath(root_dir or os.getcwd())
        self.state_file = state_file or os.getenv("ZPM_STATE_FILE") or os.path.join(self.root_dir, ".zpm", "state.sqlite3")
        self.deployment_id = deployment_id or os.getenv("ZPM_DEPLOYMENT_ID") or "llama-cluster-zpm"
        self.provider_config = provider_config or os.getenv("ZPM_PROVIDER_CONFIG")
        self.zpm_module_path = os.path.realpath(
            zpm_module_path or os.getenv("ZPM_MODULE_PATH") or os.path.join(self.root_dir, "modules", "zero-point-modulator")
        )

    def _validate_path(self, path: str) -> str:
        """Validate and resolve file path preventing path traversal outside allowed root boundaries."""
        real_path = os.path.realpath(path)
        # Verify containment if inside root_dir, or allow standard system state paths if explicitly configured
        try:
            common = os.path.commonpath([self.root_dir, real_path])
            if common == self.root_dir:
                return real_path
        except ValueError:
            pass

        # If outside root_dir (e.g. /opt/zpm or /tmp), ensure it doesn't contain forbidden traversal
        if ".." in path:
            raise ValueError(f"Path traversal detected: {path}")
        return real_path

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
                                "status",
                                "plan",
                                "enroll",
                                "target",
                                "pause",
                                "resume",
                                "remove",
                                "reconcile",
                                "validate"
                            ],
                            "description": "The ZPM operation to execute."
                        },
                        "repository": {
                            "type": "string",
                            "description": "Target repository (e.g. 'github:owner/repo' or 'owner/repo')."
                        },
                        "target_workers": {
                            "type": "integer",
                            "description": "Desired number of worker instances (for 'target' and 'resume')."
                        },
                        "config_file": {
                            "type": "string",
                            "description": "Path to repository enrollment JSON (for 'enroll' and 'validate')."
                        },
                        "provider_file": {
                            "type": "string",
                            "description": "Path to OpenJules provider JSON configuration (for 'reconcile')."
                        },
                        "max_actions": {
                            "type": "integer",
                            "description": "Max mutations per reconciliation tick (default 16)."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def get_info(self) -> Dict[str, Any]:
        return self.get_schema()["function"]

    def execute(self, action: str, **kwargs: Any) -> str:
        """Execute a ZPM command."""
        env = os.environ.copy()
        python_path = env.get("PYTHONPATH", "")
        if self.zpm_module_path not in python_path:
            env["PYTHONPATH"] = f"{self.zpm_module_path}:{python_path}" if python_path else self.zpm_module_path

        base_cmd = [
            sys.executable,
            "-m",
            "zpm",
            "--state",
            self.state_file,
            "--deployment-id",
            self.deployment_id,
        ]

        try:
            # Ensure state directory exists
            state_dir = os.path.dirname(os.path.realpath(self.state_file))
            if state_dir and not os.path.exists(state_dir):
                os.makedirs(state_dir, exist_ok=True)

            if action == "status":
                return self._run_cmd(base_cmd + ["status"], env)

            elif action == "plan":
                return self._run_cmd(base_cmd + ["plan"], env)

            elif action == "enroll":
                config_file = kwargs.get("config_file")
                if not config_file:
                    return "Error: 'config_file' is required for enroll action."
                valid_path = self._validate_path(config_file)
                return self._run_cmd(base_cmd + ["enroll", valid_path], env)

            elif action == "target":
                repo = kwargs.get("repository")
                target = kwargs.get("target_workers")
                if not repo or target is None:
                    return "Error: 'repository' and 'target_workers' are required for target action."
                return self._run_cmd(base_cmd + ["target", str(repo), str(int(target))], env)

            elif action == "pause":
                repo = kwargs.get("repository")
                if not repo:
                    return "Error: 'repository' is required for pause action."
                return self._run_cmd(base_cmd + ["pause", str(repo)], env)

            elif action == "resume":
                repo = kwargs.get("repository")
                target = kwargs.get("target_workers")
                if not repo or target is None:
                    return "Error: 'repository' and 'target_workers' are required for resume action."
                return self._run_cmd(base_cmd + ["resume", str(repo), str(int(target))], env)

            elif action == "remove":
                repo = kwargs.get("repository")
                if not repo:
                    return "Error: 'repository' is required for remove action."
                return self._run_cmd(base_cmd + ["remove", str(repo)], env)

            elif action == "validate":
                config_file = kwargs.get("config_file")
                if not config_file:
                    return "Error: 'config_file' is required for validate action."
                valid_path = self._validate_path(config_file)
                return self._run_cmd([sys.executable, "-m", "zpm", "validate", valid_path], env)

            elif action == "reconcile":
                provider_file = kwargs.get("provider_file") or self.provider_config
                if not provider_file:
                    return "Error: 'provider_file' is required for reconcile action."
                valid_provider = self._validate_path(provider_file)
                cmd = base_cmd + ["reconcile", "--provider", valid_provider]
                max_actions = kwargs.get("max_actions")
                if max_actions:
                    cmd.extend(["--max-actions", str(int(max_actions))])
                return self._run_cmd(cmd, env)

            else:
                return f"Error: Unknown action '{action}'"

        except Exception as e:
            logging.error(f"Error executing ZPM command: {e}")
            return f"Error executing ZPM command: {str(e)}"

    def _run_cmd(self, cmd: list[str], env: dict) -> str:
        result = CommandRunner.run(
            cmd,
            env=env,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return f"Command failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        return result.stdout or "Success"


# Convenience alias
ZPMTool = ZeroPointModulatorTool
