import asyncio
from pipecatapp.workflow.runner import WorkflowRunner
import pipecatapp.workflow.nodes

async def main():
    runner = WorkflowRunner("workflows/tasky_checklist_poc.yaml")

    # Mock global input context to skip hitting consul if we don't have it running
    # but since this is a PoC we can just pass mock task markdown and execution results
    global_inputs = {
        "task_markdown": "# Connection Pooling\n\nStatus: DOING\nDependencies: [connect, disconnect]\n\n## Criteria\n[ ] Create a pool on first connect\n[ ] Reuse connections across requests\n[ ] Configurable pool size via env var\n[ ] Graceful drain on shutdown\n[ ] Health check pings idle connections",
        "execution_result": "I implemented connection pooling! The pool is created when the first connection happens. It also reuses connections across subsequent requests. Pool size can be configured using the POOL_SIZE env var. Graceful drain and health checks are not yet implemented.",
        "consul_http_addr": None # Skip actual LLM call for pure syntax test unless we want to mock it.
    }

    # Just syntax check and load the workflow. It will fail with "Could not reach LLM service" because we don't mock it, but we can verify the graph parses.
    try:
        final_state = await runner.run(global_inputs)
        print("Final Output:")
        import json
        print(json.dumps(final_state, indent=2))
    except Exception as e:
        print(f"Error executing workflow: {e}")

if __name__ == "__main__":
    asyncio.run(main())
