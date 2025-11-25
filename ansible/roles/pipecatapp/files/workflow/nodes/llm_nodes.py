from .registry import registry
from ..node import Node
from ..context import WorkflowContext
from pipecat.services.openai.llm import OpenAILLMService
import os
import httpx

# This is a simplified version for now. We will need to make this more robust.
async def discover_main_llm_service():
    # In a real scenario, this would involve Consul discovery.
    # For now, we'll hardcode a default.
    return os.getenv("LLM_BASE_URL", "http://127.0.0.1:8081/v1")

@registry.register
class VisionLLMNode(Node):
    """A node that calls the main vision-capable LLM."""
    async def execute(self, context: WorkflowContext):
        messages = self.get_input(context, "messages")

        base_url = await discover_main_llm_service()
        chat_url = f"{base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        # We need a way to get the vision model name
        vision_model_name = os.getenv("VISION_MODEL_NAME", "llava-llama-3")
        payload = {"model": vision_model_name, "messages": messages, "max_tokens": 1024, "temperature": 0.7}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(chat_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"]
            self.set_output(context, "response_text", result)
        except (httpx.RequestError, KeyError, IndexError) as e:
            print(f"Error calling/parsing vision LLM: {e}")
            self.set_output(context, "response_text", "Error interacting with vision model.")

@registry.register
class PromptBuilderNode(Node):
    """A node that constructs the prompt for the LLM."""
    async def execute(self, context: WorkflowContext):
        system_prompt = self.get_input(context, "system_prompt")
        user_text = self.get_input(context, "user_text")
        screenshot = self.get_input(context, "screenshot")

        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [
                {"type": "text", "text": user_text},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot}"}}
            ]}
        ]
        self.set_output(context, "messages", messages)
