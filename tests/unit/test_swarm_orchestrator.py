"""Unit and integration tests for hybrid npcpy + npcsh/npcrs swarm orchestration."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml
from pydantic import ValidationError

from pipecatapp.npcsh_daemon import (
    NPCSHDaemon,
    execute_jinx_file,
    send_daemon_request,
)
from pipecatapp.swarm_orchestrator import (
    ClusterActionPlan,
    RemediationAction,
    build_swarm,
    collect_node_metrics,
    collect_node_operator_focus,
    dispatch_node_jinx,
    load_swarm_from_team_dir,
    query_psychic_recent_files,
    run_swarm_cycle,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
NPC_TEAM_DIR = REPO_ROOT / "npc_team"


def test_pydantic_models_validation():
    action = RemediationAction(
        target_node="worker-01",
        action="drain",
        priority=2,
        rationale="Thermal throttling detected",
    )
    plan = ClusterActionPlan(cluster_health="degraded", actions=[action])
    assert plan.cluster_health == "degraded"
    assert plan.actions[0].action == "drain"

    with pytest.raises(ValidationError):
        RemediationAction(
            target_node="worker-01",
            action="reboot_everything",  # type: ignore[arg-type]
            priority=2,
            rationale="Invalid action",
        )

    with pytest.raises(ValidationError):
        RemediationAction(
            target_node="worker-01",
            action="drain",
            priority=6,
            rationale="Priority out of range",
        )


def test_build_swarm_isolated_db_paths_and_config(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCAL_INFERENCE_KEY", "sk-local-test-key")
    coordinator_cfg = {"model": "qwen2.5-32b-instruct", "api_url": "http://10.0.0.10:8081/v1"}
    worker_cfgs = [
        {"name": "mem_worker", "focus": "Memory pressure", "model": "llama-3.1-8b", "api_url": "http://10.0.0.11:8081/v1"},
        {"name": "net_worker", "focus": "RPC latency", "model": "llama-3.1-8b", "api_url": "http://10.0.0.12:8081/v1"},
    ]

    coordinator, workers = build_swarm(
        coordinator_cfg,
        worker_cfgs,
        local_db_dir=str(tmp_path),
        node_id="node01",
    )

    assert coordinator.name == "forenpc"
    assert coordinator.provider == "openai-like"
    assert coordinator.api_key == "sk-local-test-key"
    assert coordinator.db_path == str(tmp_path / "npcpy_node01_forenpc.db")
    assert os.path.exists(coordinator.db_path)

    assert len(workers) == 2
    for worker in workers:
        assert worker.provider == "openai-like"
        assert worker.api_key == "sk-local-test-key"
        assert worker.db_path.startswith(str(tmp_path))
        assert "npcsh_history.db" not in worker.db_path
        assert os.path.exists(worker.db_path)


def test_load_swarm_from_team_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCAL_COORDINATOR_MODEL", "local-coord-70b")
    monkeypatch.setenv("LOCAL_WORKER_MODEL", "local-worker-8b")
    monkeypatch.setenv("LOCAL_INFERENCE_URL", "http://127.0.0.1:9999/v1")

    coordinator, workers = load_swarm_from_team_dir(
        team_dir=str(NPC_TEAM_DIR),
        local_db_dir=str(tmp_path),
    )

    assert coordinator.name == "forenpc"
    assert coordinator.model == "local-coord-70b"
    assert coordinator.api_url == "http://127.0.0.1:9999/v1"
    assert [w.name for w in workers] == ["memory_analyst", "network_analyst", "thermal_analyst"]
    assert all(w.model == "local-worker-8b" for w in workers)
    assert all(w.db_path.startswith(str(tmp_path)) for w in workers)


def test_run_swarm_cycle_mocked_call_sequence(tmp_path):
    coordinator, workers = build_swarm(
        {"model": "coord", "api_url": "http://127.0.0.1:8081/v1"},
        [{"name": "w1", "focus": "Memory", "model": "w-8b", "api_url": "http://127.0.0.1:8081/v1"}],
        local_db_dir=str(tmp_path),
    )

    expected_plan = ClusterActionPlan(
        cluster_health="degraded",
        actions=[
            RemediationAction(
                target_node="worker-01",
                action="rebalance_shards",
                priority=2,
                rationale="KV-cache slot contention",
            )
        ],
    )

    with (
        patch("pipecatapp.swarm_orchestrator.NPCArray") as mock_array_cls,
        patch("pipecatapp.swarm_orchestrator.Team") as mock_team_cls,
        patch("pipecatapp.swarm_orchestrator.get_llm_response") as mock_get_llm,
    ):
        mock_array = mock_array_cls.return_value
        mock_array.infer.return_value = [{"npc": "w1", "response": "KV cache high"}]
        mock_array.debate.return_value = "Consensus: KV cache skew on worker-01"

        mock_team = mock_team_cls.return_value
        mock_team.orchestrate.return_value = "Remediation brief: rebalance shards on worker-01"

        mock_get_llm.return_value = {"response": expected_plan, "raw": expected_plan.model_dump_json()}

        plan = run_swarm_cycle("node=worker-01 kv_usage=0.92", coordinator, workers)

        assert plan == expected_plan
        mock_array_cls.assert_called_once_with(workers)
        mock_array.infer.assert_called_once()
        mock_array.debate.assert_called_once()
        assert mock_array.debate.call_args.kwargs["rounds"] == 2
        mock_team_cls.assert_called_once_with(npcs=[coordinator, *workers], forenpc=coordinator)
        mock_team.orchestrate.assert_called_once()
        assert mock_get_llm.call_args.kwargs["npc"] is coordinator
        assert mock_get_llm.call_args.kwargs["format"] is ClusterActionPlan


def test_run_swarm_cycle_end_to_end_local_npcpy_and_sqlite_state(tmp_path):
    coordinator, workers = load_swarm_from_team_dir(
        team_dir=str(NPC_TEAM_DIR),
        local_db_dir=str(tmp_path),
    )

    def _fake_http_post(url, headers=None, json=None, timeout=10.0):
        resp = MagicMock()
        resp.status_code = 200
        if "response_format" in (json or {}):
            payload = {
                "cluster_health": "critical",
                "actions": [
                    {
                        "target_node": "worker-02",
                        "action": "restart_worker",
                        "priority": 1,
                        "rationale": "OOM risk on llama-worker KV slots",
                    }
                ],
            }
            resp.json.return_value = {
                "choices": [{"message": {"content": json_lib_dumps(payload)}}]
            }
        else:
            resp.json.return_value = {
                "choices": [{"message": {"content": "Confirmed KV-cache OOM signal on worker-02"}}]
            }
        return resp

    json_lib_dumps = json.dumps
    with patch("pipecatapp.npcpy.httpx.post", side_effect=_fake_http_post), patch(
        "pipecatapp.npcpy.llm_funcs.httpx.post", side_effect=_fake_http_post
    ):
        plan = run_swarm_cycle(
            "node=worker-02 mem_pressure=97% kv_cache=critical oom_events=2",
            coordinator,
            workers,
        )

    assert isinstance(plan, ClusterActionPlan)
    assert plan.cluster_health == "critical"
    assert plan.actions[0].target_node == "worker-02"
    assert plan.actions[0].action == "restart_worker"

    # Verify SQLite persistence in isolated node-local db_path files
    for npc in [coordinator, *workers]:
        with sqlite3.connect(npc.db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM npc_history").fetchone()[0]
            assert count >= 2

    with sqlite3.connect(coordinator.db_path) as conn:
        team_count = conn.execute("SELECT COUNT(*) FROM team_orchestration_log").fetchone()[0]
        assert team_count == 1


def test_dispatch_node_jinx_and_collect_metrics_security():
    ignore_action = RemediationAction(
        target_node="worker-01",
        action="ignore",
        priority=5,
        rationale="All metrics healthy",
    )
    assert dispatch_node_jinx("worker-01", ignore_action) == "no-op"

    drain_action = RemediationAction(
        target_node="worker-01",
        action="drain",
        priority=1,
        rationale="High thermal load",
    )
    with patch("pipecatapp.swarm_orchestrator.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="npcsh-action status=dispatched action=drain\n")
        output = dispatch_node_jinx(
            "worker-01",
            drain_action,
            team_dir="./npc_team",
            target_service="llama-worker",
        )
        assert "status=dispatched" in output
        cmd = mock_run.call_args[0][0]
        assert cmd == [
            "ssh",
            "worker-01",
            "npc",
            "./npc_team/jinxes/apply_action.jinx",
            "action=drain",
            "priority=1",
            "target_service=llama-worker",
        ]

    with patch("pipecatapp.swarm_orchestrator.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="node=worker-01 scope=all\n")
        metrics_out = collect_node_metrics("worker-01", team_dir="./npc_team")
        assert "node=worker-01" in metrics_out

    with pytest.raises(ValueError, match="Invalid target node host"):
        dispatch_node_jinx("-oProxyCommand=evil", drain_action)

    with pytest.raises(ValueError, match="Invalid npc_team directory path"):
        dispatch_node_jinx("worker-01", drain_action, team_dir="../../etc")


def test_npcsh_daemon_and_jinx_execution_over_unix_socket(tmp_path):
    socket_path = tmp_path / "daemon.sock"
    daemon = NPCSHDaemon(socket_path=str(socket_path), allowed_root=str(NPC_TEAM_DIR))
    daemon.start(background=True)
    try:
        ping_resp = send_daemon_request(str(socket_path), {"command": "ping"})
        assert ping_resp["status"] == "ok"
        assert ping_resp["pong"] is True

        metrics_resp = send_daemon_request(
            str(socket_path),
            {
                "command": "run_jinx",
                "jinx_path": str(NPC_TEAM_DIR / "jinxes" / "collect_metrics.jinx"),
                "params": {"probe_scope": "memory"},
            },
        )
        assert metrics_resp["status"] == "ok"
        assert metrics_resp["returncode"] == 0
        assert "scope=memory" in metrics_resp["stdout"]

        action_resp = send_daemon_request(
            str(socket_path),
            {
                "command": "run_jinx",
                "jinx_path": str(NPC_TEAM_DIR / "jinxes" / "apply_action.jinx"),
                "params": {"action": "drain", "target_service": "llama-worker", "priority": 2},
                "dry_run": True,
            },
        )
        assert action_resp["status"] == "ok"
        assert "action=drain" in action_resp["stdout"]
        assert "dry-run" in action_resp["stdout"]
    finally:
        daemon.stop()


def test_jinx_execution_blocks_shell_injection(tmp_path):
    with pytest.raises(ValueError, match="Invalid characters"):
        execute_jinx_file(
            str(NPC_TEAM_DIR / "jinxes" / "apply_action.jinx"),
            params={"action": "drain; rm -rf /"},
        )

    with pytest.raises(ValueError, match="Path traversal blocked"):
        execute_jinx_file(
            str(NPC_TEAM_DIR / "jinxes" / "apply_action.jinx"),
            allowed_root=str(tmp_path),
        )


def test_infrastructure_configs_and_continuous_batching():
    # 1. Verify npc_team files parse cleanly
    for fname in [
        "cluster.ctx",
        "forenpc.npc",
        "worker_analyst.npc",
        "jinxes/collect_metrics.jinx",
        "jinxes/apply_action.jinx",
        "jinxes/recent_operator_files.jinx",
    ]:
        content = (NPC_TEAM_DIR / fname).read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert isinstance(parsed, dict)

    # 2. Verify persistent systemd service unit
    service_text = (REPO_ROOT / "ansible" / "roles" / "npcsh" / "files" / "npcsh-daemon.service").read_text(
        encoding="utf-8"
    )
    assert "ExecStart=/usr/local/bin/npcsh-daemon --socket /run/npcsh/daemon.sock" in service_text
    assert 'Environment="LOCAL_INFERENCE_KEY=sk-local-no-auth"' in service_text

    # 3. Verify llama-server continuous batching flags in Nomad templates
    expert_tmpl = (REPO_ROOT / "ansible" / "jobs" / "expert.nomad.j2").read_text(encoding="utf-8")
    router_tmpl = (REPO_ROOT / "ansible" / "jobs" / "router.nomad.j2").read_text(encoding="utf-8")
    assert "-np 4 --cont-batching" in expert_tmpl
    assert "-np 4 --cont-batching" in router_tmpl

    # 4. Verify dependencies declared
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    reqs = (REPO_ROOT / "pipecatapp" / "requirements-core.txt").read_text(encoding="utf-8")
    assert "npcpy" in pyproject
    assert "pydantic" in pyproject
    assert "npcpy" in reqs
    assert "npcsh" in reqs


def _create_psychic_events_db(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE events (
                id INTEGER PRIMARY KEY,
                timestamp INTEGER NOT NULL,
                query TEXT NOT NULL,
                file_path TEXT NOT NULL,
                full_path TEXT NOT NULL,
                mtime INTEGER,
                file_size INTEGER,
                subsession_id INTEGER,
                action TEXT NOT NULL,
                session_id TEXT NOT NULL,
                episode_queries TEXT,
                rank INTEGER,
                is_dir INTEGER
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE sessions (
                session_id TEXT PRIMARY KEY,
                cwd TEXT NOT NULL,
                timezone TEXT NOT NULL,
                created_at INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE hidden_prefixes (
                path TEXT PRIMARY KEY,
                created_at INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE imported_paths (
                full_path TEXT PRIMARY KEY,
                uses INTEGER NOT NULL,
                last_used INTEGER NOT NULL,
                sources TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO hidden_prefixes (path, created_at) VALUES (?, ?)",
            ("/opt/secret-dir", 1700000000),
        )
        rows = [
            (1, 1700000100, "llama", "llama-server.log", "/var/log/llama-server.log", None, None, 1, "click", "s1", '["ll","llama"]', 1, 0),
            (2, 1700000200, "npc", "cluster.ctx", "/opt/pipecatapp/npc_team/cluster.ctx", None, None, 2, "click", "s1", '["cl"]', 1, 0),
            (3, 1700000250, "imp", "noise.txt", "/tmp/only-impression.txt", None, None, 3, "impression", "s1", None, 4, 0),
            (4, 1700000300, "", "nomad", "/etc/nomad.d", None, None, 4, "startup_visit", "s1", None, None, 1),
            (5, 1700000350, "sec", "keys.pem", "/opt/secret-dir/keys.pem", None, None, 5, "click", "s1", None, 1, 0),
        ]
        conn.executemany(
            """
            INSERT INTO events (
                id, timestamp, query, file_path, full_path, mtime, file_size,
                subsession_id, action, session_id, episode_queries, rank, is_dir
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()


def test_query_psychic_recent_files_readonly_and_hidden_filter(tmp_path):
    db_file = tmp_path / "events.db"
    _create_psychic_events_db(db_file)

    all_recent = query_psychic_recent_files(db_path=str(db_file), limit=10, include_dirs=True)
    paths = [item["full_path"] for item in all_recent]
    assert paths == [
        "/etc/nomad.d",
        "/opt/pipecatapp/npc_team/cluster.ctx",
        "/var/log/llama-server.log",
    ]
    assert "/tmp/only-impression.txt" not in paths
    assert "/opt/secret-dir/keys.pem" not in paths

    files_only = query_psychic_recent_files(db_path=str(db_file), limit=10, include_dirs=False)
    assert [item["full_path"] for item in files_only] == [
        "/opt/pipecatapp/npc_team/cluster.ctx",
        "/var/log/llama-server.log",
    ]

    assert query_psychic_recent_files(db_path=str(tmp_path / "missing.db")) == []


def test_recent_operator_files_jinx_via_daemon(tmp_path):
    db_file = tmp_path / "events.db"
    _create_psychic_events_db(db_file)

    socket_path = tmp_path / "daemon.sock"
    daemon = NPCSHDaemon(socket_path=str(socket_path), allowed_root=str(NPC_TEAM_DIR))
    daemon.start(background=True)
    try:
        resp = send_daemon_request(
            str(socket_path),
            {
                "command": "run_jinx",
                "jinx_path": str(NPC_TEAM_DIR / "jinxes" / "recent_operator_files.jinx"),
                "params": {"limit": 2, "db_path": str(db_file)},
            },
        )
        assert resp["status"] == "ok"
        assert resp["returncode"] == 0
        payload = json.loads(resp["stdout"])
        assert payload["db_path"] == str(db_file)
        assert [r["full_path"] for r in payload["recent_files"]] == [
            "/etc/nomad.d",
            "/opt/pipecatapp/npc_team/cluster.ctx",
        ]
    finally:
        daemon.stop()


def test_collect_node_operator_focus_ssh_dispatch():
    with patch("pipecatapp.swarm_orchestrator.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout='{"status":"ok","recent_files":[]}\n')
        out = collect_node_operator_focus("controller-01", team_dir="./npc_team", limit=5)
        assert '"status":"ok"' in out
        cmd = mock_run.call_args[0][0]
        assert cmd == [
            "ssh",
            "controller-01",
            "npc",
            "./npc_team/jinxes/recent_operator_files.jinx",
            "limit=5",
        ]

    with pytest.raises(ValueError, match="Invalid target node host"):
        collect_node_operator_focus("-oProxyCommand=evil")

