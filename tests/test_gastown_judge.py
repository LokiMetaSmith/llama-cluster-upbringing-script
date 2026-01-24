import asyncio
import os
import time
import json
import logging
from pipecatapp.pmm_memory import PMMMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_gastown_judge")

async def test_gastown_judge():
    db_path = "test_judge.db"

    # Clean up previous run
    if os.path.exists(db_path):
        os.remove(db_path)

    logger.info("Initializing PMMMemory...")
    memory = PMMMemory(db_path=db_path)

    technician_id = "tech_001"

    # 1. Simulate Technician creating work
    logger.info("Simulating Technician Work...")
    work_item_id = await memory.create_work_item(
        "Complex Feature Implementation",
        "user",
        technician_id
    )
    # Technician finishes
    await memory.update_work_item(work_item_id, status="completed", meta_update={"output": "Done"})

    # 2. Simulate Judge Validation
    logger.info("Simulating Judge Agent...")
    judge_verdict = {
        "judge_verdict": "PASS - Correct implementation",
        "passed": True,
        "timestamp": time.time()
    }

    # Judge updates the SAME work item with validation results
    await memory.update_work_item(
        work_item_id,
        validation_results=judge_verdict
    )

    # 3. Verify Ledger
    logger.info("Verifying Ledger State...")
    item = await memory.get_work_item(work_item_id)
    logger.info(f"Retrieved Item: {item}")

    assert item['id'] == work_item_id
    assert item['status'] == "completed" # Status remains from technician

    # Check validation results
    val_res = item['validation_results']
    assert val_res['passed'] is True
    assert "PASS" in val_res['judge_verdict']

    logger.info("✅ Judge Integration Verified!")

    memory.close()
    os.remove(db_path)

if __name__ == "__main__":
    asyncio.run(test_gastown_judge())
