import os
import sys
import logging
import time
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WorkerAgent")

def main():
    """
    Entry point for the ephemeral worker agent.
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

    # In a full implementation, this would:
    # 1. Initialize an LLM client (OpenAI/Local)
    # 2. Query the LLM with the prompt + context
    # 3. Perform actions (git clone, edit files, etc.)
    # 4. Report back to a central 'Memory Service' or 'World Model'

    # For this prototype, we simulate work
    try:
        logger.info("Processing task...")
        # Simulate thinking/working time
        time.sleep(2)

        # Report to Shared Brain
        if memory_url:
            try:
                requests.post(f"{memory_url}/events", json={
                    "kind": "worker_result",
                    "content": f"Task {task_id} completed.",
                    "meta": {"task_id": task_id, "status": "success"}
                })
                logger.info("Reported result to Memory Service.")
            except Exception as e:
                logger.error(f"Failed to report to memory service: {e}")

        logger.info(f"Task {task_id} completed successfully.")

        # Print a special marker for the Orchestrator to potentially pick up from logs
        print(f"RESULT_JSON={{\"task_id\": \"{task_id}\", \"status\": \"success\", \"output\": \"Simulated completion\"}}")

    except Exception as e:
        logger.error(f"Task failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
