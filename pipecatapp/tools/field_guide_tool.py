import os
import logging
from typing import Dict, Any

class FieldGuideTool:
    """A tool for curating and interacting with the swarm's Field Guide (Stigmergy).

    The Field Guide is a shared document that institutionalizes knowledge for the agent
    swarm across tasks. It is strictly limited to a line budget (default 200 lines) to force
    curation, prioritization, and dense summarization.
    """

    def __init__(self, filepath: str = ".liminal/field_guide.md", line_budget: int = 200):
        self.name = "field_guide"
        self.description = (
            "Read and update the shared Field Guide to capture institutional knowledge, "
            "learnings, and critical operational context for future tasks and agents. "
            f"The guide has a strict limit of {line_budget} lines to force prioritization."
        )
        self.filepath = filepath
        self.line_budget = line_budget
        self.logger = logging.getLogger(__name__)

        # Ensure directory and file exist
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                f.write("# Agent Swarm Field Guide\n\n*Capture key learnings here.*\n")

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
                            "enum": ["read", "update"],
                            "description": "Whether to read the current guide or update it."
                        },
                        "content": {
                            "type": "string",
                            "description": "The new content to write to the guide. Required for 'update' action. Must be highly curated."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, content: str = None, **kwargs) -> str:
        if action == "read":
            return self._read_guide()
        elif action == "update":
            if not content:
                return "Error: 'content' must be provided for the 'update' action."
            return self._update_guide(content)
        return f"Error: Unknown action '{action}'"

    def _read_guide(self) -> str:
        try:
            with open(self.filepath, "r") as f:
                content = f.read()
            return f"--- FIELD GUIDE ({self.filepath}) ---\n{content}\n--- END FIELD GUIDE ---"
        except Exception as e:
            self.logger.error(f"Failed to read field guide: {e}")
            return f"Error reading field guide: {e}"

    def _update_guide(self, content: str) -> str:
        lines = content.split('\n')
        if len(lines) > self.line_budget:
            return (
                f"Error: Your content exceeds the strict {self.line_budget} line budget "
                f"(provided {len(lines)} lines). Please condense and summarize the most "
                "critical knowledge."
            )

        try:
            with open(self.filepath, "w") as f:
                f.write(content)
            return f"Successfully updated {self.filepath} ({len(lines)} lines)."
        except Exception as e:
            self.logger.error(f"Failed to write field guide: {e}")
            return f"Error writing field guide: {e}"
