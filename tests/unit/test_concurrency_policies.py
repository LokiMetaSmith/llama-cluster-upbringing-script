import pytest
import asyncio
from pipecatapp.concurrency.queue_manager import (
    ConcurrencyQueueManager,
    ConcurrencyPolicy,
    JobQueuePolicy
)

@pytest.mark.asyncio
async def test_policy_prefer_old():
    """
    PREFER_OLD: Keeps the running/older task and drops any newly triggered tasks under the same job key.
    This simulates the weekend 'wholesale repacking' scenario.
    """
    manager = ConcurrencyQueueManager()
    manager.set_policy("repack-job", JobQueuePolicy(ConcurrencyPolicy.PREFER_OLD, concurrency_limit=1))

    executed_tasks = []

    async def mock_executor(task_id, payload):
        executed_tasks.append(task_id)
        # Simulate a long running job (e.g. 7 hours repacking)
        await asyncio.sleep(payload.get("duration", 0.1))
        return f"Done {task_id}"

    # 1. Trigger the first "weekend wholesale" job
    fut1 = await manager.submit("repack-job", "task-wholesale-1", {"duration": 0.5}, mock_executor)
    assert fut1 is not None
    assert len(manager.get_active_tasks("repack-job")) == 1

    # Give it a moment to enter the executor
    await asyncio.sleep(0.01)

    # 2. While the first is running, trigger a second job
    fut2 = await manager.submit("repack-job", "task-wholesale-2", {"duration": 0.5}, mock_executor)

    # Under PREFER_OLD, the second job should be dropped/ignored (returns None)
    assert fut2 is None
    assert len(manager.get_active_tasks("repack-job")) == 1
    assert manager.get_active_tasks("repack-job")[0].task_id == "task-wholesale-1"

    # Wait for the first job to finish
    res1 = await fut1
    assert res1 == "Done task-wholesale-1"
    assert executed_tasks == ["task-wholesale-1"]


@pytest.mark.asyncio
async def test_policy_prefer_new():
    """
    PREFER_NEW: Cancels the running task and launches the new one.
    """
    manager = ConcurrencyQueueManager()
    manager.set_policy("repack-job", JobQueuePolicy(ConcurrencyPolicy.PREFER_NEW, concurrency_limit=1))

    executed_tasks = []
    cancelled_tasks = []

    async def mock_executor(task_id, payload):
        executed_tasks.append(task_id)
        try:
            await asyncio.sleep(5.0)  # Very long run time
            return f"Done {task_id}"
        except asyncio.CancelledError:
            cancelled_tasks.append(task_id)
            raise

    async def mock_on_cancel(task_id, payload):
        # Callback simulated for killing worker/reclaiming resources
        pass

    # 1. Trigger the first job
    fut1 = await manager.submit("repack-job", "task-1", {}, mock_executor, on_cancel=mock_on_cancel)
    assert fut1 is not None

    # Let the first task enter the executor
    await asyncio.sleep(0.05)

    # 2. Trigger a second job
    fut2 = await manager.submit("repack-job", "task-2", {}, mock_executor, on_cancel=mock_on_cancel)
    assert fut2 is not None

    # First task should be cancelled
    with pytest.raises(asyncio.CancelledError):
        await fut1

    # Give second task a moment to execute
    await asyncio.sleep(0.05)

    # Verify task list
    assert "task-1" in executed_tasks
    assert "task-1" in cancelled_tasks
    assert "task-2" in executed_tasks


@pytest.mark.asyncio
async def test_policy_wait():
    """
    WAIT: Queues up the subsequent tasks up to max_queue_size, running them sequentially.
    """
    manager = ConcurrencyQueueManager()
    manager.set_policy("repack-job", JobQueuePolicy(ConcurrencyPolicy.WAIT, concurrency_limit=1, max_queue_size=2))

    executed_tasks = []

    async def mock_executor(task_id, payload):
        executed_tasks.append(task_id)
        await asyncio.sleep(payload.get("duration", 0.05))
        return f"Done {task_id}"

    # 1. Start task 1
    fut1 = await manager.submit("repack-job", "task-1", {"duration": 0.1}, mock_executor)
    assert fut1 is not None

    # Give it a moment to enter the executor
    await asyncio.sleep(0.01)

    # 2. Submit task 2 (should be queued)
    fut2 = await manager.submit("repack-job", "task-2", {"duration": 0.05}, mock_executor)
    assert fut2 is not None
    assert len(manager.get_queued_tasks("repack-job")) == 1

    # 3. Submit task 3 (should be queued)
    fut3 = await manager.submit("repack-job", "task-3", {"duration": 0.05}, mock_executor)
    assert fut3 is not None
    assert len(manager.get_queued_tasks("repack-job")) == 2

    # 4. Submit task 4 (exceeds max_queue_size of 2) - should be dropped (None)
    fut4 = await manager.submit("repack-job", "task-4", {"duration": 0.05}, mock_executor)
    assert fut4 is None

    # Wait for the first task to complete
    res1 = await fut1
    assert res1 == "Done task-1"

    # Wait for task 2 and 3 to complete (they run sequentially once task 1 finishes)
    res2 = await fut2
    res3 = await fut3

    assert res2 == "Done task-2"
    assert res3 == "Done task-3"
    assert executed_tasks == ["task-1", "task-2", "task-3"]


@pytest.mark.asyncio
async def test_policy_parallel():
    """
    PARALLEL: Runs tasks in parallel up to the concurrency limit.
    """
    manager = ConcurrencyQueueManager()
    manager.set_policy("parallel-job", JobQueuePolicy(ConcurrencyPolicy.PARALLEL, concurrency_limit=2))

    executed_tasks = []

    async def mock_executor(task_id, payload):
        executed_tasks.append(task_id)
        await asyncio.sleep(0.1)
        return f"Done {task_id}"

    # Submit task 1 & 2
    fut1 = await manager.submit("parallel-job", "task-1", {}, mock_executor)
    fut2 = await manager.submit("parallel-job", "task-2", {}, mock_executor)

    assert fut1 is not None
    assert fut2 is not None

    # Give them a moment to enter the executor
    await asyncio.sleep(0.01)

    # Both should be active/running in parallel
    assert len(manager.get_active_tasks("parallel-job")) == 2

    # Submit task 3 (exceeds limit 2, so should be queued)
    fut3 = await manager.submit("parallel-job", "task-3", {}, mock_executor)
    assert fut3 is not None
    assert len(manager.get_queued_tasks("parallel-job")) == 1

    await asyncio.gather(fut1, fut2, fut3)
    assert set(executed_tasks) == {"task-1", "task-2", "task-3"}
