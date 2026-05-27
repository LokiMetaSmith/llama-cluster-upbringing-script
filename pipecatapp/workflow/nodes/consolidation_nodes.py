from typing import Any, List
from .registry import registry
from ..node import Node
from ..context import WorkflowContext
import os
import json
import httpx
try:
    from ...memory import MemoryStore
except ImportError:
    from memory import MemoryStore

@registry.register
class ContinuousConsolidationNode(Node):
    """
    A durable, background node that polls for unconsolidated memories
    and connects them into cross-cutting insights.
    """
    async def execute(self, context: WorkflowContext):
        # 1. Fetch MemoryStore
        memory_store = context.global_inputs.get("memory_store")
        if not memory_store:
            memory_store = MemoryStore()

        # 2. Extract configuration
        limit = self.config.get("config", {}).get("limit", 10)
        llm_base_url = os.getenv("LLM_BASE_URL", f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8081/v1")

        # 3. Get unconsolidated memories
        unconsolidated = memory_store.get_unconsolidated_memories(limit=limit)

        if not unconsolidated or len(unconsolidated) == 0:
            self.set_output(context, "consolidated_count", 0)
            self.set_output(context, "insight", "No memories to consolidate.")
            return

        # 4. Formulate the consolidation prompt
        memories_text = ""
        memory_ids = []
        for mem in unconsolidated:
            memory_ids.append(mem["id"])
            summary = mem.get("summary") or mem.get("raw_text") or ""
            memories_text += f"- ID {mem['id']}: {summary}\n"

        system_prompt = (
            "You are a background consolidation agent. Review the following unconsolidated memories, "
            "identify common themes or connections, and generate a single cohesive insight that summarizes them. "
            "Return only the insight text."
        )

        # 5. Call LLM for insight
        chat_url = f"{llm_base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "default",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": memories_text}
            ],
            "temperature": 0.2
        }

        insight = "Failed to generate insight."
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(chat_url, headers=headers, json=payload, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    insight = data["choices"][0]["message"]["content"]
        except Exception as e:
            self.set_output(context, "consolidated_count", 0)
            self.set_output(context, "insight", f"Error during LLM consolidation: {e}")
            return

        # 6. Save the new consolidation and mark memories as consolidated
        short_summary = f"Consolidation of {len(unconsolidated)} memories"
        memory_store.add_consolidation(source_ids=memory_ids, summary=short_summary, insight=insight)

        for mem_id in memory_ids:
            memory_store.mark_memory_consolidated(mem_id)

        self.set_output(context, "consolidated_count", len(unconsolidated))
        self.set_output(context, "insight", insight)
