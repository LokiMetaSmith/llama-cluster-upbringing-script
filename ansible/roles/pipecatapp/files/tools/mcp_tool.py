class MCP_Tool:
    """Master Control Program for agent introspection and self-control.

    This tool provides methods for the agent to inspect its own state, such
    as the status of its processing pipelines and the contents of its memory.

    Attributes:
        twin_service: A reference to the main TwinService instance.
        runner: A reference to the PipelineRunner instance.
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self, twin_service, runner):
        """Initializes the MCP_Tool.

        Args:
            twin_service: The instance of the main TwinService.
            runner: The instance of the PipelineRunner managing the agent's tasks.
        """
        self.twin_service = twin_service
        self.runner = runner
        self.description = "Master Control Program for agent introspection and self-control."
        self.name = "mcp_tool"

    def get_status(self) -> str:
        """Returns the current status of the agent's running pipelines.

        Returns:
            str: A formatted string reporting the status of each active pipeline task.
        """
        if not self.runner:
            return "Error: PipelineRunner not available."

        tasks = self.runner.get_tasks()
        if not tasks:
            return "No active pipelines."

        status_report = "Current pipeline status:\n"
        for task in tasks:
            status_report += f"- Task {task.get_name()}: {task.get_state().value}\n"

        return status_report

    def get_memory_summary(self) -> str:
        """Returns a summary of the agent's memory.

        Provides counts of items in both short-term (conversational) and
        long-term (vector store) memory.

        Returns:
            str: A string summarizing the memory contents.
        """
        short_term = len(self.twin_service.short_term_memory)
        long_term = self.twin_service.long_term_memory.index.ntotal
        return f"Short-term memory contains {short_term} turns. Long-term memory contains {long_term} entries."

    def clear_short_term_memory(self) -> str:
        """Clears the agent's short-term conversational memory.

        Returns:
            str: A confirmation message that the memory has been cleared.
        """
        self.twin_service.short_term_memory.clear()
        return "Short-term memory cleared."
