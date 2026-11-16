"""Control plane swarm orchestrator built on npcpy (NPCArray, Team, forenpc) and Pydantic."""

from __future__ import annotations

import os
import re
import sqlite3
import subprocess
import sys
import urllib.parse
from typing import Any, List, Literal, Optional

import yaml
from pydantic import BaseModel, Field

_PIPECATAPP_DIR = os.path.dirname(os.path.abspath(__file__))
if _PIPECATAPP_DIR not in sys.path:
    sys.path.append(_PIPECATAPP_DIR)

from npcpy import NPC, Team  # noqa: E402
from npcpy.llm_funcs import get_llm_response  # noqa: E402
from npcpy.npc_array import NPCArray  # noqa: E402

_ENV_EXPR_RE = re.compile(
    r"""\{\{\s*env\(\s*['"]([A-Za-z_][A-Za-z0-9_]*)['"]\s*,\s*['"]([^'"]*)['"]\s*\)\s*\}\}"""
)
_HOST_RE = re.compile(r"^[a-zA-Z0-9._:@-]+$")
_SAFE_TOKEN_RE = re.compile(r"^[a-zA-Z0-9._/-]+$")


class RemediationAction(BaseModel):
    """Strict remediation action dispatched to a worker node via npcsh/npcrs."""

    target_node: str = Field(description="Hostname or IP of the affected cluster node")
    action: Literal["drain", "restart_worker", "rebalance_shards", "ignore"]
    priority: int = Field(ge=1, le=5)
    rationale: str


class ClusterActionPlan(BaseModel):
    """Deterministic cluster remediation plan produced by the forenpc coordinator."""

    cluster_health: Literal["healthy", "degraded", "critical"]
    actions: List[RemediationAction]


def _resolve_env_templates(value: Any) -> Any:
    if isinstance(value, str):
        return _ENV_EXPR_RE.sub(lambda m: os.getenv(m.group(1), m.group(2)), value)
    if isinstance(value, dict):
        return {k: _resolve_env_templates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_env_templates(v) for v in value]
    return value


def _validate_node_host(node_host: str) -> str:
    cleaned = (node_host or "").strip()
    if not cleaned or cleaned.startswith("-") or not _HOST_RE.match(cleaned):
        raise ValueError(f"Invalid target node host: {node_host!r}")
    return cleaned


def _validate_team_dir(team_dir: str) -> str:
    cleaned = (team_dir or "").strip()
    if not cleaned or ".." in cleaned.split("/") or not _SAFE_TOKEN_RE.match(cleaned):
        raise ValueError(f"Invalid npc_team directory path: {team_dir!r}")
    return cleaned.rstrip("/") or "."


def _validate_safe_arg(value: str, label: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned or cleaned.startswith("-") or not re.match(r"^[a-zA-Z0-9._-]+$", cleaned):
        raise ValueError(f"Invalid {label}: {value!r}")
    return cleaned


def build_swarm(
    coordinator_cfg: dict[str, Any],
    worker_cfgs: list[dict[str, Any]],
    local_db_dir: str = "/var/tmp",
    node_id: Optional[str] = None,
) -> tuple[NPC, list[NPC]]:
    """Construct the forenpc coordinator and domain worker NPCs with isolated SQLite db_path."""
    local_key = os.getenv("LOCAL_INFERENCE_KEY", "sk-local-no-auth")
    prefix = f"{_validate_safe_arg(node_id, 'node_id')}_" if node_id else ""

    coordinator = NPC(
        name="forenpc",
        primary_directive=coordinator_cfg.get(
            "primary_directive",
            "You are the cluster orchestration coordinator. Synthesize worker telemetry "
            "reports, delegate targeted root-cause checks to specialists, and determine "
            "minimal-disruption remediation actions.",
        ),
        model=coordinator_cfg["model"],
        provider=coordinator_cfg.get("provider", "openai-like"),
        api_url=coordinator_cfg["api_url"],
        api_key=local_key,
        db_path=os.path.join(local_db_dir, f"npcpy_{prefix}forenpc.db"),
    )

    workers = [
        NPC(
            name=cfg["name"],
            primary_directive=f"You are a cluster telemetry analyst. {cfg['focus']}",
            model=cfg["model"],
            provider=cfg.get("provider", "openai-like"),
            api_url=cfg["api_url"],
            api_key=local_key,
            db_path=os.path.join(local_db_dir, f"npcpy_{prefix}{cfg['name']}.db"),
        )
        for cfg in worker_cfgs
    ]
    return coordinator, workers


def load_swarm_from_team_dir(
    team_dir: str = "./npc_team",
    local_db_dir: str = "/var/tmp",
    node_id: Optional[str] = None,
) -> tuple[NPC, list[NPC]]:
    """Load coordinator and worker configuration from shared declarative npc_team/ files."""
    resolved_dir = os.path.abspath(team_dir)
    ctx_path = os.path.join(resolved_dir, "cluster.ctx")
    forenpc_path = os.path.join(resolved_dir, "forenpc.npc")
    worker_path = os.path.join(resolved_dir, "worker_analyst.npc")

    ctx_data: dict[str, Any] = {}
    if os.path.exists(ctx_path):
        with open(ctx_path, "r", encoding="utf-8") as handle:
            ctx_data = _resolve_env_templates(yaml.safe_load(handle) or {})

    forenpc_data: dict[str, Any] = {}
    if os.path.exists(forenpc_path):
        with open(forenpc_path, "r", encoding="utf-8") as handle:
            forenpc_data = _resolve_env_templates(yaml.safe_load(handle) or {})

    worker_data: dict[str, Any] = {}
    if os.path.exists(worker_path):
        with open(worker_path, "r", encoding="utf-8") as handle:
            worker_data = _resolve_env_templates(yaml.safe_load(handle) or {})

    coordinator_cfg = {
        "model": forenpc_data.get("model") or ctx_data.get("model", "qwen2.5-32b-instruct"),
        "api_url": forenpc_data.get("api_url") or ctx_data.get("api_url", "http://127.0.0.1:8081/v1"),
        "provider": forenpc_data.get("provider") or ctx_data.get("provider", "openai-like"),
        "primary_directive": forenpc_data.get(
            "primary_directive",
            "You are the cluster orchestration coordinator. Synthesize worker telemetry "
            "reports, delegate targeted root-cause checks to specialists, and determine "
            "minimal-disruption remediation actions.",
        ),
    }

    default_worker_model = worker_data.get("model", "llama-3.1-8b-instruct")
    default_worker_url = worker_data.get("api_url") or coordinator_cfg["api_url"]
    specialties = ctx_data.get("worker_specialties") or [
        {
            "name": worker_data.get("name", "worker_analyst"),
            "focus": worker_data.get(
                "primary_directive",
                "Focus on memory/KV-cache pressure, network/RPC latency, and thermals/power.",
            ),
            "model": default_worker_model,
            "api_url": default_worker_url,
        }
    ]
    worker_cfgs = [
        {
            "name": spec["name"],
            "focus": spec["focus"],
            "model": spec.get("model", default_worker_model),
            "api_url": spec.get("api_url", default_worker_url),
        }
        for spec in specialties
    ]

    db_dir = ctx_data.get("db_dir", local_db_dir) if local_db_dir == "/var/tmp" else local_db_dir
    return build_swarm(coordinator_cfg, worker_cfgs, local_db_dir=db_dir, node_id=node_id)


def run_swarm_cycle(
    telemetry_snapshot: str,
    coordinator: NPC,
    workers: list[NPC],
) -> ClusterActionPlan:
    """Execute the 3-stage npcpy map-reduce swarm cycle returning a ClusterActionPlan."""
    # 1. Parallel evaluation & consensus via NPCArray
    worker_pool = NPCArray(workers)
    initial_assessments = worker_pool.infer(
        f"Analyze this cluster telemetry snapshot from your specialty perspective "
        f"and flag any anomalies:\n\n{telemetry_snapshot}"
    )
    consensus_findings = worker_pool.debate(
        topic=(
            "Reconcile your anomaly assessments and agree on the top root causes:\n"
            f"{initial_assessments}"
        ),
        rounds=2,
    )

    # 2. Hierarchical orchestration via Team + forenpc
    cluster_team = Team(npcs=[coordinator, *workers], forenpc=coordinator)
    orchestrated_report = cluster_team.orchestrate(
        f"Review the worker consensus below. Query specialists if any node state is "
        f"ambiguous, then produce a final remediation brief.\n\n{consensus_findings}"
    )

    # 3. Deterministic Pydantic output contract
    structured = get_llm_response(
        prompt=(
            "Convert this remediation brief into a structured ClusterActionPlan:\n\n"
            f"{orchestrated_report}"
        ),
        npc=coordinator,
        format=ClusterActionPlan,
    )
    response = structured["response"]
    if isinstance(response, ClusterActionPlan):
        return response
    if isinstance(response, str):
        return ClusterActionPlan.model_validate_json(response)
    return ClusterActionPlan.model_validate(response)


def dispatch_node_jinx(
    node_host: str,
    action: RemediationAction,
    team_dir: str = "./npc_team",
    target_service: Optional[str] = None,
) -> str:
    """Execute a declarative .jinx remediation pipeline on a target node via npcsh/npcrs."""
    if action.action == "ignore":
        return "no-op"

    safe_host = _validate_node_host(node_host)
    safe_team_dir = _validate_team_dir(team_dir)

    cmd = [
        "ssh",
        safe_host,
        "npc",
        f"{safe_team_dir}/jinxes/apply_action.jinx",
        f"action={action.action}",
        f"priority={action.priority}",
    ]
    if target_service:
        safe_svc = _validate_safe_arg(target_service, "target_service")
        cmd.append(f"target_service={safe_svc}")

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def collect_node_metrics(
    node_host: str,
    team_dir: str = "./npc_team",
    probe_scope: str = "all",
) -> str:
    """Execute the collect_metrics.jinx probe on a target node via npcsh/npcrs."""
    safe_host = _validate_node_host(node_host)
    safe_team_dir = _validate_team_dir(team_dir)
    safe_scope = _validate_safe_arg(probe_scope, "probe_scope")

    cmd = [
        "ssh",
        safe_host,
        "npc",
        f"{safe_team_dir}/jinxes/collect_metrics.jinx",
        f"probe_scope={safe_scope}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def resolve_psychic_db_path(db_path: Optional[str] = None) -> str:
    """Resolve psychic's node-local events.db path without touching shared homes unless fallback."""
    if db_path and db_path.strip():
        cleaned = db_path.strip()
        if ".." in cleaned.split("/"):
            raise ValueError(f"Invalid psychic db_path: {db_path!r}")
        return os.path.realpath(os.path.expanduser(cleaned))

    env_dir = os.getenv("PSYCHIC_DATA_DIR", "").strip()
    user = os.getenv("USER", "pipecatapp")
    candidates = [
        os.path.join(env_dir, "events.db") if env_dir else "",
        f"/var/tmp/psychic_{user}/events.db",
        os.path.expanduser("~/.local/share/psychic/events.db"),
    ]
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return os.path.realpath(candidate)
    return os.path.realpath(candidates[0] or candidates[1])


def query_psychic_recent_files(
    db_path: Optional[str] = None,
    limit: int = 10,
    include_dirs: bool = True,
) -> list[dict[str, Any]]:
    """Read-only SQLite query over psychic's events.db for recent operator focus paths."""
    clamped_limit = max(1, min(200, int(limit)))
    resolved_db = resolve_psychic_db_path(db_path)
    if not os.path.isfile(resolved_db):
        return []

    uri = f"file:{urllib.parse.quote(resolved_db)}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=5.0)
    try:
        hidden_prefixes: list[str] = []
        try:
            hidden_prefixes = [
                str(row[0]).rstrip("/")
                for row in conn.execute("SELECT path FROM hidden_prefixes").fetchall()
                if row[0]
            ]
        except sqlite3.OperationalError:
            hidden_prefixes = []

        def _is_hidden(path_val: str) -> bool:
            return any(
                path_val == pref or path_val.startswith(pref + "/")
                for pref in hidden_prefixes
            )

        dir_clause = "" if include_dirs else "AND (is_dir IS NULL OR is_dir = 0)"
        rows = conn.execute(
            f"""
            WITH ranked AS (
                SELECT
                    full_path,
                    timestamp,
                    action,
                    query,
                    episode_queries,
                    is_dir,
                    COUNT(*) OVER (PARTITION BY full_path) AS interactions,
                    ROW_NUMBER() OVER (PARTITION BY full_path ORDER BY timestamp DESC, id DESC) AS rn
                FROM events
                WHERE action IN ('click', 'jump', 'startup_visit', 'scroll')
                  AND full_path IS NOT NULL
                  AND full_path != ''
                  {dir_clause}
            )
            SELECT full_path, timestamp, interactions, action, query, episode_queries, is_dir
            FROM ranked
            WHERE rn = 1
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (clamped_limit * 3,),
        ).fetchall()

        results: list[dict[str, Any]] = []
        for row in rows:
            full_path = str(row[0])
            if _is_hidden(full_path):
                continue
            results.append(
                {
                    "full_path": full_path,
                    "last_timestamp": row[1],
                    "interactions": row[2],
                    "action": row[3],
                    "last_query": row[4],
                    "episode_queries": row[5],
                    "is_dir": bool(row[6]) if row[6] is not None else None,
                }
            )
            if len(results) >= clamped_limit:
                break

        if not results:
            try:
                imp_rows = conn.execute(
                    """
                    SELECT full_path, last_used, uses, sources
                    FROM imported_paths
                    WHERE full_path IS NOT NULL AND full_path != ''
                    ORDER BY last_used DESC
                    LIMIT ?
                    """,
                    (clamped_limit * 3,),
                ).fetchall()
                for row in imp_rows:
                    full_path = str(row[0])
                    if _is_hidden(full_path):
                        continue
                    results.append(
                        {
                            "full_path": full_path,
                            "last_timestamp": row[1],
                            "interactions": row[2],
                            "action": f"imported:{row[3]}",
                            "last_query": "",
                            "episode_queries": None,
                            "is_dir": None,
                        }
                    )
                    if len(results) >= clamped_limit:
                        break
            except sqlite3.OperationalError:
                pass

        return results
    finally:
        conn.close()


def collect_node_operator_focus(
    node_host: str,
    team_dir: str = "./npc_team",
    limit: int = 10,
) -> str:
    """Execute recent_operator_files.jinx on a remote node via npcsh/npcrs without TUI."""
    safe_host = _validate_node_host(node_host)
    safe_team_dir = _validate_team_dir(team_dir)
    clamped_limit = max(1, min(200, int(limit)))

    cmd = [
        "ssh",
        safe_host,
        "npc",
        f"{safe_team_dir}/jinxes/recent_operator_files.jinx",
        f"limit={clamped_limit}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


sys.modules.setdefault("swarm_orchestrator", sys.modules[__name__])
sys.modules.setdefault("pipecatapp.swarm_orchestrator", sys.modules[__name__])

__all__ = [
    "ClusterActionPlan",
    "RemediationAction",
    "build_swarm",
    "collect_node_metrics",
    "collect_node_operator_focus",
    "dispatch_node_jinx",
    "load_swarm_from_team_dir",
    "query_psychic_recent_files",
    "resolve_psychic_db_path",
    "run_swarm_cycle",
]
