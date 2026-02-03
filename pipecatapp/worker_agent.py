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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WorkerAgent")

MAX_STEPS = 20
CHECK_STEP = 10
ENSEMBLE_SIZE = 3

async def main_async():
    """
    Async Entry point for the ephemeral worker agent.
    It reads its instructions from environment variables, performs the task,
    and then exits.
    """
    task_id = os.getenv("WORKER_TASK_ID", "unknown")
    prompt = os.getenv("WORKER_PROMPT")
    context = os.getenv("WORKER_CONTEXT", "")
    work_item_id = os.getenv("WORK_ITEM_ID") # Gas Town Work Item ID

    logger.info(f"Starting Worker Agent for Task ID: {task_id}")

    if not prompt:
        logger.error("No WORKER_PROMPT environment variable found. Exiting.")
        sys.exit(1)

    logger.info(f"Received Prompt: {prompt}")
    logger.info(f"Received Context length: {len(context)} chars")

    # Discover Services via Consul
    consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
    token = os.getenv("CONSUL_HTTP_TOKEN")
    headers = {"X-Consul-Token": token} if token else {}
    memory_url = None
    llm_base_url = None
    memory_client = None

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
                memory_url = f"http://{addr}:{port}"
                memory_client = PMMMemoryClient(base_url=memory_url)
                logger.info(f"Discovered Event Bus ({event_bus_service_name}) at {memory_url}")

        # 2. Discover LLM Service (router-api or llamacpp-rpc-api)
        # We try 'router-api' first as it's the main entry point
        llm_service_name = os.getenv("LLAMA_API_SERVICE_NAME", "router-api")
        resp = requests.get(f"{consul_addr}/v1/catalog/service/{llm_service_name}", headers=headers)
        if resp.status_code == 200:
            services = resp.json()
            if services:
                svc = services[0]
                addr = svc.get("ServiceAddress", "localhost")
                port = svc.get("ServicePort", int(os.getenv("ROUTER_PORT", 8081))) # Default likely 8081 for router
                llm_base_url = f"http://{addr}:{port}/v1"
                logger.info(f"Discovered LLM Service at {llm_base_url}")
    except Exception as e:
        logger.warning(f"Failed to discover services: {e}")

    # Report Startup
    if memory_client:
        try:
            # Event Bus
            await memory_client.add_event(
                kind="worker_started",
                content=f"Task {task_id} started.",
                meta={"task_id": task_id, "status": "started", "work_item_id": work_item_id}
            )
            # Gas Town Work Ledger
            if work_item_id:
                await memory_client.update_work_item(work_item_id, status="in_progress")
        except Exception as e:
            logger.error(f"Failed to report start: {e}")

    # Initialize Tools
    tools = create_tools(config={}, twin_service=None, runner=None)
    tools["submit_solution"] = SubmitSolutionTool()
    logger.info(f"Initialized tools: {list(tools.keys())}")

    # Initialize Message History
    system_prompt = f"""You are a helpful worker agent.
You have access to the following tools: {list(tools.keys())}.
Your task is: {prompt}
Context: {context}

INSTRUCTIONS:
1. Think step-by-step.
2. If you need to use a tool, respond with a JSON object: {{ "tool": "tool_name", "args": {{ ... }} }}
3. If you have a final answer (and have already submitted your solution if required), respond with just the text.
4. IMPORTANT: When you have completed the coding task, you MUST use the `submit_solution` tool to return your work.
"""
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

    step_count = 0
    final_output = ""
    status = "running"

    try:
        async with httpx.AsyncClient() as client:
            while step_count < MAX_STEPS:
                step_count += 1
                logger.info(f"--- Step {step_count} ---")

                # REASONING LIMIT CHECK
                if step_count == CHECK_STEP:
                    logger.info("Soft limit reached. Performing progress check.")
                    # Inject prompt to summarize
                    check_messages = messages + [{"role": "user", "content": "You have been working for a while. Briefly summarize your progress and state if you are stuck or making good progress."}]

                    try:
                        resp = await client.post(
                            f"{llm_base_url}/chat/completions",
                            json={"model": "gpt-3.5-turbo", "messages": check_messages, "temperature": 0.0},
                            timeout=60.0
                        )
                        resp.raise_for_status()
                        summary = resp.json()['choices'][0]['message']['content']
                        logger.info(f"Agent Summary: {summary}")

                        # Judge Loop
                        judge_prompt = f"Analyze the following agent summary. Is the agent making progress or stuck/incoherent? Respond with 'CONTINUE' or 'TERMINATE'.\n\nSummary: {summary}"
                        judge_resp = await client.post(
                            f"{llm_base_url}/chat/completions",
                            json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": judge_prompt}], "temperature": 0.0},
                            timeout=30.0
                        )
                        judge_decision = judge_resp.json()['choices'][0]['message']['content']
                        if "TERMINATE" in judge_decision.upper():
                            logger.warning("Agent deemed incoherent or stuck. Terminating.")
                            final_output = "Terminated due to lack of progress."
                            status = "failed"
                            break
                    except Exception as e:
                        logger.warning(f"Progress check failed: {e}")

                # ENSEMBLE THOUGHTS (Best-of-N)
                # Generate N completions
                candidates = []
                logger.info(f"Generating {ENSEMBLE_SIZE} candidates...")

                tasks = []
                for _ in range(ENSEMBLE_SIZE):
                     # Add temperature variance
                     temp = 0.7 if _ > 0 else 0.0
                     tasks.append(client.post(
                        f"{llm_base_url}/chat/completions",
                        json={"model": "gpt-3.5-turbo", "messages": messages, "temperature": temp},
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
                    break

                # SELECT BEST THOUGHT
                if len(valid_responses) == 1:
                    selected_response = valid_responses[0]
                else:
                    # Ask LLM to pick the best one
                    selection_prompt = "Here are multiple possible next steps. Select the most coherent and logical one. Respond with the index (0, 1, or 2) only.\n\n"
                    for i, r in enumerate(valid_responses):
                        selection_prompt += f"--- Option {i} ---\n{r}\n\n"

                    try:
                         sel_resp = await client.post(
                            f"{llm_base_url}/chat/completions",
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

                # Append to history
                messages.append({"role": "assistant", "content": selected_response})

                # PARSE & EXECUTE TOOL
                if "{" in selected_response and "}" in selected_response:
                    try:
                        start = selected_response.find("{")
                        end = selected_response.rfind("}") + 1
                        json_str = selected_response[start:end]
                        tool_call = json.loads(json_str)

                        tool_name = tool_call.get("tool")
                        tool_args = tool_call.get("args", {})

                        if tool_name in tools:
                            logger.info(f"Executing tool {tool_name}...")
                            tool_instance = tools[tool_name]
                            if asyncio.iscoroutinefunction(tool_instance.run):
                                output = await tool_instance.run(**tool_args)
                            else:
                                output = tool_instance.run(**tool_args)

                            logger.info(f"Tool Output: {str(output)[:100]}...")
                            messages.append({"role": "tool", "content": f"Tool output: {output}"})

                            if tool_name == "submit_solution":
                                final_output = output
                                status = "success"
                                break # Task Done
                        else:
                             messages.append({"role": "tool", "content": f"Error: Unknown tool '{tool_name}'"})
                    except json.JSONDecodeError:
                        messages.append({"role": "tool", "content": "Error: Invalid JSON format for tool call."})
                else:
                    # No tool call, just chatter or final answer?
                    if "final answer" in selected_response.lower():
                        messages.append({"role": "user", "content": "Please use the 'submit_solution' tool to submit your final work."})
                    else:
                        pass

        # END OF LOOP

        if status == "success":
            logger.info("Task completed successfully.")
            print(f"RESULT_JSON={{\"task_id\": \"{task_id}\", \"status\": \"success\", \"output\": \"{final_output}\"}}")
        else:
            logger.warning("Task finished without clear success or failure.")
            print(f"RESULT_JSON={{\"task_id\": \"{task_id}\", \"status\": \"failed\", \"output\": \"{final_output}\"}}")

        # Report to Memory
        if memory_client:
             try:
                 # Event Bus
                 await memory_client.add_event(
                    kind="worker_result",
                    content=f"Task {task_id} {status}. Output: {final_output}",
                    meta={"task_id": task_id, "status": status, "work_item_id": work_item_id}
                 )
                 # Gas Town Work Ledger
                 if work_item_id:
                     if status == "success":
                         await memory_client.update_work_item(
                             work_item_id,
                             status="completed",
                             validation_results={"output": final_output}
                         )
                     else:
                         await memory_client.update_work_item(
                             work_item_id,
                             status="failed",
                             validation_results={"output": final_output}
                         )
             except Exception as e:
                 logger.error(f"Failed to report result: {e}")

    except Exception as e:
        logger.error(f"Worker crashed: {e}")
        # Failure Reporting
        if memory_client and work_item_id:
            try:
                await memory_client.update_work_item(
                    work_item_id,
                    status="failed",
                    validation_results={"error": str(e)}
                )
            except:
                pass
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main_async())
