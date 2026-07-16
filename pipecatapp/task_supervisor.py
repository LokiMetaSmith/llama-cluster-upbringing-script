import asyncio
import logging
import time
from typing import Dict, Any, Optional
from tools.swarm_tool import SwarmTool
from pmm_memory_client import PMMMemoryClient
from pipecatapp.concurrency.queue_manager import ConcurrencyQueueManager, ConcurrencyPolicy, JobQueuePolicy

class TaskSupervisor:
    """
    Monitors the progress of spawned worker tasks by polling the Shared Memory.
    If a task takes too long without a result, it intervenes (kills and optionally retries).
    Also manages job/task concurrency policies (PARALLEL, PREFER_NEW, WAIT, PREFER_OLD).
    """
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.logger = logging.getLogger(__name__)
        self.swarm_tool = self.twin_service.tools.get("swarm") or SwarmTool()
        self.memory = self.twin_service.long_term_memory
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.check_interval = 30  # seconds
        self.task_timeout = 300   # seconds (5 minutes)

        # Heartbeat loop configuration
        self.heartbeat_queue = [] # Queue of pending tasks waiting for heartbeat wakeups
        self.heartbeat_interval = 60 # Scheduled heartbeat interval in seconds

        # Concurrency Policy Gatekeeper
        self.concurrency_manager = ConcurrencyQueueManager()

    def set_job_policy(self, job_key: str, policy: JobQueuePolicy):
        """Sets the policy for a specific category of jobs (identified by job_key)."""
        self.concurrency_manager.set_policy(job_key, policy)

    async def spawn_task_with_policy(
        self,
        job_key: str,
        task_id: str,
        prompt: str,
        context: str = "",
        agent_type: str = "worker"
    ) -> Optional[asyncio.Future]:
        """
        Spawns a worker/technician task using the ConcurrencyQueueManager
        to guarantee concurrency policies are obeyed.
        """
        async def _executor(tid, payload):
            self.logger.info(f"Executing task '{tid}' under job key '{job_key}' using policy limits.")
            spawn_res = await self.swarm_tool.spawn_workers(
                tasks=[{"id": tid, "prompt": payload["prompt"], "context": payload["context"]}],
                agent_type=payload["agent_type"]
            )
            return spawn_res

        async def _on_cancel(tid, payload):
            # Terminate running Nomad/Swarm job
            nomad_job_id = f"worker-{tid}"
            self.logger.warning(f"Cancelling task '{tid}' under job key '{job_key}' because of PREFER_NEW policy.")
            try:
                await self.swarm_tool.kill_worker(nomad_job_id)
            except Exception as e:
                self.logger.error(f"Failed to kill cancelled worker {nomad_job_id}: {e}")

        payload = {
            "prompt": prompt,
            "context": context,
            "agent_type": agent_type
        }

        # Submit task to the manager
        fut = await self.concurrency_manager.submit(
            job_key=job_key,
            task_id=task_id,
            payload=payload,
            executor=_executor,
            on_cancel=_on_cancel
        )
        return fut

    async def handle_gateway_exhaustion(self, expert_name: str) -> bool:
        """
        Intercepts failover/exhaustion signals from the gateway.
        Triggers SwarmTool.spawn_workers to dynamically provision a fresh expert model.
        """
        self.logger.warning(f"Gateway reported critical exhaustion for expert '{expert_name}'. Spawning fallback worker...")
        try:
            # Dynamically spawn a new worker to handle the load/failover
            spawn_res = await self.swarm_tool.spawn_workers(
                tasks=[{"id": f"failover-{expert_name}-{int(time.time())}", "prompt": f"Handle overflow requests for expert {expert_name}", "context": ""}],
                agent_type="worker"
            )
            self.logger.info(f"Dynamic failover worker spawn result: {spawn_res}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to spawn dynamic failover worker for '{expert_name}': {e}")
            return False

    async def start(self):
        """Starts the background monitoring loop and the scheduled Heartbeat loop."""
        self.logger.info("TaskSupervisor monitoring loop started.")
        # Start both the task checker and the heartbeat loop concurrently
        await asyncio.gather(
            self._monitoring_loop(),
            self._heartbeat_loop()
        )

    async def _monitoring_loop(self):
        while True:
            try:
                await self._check_tasks()
            except Exception as e:
                self.logger.error(f"TaskSupervisor monitoring error: {e}")
            await asyncio.sleep(self.check_interval)

    async def _heartbeat_loop(self):
        self.logger.info("TaskSupervisor Heartbeat loop started.")
        while True:
            try:
                await self.run_heartbeat()
            except Exception as e:
                self.logger.error(f"TaskSupervisor heartbeat error: {e}")
            await asyncio.sleep(self.heartbeat_interval)

    async def add_heartbeat_task(self, task_id: str, prompt: str, context: str = "", agent_type: str = "worker") -> str:
        """Enqueues a task to be processed at the next scheduled heartbeat wakeup."""
        task = {
            "id": task_id,
            "prompt": prompt,
            "context": context,
            "agent_type": agent_type,
            "status": "queued"
        }
        self.heartbeat_queue.append(task)
        self.logger.info(f"Task {task_id} enqueued for the next scheduled heartbeat.")
        return f"Successfully enqueued task {task_id} in the heartbeat queue."

    async def run_heartbeat(self):
        """Executes a single heartbeat wakeup sequence over all queued tasks."""
        if not self.heartbeat_queue:
            self.logger.debug("Heartbeat Loop: No queued tasks. Workers remaining in low-power sleep state.")
            return

        self.logger.info(f"Heartbeat Loop triggered. Processing {len(self.heartbeat_queue)} queued tasks...")

        # Copy and clear the queue
        tasks_to_process = list(self.heartbeat_queue)
        self.heartbeat_queue.clear()

        for task in tasks_to_process:
            task_id = task["id"]
            self.logger.info(f"Heartbeat: Waking up technician/worker node for task '{task_id}'...")

            try:
                # 1. Wake up / Spawn the worker via SwarmTool
                spawn_res = await self.swarm_tool.spawn_workers(
                    tasks=[{"id": task_id, "prompt": task["prompt"], "context": task["context"]}],
                    agent_type=task["agent_type"]
                )
                self.logger.info(f"Heartbeat: Worker spawned for task '{task_id}'. Result: {spawn_res}")

                # 2. Complete and immediately put worker back to sleep to conserve resource
                nomad_job_id = f"worker-{task_id}" # Standard job id naming convention
                self.logger.info(f"Heartbeat task completed. Putting worker node '{nomad_job_id}' back to sleep (purging Nomad job)...")

                await self.swarm_tool.kill_worker(nomad_job_id)
                self.logger.info(f"Heartbeat: Worker '{nomad_job_id}' successfully suspended and put to sleep.")

            except Exception as e:
                self.logger.error(f"Heartbeat failed to execute task '{task_id}': {e}")

    async def _check_tasks(self):
        """Polls memory for task events and manages task lifecycle."""
        if not isinstance(self.memory, PMMMemoryClient):
            # Local memory might not support get_events in the same way or isn't shared with workers
            return

        # Get recent events
        # We assume get_events returns a list of dicts.
        # We want all 'worker_started' and 'worker_result' events.
        # Optimization: In a real system, we'd use a cursor/timestamp to only get new events.
        # For now, we fetch last 100 events.
        events = await self.memory.get_events(limit=100)

        # Process events to update state
        for event in reversed(events): # Process chronological order
            kind = event.get("kind")
            meta = event.get("meta", {})
            task_id = meta.get("task_id")

            if not task_id:
                continue

            if kind == "worker_started":
                if task_id not in self.active_tasks:
                    self.active_tasks[task_id] = {
                        "start_time": event.get("timestamp"),
                        "meta": meta,
                        "status": "running",
                        "nomad_job_id": meta.get("nomad_job_id")
                    }
            elif kind == "worker_result":
                if task_id in self.active_tasks:
                    self.logger.info(f"Task {task_id} completed successfully.")
                    del self.active_tasks[task_id]

        # Check for timeouts
        now = time.time()
        tasks_to_remove = []

        for task_id, info in self.active_tasks.items():
            start_time = info.get("start_time", now)
            duration = now - start_time

            if duration > self.task_timeout:
                self.logger.warning(f"Task {task_id} timed out after {duration:.0f}s. Taking corrective action.")

                # Corrective Action: Kill the worker
                nomad_job_id = info.get("nomad_job_id")
                if nomad_job_id:
                    self.logger.info(f"Terminating stalled Nomad job {nomad_job_id} via SwarmTool...")
                    try:
                        kill_res = await self.swarm_tool.kill_worker(nomad_job_id)
                        self.logger.info(f"Kill result: {kill_res}")
                    except Exception as ke:
                        self.logger.error(f"Failed to kill stalled worker {nomad_job_id}: {ke}")
                else:
                    self.logger.warning(f"No nomad_job_id found for task {task_id}; unable to kill job directly.")

                # Trigger automated retry
                prompt = info["meta"].get("prompt")
                context = info["meta"].get("context") or ""
                if prompt:
                    self.logger.info(f"Triggering automated retry for task {task_id}...")
                    try:
                        agent_type = info["meta"].get("agent_type", "worker")
                        spawn_res = await self.swarm_tool.spawn_workers(
                            tasks=[{"id": task_id, "prompt": prompt, "context": context}],
                            agent_type=agent_type
                        )
                        self.logger.info(f"Retry spawn result: {spawn_res}")
                    except Exception as se:
                        self.logger.error(f"Failed to retry spawn for task {task_id}: {se}")
                else:
                    self.logger.warning(f"No original prompt context found for task {task_id}; skipping automated retry.")

                self.logger.info(f"Marking task {task_id} as failed/timed-out in monitoring.")
                tasks_to_remove.append(task_id)

        for tid in tasks_to_remove:
            del self.active_tasks[tid]
