from .registry import registry
from ..node import Node
from ..context import WorkflowContext
from pipecat.services.openai.llm import OpenAILLMService
import os
import httpx
import asyncio
import re

try:
    from ...secret_manager import secret_manager
except ImportError:
    from secret_manager import secret_manager

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
    """A simple LLM node with configurable model tiers and Ensembling support."""
    async def execute(self, context: WorkflowContext):
        # 1. Gather Inputs
        messages = None
        # Check if 'messages' is a configured input
        if any(i["name"] == "messages" for i in self.config.get("inputs", [])):
             messages = self.get_input(context, "messages")

        if not messages:
            # Fallback to constructing messages from user_text or other inputs
            user_text = ""
            if any(i["name"] == "user_text" for i in self.config.get("inputs", [])):
                 user_text = self.get_input(context, "user_text") or ""

            # Aggregate other inputs (e.g. reports)
            for input_config in self.config.get("inputs", []):
                 name = input_config["name"]
                 if name not in ["messages", "user_text", "reasoning"]:
                     val = self.get_input(context, name)
                     if val:
                         user_text += f"\n\n{name.replace('_', ' ').title()}:\n{val}"

            if not user_text:
                user_text = "Hello"

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
            target_service = "rpc-router"
        elif tier == "capable":
            # CodeLlama or similar high-end
            target_service = "rpc-coding"
        else: # balanced / default
            # Llama-3-8B is the main expert
            target_service = "rpc-main"

        response_text = f"Error: Could not reach {tier} service."

        # 3. Call Service
        if consul_http_addr:
            try:
                token = secret_manager.get_secret("CONSUL_HTTP_TOKEN")
                headers = {"X-Consul-Token": token} if token else {}
                async with httpx.AsyncClient(headers=headers) as client:
                    # Discovery
                    response = await client.get(f"{consul_http_addr}/v1/health/service/{target_service}?passing")
                    response.raise_for_status()
                    services = response.json()

                    if services:
                        address = services[0]['Service']['Address']
                        port = services[0]['Service']['Port']
                        base_url = f"http://{address}:{port}/v1"
                        chat_url = f"{base_url}/chat/completions"

                        # CHECK FOR ENSEMBLING
                        ensemble_size = self.config.get("ensemble_size", 1)
                        # Also allow overriding from input
                        if any(i["name"] == "ensemble_size" for i in self.config.get("inputs", [])):
                             input_size = self.get_input(context, "ensemble_size")
                             if input_size:
                                 ensemble_size = int(input_size)

                        payload = {
                            "model": target_service,
                            "messages": messages,
                            "temperature": 0.7
                        }

                        # Check for reasoning config
                        reasoning_config = None
                        if any(i["name"] == "reasoning" for i in self.config.get("inputs", [])):
                            reasoning_config = self.get_input(context, "reasoning")
                        reasoning_config = reasoning_config or self.config.get("reasoning")

                        if reasoning_config:
                            payload["reasoning"] = reasoning_config

                        if ensemble_size <= 1:
                            # Standard Single Execution
                            llm_res = await client.post(chat_url, json=payload, timeout=120)
                            llm_res.raise_for_status()
                            response_data = llm_res.json()
                            response_text = response_data["choices"][0]["message"]["content"]

                            reasoning_details = response_data["choices"][0]["message"].get("reasoning_details") or \
                                                response_data["choices"][0]["message"].get("reasoning")
                            if reasoning_details:
                                 self.set_output(context, "reasoning_details", reasoning_details)
                        else:
                            # ENSEMBLE EXECUTION (Best-of-N)
                            tasks = []
                            for i in range(ensemble_size):
                                # Vary temperature slightly if needed, or rely on inherent stochasticity
                                # Here we keep it simple or slightly boost temp for variety
                                p = payload.copy()
                                if i > 0:
                                    p["temperature"] = 0.8 # Slightly higher for candidates

                                tasks.append(client.post(chat_url, json=p, timeout=120))

                            results = await asyncio.gather(*tasks, return_exceptions=True)
                            candidates = []
                            for r in results:
                                if isinstance(r, httpx.Response) and r.status_code == 200:
                                    candidates.append(r.json()["choices"][0]["message"]["content"])

                            if not candidates:
                                response_text = "Error: All ensemble calls failed."
                            elif len(candidates) == 1:
                                response_text = candidates[0]
                            else:
                                # SELECT BEST CANDIDATE
                                # We ask the same model (or a fast one) to pick the best.
                                # Using the same model for simplicity.
                                selection_prompt = "Select the most coherent, complete, and correct response from the following options. Respond ONLY with the index number (e.g., 0, 1, 2).\n\n"
                                for idx, cand in enumerate(candidates):
                                    selection_prompt += f"--- Option {idx} ---\n{cand}\n\n"

                                sel_payload = {
                                    "model": target_service,
                                    "messages": [{"role": "user", "content": selection_prompt}],
                                    "temperature": 0.0
                                }
                                sel_res = await client.post(chat_url, json=sel_payload, timeout=60)
                                if sel_res.status_code == 200:
                                    sel_text = sel_res.json()["choices"][0]["message"]["content"]
                                    match = re.search(r"\d+", sel_text)
                                    if match:
                                        best_idx = int(match.group(0))
                                        if 0 <= best_idx < len(candidates):
                                            response_text = candidates[best_idx]
                                        else:
                                            response_text = candidates[0]
                                    else:
                                        response_text = candidates[0]
                                else:
                                    response_text = candidates[0]

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

        service_name = f"rpc-{expert_name}"
        expert_response = f"Could not find or contact expert service: {expert_name}"

        try:
            token = secret_manager.get_secret("CONSUL_HTTP_TOKEN")
            headers = {"X-Consul-Token": token} if token else {}
            async with httpx.AsyncClient(headers=headers) as client:
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

@registry.register
class ExternalLLMNode(Node):
    """A node that calls an external LLM service directly (e.g., OpenRouter, OpenAI)."""
    async def execute(self, context: WorkflowContext):
        expert_id = self.config.get("expert_id")
        raw_input = self.get_input(context, "messages")
        external_experts_config = context.global_inputs.get("external_experts_config", {})

        # Construct messages payload
        messages = []

        # 1. Add System Prompt from Config
        system_prompt = self.config.get("system_prompt")
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # 2. Handle Input
        if isinstance(raw_input, str):
            messages.append({"role": "user", "content": raw_input})
        elif isinstance(raw_input, list):
            messages.extend(raw_input)
        else:
            # Fallback for unexpected types
            messages.append({"role": "user", "content": str(raw_input)})

        if not expert_id:
             self.set_output(context, "response", "Error: expert_id is required in node config.")
             return

        if expert_id not in external_experts_config:
             self.set_output(context, "response", f"Error: Expert '{expert_id}' not found in external configuration.")
             return

        expert_config = external_experts_config[expert_id]
        base_url = expert_config.get("base_url")
        api_key_env = expert_config.get("api_key_env")
        model = expert_config.get("model")

        api_key = secret_manager.get_secret(api_key_env)
        if not api_key:
             self.set_output(context, "response", f"Error: API key environment variable '{api_key_env}' not found in SecretManager.")
             return

        # Prepare payload
        payload = {
            "model": model,
            "messages": messages,
            "temperature": self.config.get("temperature", 0.7)
        }

        # Support reasoning parameters if provided in input
        reasoning_config = self.get_input(context, "reasoning")
        if reasoning_config:
             payload["reasoning"] = reasoning_config

        chat_url = f"{base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # OpenRouter specific headers
        if "openrouter.ai" in base_url:
             headers["HTTP-Referer"] = "https://pipecat-agent.internal"
             headers["X-Title"] = "Pipecat Agent"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(chat_url, headers=headers, json=payload, timeout=120)
                response.raise_for_status()
                response_data = response.json()
                result = response_data["choices"][0]["message"]["content"]

                # Check for reasoning details
                reasoning_details = response_data["choices"][0]["message"].get("reasoning_details") or \
                                    response_data["choices"][0]["message"].get("reasoning")
                if reasoning_details:
                     self.set_output(context, "reasoning_details", reasoning_details)

                self.set_output(context, "response", result)

        except Exception as e:
            print(f"Error calling external expert {expert_id}: {e}")
            self.set_output(context, "response", f"Error calling external expert: {e}")
@registry.register
class LLMRouterNode(Node):
    """
    Routes a query to the best available expert using LLMRouter.
    """
    async def execute(self, context: WorkflowContext):
        query = self.get_input(context, "user_text")

        # NOTE: This implementation assumes LLMRouter is installed and configured.
        # Since we are in a proof-of-concept phase, we might need to mock or
        # configure it dynamically.

        try:
            from llmrouter import LLMRouter

            # TODO: Load a real routing config or trained model here.
            # For the PoC, we might use a simple rule-based or zero-shot router if supported,
            # or just a mock if the library requires training data we don't have yet.
            #
            # Ideally, the router is initialized once at startup, not per-request.
            # But for now, we'll keep it self-contained or use a singleton pattern if available.

            # Mocking the router behavior for now until we have training data/config
            # mapped to our local services.
            # In a real scenario:
            # router = LLMRouter(config_path="...")
            # route = router.route(query)
            # selected_model = route.model_name

            # Simple heuristic fallback (PoC logic) mimicking what a router might do
            if "code" in query.lower() or "python" in query.lower() or "function" in query.lower():
                selected_model = "qwen2.5-coder"
            elif "vision" in query.lower() or "see" in query.lower() or "image" in query.lower():
                selected_model = "llava-llama-3"
            else:
                selected_model = "llama-3-8b"

            # Map selected model to Consul service
            service_mapper = {
                "qwen2.5-coder": "rpc-coding",
                "llava-llama-3": "rpc-vision", # Hypothetical
                "llama-3-8b": "rpc-main",
                "phi-3": "rpc-router"
            }

            service_name = service_mapper.get(selected_model, "rpc-main")

            # Reusing logic similar to SimpleLLMNode to call the service
            consul_http_addr = context.global_inputs.get("consul_http_addr")
            response_text = f"Error: Could not reach {service_name}."

            if consul_http_addr:
                token = secret_manager.get_secret("CONSUL_HTTP_TOKEN")
                headers = {"X-Consul-Token": token} if token else {}
                async with httpx.AsyncClient(headers=headers) as client:
                    response = await client.get(f"{consul_http_addr}/v1/health/service/{service_name}?passing")
                    response.raise_for_status()
                    services = response.json()

                    if services:
                        address = services[0]['Service']['Address']
                        port = services[0]['Service']['Port']
                        base_url = f"http://{address}:{port}/v1"

                        payload = {
                            "model": service_name,
                            "messages": [{"role": "user", "content": query}],
                            "temperature": 0.7
                        }

                        chat_url = f"{base_url}/chat/completions"
                        llm_res = await client.post(chat_url, json=payload, timeout=120)
                        llm_res.raise_for_status()
                        response_text = llm_res.json()["choices"][0]["message"]["content"]
                    else:
                        response_text = f"Error: Service {service_name} (mapped from {selected_model}) not found."

        except ImportError:
            response_text = "Error: LLMRouter library not installed."
        except Exception as e:
            print(f"Error in LLMRouterNode: {e}")
            response_text = f"Error routing query: {e}"

        self.set_output(context, "response", response_text)
