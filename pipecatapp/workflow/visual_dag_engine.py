import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pipecatapp.workflow.routing_and_delegation import (
    HybridModelRouter,
    MessageEnvelope,
    WorktreeDelegationManager,
)


@dataclass
class VisualWorkflowNode:
    id: str
    label: str
    node_type: str  # "orchestrator" | "router_gate" | "worktree_subagent" | "critic" | "barrier_merge"
    profile: str
    route: str
    isolate_worktree: bool = False
    depends_on: List[str] = field(default_factory=list)
    instruction: str = ""
    status: str = "IDLE"  # IDLE | RUNNING | COMPLETED | FALLBACK | FAILED
    resolved_model: str = "pending"
    resolved_tier: str = "pending"


@dataclass
class VisualCommEdge:
    source: str
    target: str
    channel_type: str  # "ROUTE_DISPATCH" | "WORKTREE_SPAWN" | "ARTIFACT_RETURN" | "CRITIQUE_FEEDBACK"
    payload_schema: str
    active: bool = False
    last_message_preview: str = ""


class VisualWorkflowDAG:
    def __init__(self, name: str, router: HybridModelRouter, worktree_mgr: WorktreeDelegationManager):
        self.name = name
        self.router = router
        self.worktree_mgr = worktree_mgr
        self.nodes: Dict[str, VisualWorkflowNode] = {}
        self.edges: List[VisualCommEdge] = []
        self.message_log: List[MessageEnvelope] = []

    def add_node(self, node: VisualWorkflowNode):
        self.nodes[node.id] = node

    def add_edge(self, edge: VisualCommEdge):
        self.edges.append(edge)

    def record_communication(self, source: str, target: str, payload: Dict[str, Any]):
        node = self.nodes[target]
        env = MessageEnvelope(
            edge_id=f"{source}->{target}",
            source_node=source,
            target_node=target,
            profile=node.profile,
            model_route=node.route,
            payload=payload,
        )
        self.message_log.append(env)
        for e in self.edges:
            if e.source == source and e.target == target:
                e.active = True
                preview = str(payload.get("summary") or payload.get("task") or "")[:48]
                e.last_message_preview = preview.replace('"', "'")

    async def execute_dag(self, initial_prompt: str) -> Dict[str, Any]:
        completed_outputs: Dict[str, Dict[str, Any]] = {}
        pending = set(self.nodes.keys())

        while pending:
            ready = [
                nid for nid in pending
                if all(dep in completed_outputs for dep in self.nodes[nid].depends_on)
            ]
            if not ready:
                raise RuntimeError("Cycle or unsatisfied dependency detected in workflow DAG.")

            tasks = [self._run_single_node(nid, initial_prompt, completed_outputs) for nid in ready]
            results = await asyncio.gather(*tasks)

            for nid, res in zip(ready, results):
                completed_outputs[nid] = res
                pending.remove(nid)

        return completed_outputs

    async def _run_single_node(
        self, nid: str, root_prompt: str, upstream_outputs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        node = self.nodes[nid]
        node.status = "RUNNING"

        upstream_context = "\n\n".join(
            f"--- Output from [{dep}] (Model: {upstream_outputs[dep].get('model_used')}) ---\n"
            f"{upstream_outputs[dep].get('summary', '')}"
            for dep in node.depends_on
        )
        full_prompt = f"{node.instruction}\n\n[ROOT GOAL]: {root_prompt}\n\n{upstream_context}".strip()

        if node.isolate_worktree:
            res = await self.worktree_mgr.execute_in_worktree(
                parent_node=node.depends_on[0] if node.depends_on else "root",
                subagent_id=node.id,
                task_prompt=full_prompt,
                router=self.router,
                profile_name=node.profile,
                override_route=node.route,
            )
        else:
            llm_out = await self.router.complete(
                node_id=node.id,
                profile_name=node.profile,
                messages=[{"role": "user", "content": full_prompt}],
                override_route=node.route,
            )
            res = {
                "subagent_id": node.id,
                "summary": llm_out["content"],
                "model_used": llm_out["model_used"],
                "tier_used": llm_out["tier_used"],
            }

        node.resolved_model = res["model_used"]
        node.resolved_tier = res["tier_used"]
        node.status = "FALLBACK" if res["tier_used"] == "fallback" else "COMPLETED"

        for edge in self.edges:
            if edge.source == nid:
                self.record_communication(nid, edge.target, res)

        return res

    def to_mermaid(self) -> str:
        lines = [
            "flowchart TD",
            "  classDef localTier fill:#113f2b,stroke:#2ea043,color:#fff,stroke-width:2px;",
            "  classDef cloudFallback fill:#4a2b0f,stroke:#d29922,color:#fff,stroke-width:2px;",
            "  classDef worktreeBox fill:#162944,stroke:#58a6ff,color:#fff,stroke-dasharray: 5 5;",
        ]
        for nid, n in self.nodes.items():
            wt_badge = " [git-worktree]" if n.isolate_worktree else ""
            label = (
                f"<b>{n.label}</b>{wt_badge}<br/>"
                f"Profile: {n.profile}<br/>"
                f"Route: {n.route} ({n.resolved_model})<br/>"
                f"Tier: {n.resolved_tier} | Status: {n.status}"
            )
            shape_open, shape_close = ("{{", "}}") if n.node_type == "router_gate" else ("([", "])") if n.isolate_worktree else ("[", "]")
            lines.append(f'  {nid}{shape_open}"{label}"{shape_close}')

            if n.resolved_tier == "fallback":
                lines.append(f"  class {nid} cloudFallback;")
            elif n.isolate_worktree:
                lines.append(f"  class {nid} worktreeBox;")
            else:
                lines.append(f"  class {nid} localTier;")

        for e in self.edges:
            arrow = "==>" if e.active else "-->"
            edge_label = f"{e.channel_type}: {e.payload_schema}"
            if e.last_message_preview:
                edge_label += f" | '{e.last_message_preview}...'"
            lines.append(f'  {e.source} {arrow}|"{edge_label}"| {e.target}')

        return "\n".join(lines)

    def to_reactflow_json(self) -> Dict[str, Any]:
        return {
            "workflow_name": self.name,
            "nodes": [
                {
                    "id": n.id,
                    "type": n.node_type,
                    "data": {
                        "label": n.label,
                        "profile": n.profile,
                        "route": n.route,
                        "isolate_worktree": n.isolate_worktree,
                        "resolved_model": n.resolved_model,
                        "resolved_tier": n.resolved_tier,
                        "status": n.status,
                    },
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "id": f"{e.source}-{e.target}",
                    "source": e.source,
                    "target": e.target,
                    "animated": e.active,
                    "label": f"{e.channel_type} ({e.payload_schema})",
                    "data": {"preview": e.last_message_preview},
                }
                for e in self.edges
            ],
        }
