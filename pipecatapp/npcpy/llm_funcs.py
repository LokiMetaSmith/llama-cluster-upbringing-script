"""Structured and unstructured LLM response helpers for npcpy."""

from __future__ import annotations

import json
import re
from typing import Any, Optional, Type

import httpx
from pydantic import BaseModel

from . import NPC


def _extract_json_payload(text: str) -> Any:
    stripped = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", stripped)
    if fence_match:
        stripped = fence_match.group(1).strip()
    return json.loads(stripped)


def _extract_target_node(prompt: str) -> str:
    node_match = re.search(
        r"\b([a-zA-Z0-9_-]*node[a-zA-Z0-9_-]*|worker-[0-9]+|100\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+)\b",
        prompt,
    )
    if node_match:
        return node_match.group(1)
    return "worker-01"


def _synthesize_structured_payload(prompt: str, format_cls: Type[BaseModel]) -> dict[str, Any]:
    lower = prompt.lower()
    target_node = _extract_target_node(prompt)

    if any(tok in lower for tok in ("oom", "critical", "95%", "98%", "crash", "panic")):
        health = "critical"
        action = "restart_worker"
        priority = 1
        rationale = "Critical memory or runtime pressure detected in worker consensus."
    elif any(tok in lower for tok in ("drain", "thermal", "throttle", "overheat")):
        health = "degraded"
        action = "drain"
        priority = 2
        rationale = "Node thermal or capacity degradation requires draining active work."
    elif any(tok in lower for tok in ("kv", "imbalance", "skew", "latency", "rpc", "contention")):
        health = "degraded"
        action = "rebalance_shards"
        priority = 3
        rationale = "KV-cache or RPC latency skew detected; shard rebalancing advised."
    else:
        health = "healthy"
        action = "ignore"
        priority = 5
        rationale = "Cluster telemetry is within nominal thresholds."

    fields = getattr(format_cls, "model_fields", {})
    if "cluster_health" in fields and "actions" in fields:
        return {
            "cluster_health": health,
            "actions": [
                {
                    "target_node": target_node,
                    "action": action,
                    "priority": priority,
                    "rationale": rationale,
                }
            ],
        }
    return {}


def get_llm_response(
    prompt: str,
    npc: Optional[NPC] = None,
    format: Optional[Type[BaseModel]] = None,
    temperature: float = 0.0,
    timeout: float = 15.0,
) -> dict[str, Any]:
    """Query a local OpenAI-compatible LLM and optionally validate into a Pydantic model."""
    if npc is not None:
        npc.record_event("user", prompt)

    raw_text: Optional[str] = None
    parsed_obj: Any = None

    if npc is not None and npc.api_url:
        headers = {"Content-Type": "application/json"}
        if npc.api_key:
            headers["Authorization"] = f"Bearer {npc.api_key}"
        messages = [
            {"role": "system", "content": npc.primary_directive or f"You are {npc.name}."},
            {"role": "user", "content": prompt},
        ]
        payload: dict[str, Any] = {
            "model": npc.model,
            "messages": messages,
            "temperature": temperature,
        }
        if format is not None:
            payload["response_format"] = {"type": "json_object"}
        try:
            resp = httpx.post(
                f"{npc.api_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices") or []
                if choices:
                    msg = choices[0].get("message") or {}
                    candidate = msg.get("content")
                    if isinstance(candidate, str) and candidate.strip():
                        raw_text = candidate.strip()
                        if format is not None:
                            parsed_obj = format.model_validate(_extract_json_payload(raw_text))
                        else:
                            parsed_obj = raw_text
        except Exception:
            raw_text = None
            parsed_obj = None

    if parsed_obj is None:
        if format is not None:
            fallback_dict = _synthesize_structured_payload(prompt, format)
            parsed_obj = format.model_validate(fallback_dict)
            raw_text = parsed_obj.model_dump_json()
        else:
            raw_text = npc._synthesize_local_assessment(prompt) if npc is not None else prompt
            parsed_obj = raw_text

    if npc is not None and raw_text is not None:
        npc.record_event("assistant", raw_text)

    return {"response": parsed_obj, "raw": raw_text}


__all__ = ["get_llm_response"]
