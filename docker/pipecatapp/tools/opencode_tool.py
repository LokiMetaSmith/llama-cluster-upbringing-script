import os
import asyncio
import logging
from opencode_ai import AsyncOpencode

class OpencodeTool:
    """A tool for using the OpenCode coding agent.

    This class interfaces with the OpenCode server to perform complex coding tasks.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self, base_url: str = None, provider_id: str = "openai", model_id: str = "gpt-4o"):
        """Initializes the OpencodeTool.

        Args:
            base_url (str): The base URL of the OpenCode server.
            provider_id (str): The AI provider ID (e.g., "openai", "anthropic").
            model_id (str): The model ID (e.g., "gpt-4o", "claude-3-5-sonnet").
        """
        self.description = "Delegate complex coding tasks to the OpenCode agent."
        self.name = "opencode"
        self.base_url = base_url or os.getenv("OPENCODE_API_URL")
        self.provider_id = provider_id
        self.model_id = model_id

    async def run(self, task: str) -> str:
        """Runs a coding task using the OpenCode agent.

        Args:
            task (str): The task description.

        Returns:
            str: The result of the task execution.
        """
        if not self.base_url:
             return "Error: OpenCode server URL not configured."

        try:
            client = AsyncOpencode(base_url=self.base_url)

            # Create a session
            session = await client.session.create()
            session_id = session.id
            logging.info(f"Created OpenCode session: {session_id}")

            part = {"type": "text", "text": task}

            response = await client.session.chat(
                id=session_id,
                parts=[part],
                provider_id=self.provider_id,
                model_id=self.model_id
            )

            return f"OpenCode Agent Task '{task}' initiated. Session ID: {session_id}. Response: {response}"

        except Exception as e:
            logging.error(f"Error running OpenCode task: {e}")
            return f"Error executing OpenCode task: {e}"
