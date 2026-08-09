import logging
import aiohttp
import asyncio
import re

OUTPUT_RESERVE_CAP = 2000

# Global configuration for Model Tiers (Meta-Harness Pattern - Cost Lever #1)
MODEL_TIERS = {
    "high-reasoning": "gpt-4",
    "fast-worker": "gpt-3.5-turbo",
    "cheap-fallback": "claude-3-haiku"
}

class CostTracker:
    """Tracks token usage and estimates costs for LLM API calls."""
    def __init__(self):
        self.total_cost = 0.0
        self.usage_by_model = {}
        # Example rates per 1M tokens (input, output)
        self.rates = {
            "gpt-4": (30.0, 60.0),
            "gpt-3.5-turbo": (0.50, 1.50),
            "claude-3-opus": (15.0, 75.0),
            "claude-3-sonnet": (3.0, 15.0),
            "claude-3-haiku": (0.25, 1.25),
        }

    def record_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        if model not in self.usage_by_model:
            self.usage_by_model[model] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "estimated_cost": 0.0
            }

        self.usage_by_model[model]["prompt_tokens"] += prompt_tokens
        self.usage_by_model[model]["completion_tokens"] += completion_tokens
        self.usage_by_model[model]["total_tokens"] += (prompt_tokens + completion_tokens)

        cost = self._estimate_cost(model, prompt_tokens, completion_tokens)
        self.usage_by_model[model]["estimated_cost"] += cost
        self.total_cost += cost

    def _estimate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        # Default fallback to $1.0 input / $2.0 output per 1M if not found
        input_rate, output_rate = self.rates.get(model, (1.0, 2.0))
        return (prompt_tokens / 1_000_000) * input_rate + (completion_tokens / 1_000_000) * output_rate

    def get_summary(self):
        return {
            "total_cost": self.total_cost,
            "usage_by_model": self.usage_by_model
        }


global_cost_tracker = CostTracker()

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
        budget_limit (float, optional): The maximum allowed spend before downshifting or suspending.
        fallback_model (str, optional): The cheaper model to downshift to when budget_limit is reached.
        max_prompt_tokens (int, optional): Automatically compact the context if it exceeds this threshold.
        enable_dynamic_routing (bool, optional): If true, routes simple/short prompts to fallback_model automatically.
    """

    def __init__(self, base_url: str, api_key: str, model: str | None = None, budget_limit: float | None = None, fallback_model: str | None = None, max_prompt_tokens: int | None = None, enable_dynamic_routing: bool = False, tier: str | None = None):
        """Initializes the ExternalLLMClient.

        Args:
            base_url (str): The base URL for the API endpoint.
            api_key (str): The API key for authentication.
            model (str, optional): The name of the model to be used.
            budget_limit (float, optional): Optional maximum budget limit.
            fallback_model (str, optional): Optional model to downshift to if budget is exceeded.
            max_prompt_tokens (int, optional): Threshold for context compaction.
            enable_dynamic_routing (bool, optional): Enables task-level routing.
            tier (str, optional): The capability tier of the model to resolve to. Overrides `model`.
        """
        self.base_url = base_url
        self.api_key = api_key

        self.model = model
        if tier:
            if tier in MODEL_TIERS:
                self.model = MODEL_TIERS[tier]
                logging.info(f"Resolved tier '{tier}' to model '{self.model}'")
            else:
                logging.warning(f"Tier '{tier}' not found in MODEL_TIERS configuration. Falling back to default model.")
                self.model = model or "gpt-3.5-turbo"
        elif not model:
            self.model = "gpt-3.5-turbo" # Safe default if neither provided

        self.budget_limit = budget_limit
        self.fallback_model = fallback_model
        self.max_prompt_tokens = max_prompt_tokens
        self.enable_dynamic_routing = enable_dynamic_routing
        self._session = None

    def _compact_prompt(self, prompt: str) -> str:
        """Compacts the prompt if it exceeds the maximum token limit by truncating from the middle."""
        if not self.max_prompt_tokens:
            return prompt

        estimated_tokens = len(prompt) // 4
        if estimated_tokens <= self.max_prompt_tokens:
            return prompt

        logging.info(f"Compacting context: estimated tokens ({estimated_tokens}) exceeds max ({self.max_prompt_tokens})")

        # Simple truncation heuristic: keep first 40% and last 40%
        chars_allowed = self.max_prompt_tokens * 4
        half_chars = int(chars_allowed * 0.4)

        return prompt[:half_chars] + "\n...[Context automatically compacted]...\n" + prompt[-half_chars:]

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

        current_model = self.model
        prompt_to_send = self._compact_prompt(prompt)
        estimated_input_tokens = len(prompt_to_send) // 4

        # Dynamic Routing (Cost Lever #2)
        if self.enable_dynamic_routing and self.fallback_model:
            # Simple heuristic: if the prompt is very short/simple, route to the cheaper model
            if estimated_input_tokens < 150:
                logging.info(f"Dynamic routing triggered: prompt is simple ({estimated_input_tokens} tokens). Routing to {self.fallback_model}.")
                current_model = self.fallback_model

        # Budget Enforcement / Downshifting (Cost Lever #3)
        if self.budget_limit is not None and global_cost_tracker.total_cost >= self.budget_limit:
            if self.fallback_model:
                logging.warning(f"Budget limit ({self.budget_limit}) reached! Downshifting from {current_model} to {self.fallback_model}.")
                current_model = self.fallback_model
            else:
                logging.error(f"Budget limit ({self.budget_limit}) reached and no fallback model configured. Suspending requests.")
                return f"Error: Budget limit reached. Request suspended."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": current_model,
            "messages": [{"role": "user", "content": prompt_to_send}],
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

            usage = response_json.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)

            if prompt_tokens > 0 or completion_tokens > 0:
                global_cost_tracker.record_usage(current_model, prompt_tokens, completion_tokens)

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