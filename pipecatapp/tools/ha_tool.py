import os
import aiohttp
import logging

class HA_Tool:
    """A tool for interacting with a Home Assistant instance.

    This tool provides a method to send natural language commands to Home
    Assistant's `ai_task` service, allowing the agent to control smart home
    devices and query their state.

    Attributes:
        ha_url (str): The base URL of the Home Assistant instance.
        ha_token (str): A long-lived access token for Home Assistant.
        headers (dict): A dictionary of HTTP headers for API requests.
    """
    def __init__(self, ha_url=None, ha_token=None):
        """Initializes the Home Assistant tool.

        Args:
            ha_url (str, optional): The URL for the Home Assistant API.
                Defaults to the value of the HA_URL environment variable.
            ha_token (str, optional): The long-lived access token.
                Defaults to the value of the HA_TOKEN environment variable.

        Raises:
            ValueError: If the Home Assistant URL or token is not provided.
        """
        self.ha_url = ha_url or os.getenv("HA_URL")
        self.ha_token = ha_token or os.getenv("HA_TOKEN")
        if not self.ha_url or not self.ha_token:
            raise ValueError("Home Assistant URL and Token must be provided.")
        self.headers = {
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json",
        }
        self._session = None


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "ha_tool"),
                "description": getattr(self, "description", "Tool HA_Tool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: close, call_ai_task"
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
        if action == "close":
            return getattr(self, "close")(**kwargs.get("kwargs", kwargs))
        if action == "call_ai_task":
            return getattr(self, "call_ai_task")(**kwargs.get("kwargs", kwargs))
        else:
            return f"Unknown action: {action}"

    async def close(self):
        """Closes the underlying aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None

    def _get_session(self) -> aiohttp.ClientSession:
        if not self._session:
            self._session = aiohttp.ClientSession()
        return self._session

    async def call_ai_task(self, instructions: str) -> str:
        """Calls the Home Assistant 'ai_task.generate_data' service.

        This method sends natural language instructions to Home Assistant,
        enabling control over smart devices and retrieval of information.
        For example: 'Turn on the living room light' or 'What is the
        temperature in the bedroom?'

        Args:
            instructions (str): The natural language command to send.

        Returns:
            str: A confirmation message on success, or an error message.
        """
        if not instructions:
            return "Error: Instructions cannot be empty."

        logging.info(f"Calling Home Assistant with instructions: {instructions}")

        api_url = f"{self.ha_url}/api/services/ai_task/generate_data"
        payload = {
            "task_name": "pipecat_llm_request",
            "instructions": instructions,
        }

        session = self._get_session()
        try:
            async with session.post(api_url, headers=self.headers, json=payload, timeout=10) as response:
                response.raise_for_status()
                # The actual response from the service call is not the primary result.
                # The result is the state change in Home Assistant.
                # We will return a confirmation message.
                logging.info(f"Home Assistant API call successful. Status code: {response.status}")
                return f"Successfully sent command to Home Assistant: '{instructions}'"
        except Exception as e:
            logging.error(f"Error calling Home Assistant API: {e}")
            return f"Error calling Home Assistant API: {e}"
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}"