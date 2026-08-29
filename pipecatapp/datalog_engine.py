"""Datalog State Engine for Maintained Agentic Memory in PipecatApp.

Provides deterministic logic evaluation, incremental support counting,
retraction propagation, temporal validity bounds, and provenance explanations.
"""

import time
from typing import Dict, Any, List, Tuple, Optional, Set

class FactRecord:
    """Represents a fact in the Datalog database."""

    def __init__(
        self,
        predicate: str,
        args: Tuple[Any, ...],
        valid_from: float = 0.0,
        valid_to: float = float("inf"),
        is_base: bool = True,
        derived_by: Optional[List[Dict[str, Any]]] = None
    ):
        self.predicate = predicate
        self.args = tuple(args)
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.is_base = is_base
        self.derived_by = derived_by or []  # List of dicts describing rule & premise facts

    @property
    def key(self) -> Tuple[str, Tuple[Any, ...]]:
        return (self.predicate, self.args)

    def is_valid_at(self, timestamp: float) -> bool:
        return self.valid_from <= timestamp < self.valid_to

    def __repr__(self) -> str:
        arg_str = ", ".join(repr(a) for a in self.args)
        time_str = f"[{self.valid_from}, {self.valid_to})"
        return f"{self.predicate}({arg_str}) {time_str}"


class DatalogRule:
    """Represents a Datalog deductive rule: Head :- Body1, Body2, ..."""

    def __init__(self, head_predicate: str, head_args: Tuple[str, ...], body: List[Tuple[str, Tuple[str, ...]]]):
        self.head_predicate = head_predicate
        self.head_args = head_args  # e.g., ('Attacker', 'ObjB')
        self.body = body            # e.g., [('controls', ('Attacker', 'ObjA')), ('points_to', ('ObjA', 'ObjB'))]

    def __repr__(self) -> str:
        head = f"{self.head_predicate}({', '.join(self.head_args)})"
        body_str = ", ".join(f"{pred}({', '.join(args)})" for pred, args in self.body)
        return f"{head} :- {body_str}."


class DatalogEngine:
    """Deterministic Datalog fixed-point analysis engine with support-based retractions."""

    def __init__(self):
        # Maps fact key -> FactRecord
        self.facts: Dict[Tuple[str, Tuple[Any, ...]], FactRecord] = {}
        # List of active Datalog rules
        self.rules: List[DatalogRule] = []
        # Support map for derived facts: fact_key -> Set of (rule_index, premise_fact_keys_tuple)
        self.support: Dict[Tuple[str, Tuple[Any, ...]], Set[Tuple[int, Tuple[Tuple[str, Tuple[Any, ...]], ...]]]] = {}

    def add_rule(self, head_predicate: str, head_args: Tuple[str, ...], body: List[Tuple[str, Tuple[str, ...]]]) -> DatalogRule:
        rule = DatalogRule(head_predicate, head_args, body)
        self.rules.append(rule)
        self.evaluate()
        return rule

    def assert_fact(
        self,
        predicate: str,
        *args: Any,
        valid_from: Optional[float] = None,
        valid_to: float = float("inf")
    ) -> FactRecord:
        """Asserts a base fact and triggers incremental rule evaluation."""
        now = time.time() if valid_from is None else valid_from
        key = (predicate, tuple(args))

        if key in self.facts:
            record = self.facts[key]
            record.valid_from = min(record.valid_from, now)
            record.valid_to = max(record.valid_to, valid_to)
            record.is_base = True
        else:
            record = FactRecord(predicate, tuple(args), valid_from=now, valid_to=valid_to, is_base=True)
            self.facts[key] = record

        self.evaluate()
        return record

    def retract_fact(self, predicate: str, *args: Any) -> bool:
        """Retracts a base fact and recursively purges derived facts whose support drops to zero."""
        key = (predicate, tuple(args))
        if key not in self.facts:
            return False

        record = self.facts[key]

        if not record.is_base and key in self.support and len(self.support[key]) > 0:
            # Derived fact with active support cannot be manually retracted without retracting underlying premises
            return False

        # Mark base status as False or remove fact
        if key in self.support and len(self.support[key]) > 0:
            record.is_base = False
        else:
            del self.facts[key]

        # Cascading retraction update
        self._prune_unsupported_facts()
        return True

    def evaluate(self) -> None:
        """Evaluates rules until fixed point is reached."""
        changed = True
        while changed:
            changed = False
            for rule_idx, rule in enumerate(self.rules):
                if self._evaluate_single_rule(rule_idx, rule):
                    changed = True

    def _evaluate_single_rule(self, rule_idx: int, rule: DatalogRule) -> bool:
        new_derived = False

        def match_body(
            body_idx: int,
            bindings: Dict[str, Any],
            matched_premises: List[FactRecord]
        ):
            nonlocal new_derived
            if body_idx == len(rule.body):
                # All body predicates matched! Construct head fact
                head_args = tuple(bindings[var] for var in rule.head_args)
                head_key = (rule.head_predicate, head_args)

                # Temporal validity of derived fact is intersection of premise validity intervals
                v_from = max(p.valid_from for p in matched_premises)
                v_to = min(p.valid_to for p in matched_premises)

                if v_from >= v_to:
                    return  # Invalid temporal range

                premise_keys = tuple(p.key for p in matched_premises)
                support_item = (rule_idx, premise_keys)

                if head_key not in self.support:
                    self.support[head_key] = set()

                if support_item not in self.support[head_key]:
                    self.support[head_key].add(support_item)

                    if head_key not in self.facts:
                        derived_record = FactRecord(
                            rule.head_predicate,
                            head_args,
                            valid_from=v_from,
                            valid_to=v_to,
                            is_base=False,
                            derived_by=[{
                                "rule_index": rule_idx,
                                "rule": str(rule),
                                "premises": [p.key for p in matched_premises]
                            }]
                        )
                        self.facts[head_key] = derived_record
                        new_derived = True
                    else:
                        rec = self.facts[head_key]
                        rec.valid_from = min(rec.valid_from, v_from)
                        rec.valid_to = max(rec.valid_to, v_to)
                        rec.derived_by.append({
                            "rule_index": rule_idx,
                            "rule": str(rule),
                            "premises": [p.key for p in matched_premises]
                        })
                return

            pred, patterns = rule.body[body_idx]
            # Find candidate matching facts
            for fact_key, fact in list(self.facts.items()):
                if fact.predicate != pred or len(fact.args) != len(patterns):
                    continue

                new_bindings = dict(bindings)
                match_possible = True
                for pat, arg in zip(patterns, fact.args):
                    if pat[0].isupper():  # Variable
                        if pat in new_bindings:
                            if new_bindings[pat] != arg:
                                match_possible = False
                                break
                        else:
                            new_bindings[pat] = arg
                    else:  # Constant symbol
                        if pat != arg:
                            match_possible = False
                            break

                if match_possible:
                    match_body(body_idx + 1, new_bindings, matched_premises + [fact])

        match_body(0, {}, [])
        return new_derived

    def _prune_unsupported_facts(self) -> None:
        """Cascading retraction: removes derived facts that lose all premise support."""
        changed = True
        while changed:
            changed = False
            for head_key in list(self.support.keys()):
                supports = self.support[head_key]
                valid_supports = set()

                for rule_idx, premise_keys in supports:
                    # Premise is valid if all premise keys still exist in self.facts
                    if all(pk in self.facts for pk in premise_keys):
                        valid_supports.add((rule_idx, premise_keys))

                if len(valid_supports) != len(supports):
                    self.support[head_key] = valid_supports
                    changed = True

                if len(valid_supports) == 0:
                    del self.support[head_key]
                    if head_key in self.facts and not self.facts[head_key].is_base:
                        del self.facts[head_key]
                        changed = True

    def query(self, predicate: Optional[str] = None, timestamp: Optional[float] = None) -> List[FactRecord]:
        """Queries currently active facts, optionally filtered by predicate and timestamp."""
        now = time.time() if timestamp is None else timestamp
        results = []
        for fact in self.facts.values():
            if predicate is not None and fact.predicate != predicate:
                continue
            if fact.is_valid_at(now):
                results.append(fact)
        return results

    def explain(self, predicate: str, *args: Any) -> Dict[str, Any]:
        """Builds an explicit provenance tree explaining why a fact is currently believed."""
        key = (predicate, tuple(args))
        if key not in self.facts:
            return {"fact": f"{predicate}{args}", "status": "NOT_FOUND"}

        record = self.facts[key]
        if record.is_base:
            return {"fact": repr(record), "type": "base_observation", "support": []}

        tree = {
            "fact": repr(record),
            "type": "derived",
            "derivations": []
        }

        if key in self.support:
            for rule_idx, premise_keys in self.support[key]:
                rule = self.rules[rule_idx]
                derivation_branch = {
                    "rule": str(rule),
                    "premises": [self.explain(pk[0], *pk[1]) for pk in premise_keys]
                }
                tree["derivations"].append(derivation_branch)

        return tree
