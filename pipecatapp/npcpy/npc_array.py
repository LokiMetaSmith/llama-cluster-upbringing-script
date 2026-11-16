"""Vectorized worker fan-out and multi-round consensus via NPCArray."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

from . import NPC


class NPCArray:
    """Executes parallel inference and multi-round debate across worker NPCs."""

    def __init__(self, npcs: list[NPC]) -> None:
        self.npcs = list(npcs)

    def infer(
        self,
        prompt: str,
        max_workers: Optional[int] = None,
        temperature: float = 0.2,
    ) -> list[dict[str, Any]]:
        """Run parallel single-pass inference across all NPCs in the array."""
        if not self.npcs:
            return []

        worker_count = max_workers or min(len(self.npcs), 8)

        def _run_one(npc: NPC) -> dict[str, Any]:
            response = npc.infer(prompt, temperature=temperature)
            return {
                "npc": npc.name,
                "model": npc.model,
                "response": response,
            }

        with ThreadPoolExecutor(max_workers=worker_count) as pool:
            return list(pool.map(_run_one, self.npcs))

    def debate(self, topic: str, rounds: int = 2, max_workers: Optional[int] = None) -> str:
        """Run multi-round debate to reconcile worker signals and filter false positives."""
        if not self.npcs:
            return "No worker NPCs available for debate."

        total_rounds = max(1, rounds)
        current_context = topic
        round_outputs: list[dict[str, Any]] = []

        for round_idx in range(1, total_rounds + 1):
            round_prompt = (
                f"Consensus Round {round_idx}/{total_rounds}:\n"
                f"{current_context}\n\n"
                "Reconcile conflicting signals, suppress single-sample noise, and state "
                "confirmed root causes."
            )
            round_outputs = self.infer(round_prompt, max_workers=max_workers, temperature=0.1)
            formatted_round = "\n".join(
                f"[{item['npc']}] {item['response']}" for item in round_outputs
            )
            current_context = f"{topic}\n\nRound {round_idx} positions:\n{formatted_round}"

        summary_lines = [
            f"Consensus after {total_rounds} rounds across {len(self.npcs)} workers:"
        ]
        for item in round_outputs:
            summary_lines.append(f"- {item['npc']}: {item['response']}")
        return "\n".join(summary_lines)


__all__ = ["NPCArray"]
