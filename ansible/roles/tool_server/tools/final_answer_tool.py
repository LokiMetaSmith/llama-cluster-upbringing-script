class FinalAnswerTool:
    """A tool to signal that the task is completed."""

    def __init__(self):
        self.name = "final_answer"

    def submit_task(self, summary: str):
        """
        Call this tool when you have completed the user's request.

        Args:
            summary (str): A detailed summary of what was done and the final result.
        """
        return f"Task submitted with summary: {summary}"
