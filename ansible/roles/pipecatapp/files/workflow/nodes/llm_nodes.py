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
        tool_result = self.get_input(context, "tool_result")

        # In a real implementation, we would manage a persistent message history.
        # For now, we'll just build it fresh on each turn.
        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [
                {"type": "text", "text": user_text},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot}"}}
            ]}
        ]

        if tool_result:
            messages.append({"role": "tool", "content": [{"type": "text", "text": tool_result}]})

        self.set_output(context, "messages", messages)

@registry.register
class SimpleLLMNode(Node):
    """A simple LLM node with configurable model tiers."""
    async def execute(self, context: WorkflowContext):
        # 1. Gather Inputs
        messages = self.get_input(context, "messages")
        if not messages:
            # Fallback to constructing messages from user_text if raw messages aren't provided
            user_text = self.get_input(context, "user_text") or "Hello"
            system_prompt = self.config.get("system_prompt", "You are a helpful assistant.")
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ]

        # 2. Determine Service based on Tier
        tier = self.config.get("model_tier", "balanced")
        consul_http_addr = context.global_inputs.get("consul_http_addr")

        # Mapping logic (simplified for now, ideally strictly matches Consul service names)
        if tier == "fast":
            # Phi-3 is usually the 'fast' or 'router' expert
            target_service = "llamacpp-rpc-router"
        elif tier == "capable":
            # CodeLlama or similar high-end
            target_service = "llamacpp-rpc-coding"
        else: # balanced / default
            # Llama-3-8B is the main expert
            target_service = "llamacpp-rpc-main"

        response_text = f"Error: Could not reach {tier} service."

        # 3. Call Service
        if consul_http_addr:
            try:
                async with httpx.AsyncClient() as client:
                    # Discovery
                    response = await client.get(f"{consul_http_addr}/v1/health/service/{target_service}?passing")
                    response.raise_for_status()
                    services = response.json()

                    if services:
                        address = services[0]['Service']['Address']
                        port = services[0]['Service']['Port']
                        base_url = f"http://{address}:{port}/v1"

                        # Call Chat Completion
                        payload = {
                            "model": target_service, # Model name often ignored by llama.cpp rpc, but good practice
                            "messages": messages,
                            "temperature": 0.7
                        }

                        # Check for reasoning config in input or self.config
                        reasoning_config = self.get_input(context, "reasoning") or self.config.get("reasoning")
                        if reasoning_config:
                            # Standard OpenRouter/OpenAI 'reasoning' parameter or 'extra_body'
                            # Some backends expect it in 'extra_body', others top-level (OpenRouter unified)
                            # We'll put it top-level as per OpenRouter docs for direct API calls,
                            # but some libraries wrap it. Since we are using raw httpx, top-level is correct for OpenRouter.
                            # However, standard OpenAI API puts it in extra_body or specialized fields.
                            # If we are calling OpenRouter directly, top-level `reasoning` is fine.
                            # If we are calling a local llama-server that mimics OpenAI, it might just ignore it or
                            # support it if it's a newer version.
                            # Let's support both by injecting it into the payload.
                            payload["reasoning"] = reasoning_config

                        chat_url = f"{base_url}/chat/completions"
                        llm_res = await client.post(chat_url, json=payload, timeout=120)
                        llm_res.raise_for_status()
                        response_data = llm_res.json()
                        response_text = response_data["choices"][0]["message"]["content"]

                        # Preserve reasoning details if present, for future turns (though SimpleLLMNode is usually one-off)
                        # We could store it in context if needed.
                        reasoning_details = response_data["choices"][0]["message"].get("reasoning_details") or \
                                            response_data["choices"][0]["message"].get("reasoning")
                        if reasoning_details:
                             self.set_output(context, "reasoning_details", reasoning_details)

                    else:
                         response_text = f"Error: Service {target_service} not found in Consul."

            except Exception as e:
                print(f"Error in SimpleLLMNode ({tier}): {e}")
                response_text = f"Error interacting with {tier} model: {e}"

        self.set_output(context, "response", response_text)

@registry.register
class ExpertRouterNode(Node):
    """A node that routes a query to a specific expert LLM service."""
    async def execute(self, context: WorkflowContext):
        expert_name = self.get_input(context, "expert_name")
        query = self.get_input(context, "query")
        consul_http_addr = context.global_inputs.get("consul_http_addr")

        if not expert_name or not query or not consul_http_addr:
            self.set_output(context, "expert_response", "Error: expert_name, query, and consul_http_addr are required.")
            return

        service_name = f"llamacpp-rpc-{expert_name}"
        expert_response = f"Could not find or contact expert service: {expert_name}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{consul_http_addr}/v1/health/service/{service_name}?passing")
                response.raise_for_status()
                services = response.json()

                if services:
                    address = services[0]['Service']['Address']
                    port = services[0]['Service']['Port']
                    base_url = f"http://{address}:{port}/v1"

                    # We need a way to get the system prompt for the expert
                    # For now, we'll just send the query.
                    payload = {"model": expert_name, "messages": [{"role": "user", "content": query}]}

                    # Check for reasoning config
                    reasoning_config = self.get_input(context, "reasoning") or self.config.get("reasoning")
                    if reasoning_config:
                        payload["reasoning"] = reasoning_config

                    chat_url = f"{base_url}/chat/completions"

                    expert_res = await client.post(chat_url, json=payload, timeout=120)
                    expert_res.raise_for_status()
                    expert_data = expert_res.json()
                    expert_response = expert_data["choices"][0]["message"]["content"]

                    reasoning_details = expert_data["choices"][0]["message"].get("reasoning_details") or \
                                        expert_data["choices"][0]["message"].get("reasoning")
                    if reasoning_details:
                        self.set_output(context, "reasoning_details", reasoning_details)

        except (httpx.RequestError, KeyError, IndexError) as e:
            print(f"Error routing to expert {expert_name}: {e}")

        self.set_output(context, "expert_response", expert_response)
