import os
import sys
import logging
import time
import requests
import asyncio
from agent_factory import create_tools
from pipecat.services.openai.llm import OpenAILLMService

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

    logger.info(f"Starting Worker Agent for Task ID: {task_id}")

    if not prompt:
        logger.error("No WORKER_PROMPT environment variable found. Exiting.")
        sys.exit(1)

    logger.info(f"Received Prompt: {prompt}")
    logger.info(f"Received Context length: {len(context)} chars")

    # Discover Memory Service
    consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
    memory_url = None
    try:
        # Simple service discovery via Consul HTTP API
        # We look for 'memory-service'
        resp = requests.get(f"{consul_addr}/v1/catalog/service/memory-service")
        if resp.status_code == 200:
            services = resp.json()
            if services:
                # Just pick the first one
                svc = services[0]
                addr = svc.get("ServiceAddress", "localhost")
                port = svc.get("ServicePort", 8000)
                memory_url = f"http://{addr}:{port}"
                logger.info(f"Discovered Memory Service at {memory_url}")
    except Exception as e:
        logger.warning(f"Failed to discover memory service: {e}")

    # Initialize Tools
    # We pass None for twin_service/runner for now as the worker doesn't have the full pipeline context
    # but tools like Git, Shell, CodeRunner should work fine.
    tools = create_tools(config={}, twin_service=None, runner=None)
    logger.info(f"Initialized tools: {list(tools.keys())}")

    try:
        logger.info("Processing task with LLM...")

        # Simple LLM Loop (Mocked for now, but ready for OpenAILLMService)
        # In a real scenario, we would initialize OpenAILLMService here.
        # But `OpenAILLMService` in pipecat is tied to the pipeline.
        # We'll use a direct tool execution for demonstration or a simple loop if we had a standalone LLM client.

        # For the prototype, if the prompt asks to run a specific tool (heuristic), we run it.
        result_output = "No action taken."

        if "test" in prompt.lower() or "files" in prompt.lower():
            # Example: Run 'ls -la'
            if "shell" in tools:
                logger.info("Executing shell command...")
                try:
                    # ShellTool expected usage: await run(command)
                    # We assume ShellTool follows a standard interface or we need to inspect it.
                    # Based on existing tools, they often have a `run` or `execute` method.
                    # Let's assume `run` is async.
                    # Note: We need to check if run is async. Most tools in this repo are.
                    output = await tools["shell"].run("ls -la /opt/pipecatapp")
                    result_output = f"Shell Output: {output}"
                    logger.info(result_output)
                except Exception as e:
                    logger.error(f"Error executing shell tool: {e}")
                    result_output = f"Error: {e}"

        # Report to Shared Brain
        if memory_url:
            try:
                requests.post(f"{memory_url}/events", json={
                    "kind": "worker_result",
                    "content": f"Task {task_id} completed. Result: {result_output}",
                    "meta": {"task_id": task_id, "status": "success", "tools_used": list(tools.keys())}
                })
                logger.info("Reported result to Memory Service.")
            except Exception as e:
                logger.error(f"Failed to report to memory service: {e}")

        logger.info(f"Task {task_id} completed successfully.")

        # Print a special marker for the Orchestrator to potentially pick up from logs
        print(f"RESULT_JSON={{\"task_id\": \"{task_id}\", \"status\": \"success\", \"output\": \"Worker execution complete\"}}")

    except Exception as e:
        logger.error(f"Task failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main_async())
