import logging
from typing import Dict, Any, Optional
from pipecatapp.memory_backends_impl.pmm_backend import PMMMemoryBackend

class MemoryCandidateTool:
    """A tool for managing the memory candidate promotion pipeline.

    Subagents emit candidate facts/conventions without polluting permanent memory.
    The orchestrator or verifier promotes high-value candidates to durable storage.
    """

    def __init__(self, backend: Optional[PMMMemoryBackend] = None, db_path: str = "pmm_memory.db"):
        self.name = "memory_candidate"
        self.logger = logging.getLogger(__name__)
        self.backend = backend or PMMMemoryBackend(db_path=db_path)

    def get_schema(self) -> dict:
        """Returns the JSON schema for MemoryCandidateTool."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": (
                    "Emit, list, promote, or reject memory candidates before writing to durable storage."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["emit", "list_pending", "promote", "reject"],
                            "description": "Action to perform on memory candidates."
                        },
                        "candidate_text": {
                            "type": "string",
                            "description": "The candidate fact, convention, or decision text to emit."
                        },
                        "source": {
                            "type": "string",
                            "description": "The subagent or component emitting the candidate (e.g., 'subagent-coder')."
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Session identifier (default: 'global')."
                        },
                        "category": {
                            "type": "string",
                            "enum": ["convention", "decision", "bugfix", "architecture"],
                            "description": "Category of the candidate (default: 'convention')."
                        },
                        "importance": {
                            "type": "integer",
                            "description": "Importance rating from 1 (low) to 5 (critical) (default: 3)."
                        },
                        "candidate_id": {
                            "type": "integer",
                            "description": "Candidate ID to promote or reject."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    async def execute(self, action: str, candidate_text: str = "", source: str = "agent",
                      session_id: str = "global", category: str = "convention",
                      importance: int = 3, candidate_id: int = 0, **kwargs) -> str:
        """Executes candidate promotion actions."""
        try:
            if action == "emit":
                if not candidate_text:
                    return "Error: candidate_text is required for emit action."
                cid = self.backend.emit_candidate(
                    source=source,
                    candidate_text=candidate_text,
                    session_id=session_id,
                    category=category,
                    importance=importance
                )
                return f"Successfully emitted memory candidate (ID: {cid}) for session '{session_id}'."

            elif action == "list_pending":
                sid = session_id if session_id != "global" else None
                candidates = self.backend.list_pending_candidates(session_id=sid)
                if not candidates:
                    return "No pending memory candidates found."
                lines = [f"=== Pending Memory Candidates ({len(candidates)}) ==="]
                for c in candidates:
                    lines.append(
                        f"[{c['id']}] Session: {c['session_id']} | Source: {c['source']} | "
                        f"Category: {c['category']} | Imp: {c['importance']}\n"
                        f"     Text: {c['candidate_text']}"
                    )
                return "\n".join(lines)

            elif action == "promote":
                if not candidate_id:
                    return "Error: candidate_id is required for promote action."
                mem_id = self.backend.promote_candidate(candidate_id)
                if mem_id is None:
                    return f"Error: Candidate ID {candidate_id} not found or already processed."
                return f"Successfully promoted candidate ID {candidate_id} to durable memory (Event ID: {mem_id})."

            elif action == "reject":
                if not candidate_id:
                    return "Error: candidate_id is required for reject action."
                success = self.backend.reject_candidate(candidate_id)
                if not success:
                    return f"Error: Candidate ID {candidate_id} not found or already processed."
                return f"Successfully rejected candidate ID {candidate_id}."

            else:
                return f"Error: Unknown action '{action}'"

        except Exception as e:
            self.logger.error(f"Error executing memory_candidate action '{action}': {e}", exc_info=True)
            return f"Error processing memory candidate: {e}"
