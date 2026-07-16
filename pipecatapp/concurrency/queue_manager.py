import asyncio
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Awaitable

logger = logging.getLogger(__name__)

class ConcurrencyPolicy(Enum):
    PARALLEL = "parallel"
    PREFER_NEW = "prefer_new"
    WAIT = "wait"
    PREFER_OLD = "prefer_old"

class JobQueuePolicy:
    def __init__(
        self,
        policy: ConcurrencyPolicy,
        concurrency_limit: int = 1,
        max_queue_size: int = 10
    ):
        self.policy = policy
        self.concurrency_limit = concurrency_limit
        self.max_queue_size = max_queue_size

class TaskState:
    def __init__(self, task_id: str, payload: Any):
        self.task_id = task_id
        self.payload = payload
        self.task: Optional[asyncio.Task] = None
        self.future = asyncio.Future()

class ConcurrencyQueueManager:
    """
    Manages concurrency and queue semantics for jobs based on ConcurrencyPolicy.
    Allows registering tasks under specific job/config keys, enforcing limits,
    queueing, or termination policies before executing them.
    """
    def __init__(self):
        # Maps job_key -> list of currently running TaskStates
        self.active_tasks: Dict[str, List[TaskState]] = {}
        # Maps job_key -> list of queued TaskStates
        self.queues: Dict[str, List[TaskState]] = {}
        # Maps job_key -> JobQueuePolicy
        self.policies: Dict[str, JobQueuePolicy] = {}

    def set_policy(self, job_key: str, policy: JobQueuePolicy):
        """Sets or overrides the concurrency policy for a specific job key."""
        self.policies[job_key] = policy

    def get_policy(self, job_key: str) -> JobQueuePolicy:
        """Gets the policy for a job key, defaulting to PREFER_OLD with concurrency limit 1."""
        return self.policies.get(
            job_key,
            JobQueuePolicy(ConcurrencyPolicy.PREFER_OLD, concurrency_limit=1)
        )

    def get_active_tasks(self, job_key: str) -> List[TaskState]:
        return self.active_tasks.get(job_key, [])

    def get_queued_tasks(self, job_key: str) -> List[TaskState]:
        return self.queues.get(job_key, [])

    async def submit(
        self,
        job_key: str,
        task_id: str,
        payload: Any,
        executor: Callable[[str, Any], Awaitable[Any]],
        on_cancel: Optional[Callable[[str, Any], Awaitable[None]]] = None
    ) -> Optional[Any]:
        """
        Submits a task for execution under a job_key.

        Args:
            job_key (str): The configuration/job key identifying the class of task.
            task_id (str): Unique ID for this task invocation.
            payload (Any): Arbitrary payload/parameters passed to executor.
            executor (Callable): Async function to execute the task, e.g. executor(task_id, payload).
            on_cancel (Callable): Async function to clean up/kill the task if cancelled by PREFER_NEW.

        Returns:
            The result of the execution if it starts or finishes, or None if dropped/queued.
            If queued, the execution is deferred, and it runs asynchronously.
        """
        policy = self.get_policy(job_key)

        # Initialize active lists and queues if they don't exist
        if job_key not in self.active_tasks:
            self.active_tasks[job_key] = []
        if job_key not in self.queues:
            self.queues[job_key] = []

        active = self.active_tasks[job_key]
        queue = self.queues[job_key]

        # Filter out finished active tasks
        self.active_tasks[job_key] = [t for t in active if not t.future.done()]
        active = self.active_tasks[job_key]

        # Check concurrency limit
        if len(active) < policy.concurrency_limit:
            # We can execute immediately
            task_state = TaskState(task_id, payload)
            active.append(task_state)
            task = asyncio.create_task(self._run_task(job_key, task_state, executor))
            task_state.task = task
            return task_state.future

        # Concurrency limit reached. Apply policy.
        if policy.policy == ConcurrencyPolicy.PARALLEL:
            # In PARALLEL, limit is still enforced. But normally concurrency_limit is set high.
            # If we hit the limit, what do we do? We can either wait or drop. Let's treat PARALLEL
            # as having its limit, and if reached we can queue/wait or drop. In general, PARALLEL
            # behaves like WAIT with concurrency limit. Let's fallback to waiting.
            pass

        if policy.policy == ConcurrencyPolicy.PREFER_OLD:
            # Drop the new task. Do not run or queue.
            logger.info(f"[{job_key}] Concurrency policy PREFER_OLD: Dropping new task {task_id}.")
            return None

        elif policy.policy == ConcurrencyPolicy.PREFER_NEW:
            # Cancel/Kill existing active task(s) to make room, then run the new one
            logger.info(f"[{job_key}] Concurrency policy PREFER_NEW: Cancelling active tasks to run {task_id}.")

            # Cancel active tasks
            to_cancel = list(active)
            for running_task in to_cancel:
                if running_task.task:
                    running_task.task.cancel()
                running_task.future.cancel()
                if on_cancel:
                    try:
                        await on_cancel(running_task.task_id, running_task.payload)
                    except Exception as e:
                        logger.error(f"Error in on_cancel callback for {running_task.task_id}: {e}")

            # Re-filter active tasks
            self.active_tasks[job_key] = [t for t in active if not t.future.done()]
            active = self.active_tasks[job_key]

            # Execute the new one
            task_state = TaskState(task_id, payload)
            active.append(task_state)
            task = asyncio.create_task(self._run_task(job_key, task_state, executor))
            task_state.task = task
            return task_state.future

        elif policy.policy == ConcurrencyPolicy.WAIT or policy.policy == ConcurrencyPolicy.PARALLEL:
            # Queue the task if there's room
            if len(queue) >= policy.max_queue_size:
                logger.warning(f"[{job_key}] Queue size limit reached ({policy.max_queue_size}). Dropping task {task_id}.")
                return None

            logger.info(f"[{job_key}] Concurrency policy {policy.policy.name}: Queueing task {task_id}.")
            task_state = TaskState(task_id, payload)
            queue.append(task_state)
            return task_state.future

        return None

    async def _run_task(
        self,
        job_key: str,
        task_state: TaskState,
        executor: Callable[[str, Any], Awaitable[Any]]
    ):
        """Runs the task executor, handles completion, and triggers the next queued task."""
        try:
            if task_state.future.cancelled():
                return

            res = await executor(task_state.task_id, task_state.payload)
            if not task_state.future.done():
                task_state.future.set_result(res)
        except asyncio.CancelledError:
            logger.info(f"Task {task_state.task_id} was cancelled.")
            if not task_state.future.done():
                task_state.future.cancel()
        except Exception as e:
            logger.error(f"Error executing task {task_state.task_id}: {e}")
            if not task_state.future.done():
                task_state.future.set_exception(e)
        finally:
            # Clean up active tasks list
            if job_key in self.active_tasks:
                self.active_tasks[job_key] = [t for t in self.active_tasks[job_key] if t != task_state]

            # Process next item in the queue if available
            self._process_queue(job_key, executor)

    def _process_queue(self, job_key: str, executor: Callable[[str, Any], Awaitable[Any]]):
        """Checks if there's room in active tasks and starts the next queued task."""
        policy = self.get_policy(job_key)
        active = self.active_tasks.get(job_key, [])
        queue = self.queues.get(job_key, [])

        # Filter active
        self.active_tasks[job_key] = [t for t in active if not t.future.done()]
        active = self.active_tasks[job_key]

        while len(active) < policy.concurrency_limit and queue:
            next_task = queue.pop(0)
            if next_task.future.cancelled():
                continue
            active.append(next_task)
            task = asyncio.create_task(self._run_task(job_key, next_task, executor))
            next_task.task = task
