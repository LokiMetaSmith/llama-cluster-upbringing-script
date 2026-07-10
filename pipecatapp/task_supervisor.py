import asyncio
import logging
import time
from typing import Dict, Any
from tools.swarm_tool import SwarmTool
from pmm_memory_client import PMMMemoryClient

class TaskSupervisor:
    """
    Monitors the progress of spawned worker tasks by polling the Shared Memory.
    If a task takes too long without a result, it intervenes (kills and optionally retries).
    """
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.logger = logging.getLogger(__name__)
        self.swarm_tool = self.twin_service.tools.get("swarm") or SwarmTool()
        self.memory = self.twin_service.long_term_memory
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.check_interval = 30  # seconds
        self.task_timeout = 300   # seconds (5 minutes)

    async def start(self):
        """Starts the background monitoring loop."""
        self.logger.info("TaskSupervisor monitoring loop started.")
        while True:
            try:
                await self._check_tasks()
            except Exception as e:
                self.logger.error(f"TaskSupervisor error: {e}")
            await asyncio.sleep(self.check_interval)

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
