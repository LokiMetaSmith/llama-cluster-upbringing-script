"""DatalogMemory: Integrated Datalog Maintained State Store backed by PMMMemory Event Ledger.
"""

from typing import Dict, Any, List, Optional, Tuple
from pipecatapp.datalog_engine import DatalogEngine, FactRecord
from pipecatapp.pmm_memory import PMMMemory

class DatalogMemory:
    """Combines a deterministic Datalog state engine with an append-only event-sourced PMMMemory ledger."""

    def __init__(self, pmm: Optional[PMMMemory] = None, db_path: str = "pmm_datalog_memory.db"):
        self.pmm = pmm or PMMMemory(db_path=db_path)
        self.engine = DatalogEngine()

    def assert_fact(
        self,
        predicate: str,
        *args: Any,
        valid_from: Optional[float] = None,
        valid_to: float = float("inf"),
        meta: Optional[Dict[str, Any]] = None
    ) -> FactRecord:
        """Asserts a fact into the Datalog engine and records an event in the PMM ledger."""
        fact = self.engine.assert_fact(predicate, *args, valid_from=valid_from, valid_to=valid_to)

        event_meta = meta or {}
        event_meta.update({
            "predicate": predicate,
            "args": list(args),
            "valid_from": fact.valid_from,
            "valid_to": fact.valid_to,
            "is_base": fact.is_base
        })

        self.pmm.add_event_sync(
            kind="datalog_fact_asserted",
            content=f"Asserted base fact {predicate}{args}",
            meta=event_meta
        )
        return fact

    def retract_fact(self, predicate: str, *args: Any, meta: Optional[Dict[str, Any]] = None) -> bool:
        """Retracts a fact from the Datalog engine and records a retraction event in the PMM ledger."""
        success = self.engine.retract_fact(predicate, *args)
        if success:
            event_meta = meta or {}
            event_meta.update({"predicate": predicate, "args": list(args)})
            self.pmm.add_event_sync(
                kind="datalog_fact_retracted",
                content=f"Retracted fact {predicate}{args}",
                meta=event_meta
            )
        return success

    def add_rule(
        self,
        head_predicate: str,
        head_args: List[str],
        body: List[Dict[str, Any]]
    ):
        """Adds a Datalog rule and records the rule in the PMM ledger.

        body format: [{"predicate": "controls", "args": ["Attacker", "ObjA"]}, ...]
        """
        engine_body: List[Tuple[str, Tuple[str, ...]]] = [
            (b["predicate"], tuple(b["args"])) for b in body
        ]
        rule = self.engine.add_rule(head_predicate, tuple(head_args), engine_body)

        self.pmm.add_event_sync(
            kind="datalog_rule_added",
            content=f"Added Datalog rule: {rule}",
            meta={"head_predicate": head_predicate, "head_args": head_args, "body": body}
        )
        return rule

    def query_state(self, predicate: Optional[str] = None, timestamp: Optional[float] = None) -> List[Dict[str, Any]]:
        """Queries active facts from the maintained state."""
        facts = self.engine.query(predicate=predicate, timestamp=timestamp)
        return [
            {
                "predicate": f.predicate,
                "args": list(f.args),
                "valid_from": f.valid_from,
                "valid_to": f.valid_to,
                "is_base": f.is_base,
                "representation": repr(f)
            }
            for f in facts
        ]

    def explain(self, predicate: str, *args: Any) -> Dict[str, Any]:
        """Explains the provenance and support graph for a fact."""
        return self.engine.explain(predicate, *args)
