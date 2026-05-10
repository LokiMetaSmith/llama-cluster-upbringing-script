import os
import sys
import logging
import time
import requests
import asyncio
import httpx
import json
import re
from agent_factory import create_tools
from tools.submit_solution_tool import SubmitSolutionTool
from pmm_memory_client import PMMMemoryClient
from durable_execution import DurableExecutionEngine, durable_step

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WorkerAgent")

MAX_STEPS = 20
CHECK_STEP = 10
ENSEMBLE_SIZE = 3


class WorkerAgent:
    def __init__(self):
        self.task_id = os.getenv("WORKER_TASK_ID", "unknown")
        self.prompt = os.getenv("WORKER_PROMPT")
        self.context = os.getenv("WORKER_CONTEXT", "")
        self.work_item_id = os.getenv("WORK_ITEM_ID")
        self.max_steps = int(os.getenv("MAX_STEPS", "20"))

        self.consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
        self.token = os.getenv("CONSUL_HTTP_TOKEN")
        self.headers = {"X-Consul-Token": self.token} if self.token else {}
        self.memory_url = None
        self.llm_base_url = None
        self.memory_client = None

        self.tools = {}
        self.messages = []

        # Durable Execution State
        self.durable_engine = DurableExecutionEngine()
        self.current_flow_id = self.task_id
        self.step_counter = 0

    def rehydrate_and_resume(self) -> bool:
        """Checks for existing state and prepares to resume if a crash occurred."""
        try:
            cursor = self.durable_engine.conn.cursor()
            cursor.execute("""
                SELECT step_sequence, status, internal_context FROM execution_log
                WHERE flowId = ? ORDER BY step_sequence DESC LIMIT 1
            """, (self.task_id,))
            row = cursor.fetchone()

            if not row:
                return False

            last_seq, status_str, context_blob = row

            if status_str == "PENDING":
                logger.info(f"Detected incomplete execution for {self.task_id} at sequence {last_seq}. Resuming.")
                if last_seq > 0:
                    cursor.execute("""
                        SELECT internal_context FROM execution_log
                        WHERE flowId = ? AND step_sequence = ?
                    """, (self.task_id, last_seq - 1))
                    prev_row = cursor.fetchone()
                    if prev_row and prev_row[0]:
                        import pickle
                        ctx = pickle.loads(prev_row[0])
                        if "messages" in ctx:
                            self.messages = ctx["messages"]
                            logger.info(f"Restored {len(self.messages)} messages from history.")
                return True
        except Exception as e:
            logger.error(f"Failed to rehydrate state: {e}")
            return False

    @durable_step
    async def perform_step(self, step_count: int, client: httpx.AsyncClient) -> tuple[str, str]:
        """Executes a single step of the reasoning loop."""
        final_output = ""
        status = "running"
        CHECK_STEP = 10
        ENSEMBLE_SIZE = 3

        logger.info(f"--- Step {step_count} ---")

        if step_count == CHECK_STEP:
            logger.info("Soft limit reached. Performing progress check.")
            check_messages = self.messages + [{"role": "user", "content": "You have been working for a while. Briefly summarize your progress and state if you are stuck or making good progress."}]

            try:
                resp = await client.post(
                    f"{self.llm_base_url}/chat/completions",
                    json={"model": "gpt-3.5-turbo", "messages": check_messages, "temperature": 0.0},
                    timeout=60.0
                )
                resp.raise_for_status()
                summary = resp.json()['choices'][0]['message']['content']
                logger.info(f"Agent Summary: {summary}")

                judge_prompt = f"Analyze the following agent summary. Is the agent making progress or stuck/incoherent? Respond with 'CONTINUE' or 'TERMINATE'.\n\nSummary: {summary}"
                judge_resp = await client.post(
                    f"{self.llm_base_url}/chat/completions",
                    json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": judge_prompt}], "temperature": 0.0},
                    timeout=30.0
                )
                judge_decision = judge_resp.json()['choices'][0]['message']['content']
                if "TERMINATE" in judge_decision.upper():
                    logger.warning("Agent deemed incoherent or stuck. Terminating.")
                    final_output = "Terminated due to lack of progress."
                    status = "failed"
                    return status, final_output
            except Exception as e:
                logger.warning(f"Progress check failed: {e}")

        candidates = []
        logger.info(f"Generating {ENSEMBLE_SIZE} candidates...")
        tasks = []
        for i in range(ENSEMBLE_SIZE):
            temp = 0.7 if i > 0 else 0.0
            tasks.append(client.post(
                f"{self.llm_base_url}/chat/completions",
                json={"model": "gpt-3.5-turbo", "messages": self.messages, "temperature": temp},
                timeout=60.0
            ))

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        valid_responses = []
        for r in responses:
            if isinstance(r, httpx.Response) and r.status_code == 200:
                content = r.json()['choices'][0]['message']['content']
                valid_responses.append(content)

        if not valid_responses:
            logger.error("No valid responses from LLM.")
            return "failed", "No valid responses from LLM."

        if len(valid_responses) == 1:
            selected_response = valid_responses[0]
        else:
            selection_prompt = "Here are multiple possible next steps. Select the most coherent and logical one. Respond with the index (0, 1, or 2) only.\n\n"
            for i, r in enumerate(valid_responses):
                selection_prompt += f"--- Option {i} ---\n{r}\n\n"

            try:
                sel_resp = await client.post(
                    f"{self.llm_base_url}/chat/completions",
                    json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": selection_prompt}], "temperature": 0.0},
                    timeout=30.0
                )
                sel_content = sel_resp.json()['choices'][0]['message']['content']
                match = re.search(r"\d+", sel_content)
                if match:
                    idx = int(match.group(0))
                    if 0 <= idx < len(valid_responses):
                        selected_response = valid_responses[idx]
                    else:
                        selected_response = valid_responses[0]
                else:
                    selected_response = valid_responses[0]
            except:
                selected_response = valid_responses[0]

        logger.info(f"Selected Thought: {selected_response[:100]}...")
        self.messages.append({"role": "assistant", "content": selected_response})

        if "{" in selected_response and "}" in selected_response:
            try:
                start = selected_response.find("{")
                end = selected_response.rfind("}") + 1
                json_str = selected_response[start:end]
                tool_call = json.loads(json_str)

                tool_name = tool_call.get("tool")
                tool_args = tool_call.get("args", {})

                if tool_name in self.tools:
                    logger.info(f"Executing tool {tool_name}...")
                    tool_instance = self.tools[tool_name]
                    if asyncio.iscoroutinefunction(tool_instance.run):
                        output = await tool_instance.run(**tool_args)
                    else:
                        output = tool_instance.run(**tool_args)

                    logger.info(f"Tool Output: {str(output)[:100]}...")
                    self.messages.append({"role": "tool", "content": f"Tool output: {output}"})

                    if tool_name == "submit_solution":
                        final_output = output
                        status = "success"
                else:
                    self.messages.append({"role": "tool", "content": f"Error: Unknown tool '{tool_name}'"})
            except json.JSONDecodeError:
                self.messages.append({"role": "tool", "content": "Error: Invalid JSON format for tool call."})
        else:
            if "final answer" in selected_response.lower():
                self.messages.append({"role": "user", "content": "Please use the 'submit_solution' tool to submit your final work."})

        return status, final_output

    async def run(self):
        logger.info(f"Starting Worker Agent for Task ID: {self.task_id}")

        if not self.prompt:
            logger.error("No WORKER_PROMPT environment variable found. Exiting.")
            sys.exit(1)

        logger.info(f"Received Prompt: {self.prompt}")
        logger.info(f"Received Context length: {len(self.context)} chars")

        try:
            resp = requests.get(f"{self.consul_addr}/v1/catalog/service/pmm-memory-service", headers=self.headers, timeout=5)
            if resp.status_code == 200 and resp.json():
                svc = resp.json()[0]
                self.memory_url = f"http://{svc['ServiceAddress']}:{svc['ServicePort']}"
                logger.info(f"Found Memory Service at {self.memory_url}")
        except Exception as e:
            logger.warning(f"Could not discover Memory Service: {e}")

        try:
            resp = requests.get(f"{self.consul_addr}/v1/catalog/service/llamacpp-rpc-api", headers=self.headers, timeout=5)
            if resp.status_code == 200 and resp.json():
                svc = resp.json()[0]
                self.llm_base_url = f"http://{svc['ServiceAddress']}:{svc['ServicePort']}/v1"
                logger.info(f"Found LLM API at {self.llm_base_url}")
            else:
                self.llm_base_url = "http://10.0.0.1:8080/v1"
                logger.warning(f"LLM API not found in Consul. Defaulting to {self.llm_base_url}")
        except Exception as e:
            self.llm_base_url = "http://10.0.0.1:8080/v1"
            logger.warning(f"Error discovering LLM API: {e}. Defaulting to {self.llm_base_url}")

        if self.memory_url:
            self.memory_client = PMMMemoryClient(self.memory_url)

        self.tools = create_tools()
        self.tools["submit_solution"] = SubmitSolutionTool()
        logger.info(f"Initialized tools: {list(self.tools.keys())}")

        if not self.rehydrate_and_resume():
            system_prompt = f"""You are a helpful worker agent.
You have access to the following tools: {list(self.tools.keys())}.
Your task is: {self.prompt}
Context: {self.context}

INSTRUCTIONS:
1. Think step-by-step.
2. If you need to use a tool, respond with a JSON object: {{ "tool": "tool_name", "args": {{ ... }} }}
3. If you have a final answer (and have already submitted your solution if required), respond with just the text.
4. IMPORTANT: When you have completed the coding task, you MUST use the `submit_solution` tool to return your work.
"""
            self.messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": self.prompt}]

        step_count = len([m for m in self.messages if m["role"] == "assistant"])
        final_output = ""
        status = "running"

        try:
            async with httpx.AsyncClient() as client:
                while step_count < self.max_steps and status == "running":
                    step_count += 1
                    status, final_output = await self.perform_step(step_count, client)

            if status == "success":
                logger.info("Task completed successfully.")
                print(f"RESULT_JSON={{\"task_id\": \"{self.task_id}\", \"status\": \"success\", \"output\": \"{final_output}\"}}")
            else:
                logger.warning("Task finished without clear success or failure.")
                print(f"RESULT_JSON={{\"task_id\": \"{self.task_id}\", \"status\": \"failed\", \"output\": \"{final_output}\"}}")

            if self.memory_client:
                 try:
                     await self.memory_client.add_event(
                        kind="worker_result",
                        content=f"Task {self.task_id} {status}. Output: {final_output}",
                        meta={"task_id": self.task_id, "status": status, "work_item_id": self.work_item_id}
                     )
                     if self.work_item_id:
                         if status == "success":
                             await self.memory_client.update_work_item(self.work_item_id, status="completed", validation_results={"output": final_output})
                         else:
                             await self.memory_client.update_work_item(self.work_item_id, status="failed", validation_results={"output": final_output})
                 except Exception as e:
                     logger.error(f"Failed to report result: {e}")

        except Exception as e:
            logger.error(f"Worker crashed: {e}")
            if self.memory_client and self.work_item_id:
                try:
                    await self.memory_client.update_work_item(self.work_item_id, status="failed", validation_results={"error": str(e)})
                except:
                    pass
            sys.exit(1)


if __name__ == "__main__":
    agent = WorkerAgent()
    asyncio.run(agent.run())
