"""Datalog Extraction Tool for converting natural language observations into canonical Datalog facts and retractions.
"""

import json
from typing import Dict, Any, List, Optional
from pipecatapp.datalog_memory import DatalogMemory

class DatalogExtractionTool:
    """Tool that uses structured JSON payloads or LLM output to update Datalog state."""

    def __init__(self, datalog_memory: Optional[DatalogMemory] = None):
        self.datalog_memory = datalog_memory or DatalogMemory()

    def parse_and_apply_extraction(self, extraction_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Applies extracted assertions, retractions, and rules to DatalogMemory.

        Expected extraction_payload structure:
        {
            "assert_facts": [
                {"predicate": "controls", "args": ["attacker", "obj_a"]},
                {"predicate": "points_to", "args": ["obj_a", "obj_b"]}
            ],
            "retract_facts": [
                {"predicate": "points_to", "args": ["obj_a", "obj_old"]}
            ],
            "rules": [
                {
                    "head_predicate": "controls_kernel_object",
                    "head_args": ["Attacker"],
                    "body": [
                        {"predicate": "controls", "args": ["Attacker", "ObjA"]},
                        {"predicate": "points_to", "args": ["ObjA", "ObjB"]},
                        {"predicate": "kernel_object", "args": ["ObjB"]}
                    ]
                }
            ]
        }
        """
        applied_asserts = []
        applied_retracts = []
        applied_rules = []

        # Process Rules
        for r in extraction_payload.get("rules", []):
            rule_obj = self.datalog_memory.add_rule(
                head_predicate=r["head_predicate"],
                head_args=r["head_args"],
                body=r["body"]
            )
            applied_rules.append(str(rule_obj))

        # Process Assertions
        for f in extraction_payload.get("assert_facts", []):
            rec = self.datalog_memory.assert_fact(
                f["predicate"],
                *f["args"],
                valid_from=f.get("valid_from"),
                valid_to=f.get("valid_to", float("inf"))
            )
            applied_asserts.append(repr(rec))

        # Process Retractions
        for rf in extraction_payload.get("retract_facts", []):
            success = self.datalog_memory.retract_fact(rf["predicate"], *rf["args"])
            applied_retracts.append({"predicate": rf["predicate"], "args": rf["args"], "success": success})

        return {
            "status": "success",
            "asserted": applied_asserts,
            "retracted": applied_retracts,
            "rules_added": applied_rules
        }

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Standard tool execution interface."""
        action = payload.get("action", "extract_and_apply")
        if action == "extract_and_apply":
            extraction_json = payload.get("extraction")
            if isinstance(extraction_json, str):
                extraction_json = json.loads(extraction_json)
            return self.parse_and_apply_extraction(extraction_json)
        elif action == "query":
            predicate = payload.get("predicate")
            return {"results": self.datalog_memory.query_state(predicate=predicate)}
        elif action == "explain":
            predicate = payload.get("predicate")
            args = payload.get("args", [])
            return self.datalog_memory.explain(predicate, *args)
        else:
            return {"error": f"Unknown action: {action}"}
