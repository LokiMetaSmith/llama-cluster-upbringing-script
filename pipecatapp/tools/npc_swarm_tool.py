"""Pipecat agent tool wrapping npcpy swarm orchestration and npcsh .jinx dispatch."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional

from pipecatapp.swarm_orchestrator import (
    RemediationAction,
    collect_node_metrics,
    collect_node_operator_focus,
    dispatch_node_jinx,
    load_swarm_from_team_dir,
    query_psychic_recent_files,
    run_swarm_cycle,
)

logger = logging.getLogger(__name__)


class NPCSwarmTool:
    """Tool for running local npcpy map-reduce swarm cycles and npcsh/npcrs .jinx actions."""

    def __init__(
        self,
        team_dir: Optional[str] = None,
        local_db_dir: Optional[str] = None,
    ) -> None:
        self.name = "npc_swarm"
        self.description = (
            "Orchestrate local npcpy multi-node swarm evaluation and dispatch "
            "node-level npcsh/npcrs .jinx remediation and telemetry actions."
        )
        self.team_dir: str = team_dir or os.getenv("NPC_TEAM_DIR") or "./npc_team"
        self.local_db_dir: str = local_db_dir or os.getenv("NPCPY_DB_DIR") or "/var/tmp"

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": [
                                "run_swarm_cycle",
                                "dispatch_jinx",
                                "collect_metrics",
                                "recent_operator_files",
                            ],
                            "description": "Swarm orchestration or node .jinx action to execute.",
                        },
                        "telemetry_snapshot": {
                            "type": "string",
                            "description": "Cluster telemetry snapshot text for run_swarm_cycle.",
                        },
                        "node_host": {
                            "type": "string",
                            "description": "Target worker hostname or IP for dispatch_jinx / collect_metrics.",
                        },
                        "remediation_action": {
                            "type": "string",
                            "enum": ["drain", "restart_worker", "rebalance_shards", "ignore"],
                            "description": "Remediation action for dispatch_jinx.",
                        },
                        "priority": {
                            "type": "integer",
                            "description": "Priority level 1 (highest) to 5 (lowest).",
                        },
                        "rationale": {
                            "type": "string",
                            "description": "Reason for dispatching the remediation action.",
                        },
                        "target_service": {
                            "type": "string",
                            "description": "Optional target service name on the worker node.",
                        },
                        "probe_scope": {
                            "type": "string",
                            "description": "Scope for collect_metrics (e.g. 'all', 'memory', 'network').",
                        },
                        "node_id": {
                            "type": "string",
                            "description": "Optional node identifier for isolated SQLite db_path naming.",
                        },
                        "db_path": {
                            "type": "string",
                            "description": "Optional path to psychic events.db for recent_operator_files.",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Max recent operator paths to return (default 10).",
                        },
                        "include_dirs": {
                            "type": "boolean",
                            "description": "Whether to include directory visits in recent_operator_files.",
                        },
                    },
                    "required": ["action"],
                },
            },
        }

    def execute(self, action: str, **kwargs: Any) -> str:
        """Execute a swarm orchestration or node .jinx operation."""
        params = kwargs.get("kwargs", kwargs)
        if not isinstance(params, dict):
            params = {}

        if action == "run_swarm_cycle":
            telemetry_snapshot = str(params.get("telemetry_snapshot") or "")
            if not telemetry_snapshot.strip():
                return "Error: 'telemetry_snapshot' is required for run_swarm_cycle."
            node_id = params.get("node_id")
            coordinator, workers = load_swarm_from_team_dir(
                team_dir=self.team_dir,
                local_db_dir=self.local_db_dir,
                node_id=str(node_id) if node_id else None,
            )
            plan = run_swarm_cycle(telemetry_snapshot, coordinator, workers)
            logger.info(
                "Swarm cycle complete: health=%s actions=%d",
                plan.cluster_health,
                len(plan.actions),
            )
            return plan.model_dump_json()

        if action == "dispatch_jinx":
            node_host = str(params.get("node_host") or "")
            if not node_host:
                return "Error: 'node_host' is required for dispatch_jinx."
            remediation_action = str(params.get("remediation_action") or "ignore")
            priority = int(params.get("priority") or 3)
            rationale = str(params.get("rationale") or "Dispatched via NPCSwarmTool")
            target_service = params.get("target_service")
            remediation = RemediationAction(
                target_node=node_host,
                action=remediation_action,  # type: ignore[arg-type]
                priority=priority,
                rationale=rationale,
            )
            return dispatch_node_jinx(
                node_host=node_host,
                action=remediation,
                team_dir=self.team_dir,
                target_service=str(target_service) if target_service else None,
            )

        if action == "collect_metrics":
            node_host = str(params.get("node_host") or "")
            if not node_host:
                return "Error: 'node_host' is required for collect_metrics."
            probe_scope = str(params.get("probe_scope") or "all")
            return collect_node_metrics(
                node_host=node_host,
                team_dir=self.team_dir,
                probe_scope=probe_scope,
            )

        if action == "recent_operator_files":
            node_host = str(params.get("node_host") or "").strip()
            limit = int(params.get("limit") or 10)
            if node_host:
                return collect_node_operator_focus(
                    node_host=node_host,
                    team_dir=self.team_dir,
                    limit=limit,
                )
            db_path = params.get("db_path")
            include_dirs = bool(params.get("include_dirs", True))
            records = query_psychic_recent_files(
                db_path=str(db_path) if db_path else None,
                limit=limit,
                include_dirs=include_dirs,
            )
            return json.dumps({"recent_files": records})

        return f"Unknown action: {action}"
