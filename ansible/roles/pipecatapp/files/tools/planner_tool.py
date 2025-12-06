import json
import logging
import asyncio
import httpx

class PlannerTool:
    """
    A meta-tool that plans a complex task using the ProjectMapper and executes it
    by dispatching multiple workers via the SwarmTool.
    """
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.logger = logging.getLogger(__name__)

    async def _discover_llm_url(self):
        """Discovers the LLM service URL."""
        # Try to find base_url in existing router_llm if available
        if hasattr(self.twin_service, 'router_llm') and hasattr(self.twin_service.router_llm, '_client'):
             try:
                 return str(self.twin_service.router_llm._client.base_url)
             except Exception:
                 pass

        # Fallback to Consul discovery
        try:
            consul_addr = getattr(self.twin_service, 'consul_http_addr', 'http://localhost:8500')
            # Use app_config to get service name
            app_config = getattr(self.twin_service, 'app_config', {})
            service_name = app_config.get("llama_api_service_name", "llamacpp-rpc-api")

            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{consul_addr}/v1/health/service/{service_name}?passing")
                if resp.status_code == 200:
                    services = resp.json()
                    if services:
                        addr = services[0]['Service']['Address']
                        port = services[0]['Service']['Port']
                        return f"http://{addr}:{port}/v1"
        except Exception as e:
            self.logger.warning(f"Failed to discover LLM via Consul: {e}")

        # Final fallback
        return "http://localhost:8000/v1"

    async def _call_llm(self, prompt: str) -> list:
        """Calls the LLM to generate a plan."""
        base_url = await self._discover_llm_url()
        url = f"{base_url}/chat/completions"

        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "gpt-4", # Placeholder, usually ignored by local LLMs or maps to loaded model
            "messages": [
                {"role": "system", "content": "You are a Senior Architect. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1000
        }

        try:
            async with httpx.AsyncClient() as client:
                self.logger.info(f"Calling LLM at {url}")
                response = await client.post(url, json=payload, headers=headers, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                content = data['choices'][0]['message']['content']

                # Attempt to parse JSON from content (it might be wrapped in markdown code blocks)
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]

                return json.loads(content.strip())
        except Exception as e:
            self.logger.error(f"LLM planning failed: {e}")
            return None

    async def plan_and_execute(self, goal: str) -> str:
        """
        Analyzes the goal, maps the codebase, creates a plan, and dispatches workers.
        """
        self.logger.info(f"Planner started for goal: {goal}")

        # 1. Get Codebase Context
        mapper = self.twin_service.tools.get("project_mapper")
        if not mapper:
            return "Error: ProjectMapperTool not available."

        project_map = mapper.scan()
        # Summarize map to avoid token limits (naively for now)
        files_list = [f['path'] for f in project_map.get('files', [])]
        context_summary = f"Root: {project_map.get('root')}\nFiles: {', '.join(files_list[:100])}"
        if len(files_list) > 100:
            context_summary += f"... (+{len(files_list)-100} more)"

        # 2. Ask LLM to create a plan
        prompt = f"""
        Goal: {goal}

        Codebase Map:
        {context_summary}

        Decompose this goal into a list of parallelizable sub-tasks for worker agents.
        Each task should focus on a specific file or service if possible.

        Respond ONLY with a JSON list of objects.
        Format:
        [
            {{"id": "task_1", "prompt": "Detailed instruction for worker...", "context": "Relevant file paths or info"}}
        ]
        """

        plan = await self._call_llm(prompt)

        if not plan:
            self.logger.warning("Falling back to heuristic plan.")
            plan = []
            if "swarmer" in goal.lower() or "test" in goal.lower():
                 plan.append({"id": "task_1", "prompt": "Check frontend files", "context": str(files_list[:10])})
                 plan.append({"id": "task_2", "prompt": "Check backend files", "context": str(files_list[10:20])})
            else:
                 # Default plan
                 plan.append({"id": "default_task", "prompt": f"Analyze goal: {goal}", "context": "all files"})

        # 3. Dispatch to Swarm
        swarm = self.twin_service.tools.get("swarm")
        if not swarm:
            return "Error: SwarmTool not available."

        result = await swarm.spawn_workers(plan)
        return f"Planner executed.\nPlan: {json.dumps(plan)}\nResult: {result}"
