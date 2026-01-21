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
logger = logging.getLogger("TechnicianAgent")

class TechnicianAgent:
    def __init__(self):
        self.task_id = os.getenv("WORKER_TASK_ID", "unknown")
        self.prompt = os.getenv("WORKER_PROMPT")
        self.context = os.getenv("WORKER_CONTEXT", "")
        self.llm_base_url = None
        self.memory_url = None
        self.tools = {}
        self.messages = []
        self.max_steps = int(os.getenv("MAX_STEPS", "15"))

    def discover_services(self):
        """Discovers LLM and Memory services via Consul."""
        consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
        token = os.getenv("CONSUL_HTTP_TOKEN")
        headers = {"X-Consul-Token": token} if token else {}

        try:
            # 1. Discover Memory Service
            resp = requests.get(f"{consul_addr}/v1/catalog/service/memory-service", headers=headers)
            if resp.status_code == 200:
                services = resp.json()
                if services:
                    svc = services[0]
                    addr = svc.get("ServiceAddress", "localhost")
                    port = svc.get("ServicePort", 8000)
                    self.memory_url = f"http://{addr}:{port}"
                    logger.info(f"Discovered Memory Service at {self.memory_url}")

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
        """Initializes tools using the agent factory."""
        # Technician agent runs standalone, so no twin_service
        self.tools = create_tools(config={}, twin_service=None, runner=None)
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
            "agent_type": "technician"
        })

        try:
            # Synchronous post is fine for this low volume
            requests.post(f"{self.memory_url}/events", json=payload)
        except Exception as e:
            logger.error(f"Failed to report event {kind}: {e}")

    async def call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
        """Helper to call the LLM service."""
        if not self.llm_base_url:
            # Fallback for testing without LLM
            logger.warning("No LLM service available. Returning mock response.")
            return "Mock LLM Response"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.llm_base_url}/chat/completions",
                    json={
                        "model": "gpt-3.5-turbo", # Router usually ignores this
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

    async def phase_1_plan(self) -> str:
        """Generates a high-level plan."""
        logger.info("PHASE 1: Planning")
        system_prompt = (
            "You are an expert technical planner. "
            "Given a request, create a concise, step-by-step plan to achieve it using the available tools. "
            f"Available Tools: {list(self.tools.keys())}\n"
            "Do not execute the plan yet, just list the steps."
        )

        msgs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Request: {self.prompt}\nContext: {self.context}"}
        ]

        plan = await self.call_llm(msgs, temperature=0.2)
        logger.info(f"Generated Plan:\n{plan}")
        await self.report_event("technician_plan", plan)
        return plan

    async def phase_2_execute(self, plan: str) -> str:
        """Runs the ReAct loop to execute the plan."""
        logger.info("PHASE 2: Execution")

        system_prompt = f"""You are a technician agent executing a plan.
Available Tools: {list(self.tools.keys())}

Plan to follow:
{plan}

Original Request: {self.prompt}
Context: {self.context}

Instructions:
1. Review the history and the plan.
2. Decide the next action.
3. If you need to use a tool, output valid JSON: {{ "tool": "tool_name", "args": {{ ... }} }}
4. If the task is complete, output: FINAL_ANSWER: <your summary>
5. If you are stuck, output: FINAL_ANSWER: Unable to complete due to <reason>

Focus on one step at a time.
"""

        self.messages = [{"role": "system", "content": system_prompt}]

        step = 0
        final_answer = None

        while step < self.max_steps:
            step += 1
            logger.info(f"Step {step}/{self.max_steps}")

            # Get LLM response
            response = await self.call_llm(self.messages)
            logger.info(f"LLM Thought: {response}")
            self.messages.append({"role": "assistant", "content": response})

            # Parse for Final Answer
            if "FINAL_ANSWER:" in response:
                final_answer = response.split("FINAL_ANSWER:", 1)[1].strip()
                break

            # Parse for Tool Call
            tool_call = self._parse_tool_call(response)
            if tool_call:
                tool_name = tool_call.get("tool")
                tool_args = tool_call.get("args", {})

                if tool_name in self.tools:
                    logger.info(f"Executing tool: {tool_name}")
                    try:
                        tool_instance = self.tools[tool_name]
                        if asyncio.iscoroutinefunction(tool_instance.run):
                            output = await tool_instance.run(**tool_args)
                        else:
                            output = tool_instance.run(**tool_args)
                    except Exception as e:
                        output = f"Tool Execution Error: {e}"

                    logger.info(f"Tool Output: {str(output)[:200]}...") # Truncate log
                    self.messages.append({"role": "user", "content": f"Tool '{tool_name}' output: {output}"})
                else:
                    self.messages.append({"role": "user", "content": f"Error: Tool '{tool_name}' not found."})
            else:
                # No tool call found, treating as a thought or generic message
                # If the LLM is just talking, prompt it to act
                self.messages.append({"role": "user", "content": "Please continue with the next step or use a tool."})

        if not final_answer:
            final_answer = "Max steps reached without definitive completion."

        return final_answer

    def _parse_tool_call(self, text: str) -> Optional[Dict]:
        """Simple JSON extractor."""
        if "{" in text and "}" in text:
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None
        return None

    async def phase_3_reflect(self, result: str) -> str:
        """Reflects on the result."""
        logger.info("PHASE 3: Reflection")

        reflection_prompt = (
            "Review the following execution result against the original request.\n"
            f"Original Request: {self.prompt}\n"
            f"Result: {result}\n\n"
            "Is this result satisfactory and complete? "
            "If yes, repeat the result. If no, succinctly describe what is missing."
        )

        msgs = [
            {"role": "system", "content": "You are a Quality Assurance reviewer."},
            {"role": "user", "content": reflection_prompt}
        ]

        critique = await self.call_llm(msgs, temperature=0.0)
        logger.info(f"Reflection: {critique}")
        return critique

    async def run(self):
        logger.info(f"Starting Technician Agent for Task ID: {self.task_id}")

        if not self.prompt:
            logger.error("No WORKER_PROMPT env var. Exiting.")
            sys.exit(1)

        self.discover_services()
        self.initialize_tools()

        await self.report_event("worker_started", f"Technician started task {self.task_id}")

        try:
            # 1. Plan
            plan = await self.phase_1_plan()

            # 2. Execute
            execution_result = await self.phase_2_execute(plan)

            # 3. Reflect
            final_verdict = await self.phase_3_reflect(execution_result)

            # Report Success
            await self.report_event("worker_result", final_verdict, {"status": "success", "execution_log": len(self.messages)})

            # Output for Orchestrator/Logs
            print(f"RESULT_JSON={{\"task_id\": \"{self.task_id}\", \"status\": \"success\", \"output\": \"{final_verdict}\"}}")

        except Exception as e:
            logger.error(f"Technician failed: {e}")
            await self.report_event("worker_failure", str(e), {"status": "failed"})
            sys.exit(1)

if __name__ == "__main__":
    agent = TechnicianAgent()
    asyncio.run(agent.run())
