import json
import logging
import asyncio
import httpx
import re

class PlannerTool:
    """
    A meta-tool that plans a complex task using the ProjectMapper and executes it
    by dispatching multiple workers via the SwarmTool.
    """
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.logger = logging.getLogger(__name__)

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
        # We construct a prompt manually here.
        prompt = f"""
        You are a Senior Architect.
        Goal: {goal}

        Codebase Map:
        {context_summary}

        Decompose this goal into a list of parallelizable sub-tasks for worker agents.
        Each task should focus on a specific file or service if possible.

        Respond ONLY with a JSON list of objects. No markdown formatting.
        Format:
        [
            {{"id": "task_1", "prompt": "Detailed instruction for worker...", "context": "Relevant file paths or info"}}
        ]
        """

        plan = []
        llm_base_url = getattr(self.twin_service, 'llm_base_url', None)

        if llm_base_url:
            self.logger.info(f"Using LLM at {llm_base_url} for planning.")
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        f"{llm_base_url}/chat/completions",
                        json={
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.2, # Low temperature for structured output
                            "max_tokens": 1024,
                            "stream": False
                        }
                    )
                    response.raise_for_status()
                    result_json = response.json()

                    # Ensure result_json is a dict and has 'choices'
                    if isinstance(result_json, dict) and "choices" in result_json:
                         content = result_json['choices'][0]['message']['content']

                         # Clean up content if it contains markdown code blocks
                         content = re.sub(r'```json\s*', '', content)
                         content = re.sub(r'```\s*', '', content).strip()

                         try:
                             plan = json.loads(content)
                             self.logger.info(f"LLM generated plan: {plan}")
                         except json.JSONDecodeError as e:
                             self.logger.error(f"Failed to decode LLM JSON response: {e}. Content: {content}")
                    else:
                        self.logger.error(f"Unexpected LLM response format: {result_json}")

            except Exception as e:
                self.logger.error(f"Error calling LLM for planning: {e}")
                # Fallback handled below
        else:
             self.logger.warning("No LLM base URL available. Falling back to heuristic planning.")

        # Fallback if plan is still empty
        if not plan:
            self.logger.info("Using heuristic fallback plan.")
            if "swarmer" in goal.lower() or "test" in goal.lower():
                 plan.append({"id": "task_1", "prompt": "Check frontend files", "context": str(files_list[:10])})
                 plan.append({"id": "task_2", "prompt": "Check backend files", "context": str(files_list[10:20])})
            else:
                 plan.append({"id": "default_task", "prompt": f"Analyze goal: {goal}", "context": "all files"})

        # 3. Dispatch to Swarm
        swarm = self.twin_service.tools.get("swarm")
        if not swarm:
            return "Error: SwarmTool not available."

        result = await swarm.spawn_workers(plan)
        return f"Planner executed.\nPlan: {json.dumps(plan)}\nResult: {result}"
