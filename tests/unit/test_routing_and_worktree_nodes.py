import pytest
import subprocess
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

import httpx

from pipecatapp.workflow.context import WorkflowContext
from pipecatapp.workflow.nodes.routing_and_worktree_nodes import (
    DynamicRouterNode,
    WorktreeSubagentNode,
    BarrierMergeNode,
)


def create_mock_context(nodes_config=None):
    def_dict = {"nodes": nodes_config or []}
    return WorkflowContext(def_dict)


@pytest.mark.asyncio
async def test_dynamic_router_node_consul_and_fallback(tmp_path):
    soul_file = tmp_path / "soul.md"
    soul_file.write_text("Test Soul Prompt")

    config = {
        "id": "router_1",
        "default_profile": "orchestrator",
        "profiles": {
            "orchestrator": {
                "tier": "code_specialist",
                "soul_path": str(soul_file),
                "allowed_tools": ["delegate_task", "read_file"],
                "can_delegate": False,
            }
        },
        "routes": {
            "code_specialist": {
                "consul_service": "vllm-qwen",
                "local_model": "Qwen-Local",
                "fallback_model": "Claude-Cloud",
            }
        },
        "inputs": [
            {"name": "prompt", "value": "Refactor pytest suite"},
            {"name": "profile", "value": "orchestrator"},
        ],
    }

    router_node = DynamicRouterNode(config)
    context = create_mock_context([config])

    # Mock Consul failure -> Fallback
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = httpx.ConnectError("Consul unreachable")
        await router_node.execute(context)

        route_cfg = context.node_outputs["router_1"]["route_config"]
        assert route_cfg["model"] == "Claude-Cloud"
        assert route_cfg["tier_source"] == "cloud_fallback"
        assert "delegate_task" not in route_cfg["allowed_tools"]
        assert "read_file" in route_cfg["allowed_tools"]
        assert route_cfg["soul_prompt"] == "Test Soul Prompt"

    # Mock Consul success -> Local Cluster
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{"Service": {"Address": "10.0.0.1", "Port": 8000}}]
        mock_get.return_value = mock_resp

        await router_node.execute(context)

        route_cfg = context.node_outputs["router_1"]["route_config"]
        assert route_cfg["model"] == "Qwen-Local"
        assert route_cfg["base_url"] == "http://10.0.0.1:8000/v1"
        assert route_cfg["tier_source"] == "cluster_local"


@pytest.mark.asyncio
async def test_worktree_subagent_node_execution(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo_dir, check=True)

    dummy_file = repo_dir / "README.md"
    dummy_file.write_text("# Test Repo")
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True)

    route_cfg = {
        "model": "test-model",
        "tier_source": "cluster_local",
        "base_url": "http://127.0.0.1:8080/v1",
        "soul_prompt": "System Prompt",
        "allowed_tools": ["read_file"],
    }

    config = {
        "id": "wt_node",
        "verify_cmd": "",
        "inputs": [
            {"name": "route_config", "value": route_cfg},
            {"name": "task_prompt", "value": "Fix bug"},
        ],
    }

    node = WorktreeSubagentNode(config)
    context = create_mock_context([config])
    context.global_inputs["repo_root"] = str(repo_dir)

    mock_llm_resp = MagicMock()
    mock_llm_resp.status_code = 200
    mock_llm_resp.json.return_value = {
        "choices": [{"message": {"content": "Subagent code changes complete"}}]
    }
    mock_llm_resp.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_llm_resp

        await node.execute(context)

        env = context.node_outputs["wt_node"]["artifact_envelope"]
        assert env["source_node"] == "wt_node"
        assert env["summary"] == "Subagent code changes complete"
        assert env["verification_passed"] is True


@pytest.mark.asyncio
async def test_barrier_merge_node():
    pass_envelope = {
        "source_node": "wt_1",
        "branch": "selfmod/wt_1",
        "model_used": "Qwen-Local",
        "tier_source": "cluster_local",
        "summary": "Updated tests",
        "patch_diff": "diff --git a/test.py b/test.py",
        "verification_passed": True,
    }

    config = {
        "id": "merge_1",
        "require_verification_pass": True,
        "inputs": [
            {"name": "worktree_envelope", "value": pass_envelope},
            {"name": "auditor_route", "value": {"profile": "auditor"}},
        ],
    }

    merge_node = BarrierMergeNode(config)
    context = create_mock_context([config])

    await merge_node.execute(context)

    assert context.node_outputs["merge_1"]["merged_status"] == "ACCEPTED"
    assert context.node_outputs["merge_1"]["final_patch"] == "diff --git a/test.py b/test.py"

    fail_envelope = dict(pass_envelope, verification_passed=False)
    config_fail = {
        "id": "merge_1",
        "require_verification_pass": True,
        "inputs": [
            {"name": "worktree_envelope", "value": fail_envelope},
            {"name": "auditor_route", "value": {"profile": "auditor"}},
        ],
    }
    merge_node_fail = BarrierMergeNode(config_fail)
    context_fail = create_mock_context([config_fail])

    await merge_node_fail.execute(context_fail)

    assert context_fail.node_outputs["merge_1"]["merged_status"] == "REJECTED_VERIFICATION_FAILED"
    assert context_fail.node_outputs["merge_1"]["final_patch"] == ""
