import asyncio
import json
import os
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import httpx
import yaml


@dataclass
class MessageEnvelope:
    """Explicit inter-module communication packet for visual tracing."""
    edge_id: str
    source_node: str
    target_node: str
    profile: str
    model_route: str
    payload: Dict[str, Any]
    worktree_branch: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


class HybridModelRouter:
    def __init__(self, config_path: Path, event_bus: Optional[Callable[[Dict], None]] = None):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.endpoints = self.config.get("endpoints", {})
        self.routes = self.config.get("routes", {})
        self.profiles = self.config.get("profiles", {})
        self.event_bus = event_bus or (lambda evt: None)

    def resolve_profile_and_route(
        self, requested_profile: str, override_route: Optional[str] = None
    ) -> Dict[str, Any]:
        profile = self.profiles.get(requested_profile)
        if not profile:
            raise ValueError(f"Unknown profile: {requested_profile}")

        route_name = override_route or profile.get("default_route")
        route_cfg = self.routes.get(route_name)
        if not route_cfg:
            raise ValueError(f"Unknown model route: {route_name}")

        blocked = set(self.config.get("defaults", {}).get("global_blocked_child_tools", []))
        allowed_tools = [
            t for t in profile.get("allowed_tools", [])
            if profile.get("can_delegate", False) or t not in blocked
        ]

        soul_text = ""
        soul_path_str = profile.get("soul_path", "")
        if soul_path_str:
            soul_path = Path(soul_path_str)
            if soul_path.exists():
                soul_text = soul_path.read_text()

        return {
            "profile_name": requested_profile,
            "route_name": route_name,
            "primary": route_cfg["primary"],
            "fallback": route_cfg.get("fallback"),
            "allowed_tools": allowed_tools,
            "soul_prompt": soul_text,
        }

    async def complete(
        self,
        node_id: str,
        profile_name: str,
        messages: List[Dict[str, str]],
        override_route: Optional[str] = None,
    ) -> Dict[str, Any]:
        resolved = self.resolve_profile_and_route(profile_name, override_route)
        full_messages = []
        if resolved["soul_prompt"]:
            full_messages.append({"role": "system", "content": resolved["soul_prompt"]})
        full_messages.extend(messages)

        try:
            return await self._call_tier(node_id, resolved["route_name"], "primary", resolved["primary"], full_messages)
        except Exception as primary_err:
            self.event_bus({
                "type": "ROUTE_FALLBACK_TRIGGERED",
                "node_id": node_id,
                "route": resolved["route_name"],
                "reason": str(primary_err),
            })
            if not resolved.get("fallback"):
                raise
            return await self._call_tier(node_id, resolved["route_name"], "fallback", resolved["fallback"], full_messages)

    async def _call_tier(
        self, node_id: str, route_name: str, tier_label: str, tier_cfg: Dict[str, Any], messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        ep = self.endpoints[tier_cfg["endpoint"]]
        headers = {"Content-Type": "application/json"}
        if "env_key" in ep and os.getenv(ep["env_key"]):
            headers["Authorization"] = f"Bearer {os.getenv(ep['env_key'])}"

        self.event_bus({
            "type": "MODEL_DISPATCH",
            "node_id": node_id,
            "route": route_name,
            "tier": tier_label,
            "model": tier_cfg["model"],
            "endpoint": ep["base_url"],
        })

        async with httpx.AsyncClient(timeout=ep.get("timeout_sec", 60)) as client:
            resp = await client.post(
                f"{ep['base_url'].rstrip('/')}/chat/completions",
                headers=headers,
                json={
                    "model": tier_cfg["model"],
                    "messages": messages,
                    "temperature": tier_cfg.get("temperature", 0.2),
                    "max_tokens": tier_cfg.get("max_tokens", 2048),
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "content": data["choices"][0]["message"]["content"],
                "model_used": tier_cfg["model"],
                "tier_used": tier_label,
            }


class WorktreeDelegationManager:
    """Spawns isolated Git worktrees for parallel subagents and harvests diffs."""

    def __init__(self, repo_root: Path, max_concurrency: int = 10, max_depth: int = 1):
        self.repo_root = repo_root.resolve()
        self.worktree_dir = self.repo_root / ".worktrees"
        self.worktree_dir.mkdir(exist_ok=True)
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.max_depth = max_depth

    async def execute_in_worktree(
        self,
        parent_node: str,
        subagent_id: str,
        task_prompt: str,
        router: HybridModelRouter,
        profile_name: str = "worktree_coder",
        override_route: Optional[str] = None,
        current_depth: int = 0,
    ) -> Dict[str, Any]:
        if current_depth >= self.max_depth:
            raise PermissionError(
                f"Subagent spawn blocked: current_depth ({current_depth}) >= max_spawn_depth ({self.max_depth})"
            )

        run_uid = f"{subagent_id}_{uuid.uuid4().hex[:6]}"
        branch_name = f"hermes/subagent-{run_uid}"
        wt_path = self.worktree_dir / run_uid

        async with self.semaphore:
            subprocess.run(
                ["git", "worktree", "add", "-b", branch_name, str(wt_path), "HEAD"],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
            )

            try:
                scoped_messages = [
                    {
                        "role": "user",
                        "content": (
                            f"[ISOLATED WORKTREE ROOT]: {wt_path}\n"
                            f"[ASSIGNED BRANCH]: {branch_name}\n"
                            f"[TASK]: {task_prompt}"
                        ),
                    }
                ]

                llm_res = await router.complete(
                    node_id=subagent_id,
                    profile_name=profile_name,
                    messages=scoped_messages,
                    override_route=override_route,
                )

                diff_proc = subprocess.run(
                    ["git", "diff", "HEAD"],
                    cwd=wt_path,
                    capture_output=True,
                    text=True,
                )
                patch_content = diff_proc.stdout.strip()

                return {
                    "subagent_id": subagent_id,
                    "parent_node": parent_node,
                    "branch": branch_name,
                    "worktree_preserved": bool(patch_content),
                    "diff_patch": patch_content,
                    "summary": llm_res["content"],
                    "model_used": llm_res["model_used"],
                    "tier_used": llm_res["tier_used"],
                }

            finally:
                subprocess.run(
                    ["git", "worktree", "remove", "--force", str(wt_path)],
                    cwd=self.repo_root,
                    capture_output=True,
                )
