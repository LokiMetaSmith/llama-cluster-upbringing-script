import asyncio
import os
import time
import json
import logging
from pipecatapp.pmm_memory import PMMMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_gastown_memory")

async def test_gastown_memory():
    db_path = "test_memory.db"

    # Clean up previous run
    if os.path.exists(db_path):
        os.remove(db_path)

    logger.info("Initializing PMMMemory...")
    memory = PMMMemory(db_path=db_path)

    # 1. Test Work Item Creation
    logger.info("Testing create_work_item...")
    item_id = await memory.create_work_item(
        title="Test Task",
        created_by="tester",
        assignee_id="agent_007",
        meta={"priority": "high"}
    )
    logger.info(f"Created Work Item ID: {item_id}")
    assert item_id is not None

    # 2. Test Get Work Item
    logger.info("Testing get_work_item...")
    item = await memory.get_work_item(item_id)
    logger.info(f"Retrieved Item: {item}")
    assert item['title'] == "Test Task"
    assert item['status'] == "open"
    assert item['assignee_id'] == "agent_007"
    assert item['meta']['priority'] == "high"

    # 3. Test Update Work Item
    logger.info("Testing update_work_item...")
    success = await memory.update_work_item(
        item_id,
        status="in_progress",
        meta_update={"priority": "critical"}
    )
    assert success is True

    updated_item = await memory.get_work_item(item_id)
    assert updated_item['status'] == "in_progress"
    assert updated_item['meta']['priority'] == "critical"

    # 4. Test List Work Items
    logger.info("Testing list_work_items...")
    # Create another item
    await memory.create_work_item("Another Task", "tester", "agent_007")

    items = await memory.list_work_items(assignee_id="agent_007")
    logger.info(f"List Items: {len(items)} found")
    assert len(items) == 2

    logger.info("✅ All Gas Town Memory tests passed!")

    memory.close()
    os.remove(db_path)

if __name__ == "__main__":
    asyncio.run(test_gastown_memory())
