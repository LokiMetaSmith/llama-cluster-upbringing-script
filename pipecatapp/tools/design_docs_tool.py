import os
import logging
from typing import Dict, Any

class DesignDocsTool:
    """A tool for curating and interacting with the swarm's Design Docs.

    Design Docs are used by Planner agents (like the ManagerAgent) to record
    architectural decisions and resolve contention between parallel planners.
    """

    def __init__(self, filepath: str = ".liminal/design_docs.md"):
        self.name = "design_docs"
        self.description = (
            "Read and update the shared Design Docs to record architectural decisions "
            "and resolve contention between planner agents."
        )
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)

        # Ensure directory and file exist
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                f.write("# Swarm Design Documents\n\n*Record architectural decisions here.*\n")

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
                            "enum": ["read", "append", "overwrite"],
                            "description": "Whether to read, append to, or overwrite the design docs."
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to add or write. Required for append/overwrite."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, content: str = None, **kwargs) -> str:
        if action == "read":
            return self._read_docs()
        elif action in ["append", "overwrite"]:
            if not content:
                return f"Error: 'content' must be provided for the '{action}' action."
            return self._write_docs(content, mode="a" if action == "append" else "w")
        return f"Error: Unknown action '{action}'"

    def _read_docs(self) -> str:
        try:
            with open(self.filepath, "r") as f:
                content = f.read()
            return f"--- DESIGN DOCS ({self.filepath}) ---\n{content}\n--- END DESIGN DOCS ---"
        except Exception as e:
            self.logger.error(f"Failed to read design docs: {e}")
            return f"Error reading design docs: {e}"

    def _write_docs(self, content: str, mode: str = "w") -> str:
        try:
            with open(self.filepath, mode) as f:
                f.write(content + ("\n" if mode == "a" else ""))
            return f"Successfully updated {self.filepath}."
        except Exception as e:
            self.logger.error(f"Failed to write design docs: {e}")
            return f"Error writing design docs: {e}"
