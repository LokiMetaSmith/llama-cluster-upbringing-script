import logging
import aiohttp
import asyncio
import re

OUTPUT_RESERVE_CAP = 2000

def clamp_output_tokens(requested_max_tokens: int | None) -> int:
    """Clamps pre-flight output token estimation to prevent bogus rate limit exclusions."""
    requested = requested_max_tokens if (requested_max_tokens is not None and requested_max_tokens > 0) else 1000
    return min(requested, OUTPUT_RESERVE_CAP)

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
        self._session = None

    def estimate_request_tokens(self, prompt: str, requested_max_tokens: int | None = None) -> int:
        """Estimates total request tokens (input + clamped output reserve) for pre-flight routing validation."""
        # Simple heuristic: 4 characters per token
        input_tokens = len(prompt) // 4
        clamped_output = clamp_output_tokens(requested_max_tokens)
        return input_tokens + clamped_output

    async def close(self):
        """Closes the underlying aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None

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
            if not self._session:
                # Note: Using aiohttp.ClientSession for asynchronous I/O.
                # This prevents blocking the event loop during network requests.
                self._session = aiohttp.ClientSession()

            # Optional: integration with local OneCLI-like proxy
            import os
            proxy_url = os.environ.get("ONECLI_PROXY_URL")
            target_endpoint = f"{self.base_url}/chat/completions"

            if proxy_url:
                headers["X-Target-Url"] = target_endpoint
                request_url = proxy_url
            else:
                request_url = target_endpoint

            async with self._session.post(
                request_url,
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                response.raise_for_status()
                response_json = await response.json()

            content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            # DwarfStar (ds4) might include <think> blocks in the content depending on the model/mode.
            # We strip them for standard process_text if they are present.
            if "<think>" in content and "</think>" in content:
                content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)

            return content.strip()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"Error calling external LLM API for model {self.model}: {e}")
            return f"Error: Could not connect to the external model {self.model}."
        except (KeyError, IndexError) as e:
            logging.error(f"Error parsing response from LLM API for model {self.model}: {e}")
            return f"Error: Invalid response from the external model {self.model}."