class MCP_Tool:
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.description = "Master Control Program for agent introspection and self-control."
        self.name = "mcp_tool"

    def get_status(self):
        """Returns the current status of the agent's pipelines."""
        # This is a placeholder. A real implementation would query the runner.
        return "All systems nominal. Main, Vision, and Interrupt pipelines are active."

    def get_memory_summary(self):
        """Returns a summary of the agent's memory."""
        short_term = len(self.twin_service.short_term_memory)
        long_term = self.twin_service.long_term_memory.index.ntotal
        return f"Short-term memory contains {short_term} turns. Long-term memory contains {long_term} entries."

    def clear_short_term_memory(self):
        """Clears the agent's short-term conversational memory."""
        self.twin_service.short_term_memory.clear()
        return "Short-term memory cleared."
