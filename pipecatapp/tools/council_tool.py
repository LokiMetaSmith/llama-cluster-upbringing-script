import asyncio
import json
import os
import logging
import aiohttp
from typing import List, Dict, Any, Optional
from pipecatapp.net_utils import format_url

class CouncilTool:
    """A tool to convene a council of AI experts (both local and external) to deliberate on a query."""

    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.name = "council"
        self.description = "Convenes a council of experts to provide a comprehensive, multi-perspective answer. Useful for complex queries requiring diverse viewpoints."
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        # Hardcoded list of council models if openrouter is available
        self.openrouter_models = [
            "openai/gpt-4-turbo",
            "anthropic/claude-3-opus",
            "google/gemini-pro-1.5"
        ] if self.openrouter_api_key else []

    async def _discover_local_experts(self) -> Dict[str, str]:
        """Discovers available local expert services via Consul."""
        experts = {}
        # Known expert names from group_vars/all.yaml
        known_experts = ["main", "coding", "math", "extract"]

        consul_url = self.twin_service.consul_http_addr

        # Use aiohttp for async discovery
        try:
            async with aiohttp.ClientSession() as session:
                for expert_name in known_experts:
                    service_name = f"expert-api-{expert_name}"
                    try:
                        async with session.get(f"{consul_url}/v1/health/service/{service_name}?passing", timeout=2) as resp:
                            if resp.status == 200:
                                services = await resp.json()
                                if services:
                                    address = services[0]['Service']['Address']
                                    port = services[0]['Service']['Port']
                                    experts[expert_name] = format_url("http", address, port, "v1")
                    except Exception as e:
                        logging.debug(f"Expert {expert_name} not found or error: {e}")
        except Exception as e:
            logging.error(f"Error initializing ClientSession for discovery: {e}")

        return experts

    async def _query_model(self, model_info: Dict[str, Any], prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        """Queries a single model (local or external)."""
        base_url = model_info['url']
        api_key = model_info.get("api_key", "dummy")
        model_name = model_info['model']

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        if "openrouter.ai" in base_url:
            headers["HTTP-Referer"] = "https://github.com/karpathy/llm-council"
            headers["X-Title"] = "LLM Council"

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=60) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if 'choices' in data and len(data['choices']) > 0:
                            return data['choices'][0]['message']['content']
                        else:
                            return f"[Error: No choices in response from {model_info['name']}]"
                    else:
                        error_text = await resp.text()
                        logging.error(f"Error querying {model_info['name']}: {resp.status} - {error_text}")
                        return f"[Error querying {model_info['name']}: {resp.status}]"
        except Exception as e:
            logging.error(f"Exception querying {model_info['name']}: {e}")
            return f"[Exception querying {model_info['name']}: {e}]"

    async def convene(self, query: str) -> str:
        """Convening the council to answer the query."""
        logging.info(f"Convening council for query: {query}")

        local_experts = await self._discover_local_experts()

        council_members = []
        # Add local experts
        for name, url in local_experts.items():
            council_members.append({
                "name": f"local-{name}",
                "url": url,
                "model": "local",
                "type": "local"
            })

        # Add OpenRouter experts
        if self.openrouter_api_key:
            for model in self.openrouter_models:
                 council_members.append({
                    "name": model,
                    "url": "https://openrouter.ai/api/v1",
                    "model": model,
                    "type": "external",
                    "api_key": self.openrouter_api_key
                })

        if not council_members:
            return "I could not convene a council because no experts (local or external) are available."

        logging.info(f"Council members: {[m['name'] for m in council_members]}")

        # Stage 1: Initial Opinions
        stage1_tasks = []
        for member in council_members:
            system_prompt = f"You are {member['name']}, a distinguished member of an AI council. Provide your expert opinion on the user's query."
            stage1_tasks.append(self._query_model(member, query, system_prompt))

        opinions = await asyncio.gather(*stage1_tasks)

        opinions_map = {}
        for i, member in enumerate(council_members):
            opinions_map[member['name']] = opinions[i]

        # Stage 2: Peer Review
        # Each member reviews others
        stage2_tasks = []
        for member in council_members:
            other_opinions = "\n\n".join([f"--- Opinion from {n} ---\n{o}" for n, o in opinions_map.items() if n != member['name']])

            review_prompt = (
                f"Original User Query: {query}\n\n"
                f"Opinions from other council members:\n{other_opinions}\n\n"
                f"Your Initial Opinion: {opinions_map[member['name']]}\n\n"
                f"Task: Critically review the other opinions. Identify any errors, hallucinations, or missing perspectives. "
                f"Then, provide a REVISED, comprehensive answer that incorporates the best insights from the council. "
                f"Start your response with 'My Revised Opinion:'"
            )

            stage2_tasks.append(self._query_model(
                member,
                review_prompt,
                system_prompt=f"You are {member['name']}, reviewing opinions from other council members."
            ))

        reviews = await asyncio.gather(*stage2_tasks)
        formatted_reviews = "\n\n".join([f"--- {member['name']} Final Review ---\n{review}" for member, review in zip(council_members, reviews)])

        # Stage 3: Chairman Synthesis
        # Determine Chairman: prefer 'local-main', else first available
        chairman = next((m for m in council_members if "local-main" in m['name']), council_members[0])

        chairman_prompt = (
            f"User Query: {query}\n\n"
            f"Council Deliberations (Reviews and Revised Opinions):\n{formatted_reviews}\n\n"
            f"Task: You are the Chairman of the Council. Synthesize a single, coherent, and accurate final answer. "
            f"Resolve conflicts, correct errors pointed out by members, and unify the best parts of the responses. "
            f"Do not just summarize; provide the ANSWER."
        )

        final_answer = await self._query_model(
            chairman,
            chairman_prompt,
            system_prompt="You are the Chairman of the AI Council. Your goal is to provide the best possible answer based on the council's deliberation."
        )

        return final_answer
