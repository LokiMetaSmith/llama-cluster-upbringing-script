import pytest
import pytest_asyncio
import os
import json
import subprocess
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

import httpx

from pipecatapp.workflow.routing_and_delegation import (
    HybridModelRouter,
    WorktreeDelegationManager,
    MessageEnvelope,
)
from pipecatapp.workflow.visual_dag_engine import (
    VisualWorkflowDAG,
    VisualWorkflowNode,
    VisualCommEdge,
)


@pytest.fixture
def config_file(tmp_path):
    cfg_content = """
defaults:
  max_spawn_depth: 1
  max_concurrent_children: 10
  global_blocked_child_tools:
    - "delegate_task"
    - "clarify"

endpoints:
  local_ep:
    base_url: "http://127.0.0.1:8080/v1"
    timeout_sec: 10
  cloud_ep:
    base_url: "https://cloud.ai/v1"
    env_key: "CLOUD_API_KEY"
    timeout_sec: 15

routes:
  fast_route:
    primary:
      endpoint: local_ep
      model: "local-fast-model"
    fallback:
      endpoint: cloud_ep
      model: "cloud-fast-model"

profiles:
  orchestrator:
    soul_path: ""
    default_route: "fast_route"
    allowed_tools: ["delegate_task", "read_file"]
    can_delegate: true

  worker:
    soul_path: ""
    default_route: "fast_route"
    allowed_tools: ["delegate_task", "read_file"]
    can_delegate: false
"""
    p = tmp_path / "routing.yaml"
    p.write_text(cfg_content)
    return p


def test_router_profile_resolution(config_file):
    router = HybridModelRouter(config_file)
    res_orch = router.resolve_profile_and_route("orchestrator")
    assert res_orch["route_name"] == "fast_route"
    assert "delegate_task" in res_orch["allowed_tools"]

    res_worker = router.resolve_profile_and_route("worker")
    assert "delegate_task" not in res_worker["allowed_tools"]
    assert "read_file" in res_worker["allowed_tools"]


@pytest.mark.asyncio
async def test_router_primary_success(config_file):
    events = []
    router = HybridModelRouter(config_file, event_bus=events.append)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Primary LLM Response"}}]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        res = await router.complete(
            node_id="node_1",
            profile_name="orchestrator",
            messages=[{"role": "user", "content": "Hello"}],
        )

        assert res["content"] == "Primary LLM Response"
        assert res["model_used"] == "local-fast-model"
        assert res["tier_used"] == "primary"
        assert any(e["type"] == "MODEL_DISPATCH" and e["tier"] == "primary" for e in events)


@pytest.mark.asyncio
async def test_router_fallback_cascade(config_file):
    events = []
    router = HybridModelRouter(config_file, event_bus=events.append)

    mock_fallback_resp = MagicMock()
    mock_fallback_resp.status_code = 200
    mock_fallback_resp.json.return_value = {
        "choices": [{"message": {"content": "Fallback Cloud Response"}}]
    }
    mock_fallback_resp.raise_for_status = MagicMock()

    async def mock_post_side_effect(url, **kwargs):
        if "127.0.0.1" in url:
            raise httpx.ConnectError("Connection refused")
        return mock_fallback_resp

    with patch("httpx.AsyncClient.post", side_effect=mock_post_side_effect):
        res = await router.complete(
            node_id="node_1",
            profile_name="orchestrator",
            messages=[{"role": "user", "content": "Hello"}],
        )

        assert res["content"] == "Fallback Cloud Response"
        assert res["model_used"] == "cloud-fast-model"
        assert res["tier_used"] == "fallback"
        assert any(e["type"] == "ROUTE_FALLBACK_TRIGGERED" for e in events)


@pytest.mark.asyncio
async def test_worktree_delegation_execution(tmp_path, config_file):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo_dir, check=True)

    dummy_file = repo_dir / "README.md"
    dummy_file.write_text("# Test Repo")
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True)

    router = HybridModelRouter(config_file)
    with patch.object(router, "complete", new_callable=AsyncMock) as mock_complete:
        mock_complete.return_value = {
            "content": "Worktree Subagent Complete",
            "model_used": "local-fast-model",
            "tier_used": "primary",
        }

        wt_mgr = WorktreeDelegationManager(repo_root=repo_dir, max_concurrency=2, max_depth=1)
        res = await wt_mgr.execute_in_worktree(
            parent_node="root",
            subagent_id="subagent_a",
            task_prompt="Fix bug in repo",
            router=router,
            profile_name="worker",
        )

        assert res["subagent_id"] == "subagent_a"
        assert res["summary"] == "Worktree Subagent Complete"
        assert "hermes/subagent-" in res["branch"]


@pytest.mark.asyncio
async def test_visual_dag_execution_and_exports(config_file, tmp_path):
    router = HybridModelRouter(config_file)
    wt_mgr = WorktreeDelegationManager(repo_root=tmp_path)

    dag = VisualWorkflowDAG(name="test_dag", router=router, worktree_mgr=wt_mgr)

    n1 = VisualWorkflowNode(
        id="n1",
        label="Planner",
        node_type="orchestrator",
        profile="orchestrator",
        route="fast_route",
        instruction="Plan the task",
    )
    n2 = VisualWorkflowNode(
        id="n2",
        label="Worker",
        node_type="worktree_subagent",
        profile="worker",
        route="fast_route",
        depends_on=["n1"],
        instruction="Execute plan",
    )

    dag.add_node(n1)
    dag.add_node(n2)

    dag.add_edge(
        VisualCommEdge(
            source="n1",
            target="n2",
            channel_type="WORKTREE_SPAWN",
            payload_schema="TaskSpec",
        )
    )

    with patch.object(router, "complete", new_callable=AsyncMock) as mock_complete:
        mock_complete.return_value = {
            "content": "Step complete",
            "model_used": "local-fast-model",
            "tier_used": "primary",
        }

        results = await dag.execute_dag("Build feature X")

        assert "n1" in results
        assert "n2" in results
        assert results["n2"]["summary"] == "Step complete"

    mermaid_str = dag.to_mermaid()
    assert "flowchart TD" in mermaid_str
    assert "n1" in mermaid_str
    assert "n2" in mermaid_str

    rf_json = dag.to_reactflow_json()
    assert rf_json["workflow_name"] == "test_dag"
    assert len(rf_json["nodes"]) == 2
    assert len(rf_json["edges"]) == 1
