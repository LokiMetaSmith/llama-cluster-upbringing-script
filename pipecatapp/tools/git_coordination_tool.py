import os
import logging
from typing import Dict, Any, Optional

class GitCoordinationTool:
    """A tool for managing durable Git-native coordination artifacts.

    Maintains PLAN.md, STATE.md, DECISIONS.md, and EVIDENCE.md under a target project directory
    (e.g., .liminal/projects/<project_name>/) to ensure multi-agent state changes, architectural
    decisions, and evidence logs are preserved in committed Git history.
    """

    def __init__(self, base_dir: str = ".liminal/projects"):
        self.name = "git_coordination"
        self.description = (
            "Read, update, or append to durable Git coordination artifacts "
            "(PLAN.md, STATE.md, DECISIONS.md, EVIDENCE.md) for a given project."
        )
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project": {
                            "type": "string",
                            "description": "Project or task name directory under .liminal/projects/"
                        },
                        "artifact": {
                            "type": "string",
                            "enum": ["PLAN", "STATE", "DECISIONS", "EVIDENCE"],
                            "description": "The specific coordination artifact file to interact with."
                        },
                        "action": {
                            "type": "string",
                            "enum": ["read", "write", "append"],
                            "description": "Action to perform on the artifact."
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write or append to the artifact. Required for write/append actions."
                        }
                    },
                    "required": ["project", "artifact", "action"]
                }
            }
        }

    def execute(self, project: str, artifact: str, action: str, content: Optional[str] = None, **kwargs) -> str:
        abs_base = os.path.abspath(self.base_dir)
        project_dir = os.path.abspath(os.path.join(self.base_dir, project))

        if not project_dir.startswith(abs_base):
            return "Error: Path traversal attempt detected."

        os.makedirs(project_dir, exist_ok=True)
        filepath = os.path.join(project_dir, f"{artifact}.md")

        if action == "read":
            return self._read_artifact(filepath, artifact)
        elif action in ["write", "append"]:
            if not content:
                return f"Error: 'content' parameter is required for action '{action}'."
            return self._write_artifact(filepath, artifact, content, mode="a" if action == "append" else "w")
        return f"Error: Unknown action '{action}'"

    def _read_artifact(self, filepath: str, artifact: str) -> str:
        if not os.path.exists(filepath):
            return f"Artifact {artifact}.md does not exist yet at {filepath}."
        try:
            with open(filepath, "r") as f:
                data = f.read()
            return f"--- ARTIFACT ({artifact}.md) ---\n{data}\n--- END ARTIFACT ---"
        except Exception as e:
            self.logger.error(f"Failed to read artifact {filepath}: {e}")
            return f"Error reading artifact {artifact}.md: {e}"

    def _write_artifact(self, filepath: str, artifact: str, content: str, mode: str = "w") -> str:
        try:
            with open(filepath, mode) as f:
                f.write(content + ("\n" if mode == "a" else ""))
            return f"Successfully updated {filepath} ({mode} mode)."
        except Exception as e:
            self.logger.error(f"Failed to write artifact {filepath}: {e}")
            return f"Error writing artifact {artifact}.md: {e}"
