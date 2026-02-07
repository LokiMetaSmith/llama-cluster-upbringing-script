import os
import logging
from typing import Dict, Any, List

class ContextUploadTool:
    """
    A tool that allows the user or agent to upload text content to the secure context sandbox.
    This enables the "Deep Context" workflow to access user-provided rulebooks or manuals.
    """
    def __init__(self, **kwargs):
        self.sandbox_dir = os.path.abspath("/tmp/pipecat_context")
        os.makedirs(self.sandbox_dir, exist_ok=True)

    async def execute(self, content: str, filename: str) -> str:
        """
        Saves the provided content to a file in the context sandbox.

        Args:
            content (str): The text content to save.
            filename (str): The name of the file (e.g., "rules.txt").

        Returns:
            str: A confirmation message with the file path.
        """
        if not filename or not content:
            return "Error: Both 'content' and 'filename' are required."

        # Sanitize filename
        safe_filename = os.path.basename(filename)
        full_path = os.path.join(self.sandbox_dir, safe_filename)

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            logging.info(f"Saved context file to {full_path}")
            return f"Successfully saved context to '{safe_filename}'. You can now use it in Deep Context mode."
        except Exception as e:
            logging.error(f"Failed to write context file: {e}")
            return f"Error saving file: {str(e)}"

    def get_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "upload_context",
                "description": "Uploads a text file (like a rulebook or manual) to the agent's context sandbox. Use this BEFORE starting a Deep Context task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The full text content of the file."
                        },
                        "filename": {
                            "type": "string",
                            "description": "The desired filename (e.g., 'game_rules.txt')."
                        }
                    },
                    "required": ["content", "filename"]
                }
            }
        }
