class MCP_Tool:
    def __init__(self, twin_service, runner):
        self.twin_service = twin_service
        self.runner = runner
        self.description = "Master Control Program for agent introspection and self-control."
        self.name = "mcp_tool"

    def get_status(self):
        """Returns the current status of the agent's running pipelines."""
        if not self.runner:
            return "Error: PipelineRunner not available."

        tasks = self.runner.get_tasks()
        if not tasks:
            return "No active pipelines."

        status_report = "Current pipeline status:\n"
        for task in tasks:
            status_report += f"- Task {task.get_name()}: {task.get_state().value}\n"

        return status_report

    def get_memory_summary(self):
        """Returns a summary of the agent's memory."""
        short_term = len(self.twin_service.short_term_memory)
        long_term = self.twin_service.long_term_memory.index.ntotal
        return f"Short-term memory contains {short_term} turns. Long-term memory contains {long_term} entries."

    def clear_short_term_memory(self):
        """Clears the agent's short-term conversational memory."""
        self.twin_service.short_term_memory.clear()
        return "Short-term memory cleared."
