"""Local-first npcpy orchestration primitives (NPC, Team) with isolated SQLite state."""

from __future__ import annotations

import os
import re
import sqlite3
import tempfile
import time
from typing import Any, Optional

import httpx


def _default_db_dir() -> str:
    if os.path.isdir("/var/tmp") and os.access("/var/tmp", os.W_OK):
        return "/var/tmp"
    return tempfile.gettempdir()


def resolve_isolated_db_path(name: str, db_path: Optional[str] = None) -> str:
    """Resolve an isolated node-local SQLite path, avoiding shared ~/npcsh_history.db."""
    safe_name = re.sub(r"[^a-zA-Z0-9_.-]+", "_", name or "npc").strip("_") or "npc"
    if db_path:
        expanded = os.path.expanduser(db_path)
        if os.path.basename(expanded) != "npcsh_history.db":
            return os.path.abspath(expanded)
    return os.path.join(_default_db_dir(), f"npcpy_{safe_name}.db")


def _init_sqlite_db(db_path: str) -> None:
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with sqlite3.connect(db_path, timeout=30.0) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS npc_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                npc_name TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS team_orchestration_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                forenpc_name TEXT NOT NULL,
                prompt TEXT NOT NULL,
                brief TEXT NOT NULL
            )
            """
        )
        conn.commit()


class NPC:
    """Local OpenAI-compatible agent persona backed by isolated SQLite history."""

    def __init__(
        self,
        name: str,
        primary_directive: str = "",
        model: str = "llama-3.1-8b-instruct",
        provider: str = "openai-like",
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        db_path: Optional[str] = None,
        jinxes: Optional[list[str]] = None,
        file: Optional[str] = None,
    ) -> None:
        self.name = name
        self.primary_directive = primary_directive
        self.model = model
        self.provider = provider
        self.api_url = api_url.rstrip("/") if api_url else None
        self.api_key = api_key or os.getenv("LOCAL_INFERENCE_KEY", "sk-local-no-auth")
        self.db_path = resolve_isolated_db_path(name, db_path)
        self.jinxes = list(jinxes or [])
        self.file = file
        _init_sqlite_db(self.db_path)

    def record_event(self, role: str, content: str) -> None:
        """Persist a message event to this NPC's isolated SQLite database."""
        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute(
                "INSERT INTO npc_history (timestamp, npc_name, role, content) VALUES (?, ?, ?, ?)",
                (time.time(), self.name, role, content),
            )
            conn.commit()

    def _synthesize_local_assessment(self, prompt: str) -> str:
        lower = prompt.lower()
        findings: list[str] = []
        if any(tok in lower for tok in ("kv", "vram", "oom", "memory", "mem")):
            findings.append("memory/kv-cache pressure indicator detected")
        if any(tok in lower for tok in ("latency", "rpc", "packet", "timeout", "network")):
            findings.append("network/rpc latency signal detected")
        if any(tok in lower for tok in ("temp", "thermal", "throttle", "watt", "power")):
            findings.append("thermal/power threshold signal detected")
        if not findings:
            findings.append("nominal telemetry baseline observed")
        return (
            f"[{self.name} ({self.model})] Directive='{self.primary_directive[:80]}' -> "
            + "; ".join(findings)
        )

    def infer(self, prompt: str, temperature: float = 0.2, timeout: float = 10.0) -> str:
        """Run single-turn inference against a local OpenAI-compatible endpoint with offline fallback."""
        self.record_event("user", prompt)
        content: Optional[str] = None
        if self.api_url:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.primary_directive or f"You are {self.name}."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
            }
            try:
                resp = httpx.post(
                    f"{self.api_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=timeout,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices") or []
                    if choices:
                        msg = choices[0].get("message") or {}
                        raw_content = msg.get("content")
                        if isinstance(raw_content, str) and raw_content.strip():
                            content = raw_content.strip()
            except Exception:
                content = None

        if content is None:
            content = self._synthesize_local_assessment(prompt)

        self.record_event("assistant", content)
        return content


class Team:
    """Hierarchical multi-NPC team coordinated by a forenpc."""

    def __init__(
        self,
        npcs: Optional[list[NPC]] = None,
        forenpc: Optional[NPC] = None,
        team_path: Optional[str] = None,
        db_path: Optional[str] = None,
    ) -> None:
        self.npcs = list(npcs or [])
        self.forenpc = forenpc or (self.npcs[0] if self.npcs else None)
        self.team_path = team_path
        fallback_db = self.forenpc.db_path if self.forenpc is not None else None
        self.db_path = resolve_isolated_db_path(
            f"team_{self.forenpc.name}" if self.forenpc else "team",
            db_path or fallback_db,
        )
        _init_sqlite_db(self.db_path)

    def orchestrate(self, prompt: str) -> str:
        """Coordinate specialists via forenpc and persist the remediation brief."""
        forenpc_name = self.forenpc.name if self.forenpc else "forenpc"
        specialist_notes: list[str] = []
        for member in self.npcs:
            if self.forenpc is not None and member is self.forenpc:
                continue
            specialist_notes.append(f"- {member.name}: {member.primary_directive}")

        orchestration_prompt = prompt
        if specialist_notes:
            orchestration_prompt = (
                f"{prompt}\n\nAvailable specialists:\n" + "\n".join(specialist_notes)
            )

        if self.forenpc is not None:
            brief = self.forenpc.infer(orchestration_prompt)
        else:
            brief = f"[forenpc] Synthesized remediation brief for: {prompt[:200]}"

        with sqlite3.connect(self.db_path, timeout=30.0) as conn:
            conn.execute(
                "INSERT INTO team_orchestration_log (timestamp, forenpc_name, prompt, brief) VALUES (?, ?, ?, ?)",
                (time.time(), forenpc_name, prompt, brief),
            )
            conn.commit()
        return brief


__all__ = ["NPC", "Team", "resolve_isolated_db_path"]
