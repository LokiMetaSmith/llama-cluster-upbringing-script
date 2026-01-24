import os
import sys
import logging
import time
import requests
import asyncio
import httpx
from agent_factory import create_tools
from tools.submit_solution_tool import SubmitSolutionTool
from pipecat.services.openai.llm import OpenAILLMService
from pmm_memory_client import PMMMemoryClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WorkerAgent")

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

    # Report Startup to Shared Brain & Work Ledger
    if memory_client:
        try:
            # Event Bus
            await memory_client.add_event(
                kind="worker_started",
                content=f"Task {task_id} started.",
                meta={
                    "task_id": task_id,
                    "prompt": prompt,
                    "context": context,
                    "status": "started",
                    "work_item_id": work_item_id
                }
            )

            # Gas Town Work Ledger
            if work_item_id:
                await memory_client.update_work_item(work_item_id, status="in_progress")

            logger.info("Reported start to Memory Service.")
        except Exception as e:
            logger.error(f"Failed to report start to memory service: {e}")

    # Initialize Tools
    tools = create_tools(config={}, twin_service=None, runner=None)
    tools["submit_solution"] = SubmitSolutionTool()
    logger.info(f"Initialized tools: {list(tools.keys())}")

    try:
        logger.info("Processing task with LLM...")
        result_output = "No action taken."

        if llm_base_url:
            # Construct the system prompt with tool definitions
            system_prompt = f"""You are a helpful worker agent.
You have access to the following tools: {list(tools.keys())}.
Your task is: {prompt}
Context: {context}

IMPORTANT: When you have completed the coding task, you MUST use the `submit_solution` tool to return your work.
Do not just output the code in text. Use the tool.

If you need to use a tool, respond with a JSON object:
{{ "tool": "tool_name", "args": {{ ... }} }}

If you have a final answer (and have already submitted your solution), respond with just the text.
"""

            messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

            async with httpx.AsyncClient() as client:
                try:
                    logger.info(f"Querying LLM at {llm_base_url}...")
                    response = await client.post(
                        f"{llm_base_url}/chat/completions",
                        json={
                            "model": "gpt-3.5-turbo", # Placeholder, router ignores this usually
                            "messages": messages,
                            "temperature": 0.0
                        },
                        timeout=60.0
                    )
                    response.raise_for_status()
                    llm_content = response.json()['choices'][0]['message']['content']
                    logger.info(f"LLM Response: {llm_content}")

                    # Simple tool parsing (heuristic for JSON)
                    import json
                    if "{" in llm_content and "}" in llm_content:
                        try:
                            # Extract JSON blob
                            start = llm_content.find("{")
                            end = llm_content.rfind("}") + 1
                            json_str = llm_content[start:end]
                            tool_call = json.loads(json_str)

                            tool_name = tool_call.get("tool")
                            tool_args = tool_call.get("args", {})

                            if tool_name in tools:
                                logger.info(f"Executing tool {tool_name} with args {tool_args}...")
                                # Assume all tools have a 'run' method that might be async
                                tool_instance = tools[tool_name]
                                if asyncio.iscoroutinefunction(tool_instance.run):
                                    output = await tool_instance.run(**tool_args)
                                else:
                                    output = tool_instance.run(**tool_args)
                                result_output = f"Tool {tool_name} output: {output}"
                            else:
                                result_output = f"LLM requested unknown tool: {tool_name}"
                        except json.JSONDecodeError:
                            result_output = f"Failed to parse tool call from LLM: {llm_content}"
                    else:
                        result_output = llm_content

                except Exception as e:
                    logger.error(f"LLM interaction failed: {e}")
                    result_output = f"LLM Error: {e}"
        else:
            logger.warning("No LLM service found. Falling back to heuristic.")
            # Fallback heuristic
            if "test" in prompt.lower() or "files" in prompt.lower():
                if "shell" in tools:
                    output = await tools["shell"].run("ls -la /opt/pipecatapp")
                    result_output = f"Shell Output: {output}"

        # Report to Shared Brain & Work Ledger
        if memory_client:
            try:
                # Event Bus
                await memory_client.add_event(
                    kind="worker_result",
                    content=f"Task {task_id} completed. Result: {result_output}",
                    meta={
                        "task_id": task_id,
                        "status": "success",
                        "tools_used": list(tools.keys()),
                        "work_item_id": work_item_id
                    }
                )

                # Gas Town Work Ledger
                if work_item_id:
                    await memory_client.update_work_item(
                        work_item_id,
                        status="completed",
                        validation_results={"output": result_output}
                    )

                logger.info("Reported result to Memory Service.")
            except Exception as e:
                logger.error(f"Failed to report result to memory service: {e}")

        logger.info(f"Task {task_id} completed successfully.")

        # Print a special marker for the Orchestrator to potentially pick up from logs
        print(f"RESULT_JSON={{\"task_id\": \"{task_id}\", \"status\": \"success\", \"output\": \"Worker execution complete\"}}")

    except Exception as e:
        logger.error(f"Task failed: {e}")
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
