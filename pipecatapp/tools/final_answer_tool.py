class FinalAnswerTool:
    """A tool to signal that the task is completed."""

    def __init__(self):
        self.name = "final_answer"


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "finalanswertool"),
                "description": getattr(self, "description", "Tool FinalAnswerTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: submit_task"
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
        if action == "submit_task":
            return getattr(self, "submit_task")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"

    def submit_task(self, summary: str):
        """
        Call this tool when you have completed the user's request.

        Args:
            summary (str): A detailed summary of what was done and the final result.
        """
        return f"Task submitted with summary: {summary}"
