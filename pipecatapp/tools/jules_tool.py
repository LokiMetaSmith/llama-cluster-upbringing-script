import os
import logging
import httpx

class JulesTool:
    """A tool for using the Jules REST API to create coding sessions.

    This class interfaces with the Jules API to automate tasks like bug fixing
    when a crash is detected.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self, api_key: str = None):
        """Initializes the JulesTool.

        Args:
            api_key (str): The Jules API Key. Defaults to JULES_API_KEY env var.
        """
        self.description = "Delegate tasks and report crashes to the Jules autonomous AI coding agent."
        self.name = "jules"
        self.api_key = api_key or os.getenv("JULES_API_KEY")
        self.base_url = "https://jules.googleapis.com/v1alpha"
        self.input_schema = {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The task description or crash logs to delegate to Jules."
                },
                "source": {
                    "type": "string",
                    "description": "The source repository context (e.g., 'sources/github/bobalover/boba')."
                },
                "title": {
                    "type": "string",
                    "description": "Optional title for the autonomous coding session."
                },
                "automation_mode": {
                    "type": "string",
                    "description": "Optional automation mode (e.g., 'AUTO_CREATE_PR')."
                }
            },
            "required": ["prompt", "source"]
        }

    async def run(self, prompt: str, source: str, title: str = None, automation_mode: str = None) -> str:
        """Runs a task using the Jules agent by creating a new session.

        Args:
            prompt (str): The task description or crash logs.
            source (str): The source context (e.g., 'sources/github/bobalover/boba').
            title (str, optional): The title for the session.
            automation_mode (str, optional): Automation mode (e.g., 'AUTO_CREATE_PR').

        Returns:
            str: The result of the task execution (session details or error).
        """
        if not self.api_key:
             return "Error: JULES_API_KEY not configured."

        url = f"{self.base_url}/sessions"

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        payload = {
            "prompt": prompt,
            "sourceContext": {
                "source": source
            }
        }

        if title:
            payload["title"] = title

        if automation_mode:
            payload["automationMode"] = automation_mode

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()

                data = response.json()
                session_name = data.get("name")
                session_id = data.get("id")

                logging.info(f"Created Jules session: {session_id}")
                return f"Jules session created successfully. Session ID: {session_id}. Session Name: {session_name}"

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error creating Jules session: {e.response.text}")
            return f"Error creating Jules session: HTTP {e.response.status_code} - {e.response.text}"
        except Exception as e:
            logging.error(f"Error executing Jules task: {e}")
            return f"Error executing Jules task: {e}"
