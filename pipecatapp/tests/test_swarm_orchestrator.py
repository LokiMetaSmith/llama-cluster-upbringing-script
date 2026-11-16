"""Integration tests for NPCSwarmTool, SwarmTool delegation, and agent_factory registration."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import yaml

from pipecatapp.agent_factory import TOOL_CLASS_MAP
from pipecatapp.swarm_orchestrator import ClusterActionPlan, RemediationAction
from pipecatapp.tools.npc_swarm_tool import NPCSwarmTool
from pipecatapp.tools.swarm_tool import SwarmTool

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_npc_swarm_tool_registered_in_factory():
    assert "NPCSwarmTool" in TOOL_CLASS_MAP
    tool = NPCSwarmTool(team_dir=str(REPO_ROOT / "npc_team"))
    schema = tool.get_schema()
    assert schema["function"]["name"] == "npc_swarm"
    assert set(schema["function"]["parameters"]["properties"]["action"]["enum"]) == {
        "run_swarm_cycle",
        "dispatch_jinx",
        "collect_metrics",
        "recent_operator_files",
    }


def test_npc_swarm_tool_execute_actions(tmp_path):
    tool = NPCSwarmTool(
        team_dir=str(REPO_ROOT / "npc_team"),
        local_db_dir=str(tmp_path),
    )

    assert "required" in tool.execute("run_swarm_cycle")
    assert "required" in tool.execute("dispatch_jinx")
    assert "required" in tool.execute("collect_metrics")
    assert "Unknown action" in tool.execute("nonexistent")

    plan = ClusterActionPlan(
        cluster_health="healthy",
        actions=[
            RemediationAction(
                target_node="worker-01",
                action="ignore",
                priority=5,
                rationale="Nominal",
            )
        ],
    )
    with patch("pipecatapp.tools.npc_swarm_tool.run_swarm_cycle", return_value=plan):
        out = tool.execute("run_swarm_cycle", telemetry_snapshot="node=worker-01 ok")
        parsed = json.loads(out)
        assert parsed["cluster_health"] == "healthy"

    assert (
        tool.execute(
            "dispatch_jinx",
            node_host="worker-01",
            remediation_action="ignore",
            priority=5,
        )
        == "no-op"
    )

    with patch("pipecatapp.tools.npc_swarm_tool.collect_node_metrics", return_value="node=worker-01 ok") as mock_collect:
        metrics = tool.execute("collect_metrics", node_host="worker-01", probe_scope="memory")
        assert metrics == "node=worker-01 ok"
        mock_collect.assert_called_once()


def test_swarm_tool_delegates_hybrid_actions():
    swarm_tool = SwarmTool()
    with patch("pipecatapp.tools.npc_swarm_tool.NPCSwarmTool.execute", return_value="delegated-ok") as mock_exec:
        res = swarm_tool.execute("collect_metrics", node_host="worker-01")
        assert res == "delegated-ok"
        mock_exec.assert_called_once_with("collect_metrics", node_host="worker-01")


def test_npc_swarm_workflow_yaml_valid():
    workflow_path = REPO_ROOT / "workflows" / "npc_swarm_orchestration.yaml"
    data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    assert data["name"] == "npc_swarm_orchestration"
    assert len(data["nodes"]) == 3


def test_npc_swarm_and_swarm_tool_recent_operator_files(tmp_path):
    sample_records = [{"full_path": "/opt/pipecatapp/npc_team/cluster.ctx", "action": "click"}]
    tool = NPCSwarmTool(team_dir=str(REPO_ROOT / "npc_team"), local_db_dir=str(tmp_path))

    with patch("pipecatapp.tools.npc_swarm_tool.query_psychic_recent_files", return_value=sample_records) as mock_q:
        raw = tool.execute("recent_operator_files", db_path=str(tmp_path / "events.db"), limit=5)
        parsed = json.loads(raw)
        assert parsed["recent_files"] == sample_records
        mock_q.assert_called_once()

    swarm_tool = SwarmTool()
    with patch("pipecatapp.tools.npc_swarm_tool.collect_node_operator_focus", return_value='{"recent_files":[]}') as mock_remote:
        remote_out = swarm_tool.execute("recent_operator_files", node_host="controller-01", limit=3)
        assert '"recent_files":[]' in remote_out
        mock_remote.assert_called_once_with(
            node_host="controller-01",
            team_dir="./npc_team",
            limit=3,
        )
