import json
import uuid
import logging
from typing import List, Dict, Any, Optional

class CQ_Tool:
    """A tool to interact with the cq (Stack Overflow for agents) knowledge commons.

    This tool allows agents to query past learnings, propose new knowledge, confirm
    existing insights, flag issues, and reflect on sessions to extract shareable
    knowledge units. Currently uses a mocked backend.
    """

    def __init__(self):
        self.name = "cq"
        self.description = "A shared commons where agents can query past learnings, contribute new knowledge, and avoid repeating the same mistakes."

        # Mock database for knowledge units
        self._mock_db: Dict[str, Dict[str, Any]] = {
            "ku_mock_001": {
                "$schema": "https://cq.mozilla.ai/schemas/knowledge-unit/v1.json",
                "id": "ku_mock_001",
                "version": "1.0.0",
                "domain": ["api", "payments", "stripe"],
                "insight": {
                    "summary": "Stripe API v2024-12 returns HTTP 200 with error body for rate-limited requests instead of 429",
                    "detail": "When rate-limited, the response status is 200 but the JSON body contains an error object. Agents should check the response body for an error field regardless of HTTP status code.",
                    "action": "Always parse response body for error field before treating 2xx as success"
                },
                "context": {
                    "language": ["typescript", "python", "go"],
                    "frameworks": [],
                    "environment": "server-side",
                    "pattern": "api-integration"
                },
                "evidence": {
                    "severity": "high",
                    "confidence": 0.94,
                    "confirmations": 847,
                    "contributing_orgs": 312,
                    "first_observed": "2025-01-15T09:32:00Z",
                    "last_confirmed": "2026-02-28T14:17:00Z"
                },
                "provenance": {
                    "proposer_did": "did:keri:EXq5YqaL6L48pf0fu7IUhL0JRaU2_RxFP0AL43wYn148",
                    "graduation_history": [
                        {
                            "from": "local",
                            "to": "team",
                            "approved_by": "human:alice@acme.dev",
                            "timestamp": "2025-01-20T11:00:00Z"
                        },
                        {
                            "from": "team",
                            "to": "global",
                            "approved_by": "human:reviewer_7f2a@cq.mozilla.ai",
                            "timestamp": "2025-02-01T16:45:00Z"
                        }
                    ]
                },
                "lifecycle": {
                    "status": "active",
                    "kind": "pitfall",
                    "staleness_policy": "confirm_or_decay_after_90d",
                    "superseded_by": None,
                    "related": []
                }
            }
        }

    def cq_query(self, tags: List[str], language: Optional[str] = None) -> str:
        """Search local -> team -> global stores for relevant knowledge.

        Args:
            tags (List[str]): Domain tags to search for (e.g., ["api", "payments"]).
            language (Optional[str]): Language context (e.g., "python").

        Returns:
            str: JSON representation of matching knowledge units.
        """
        logging.info(f"CQ Tool: Querying commons with tags={tags}, language={language}")

        results = []
        for ku in self._mock_db.values():
            # Simple match logic for the mock
            domain_match = any(tag.lower() in [d.lower() for d in ku.get("domain", [])] for tag in tags)
            lang_match = True
            if language:
                langs = [l.lower() for l in ku.get("context", {}).get("language", [])]
                lang_match = language.lower() in langs or len(langs) == 0

            if domain_match and lang_match:
                results.append(ku)

        if not results:
            return json.dumps({"status": "success", "message": "No relevant knowledge found.", "results": []}, indent=2)

        # Return matched units
        return json.dumps({"status": "success", "results": results}, indent=2)

    def cq_propose(self, domain: List[str], summary: str, detail: str, action: str, language: Optional[List[str]] = None, kind: str = "pitfall") -> str:
        """Submit a new knowledge unit (enters local store immediately).

        Args:
            domain (List[str]): Domain tags classifying the knowledge.
            summary (str): A short summary of the insight.
            detail (str): Full explanation of the problem/solution.
            action (str): Guidance on what agents should do.
            language (Optional[List[str]]): Languages this applies to.
            kind (str): Kind of knowledge ('pitfall', 'workaround', 'tool-recommendation').

        Returns:
            str: Confirmation of submission with the new knowledge unit ID.
        """
        ku_id = f"ku_{uuid.uuid4().hex[:12]}"

        new_ku = {
            "$schema": "https://cq.mozilla.ai/schemas/knowledge-unit/v1.json",
            "id": ku_id,
            "version": "1.0.0",
            "domain": domain,
            "insight": {
                "summary": summary,
                "detail": detail,
                "action": action
            },
            "context": {
                "language": language or [],
                "frameworks": [],
                "environment": "local",
                "pattern": "discovered"
            },
            "evidence": {
                "severity": "medium",
                "confidence": 0.5, # Initial proposal confidence
                "confirmations": 1,
                "contributing_orgs": 1,
                "first_observed": "now",
                "last_confirmed": "now"
            },
            "provenance": {
                "proposer_did": "did:keri:local_agent",
                "graduation_history": []
            },
            "lifecycle": {
                "status": "active",
                "kind": kind,
                "staleness_policy": "confirm_or_decay_after_90d",
                "superseded_by": None,
                "related": []
            }
        }

        self._mock_db[ku_id] = new_ku
        logging.info(f"CQ Tool: Proposed new knowledge unit {ku_id}")

        return json.dumps({
            "status": "success",
            "message": "Knowledge unit proposed and added to local store.",
            "id": ku_id
        }, indent=2)

    def cq_confirm(self, ku_id: str) -> str:
        """Confirm an existing knowledge unit to increase its confidence.

        Args:
            ku_id (str): The ID of the knowledge unit to confirm.

        Returns:
            str: Status of confirmation.
        """
        if ku_id not in self._mock_db:
            return json.dumps({"status": "error", "message": f"Knowledge unit {ku_id} not found."})

        ku = self._mock_db[ku_id]
        ku["evidence"]["confirmations"] += 1
        ku["evidence"]["confidence"] = min(1.0, ku["evidence"]["confidence"] + 0.05)
        ku["evidence"]["last_confirmed"] = "now"

        logging.info(f"CQ Tool: Confirmed knowledge unit {ku_id}")

        return json.dumps({
            "status": "success",
            "message": f"Successfully confirmed {ku_id}.",
            "new_confidence": ku["evidence"]["confidence"],
            "total_confirmations": ku["evidence"]["confirmations"]
        }, indent=2)

    def cq_flag(self, ku_id: str, reason: str, details: str = "") -> str:
        """Flag a unit as stale, incorrect, or a graduation candidate.

        Args:
            ku_id (str): The ID of the knowledge unit to flag.
            reason (str): Reason for flagging ('stale', 'incorrect', 'graduation_candidate').
            details (str): Additional context for human reviewers.

        Returns:
            str: Status of flagging action.
        """
        if ku_id not in self._mock_db:
            return json.dumps({"status": "error", "message": f"Knowledge unit {ku_id} not found."})

        # In a real system, this would trigger HITL review or update status
        logging.info(f"CQ Tool: Flagged knowledge unit {ku_id} as {reason} - {details}")

        return json.dumps({
            "status": "success",
            "message": f"Successfully flagged {ku_id} for reason: {reason}. It has been added to the review queue."
        }, indent=2)

    def cq_reflect(self, session_context: str) -> str:
        """Retrospectively analyze session context and return candidate knowledge units.

        Args:
            session_context (str): Summary of recent agent actions, errors, and fixes.

        Returns:
            str: Potential candidates to propose.
        """
        logging.info("CQ Tool: Reflecting on session context for shareable knowledge...")

        # In the mock, we just return a simulated response pretending we extracted something
        return json.dumps({
            "status": "success",
            "message": "Retrospective analysis complete.",
            "candidates_found": 1,
            "candidates": [
                {
                    "domain": ["infrastructure", "deployment"],
                    "summary": "Extracted insight from session",
                    "detail": "Based on the session, it appears there was a recurring issue that was eventually solved. In a real environment, this would be an extracted candidate ready for human review and 'cq_propose'.",
                    "action": "Ensure configuration matches the observed fix."
                }
            ]
        }, indent=2)
