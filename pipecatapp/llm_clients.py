import logging
import requests

class ExternalLLMClient:
    """A generic client for interacting with OpenAI-compatible LLM APIs.

    This class provides a standardized way to send prompts to external LLM
    services and retrieve their responses. It is designed to be flexible
    and can be configured for any API that follows the standard chat
    completions format.

    Attributes:
        base_url (str): The base URL of the LLM API (e.g., "https://api.openai.com/v1").
        api_key (str): The API key for authentication.
        model (str): The specific model to use for the completion (e.g., "gpt-4").
    """

    def __init__(self, base_url: str, api_key: str, model: str):
        """Initializes the ExternalLLMClient.

        Args:
            base_url (str): The base URL for the API endpoint.
            api_key (str): The API key for authentication.
            model (str): The name of the model to be used.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

    async def process_text(self, prompt: str) -> str:
        """Sends a prompt to the external LLM and returns the response.

        This method makes a POST request to the chat completions endpoint of the
        configured API.

        Args:
            prompt (str): The user prompt to send to the LLM.

        Returns:
            str: The text content of the LLM's response, or an error message
                 if the request fails.
        """
        if not self.api_key:
            logging.error(f"API key is missing for expert {self.model}. Cannot make request.")
            return f"Error: API key not configured for model {self.model}."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            # Note: The 'requests' library is synchronous.
            # For a fully async application, 'aiohttp' would be a better choice,
            # but for simplicity and compatibility with the existing codebase,
            # we will use 'requests' here. Pipecat can handle running this
            # synchronous code in a separate thread.
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
            response.raise_for_status()

            response_json = response.json()
            content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content.strip()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error calling external LLM API for model {self.model}: {e}")
            return f"Error: Could not connect to the external model {self.model}."
        except (KeyError, IndexError) as e:
            logging.error(f"Error parsing response from LLM API for model {self.model}: {e}")
            return f"Error: Invalid response from the external model {self.model}."