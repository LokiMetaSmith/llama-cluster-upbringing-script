import asyncio
import os
import subprocess
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
import httpx

from .registry import registry
from ..node import Node
from ..context import WorkflowContext


@registry.register
class DynamicRouterNode(Node):
    """
    Evaluates task complexity, token pressure, and cluster health (via Consul)
    to route prompts to the optimal model tier and SOUL/profile configuration.
    """
    async def execute(self, context: WorkflowContext):
        prompt = self.get_input(context, "prompt") or self.get_input(context, "user_text") or ""
        requested_profile = self.get_input(context, "profile") or self.config.get("default_profile", "general")
        routing_table = self.config.get("routes", {})
        profiles = self.config.get("profiles", {})

        profile_cfg = profiles.get(requested_profile, {})
        tier_key = profile_cfg.get("tier") or self._classify_tier(prompt)
        route_spec = routing_table.get(tier_key, routing_table.get("default", {}))

        endpoint_info = await self._resolve_cluster_or_fallback(context, route_spec)

        route_decision = {
            "node_id": self.id,
            "profile": requested_profile,
            "soul_prompt": self._load_soul(profile_cfg.get("soul_path")),
            "tier": tier_key,
            "model": endpoint_info["model"],
            "base_url": endpoint_info["base_url"],
            "tier_source": endpoint_info["source"],  # "cluster_local" | "cloud_fallback"
            "allowed_tools": self._filter_child_tools(profile_cfg),
        }

        event_emitter = context.global_inputs.get("event_emitter") if hasattr(context, "global_inputs") else None
        if event_emitter and callable(event_emitter):
            event_emitter({
                "event": "ROUTE_DECISION",
                "node_id": self.id,
                "route_decision": route_decision,
            })

        self.set_output(context, "route_config", route_decision)
        self.set_output(context, "routed_prompt", prompt)

    def _classify_tier(self, prompt: str) -> str:
        if any(k in prompt.lower() for k in ["refactor", "pytest", "git diff", "ast", "implement"]):
            return "code_specialist"
        if len(prompt) > 2500 or "architect" in prompt.lower() or "self_modify" in prompt.lower():
            return "deep_reasoning"
        return "fast_local"

    def _filter_child_tools(self, profile_cfg: Dict[str, Any]) -> List[str]:
        blocked = {"delegate_task", "clarify", "persistent_memory_write", "workflow_hot_reload"}
        tools = profile_cfg.get("allowed_tools", [])
        if not profile_cfg.get("can_delegate", False):
            return [t for t in tools if t not in blocked]
        return tools

    def _load_soul(self, soul_path: Optional[str]) -> str:
        if soul_path and Path(soul_path).exists():
            return Path(soul_path).read_text()
        return "You are an autonomous cluster node in llama-cluster-upbringing-script."

    async def _resolve_cluster_or_fallback(self, context: WorkflowContext, route_spec: Dict[str, Any]) -> Dict[str, str]:
        consul_url = (getattr(context, "global_inputs", {}).get("consul_http_addr") if hasattr(context, "global_inputs") else None) or os.getenv("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")
        service_name = route_spec.get("consul_service", "llama-cpp-server")
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(f"{consul_url.rstrip('/')}/v1/health/service/{service_name}?passing=true")
                if resp.status_code == 200 and resp.json():
                    svc = resp.json()[0]["Service"]
                    addr = svc["Address"] or "127.0.0.1"
                    port = svc["Port"]
                    return {
                        "base_url": f"http://{addr}:{port}/v1",
                        "model": route_spec.get("local_model", "local-cluster-model"),
                        "source": "cluster_local",
                    }
        except Exception:
            pass

        return {
            "base_url": os.getenv("FALLBACK_LLM_BASE_URL", route_spec.get("fallback_url", "https://openrouter.ai/api/v1")),
            "model": route_spec.get("fallback_model", "anthropic/claude-3.7-sonnet"),
            "source": "cloud_fallback",
        }


@registry.register
class WorktreeSubagentNode(Node):
    """
    Spawns an isolated Git worktree for parallel subagent execution or self-modification.
    Enforces spawn-depth limits, blocks recursive orchestration tools, and runs verification gates.
    """
    async def execute(self, context: WorkflowContext):
        route_cfg = self.get_input(context, "route_config") or {}
        task_prompt = self.get_input(context, "task_prompt") or ""
        verify_cmd = self.config.get("verify_cmd", "pytest -q")
        repo_root = Path((getattr(context, "global_inputs", {}).get("repo_root") if hasattr(context, "global_inputs") else None) or ".").resolve()

        current_depth = int((getattr(context, "global_inputs", {}).get("spawn_depth") if hasattr(context, "global_inputs") else None) or 0)
        if current_depth >= 1:
            raise PermissionError(f"[{self.id}] Recursive worktree spawn blocked at depth {current_depth}")

        run_id = f"{self.id}_{uuid.uuid4().hex[:6]}"
        branch_name = f"selfmod/{run_id}"
        wt_path = repo_root / ".worktrees" / run_id
        wt_path.parent.mkdir(parents=True, exist_ok=True)

        emitter = (getattr(context, "global_inputs", {}).get("event_emitter") if hasattr(context, "global_inputs") else None) or (lambda e: None)
        emitter({
            "event": "WORKTREE_SPAWNED",
            "node_id": self.id,
            "branch": branch_name,
            "worktree_path": str(wt_path),
            "route_config": route_cfg,
        })

        subprocess.run(
            ["git", "worktree", "add", "-b", branch_name, str(wt_path), "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )

        try:
            subagent_response = await self._invoke_routed_model(
                route_cfg=route_cfg,
                wt_path=wt_path,
                task_prompt=task_prompt,
            )

            diff_proc = subprocess.run(
                ["git", "diff", "HEAD"], cwd=wt_path, capture_output=True, text=True
            )
            patch_diff = diff_proc.stdout.strip()

            verification_passed = True
            verify_output = ""
            if patch_diff and verify_cmd:
                v_proc = subprocess.run(
                    verify_cmd.split(), cwd=wt_path, capture_output=True, text=True
                )
                verification_passed = (v_proc.returncode == 0)
                verify_output = v_proc.stdout + "\n" + v_proc.stderr

            envelope = {
                "source_node": self.id,
                "branch": branch_name,
                "model_used": route_cfg.get("model", "unknown"),
                "tier_source": route_cfg.get("tier_source", "unknown"),
                "summary": subagent_response,
                "patch_diff": patch_diff,
                "verification_passed": verification_passed,
                "verify_log": verify_output[:2000],
            }

            emitter({
                "event": "MESSAGE_ENVELOPE_EMITTED",
                "source": self.id,
                "envelope": envelope,
            })

            self.set_output(context, "artifact_envelope", envelope)
            self.set_output(context, "patch_diff", patch_diff if verification_passed else "")
            self.set_output(context, "verified", verification_passed)
        finally:
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(wt_path)],
                cwd=repo_root,
                capture_output=True,
            )

    async def _invoke_routed_model(self, route_cfg: Dict[str, Any], wt_path: Path, task_prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("LLM_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        messages = [
            {"role": "system", "content": route_cfg.get("soul_prompt", "You are an autonomous subagent.")},
            {
                "role": "user",
                "content": (
                    f"Working Directory (Isolated Git Worktree): {wt_path}\n"
                    f"Permitted Tools: {', '.join(route_cfg.get('allowed_tools', []))}\n\n"
                    f"Task:\n{task_prompt}"
                ),
            },
        ]
        base_url = route_cfg.get("base_url", "http://127.0.0.1:8080/v1").rstrip("/")
        model = route_cfg.get("model", "default-model")
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json={"model": model, "messages": messages, "temperature": 0.2},
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]


@registry.register
class BarrierMergeNode(Node):
    """
    Synthesizes incoming worktree envelopes, auditing reports, and patch artifacts.
    Enforces verification gates before permitting self-modification or downstream merge.
    """
    async def execute(self, context: WorkflowContext):
        envelope = self.get_input(context, "worktree_envelope") or {}
        auditor_route = self.get_input(context, "auditor_route") or {}
        require_verification = self.config.get("require_verification_pass", True)

        verification_passed = envelope.get("verification_passed", True)
        if require_verification and not verification_passed:
            merged_status = "REJECTED_VERIFICATION_FAILED"
            final_patch = ""
        else:
            merged_status = "ACCEPTED"
            final_patch = envelope.get("patch_diff", "")

        summary_report = (
            f"--- Barrier Merge Synthesis ---\n"
            f"Status: {merged_status}\n"
            f"Source Subagent: {envelope.get('source_node', 'unknown')}\n"
            f"Branch: {envelope.get('branch', 'none')}\n"
            f"Model Used: {envelope.get('model_used', 'unknown')} ({envelope.get('tier_source', 'unknown')})\n"
            f"Auditor Profile: {auditor_route.get('profile', 'none')}\n"
            f"Summary: {envelope.get('summary', 'No summary')}\n"
        )

        self.set_output(context, "merged_status", merged_status)
        self.set_output(context, "final_patch", final_patch)
        self.set_output(context, "summary_report", summary_report)
