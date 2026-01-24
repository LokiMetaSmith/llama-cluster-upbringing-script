import os
import sys
import logging
import time
import requests
import asyncio
import httpx
import json
from typing import List, Dict, Any, Optional
from agent_factory import create_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JudgeAgent")

class JudgeAgent:
    def __init__(self):
        self.task_id = os.getenv("JUDGE_TASK_ID", "unknown")
        # The task_id of the work we are judging
        self.target_task_id = os.getenv("TARGET_TASK_ID")
        self.criteria = os.getenv("JUDGE_CRITERIA", "General correctness and functionality")

        self.llm_base_url = None
        self.memory_url = None
        self.tools = {}

    def discover_services(self):
        """Discovers LLM and Memory services via Consul."""
        consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
        token = os.getenv("CONSUL_HTTP_TOKEN")
        headers = {"X-Consul-Token": token} if token else {}

        try:
            # 1. Discover Memory Service / Event Bus
            event_bus_service_name = os.getenv("EVENT_BUS_SERVICE_NAME", "memory-service")
            resp = requests.get(f"{consul_addr}/v1/catalog/service/{event_bus_service_name}", headers=headers)
            if resp.status_code == 200:
                services = resp.json()
                if services:
                    svc = services[0]
                    addr = svc.get("ServiceAddress", "localhost")
                    port = svc.get("ServicePort", 8000)
                    self.memory_url = f"http://{addr}:{port}"
                    logger.info(f"Discovered Event Bus ({event_bus_service_name}) at {self.memory_url}")

            # 2. Discover LLM Service
            llm_service_name = os.getenv("LLAMA_API_SERVICE_NAME", "router-api")
            resp = requests.get(f"{consul_addr}/v1/catalog/service/{llm_service_name}", headers=headers)
            if resp.status_code == 200:
                services = resp.json()
                if services:
                    svc = services[0]
                    addr = svc.get("ServiceAddress", "localhost")
                    port = svc.get("ServicePort", int(os.getenv("ROUTER_PORT", 8081)))
                    self.llm_base_url = f"http://{addr}:{port}/v1"
                    logger.info(f"Discovered LLM Service at {self.llm_base_url}")
        except Exception as e:
            logger.warning(f"Failed to discover services: {e}")

    def initialize_tools(self):
        """Initializes verification tools."""
        # Judge needs tools to read files, run tests/linters
        self.tools = create_tools(config={}, twin_service=None, runner=None)
        # We might restrict tools later, but for now full access is fine for QA
        logger.info(f"Initialized tools: {list(self.tools.keys())}")

    async def report_event(self, kind: str, content: str, meta: Dict[str, Any] = None):
        """Reports an event to the shared memory service."""
        if not self.memory_url:
            return

        payload = {
            "kind": kind,
            "content": content,
            "meta": meta or {}
        }
        # Add standard meta
        payload["meta"].update({
            "task_id": self.task_id,
            "agent_type": "judge",
            "target_task_id": self.target_task_id
        })

        try:
            requests.post(f"{self.memory_url}/events", json=payload)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to report event {kind}: {e}")
            # Retry once
            try:
                time.sleep(1)
                requests.post(f"{self.memory_url}/events", json=payload)
            except:
                pass
        except Exception as e:
            logger.error(f"Unexpected error reporting {kind}: {e}")

    async def call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
        """Helper to call the LLM service."""
        if not self.llm_base_url:
            return "Mock LLM Response: Approved"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.llm_base_url}/chat/completions",
                    json={
                        "model": "gpt-4",
                        "messages": messages,
                        "temperature": temperature
                    },
                    timeout=120.0
                )
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except Exception as e:
                logger.error(f"LLM call failed: {e}")
                return f"Error: {str(e)}"

    async def fetch_target_result(self) -> str:
        """Fetches the result of the target task from the Event Bus."""
        if not self.memory_url or not self.target_task_id:
            return "No result available."

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.memory_url}/tasks/{self.target_task_id}")
                if resp.status_code == 200:
                    events = resp.json()
                    # Look for the final result
                    for evt in events:
                        if evt.get("kind") in ["worker_result", "manager_result"]:
                            return evt.get("content")
        except Exception as e:
            logger.error(f"Failed to fetch target result: {e}")

        return "Could not retrieve target result."

    async def judge_work(self, target_result: str) -> str:
        """Evaluates the work."""
        logger.info("Starting Judgement...")

        # 1. Run automated checks if applicable
        # (e.g., if we knew the repo path, we could run lint/test)
        # For now, we rely on LLM review of the result text + tools if needed

        system_prompt = f"""You are a strict QA Judge.
Your goal is to verify if the following work meets the criteria: "{self.criteria}".
You have access to tools to inspect files or run commands if needed.

Target Result:
{target_result}

Instructions:
1. Analyze the result.
2. If you need to verify something (e.g. read a file), output a JSON tool call.
3. If you are satisfied, output: VERDICT: PASS
4. If you find issues, output: VERDICT: FAIL - <reason>
"""
        messages = [{"role": "system", "content": system_prompt}]

        # Simple loop for tool use (limit 5 steps)
        for i in range(5):
            response = await self.call_llm(messages)
            logger.info(f"Judge Thought: {response}")
            messages.append({"role": "assistant", "content": response})

            if "VERDICT:" in response:
                return response.split("VERDICT:", 1)[1].strip()

            # Check for tool
            if "{" in response and "}" in response:
                # Naive JSON extraction
                try:
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    json_str = response[start:end]
                    tool_call = json.loads(json_str)

                    tool_name = tool_call.get("tool")
                    tool_args = tool_call.get("args", {})

                    if tool_name in self.tools:
                        logger.info(f"Judge executing {tool_name}")
                        tool_instance = self.tools[tool_name]
                        if asyncio.iscoroutinefunction(tool_instance.run):
                            output = await tool_instance.run(**tool_args)
                        else:
                            output = tool_instance.run(**tool_args)
                        messages.append({"role": "user", "content": f"Tool output: {output}"})
                    else:
                        messages.append({"role": "user", "content": "Tool not found."})
                except:
                    messages.append({"role": "user", "content": "Invalid JSON for tool call."})
            else:
                 messages.append({"role": "user", "content": "Please continue to a verdict."})

        return "FAIL - Judgement timed out"

    async def run(self):
        logger.info(f"Judge Agent starting for Target Task: {self.target_task_id}")

        if not self.target_task_id:
            logger.error("No TARGET_TASK_ID. Exiting.")
            sys.exit(1)

        self.discover_services()
        self.initialize_tools()

        await self.report_event("judge_started", f"Judging task {self.target_task_id}")

        target_result = await self.fetch_target_result()
        logger.info(f"Target Result to Judge: {target_result[:100]}...")

        verdict = await self.judge_work(target_result)
        logger.info(f"Final Verdict: {verdict}")

        if verdict.startswith("PASS"):
            await self.report_event("judge_pass", verdict, {"status": "success"})
        else:
            await self.report_event("judge_fail", verdict, {"status": "failed"})

if __name__ == "__main__":
    agent = JudgeAgent()
    asyncio.run(agent.run())
