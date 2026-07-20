import os
import json
import logging
import httpx
import asyncio
from typing import Dict, Any, List, Optional
from workflow.node import Node
from workflow.context import WorkflowContext
from .registry import registry
from pmm_memory_client import PMMMemoryClient
from agent_factory import create_tools

from judge_agent import JudgeAgent
from worker_agent import WorkerAgent

logger = logging.getLogger("ResearchNodes")

class BaseResearchNode(Node):
    def __init__(self, node_id: str, config: Dict[str, Any]):
        super().__init__(node_id, config)
        self.consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
        self.token = os.getenv("CONSUL_HTTP_TOKEN")
        self.headers = {"X-Consul-Token": self.token} if self.token else {}
        self.llm_base_url = None
        self.memory_url = None
        self.memory_client = None
        self._background_tasks = set()

    async def _discover_services(self):
        if not self.llm_base_url:
            self.llm_base_url = os.getenv("LLM_BASE_URL", "http://10.0.0.1:8000/v1")

        if not self.memory_client:
            event_bus_service_name = os.getenv("EVENT_BUS_SERVICE_NAME", "memory-service")
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f"{self.consul_addr}/v1/catalog/service/{event_bus_service_name}", headers=self.headers, timeout=5)
                    if resp.status_code == 200 and resp.json():
                        svc = resp.json()[0]
                        self.memory_url = f"http://{svc['ServiceAddress']}:{svc['ServicePort']}"
                        self.memory_client = PMMMemoryClient(self.memory_url)
            except Exception as e:
                logger.warning(f"Could not discover Memory Service: {e}")
                # Fallback
                self.memory_client = PMMMemoryClient("http://127.0.0.1:8000")

    async def call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.7, model: Optional[str] = None) -> str:
        await self._discover_services()
        # Default to the cluster's base URL and models rather than hardcoding GPT-4 everywhere
        # Let the orchestrator or environment decide the actual model routing where possible.
        req_model = model if model else os.getenv("DEFAULT_LLM_MODEL", "gpt-3.5-turbo")
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    f"{self.llm_base_url}/chat/completions",
                    json={"model": req_model, "messages": messages, "temperature": temperature},
                    timeout=120.0
                )
                resp.raise_for_status()
                data = resp.json()

                # Tokenomics Tracking
                usage = data.get("usage", {})
                if usage and self.memory_client:
                    telemetry = {
                        "model": req_model,
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "total_tokens": usage.get("total_tokens", 0),
                        "node_id": self.id
                    }
                    try:
                        # Fire and forget telemetry recording using create_task to prevent blocking
                        task = asyncio.create_task(
                            self.memory_client.add_event(
                                kind="research_telemetry",
                                content=f"Token usage for {req_model}",
                                meta=telemetry
                            )
                        )
                        self._background_tasks.add(task)
                        task.add_done_callback(self._background_tasks.discard)
                    except Exception as tele_err:
                        logger.warning(f"Failed to record token telemetry: {tele_err}")

                return data['choices'][0]['message']['content']
            except Exception as e:
                logger.error(f"LLM call failed: {e}")
                return f"Error: {e}"

@registry.register
class WikiCheckNode(BaseResearchNode):
    async def execute(self, context: WorkflowContext):
        inputs = {}
        for inp in self.config.get("inputs", []):
            name = inp["name"]
            inputs[name] = self.get_input(context, name)

        topic = inputs.get("research_topic", "")

        # Instantiate MemoryStore to check the RAG vector database
        try:
            from pipecatapp.memory import MemoryStore
        except ImportError:
            from memory import MemoryStore

        memory_store = context.global_inputs.get("memory_store")
        if not memory_store:
            # We run initialization in an executor if it does heavy I/O
            loop = asyncio.get_running_loop()
            memory_store = await loop.run_in_executor(None, MemoryStore)

        existing_knowledge = ""
        # Search for top 3 matching chunks in the FAISS index/SQLite DB
        try:
            loop = asyncio.get_running_loop()
            results = await loop.run_in_executor(None, memory_store.search, topic, 3)
            if results:
                existing_knowledge = "\n".join([f"- {res}" for res in results])
        except Exception as e:
            logger.warning(f"WikiCheckNode search failed: {e}")

        self.set_output(context, "existing_knowledge", existing_knowledge)

@registry.register
class FindNode(BaseResearchNode):
    async def execute(self, context: WorkflowContext):
        inputs = {}
        for inp in self.config.get("inputs", []):
            name = inp["name"]
            inputs[name] = self.get_input(context, name)
        await self._discover_services()
        topic = inputs.get("research_topic", "")
        session_id = inputs.get("session_id", "unknown_session")
        feedback = inputs.get("feedback", None)
        existing_knowledge = inputs.get("existing_knowledge", "")

        prompt = f"Find claims and information about: {topic}."
        if existing_knowledge:
            prompt += f"\n\nWe already know the following from our wiki. Do not repeat this information:\n{existing_knowledge}"
        if feedback:
            prompt += f"\nPrevious feedback to address: {feedback}"

        # Wrap existing WorkerAgent for the Find action
        # This adheres to using the existing agent logic structure.
        worker_agent = WorkerAgent()
        worker_agent.task_id = session_id
        worker_agent.prompt = prompt
        worker_agent.context = "You are a Finder agent. Your job is to search for information and propose claims with sources (URLs). Be concise and output a JSON list of claims, each with 'claim' and 'source_url' keys."
        worker_agent.llm_base_url = self.llm_base_url
        worker_agent.memory_client = self.memory_client

        # Set the target model dynamically based on configuration
        node_model = self.config.get("config", {}).get("model")
        if node_model:
            worker_agent.model_override = node_model

        # Set max steps very low so it just generates a plan/claims and exits
        worker_agent.max_steps = 1
        worker_agent.messages = [
            {"role": "system", "content": worker_agent.context},
            {"role": "user", "content": worker_agent.prompt}
        ]

        # Execute actual worker logic. perform_step is typically durable/async.
        async with httpx.AsyncClient() as client:
             # Just run one step to get its first thought
             status, final_output = await worker_agent.perform_step(1, client)

        # Extract the last message it appended to its own state
        result = worker_agent.messages[-1]["content"] if worker_agent.messages else ""

        try:
            start = result.find("[")
            end = result.rfind("]") + 1
            if start != -1 and end != -1:
                claims = json.loads(result[start:end])
            else:
                claims = [{"claim": result, "source_url": "unknown"}]
        except:
            claims = [{"claim": result, "source_url": "unknown"}]

        if self.memory_client:
             await self.memory_client.add_event("research_find", f"Found {len(claims)} claims for {topic}", {"session": session_id, "claims": claims})

        self.set_output(context, "claims", claims)


@registry.register
class VerifyNode(BaseResearchNode):
    async def execute(self, context: WorkflowContext):
        inputs = {}
        for inp in self.config.get("inputs", []):
            name = inp["name"]
            inputs[name] = self.get_input(context, name)
        await self._discover_services()
        claims = inputs.get("claims", [])
        session_id = inputs.get("session_id", "unknown_session")

        if not claims:
            self.set_output(context, "verified_claims", [])
            return

        # Use JudgeAgent to act as Verifier
        node_model = self.config.get("config", {}).get("model")

        verified_claims = []
        for claim in claims:
            judge_agent = JudgeAgent()
            judge_agent.task_id = session_id
            judge_agent.criteria = "You are a Verifier agent. Check the given claim and source. Does the source actually support the claim? Reply in JSON: {'verified': true/false, 'reason': '...'}"
            judge_agent.llm_base_url = self.llm_base_url
            if node_model:
                judge_agent.model_override = node_model

            # Actually use judge_agent's internal execution path
            # Since JudgeAgent.discover_services is synchronous, we run it in a thread executor
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, judge_agent.discover_services)
            # Intercept LLM URL to respect this node's discovery
            if self.llm_base_url:
                judge_agent.llm_base_url = self.llm_base_url

            # Execute judge_work
            target_text = f"Claim: {claim.get('claim')}\nSource: {claim.get('source_url')}"
            result = await judge_agent.judge_work(target_text)

            try:
                start = result.find("{")
                end = result.rfind("}") + 1
                res_json = json.loads(result[start:end])
                if res_json.get("verified", False):
                    verified_claims.append(claim)
            except:
                pass

        if self.memory_client:
             await self.memory_client.add_event("research_verify", f"Verified {len(verified_claims)}/{len(claims)} claims", {"session": session_id})

        self.set_output(context, "verified_claims", verified_claims)


@registry.register
class JudgeResearchNode(BaseResearchNode):
    async def execute(self, context: WorkflowContext):
        inputs = {}
        for inp in self.config.get("inputs", []):
            name = inp["name"]
            inputs[name] = self.get_input(context, name)
        await self._discover_services()
        verified_claims = inputs.get("verified_claims", [])
        topic = inputs.get("research_topic", "")
        session_id = inputs.get("session_id", "unknown_session")

        # Instead of raw LLM calls, use the existing JudgeAgent behavior.
        # We instantiate a JudgeAgent and configure its target criteria.
        judge_agent = JudgeAgent()
        judge_agent.criteria = f"Topic: {topic}. Are the following verified claims sufficient to answer the topic? Do we need to run tools to get more info? If sufficient, VERDICT: PASS. If not sufficient, provide feedback as VERDICT: FAIL - <feedback>. If tools are needed, output a JSON tool call first."
        judge_agent.task_id = session_id

        node_model = self.config.get("config", {}).get("model")
        if node_model:
            judge_agent.model_override = node_model

        # JudgeAgent.discover_services and initialize_tools are synchronous
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, judge_agent.discover_services)
        await loop.run_in_executor(None, judge_agent.initialize_tools)

        # Override the criteria strictly for this routing step
        judge_agent.criteria = "You are the Judge agent. Review the verified claims against the topic criteria. Reply in exactly this JSON format: {'sufficient': true/false, 'needs_tools': true/false, 'tool_requests': [{'tool': 'tool_name', 'args': {}}], 'feedback_for_finder': '...'}"

        # Execute judge_work
        target_text = f"Topic: {topic}\nClaims: {json.dumps(verified_claims)}"
        result = await judge_agent.judge_work(target_text)

        needs_tools = False
        tool_requests = []
        feedback = None
        sufficient = True

        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            res_json = json.loads(result[start:end])
            needs_tools = res_json.get("needs_tools", False)
            tool_requests = res_json.get("tool_requests", [])
            feedback = res_json.get("feedback_for_finder")
            sufficient = res_json.get("sufficient", True)
        except:
            pass

        if not sufficient and not needs_tools:
            # We need more from Finder
            self.set_output(context, "needs_more_claims", True)
            self.set_output(context, "needs_tools", False)
            self.set_output(context, "approved_claims", [])
            self.set_output(context, "tool_requests", [])
            self.set_output(context, "feedback", feedback)
            return

        self.set_output(context, "needs_more_claims", False)
        self.set_output(context, "needs_tools", needs_tools)
        self.set_output(context, "approved_claims", verified_claims if sufficient else [])
        self.set_output(context, "tool_requests", tool_requests)
        self.set_output(context, "feedback", feedback)


@registry.register
class RunToolsNode(BaseResearchNode):
    async def execute(self, context: WorkflowContext):
        inputs = {}
        for inp in self.config.get("inputs", []):
            name = inp["name"]
            inputs[name] = self.get_input(context, name)
        tool_requests = inputs.get("tool_requests", [])
        session_id = inputs.get("session_id", "unknown_session")

        tools = create_tools()
        results = []

        for req in tool_requests:
            tool_name = req.get("tool")
            args = req.get("args", {})
            if tool_name in tools:
                tool_instance = tools[tool_name]
                try:
                    if asyncio.iscoroutinefunction(tool_instance.run):
                        out = await tool_instance.run(**args)
                    else:
                        out = tool_instance.run(**args)
                    results.append({"request": req, "result": out})
                except Exception as e:
                    results.append({"request": req, "error": str(e)})

        self.set_output(context, "tool_results", results)


@registry.register
class ValidateNode(BaseResearchNode):
    async def execute(self, context: WorkflowContext):
        inputs = {}
        for inp in self.config.get("inputs", []):
            name = inp["name"]
            inputs[name] = self.get_input(context, name)
        await self._discover_services()
        claims = inputs.get("judged_claims", [])
        tool_results = inputs.get("tool_results", [])
        session_id = inputs.get("session_id", "unknown_session")

        final_report = "### Research Report\n\n"
        for claim in claims:
            final_report += f"- **Claim:** {claim.get('claim')}\n  - *Source:* {claim.get('source_url')}\n"

        for tr in tool_results:
             final_report += f"\n**Tool Result ({tr.get('request', {}).get('tool')}):**\n{tr.get('result', tr.get('error', 'No result'))}\n"

        if self.memory_client:
             await self.memory_client.add_event("research_completed", f"Compiled final research report", {"session": session_id, "report": final_report})

             # Also write to the Obsidian vault if configured in memory or environment
             vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "/tmp/obsidian_vault")
             if os.path.exists(vault_path):
                 import aiofiles
                 import time
                 import re

                 topic = inputs.get("research_topic", "unknown_topic")
                 # Sanitize topic for filename
                 safe_topic = re.sub(r'[^a-zA-Z0-9_\-]', '_', topic)

                 filepath = os.path.join(vault_path, f"Research_{safe_topic}_{int(time.time())}.md")
                 try:
                     async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                         await f.write(f"# Research: {topic}\n\n")
                         await f.write(final_report)
                         # Add the tag for the gardener just in case
                         await f.write("\n\n#agent #research\n")
                     logger.info(f"Saved research report to wiki: {filepath}")
                 except Exception as e:
                     logger.error(f"Failed to write to wiki: {e}")
                     self.set_output(context, "saved_to_wiki", False)
                     self.set_output(context, "final_report", final_report)
                     return

        self.set_output(context, "final_report", final_report)
        self.set_output(context, "saved_to_wiki", True)
