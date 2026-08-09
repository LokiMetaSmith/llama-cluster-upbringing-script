import json
import logging
import os
import re
from typing import Any, Optional

logger = logging.getLogger("HolographicMemoryTool")

class HolographicMemoryTool:
    """
    Saves and recalls structurally encoded 'holographic' memory (activation matrices)
    from the emulated physical substrate.
    """

    name = "holographic_memory"
    description = "Saves, recalls, or freezes structurally encoded 'holographic' memory states (activation matrices) representing complex, pre-optimized branched flows for continual learning."

    input_schema = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "The action to perform: 'save', 'recall', 'freeze', or 'search'."
            },
            "matrix_name": {
                "type": "string",
                "description": "A unique identifier for the activation matrix."
            },
            "matrix_data": {
                "type": "object",
                "description": "The activation matrix data to save (required for 'save' and 'freeze')."
            },
            "context_description": {
                "type": "string",
                "description": "A brief description of what this structural memory solves."
            }
        },
        "required": ["action"]
    }

    def __init__(self, memory_dir: str = "holographic_memory"):
        self.memory_dir = memory_dir
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir, exist_ok=True)

    def _sanitize_name(self, name: str) -> str:
        """Sanitizes the matrix name to prevent directory traversal."""
        # Only allow alphanumeric characters, dashes, and underscores
        return re.sub(r'[^a-zA-Z0-9_-]', '', name)

    def run(self, action: str, matrix_name: str = "", matrix_data: Optional[dict] = None, context_description: Optional[str] = None) -> Any:
        try:
            if action == "search":
                if not context_description:
                    return "Error: 'context_description' is required as the query for the 'search' action."

                results = []
                query = context_description.lower()
                for filename in os.listdir(self.memory_dir):
                    if filename.endswith(".json"):
                        with open(os.path.join(self.memory_dir, filename), "r") as mf:
                            try:
                                data = json.load(mf)
                                desc = data.get("context_description", "").lower()
                                if query in desc or desc in query:
                                    results.append(data.get("matrix_name"))
                            except json.JSONDecodeError:
                                continue

                if not results:
                    return f"No holographic memory found matching query '{context_description}'."
                return f"Found {len(results)} matching memories: {', '.join(results)}"

            safe_name = self._sanitize_name(matrix_name)
            if not safe_name:
                return "Error: Invalid matrix_name provided."

            file_path = os.path.join(self.memory_dir, f"{safe_name}.json")

            if action in ["save", "freeze"]:
                if not matrix_data:
                    return f"Error: 'matrix_data' is required for the '{action}' action."

                payload = {
                    "matrix_name": safe_name,
                    "context_description": context_description or "No description provided.",
                    "status": action,
                    "matrix_data": matrix_data
                }

                with open(file_path, "w") as f:
                    json.dump(payload, f, indent=2)

                logger.info(f"Holographic memory '{safe_name}' {action}d successfully.")
                return f"Successfully {action}d holographic memory '{safe_name}'."

            elif action == "recall":
                if not os.path.exists(file_path):
                    return f"Error: Holographic memory '{safe_name}' not found."

                with open(file_path, "r") as f:
                    data = json.load(f)

                logger.info(f"Holographic memory '{safe_name}' recalled successfully.")
                return f"Recalled Holographic Memory:\n{json.dumps(data, indent=2)}"

            else:
                return f"Error: Unknown action '{action}'."

        except Exception as e:
            logger.error(f"Error in HolographicMemoryTool: {e}")
            return f"Error processing holographic memory: {str(e)}"
