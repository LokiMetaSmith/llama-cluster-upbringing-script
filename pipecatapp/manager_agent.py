import os
import sys
import logging
import asyncio
import httpx
import json
import time
from typing import List, Dict, Any
from tools.swarm_tool import SwarmTool
from agent_factory import create_tools
from pmm_memory_client import PMMMemoryClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ManagerAgent")

class ManagerAgent:
    def __init__(self):
        self.task_id = os.getenv("MANAGER_TASK_ID", "manager-root")
        self.prompt = os.getenv("MANAGER_PROMPT")
        self.context = os.getenv("MANAGER_CONTEXT", "")
        self.llm_base_url = None
        self.memory_url = None
        self.memory_client = None
        self.swarm_tool = None
        # Gas Town: We might have a root work item ID for the manager task itself
        self.root_work_item_id = os.getenv("WORK_ITEM_ID")
        
    def discover_services(self):
        """Discovers services via Consul."""
        consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
        try:
            # Discover LLM
            llm_service_name = os.getenv("LLAMA_API_SERVICE_NAME", "router-api")
            resp = httpx.get(f"{consul_addr}/v1/catalog/service/{llm_service_name}")
            if resp.status_code == 200:
                services = resp.json()
                if services:
                    svc = services[0]
                    self.llm_base_url = f"http://{svc['ServiceAddress']}:{svc['ServicePort']}/v1"
                    logger.info(f"Discovered LLM Service at {self.llm_base_url}")

            # Discover Memory
            resp = httpx.get(f"{consul_addr}/v1/catalog/service/memory-service")
            if resp.status_code == 200:
                services = resp.json()
                if services:
                    svc = services[0]
                    self.memory_url = f"http://{svc['ServiceAddress']}:{svc['ServicePort']}"
                    self.memory_client = PMMMemoryClient(base_url=self.memory_url)
                    logger.info(f"Discovered Memory Service at {self.memory_url}")
                    
        except Exception as e:
            logger.warning(f"Service discovery warning: {e}")

    async def call_llm(self, messages: List[Dict[str, str]]) -> str:
        """Calls the LLM."""
        if not self.llm_base_url:
            return "Mock LLM Response"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.llm_base_url}/chat/completions",
                    json={"model": "gpt-4", "messages": messages, "temperature": 0.1},
                    timeout=120.0
                )
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except Exception as e:
                logger.error(f"LLM call failed: {e}")
                return "{}"

    async def get_agent_suitability(self, agent_id: str, tag: str) -> str:
        """
        Queries the agent's work history stats to determine suitability.
        This implements the 'Agent CV' logic from Gas Town.
        """
        if not self.memory_client:
            return "Stats unavailable"

        try:
            stats = await self.memory_client.get_agent_stats(agent_id)
            if not stats:
                 return "New Agent (No history)"

            total = stats.get("total_tasks", 0)
            success = stats.get("success_rate", 0)

            return f"History: {total} tasks, {success}% success rate."
        except Exception as e:
            logger.warning(f"Failed to fetch stats for {agent_id}: {e}")
            return "Stats error"

    async def map_phase(self) -> List[Dict]:
        """Analyzes the task and splits it into sub-tasks."""
        logger.info("PHASE 1: Map - Decomposing Task")
        
        system_prompt = (
            "You are a Project Manager. "
            "Break down the user's request into parallelizable sub-tasks for Technician Agents. "
            "Return ONLY a JSON list of objects, each with 'id' (short string), 'prompt' (instruction), and 'context' (data). "
            "Example: [{\"id\": \"db-mig\", \"prompt\": \"Migrate DB\", \"context\": \"...\"}]"
        )
        
        msgs = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Request: {self.prompt}\nContext: {self.context}"}
        ]
        
        response = await self.call_llm(msgs)
        try:
            # Simple cleanup to find JSON list
            start = response.find("[")
            end = response.rfind("]") + 1
            json_str = response[start:end]
            subtasks = json.loads(json_str)
            logger.info(f"Generated {len(subtasks)} sub-tasks.")
            return subtasks
        except Exception as e:
            logger.error(f"Failed to parse subtasks: {e} | Response: {response}")
            return []

    async def dispatch_phase(self, subtasks: List[Dict]):
        """Dispatches sub-tasks to Technician Agents."""
        logger.info("PHASE 2: Dispatch - Spawning Technicians")
        self.swarm_tool = SwarmTool()
        
        # Gas Town Integration: Check stats for potential assignees (simulated)
        # In a real dynamic dispatch, we'd query available agents.
        # Here we just log the stats for a hypothetical 'technician_default' to prove the loop.
        stats_info = await self.get_agent_suitability("technician_default", "general")
        logger.info(f"Candidate Agent Stats: {stats_info}")

        # We assume the sub-tasks are fit for Technician Agents (Plan-Execute-Reflect)
        result = await self.swarm_tool.spawn_workers(subtasks, agent_type="technician")
        logger.info(result)
        
        # In a real system, we would get back Job IDs to monitor.
        # SwarmTool returns a string summary currently. 
        # For this implementation, we will assume we wait for events in the Memory Service.
        return [t['id'] for t in subtasks]

    async def reduce_phase(self, task_ids: List[str]) -> str:
        """Waits for results and aggregates them using targeted task polling."""
        logger.info(f"PHASE 3: Reduce - Aggregating Results for tasks: {task_ids}")
        
        results = {}
        start_time = time.time()
        timeout = 600 # 10 minutes
        
        while len(results) < len(task_ids):
            if time.time() - start_time > timeout:
                logger.warning("Timeout waiting for sub-tasks.")
                break
                
            # Poll Memory Service for "worker_result" events
            # In a real impl, we'd filter by task_id. 
            # Here we simulate or mock if no memory service.
            if self.memory_url:
                try:
                    async with httpx.AsyncClient() as client:
                        # Iterate through pending tasks and check their status specifically
                        # This avoids race conditions where an event might be missed in the global feed
                        # if the limit is exceeded.
                        for tid in task_ids:
                            if tid in results:
                                continue

                            # Call the new /tasks/{task_id} endpoint
                            resp = await client.get(f"{self.memory_url}/tasks/{tid}")
                            if resp.status_code == 200:
                                events = resp.json()
                                # Look for a result event
                                for evt in events:
                                    if evt.get("kind") == "worker_result":
                                        results[tid] = evt.get("content")
                                        logger.info(f"Received result for {tid}")
                                        break
                                    elif evt.get("kind") == "worker_failure":
                                        results[tid] = f"FAILURE: {evt.get('content')}"
                                        logger.error(f"Task {tid} failed: {evt.get('content')}")
                                        break
                except Exception as e:
                    logger.warning(f"Error polling memory service: {e}")
            
            await asyncio.sleep(5)
            
        # Aggregate
        aggregation_prompt = (
            "You are a Project Manager. "
            "Aggregate the following sub-task results into a final report.\n\n"
        )
        for tid, res in results.items():
            aggregation_prompt += f"Task {tid}: {res}\n"
            
        if not results:
            return "No results received from workers."
            
        msgs = [{"role": "user", "content": aggregation_prompt}]
        final_report = await self.call_llm(msgs)
        return final_report

    async def verify_phase(self, target_result: str) -> str:
        """Dispatches a Judge Agent to verify the result."""
        logger.info("PHASE 4: Verification")

        judge_task_id = f"judge-{self.task_id}"

        # Dispatch Judge
        judge_task = [{
            "id": judge_task_id,
            "prompt": "Verify the quality and correctness of the provided result.",
            "context": target_result[:2000], # Truncate if too long, or pass pointer
            "target_task_id": self.task_id, # Logic to let judge pull it
            "target_work_item_id": self.root_work_item_id # Gas Town: Link validation to the ledger
        }]

        if not self.swarm_tool:
            self.swarm_tool = SwarmTool()

        await self.swarm_tool.spawn_workers(judge_task, agent_type="judge")

        # Wait for Judge Result
        verdict = "VERDICT: PASS (Default)" # Fallback

        # Similar polling loop
        # Ideally we refactor polling into a helper, but duplicating for safety now
        start_time = time.time()
        timeout = 300

        while time.time() - start_time < timeout:
            if self.memory_url:
                 try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(f"{self.memory_url}/tasks/{judge_task_id}")
                        if resp.status_code == 200:
                            events = resp.json()
                            for evt in events:
                                if evt.get("kind") == "judge_pass":
                                    logger.info("Verification Passed!")
                                    return f"VERIFICATION PASSED: {evt.get('content')}"
                                elif evt.get("kind") == "judge_fail":
                                    logger.warning("Verification Failed!")
                                    return f"VERIFICATION FAILED: {evt.get('content')}"
                 except Exception:
                     pass
            await asyncio.sleep(5)

        logger.warning("Verification timed out.")
        return "VERIFICATION TIMEOUT"

    async def run(self):
        logger.info(f"Starting Manager Agent for {self.task_id}")
        if not self.prompt:
            logger.error("No MANAGER_PROMPT. Exiting.")
            sys.exit(1)
            
        self.discover_services()
        
        # 1. Map
        subtasks = await self.map_phase()
        if not subtasks:
            logger.error("No subtasks generated.")
            sys.exit(1)
            
        # 2. Dispatch
        task_ids = await self.dispatch_phase(subtasks)
        
        # 3. Reduce
        final_report = await self.reduce_phase(task_ids)
        
        # 4. Verify
        # We temporarily store the report to memory so Judge can fetch it by ID
        if self.memory_url:
             try:
                async with httpx.AsyncClient() as client:
                    await client.post(f"{self.memory_url}/events", json={
                        "kind": "manager_result", # Intermediate result
                        "content": final_report,
                        "meta": {"task_id": self.task_id}
                    })
             except Exception: pass

        verification_result = await self.verify_phase(final_report)
        logger.info(f"Verification Result: {verification_result}")

        final_output = f"{final_report}\n\n{verification_result}"

        logger.info("FINAL REPORT:")
        print(final_output)
        
        # Final Report completion
        if self.memory_url:
             try:
                async with httpx.AsyncClient() as client:
                    await client.post(f"{self.memory_url}/events", json={
                        "kind": "manager_complete", # Distinction from intermediate result
                        "content": final_output,
                        "meta": {"task_id": self.task_id}
                    })
             except Exception as e:
                 logger.error(f"Failed to report manager result: {e}")

if __name__ == "__main__":
    agent = ManagerAgent()
    asyncio.run(agent.run())
