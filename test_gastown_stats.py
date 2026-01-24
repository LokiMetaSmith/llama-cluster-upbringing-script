import asyncio
import os
import time
import json
import logging
from pipecatapp.pmm_memory import PMMMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_gastown_stats")

async def test_gastown_stats():
    db_path = "test_stats.db"

    # Clean up previous run
    if os.path.exists(db_path):
        os.remove(db_path)

    logger.info("Initializing PMMMemory...")
    memory = PMMMemory(db_path=db_path)

    agent_id = "agent_smith"

    # 1. Populate Dummy Data
    logger.info("Populating work items...")

    # 5 Completed tasks
    for i in range(5):
        await memory.create_work_item(
            f"Success Task {i}",
            "tester",
            agent_id,
            meta={"priority": "low"}
        )
        # Manually update status to completed
        # (In real flow, create returns ID, then update uses ID. Here we query or assume sequential for loop)
        # Actually create_work_item returns ID.
        # But wait, create_work_item returns a future in async wrapper?
        # No, wrapper awaits run_in_executor.

        # Let's do it properly
        items = await memory.list_work_items(assignee_id=agent_id, limit=1)
        # The list is ordered by created_at DESC, so [0] is the one we just made
        item_id = items[0]['id']
        await memory.update_work_item(item_id, status="completed")

    # 2 Failed tasks
    for i in range(2):
        await memory.create_work_item(
            f"Fail Task {i}",
            "tester",
            agent_id
        )
        items = await memory.list_work_items(assignee_id=agent_id, limit=1)
        item_id = items[0]['id']
        await memory.update_work_item(item_id, status="failed")

    # 3 Open tasks (should count towards total but not success/fail rate? depends on logic)
    # The logic in pmm_memory.py:
    # total_tasks = COUNT(*)
    # completed = COUNT(status='completed')
    # failed = COUNT(status='failed')
    # rate = completed / total * 100

    for i in range(3):
        await memory.create_work_item(f"Open Task {i}", "tester", agent_id)

    # Total = 5 + 2 + 3 = 10

    # 2. Query Stats
    logger.info("Querying Agent Stats...")
    stats = await memory.get_agent_stats(agent_id)

    logger.info(f"Stats Result: {stats}")

    assert stats['assignee_id'] == agent_id
    assert stats['total_tasks'] == 10
    assert stats['completed_tasks'] == 5
    assert stats['failed_tasks'] == 2

    # Success Rate = 5 / 10 = 50.0%
    assert stats['success_rate'] == 50.0

    logger.info("✅ Agent Stats Logic Verified!")

    memory.close()
    os.remove(db_path)

if __name__ == "__main__":
    asyncio.run(test_gastown_stats())
