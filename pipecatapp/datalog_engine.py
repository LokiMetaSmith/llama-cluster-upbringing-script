"""Datalog State & Program Analysis Engine for PipecatApp.

Provides deterministic logic evaluation, incremental support counting,
retraction propagation, temporal validity bounds, provenance explanations,
and AST program analysis call graph indexing.
"""

import ast
import os
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
    """Deterministic Datalog fixed-point analysis engine with support-based retractions and AST program indexing."""

    def __init__(self):
        # Maps fact key -> FactRecord
        self.facts: Dict[Tuple[str, Tuple[Any, ...]], FactRecord] = {}
        # List of active Datalog rules
        self.rules: List[DatalogRule] = []
        # Support map for derived facts: fact_key -> Set of (rule_index, premise_fact_keys_tuple)
        self.support: Dict[Tuple[str, Tuple[Any, ...]], Set[Tuple[int, Tuple[Tuple[str, Tuple[Any, ...]], ...]]]] = {}

        # Program AST Analysis Relational Facts Cache
        self.ast_facts: Dict[str, List[tuple]] = {
            "defines_function": [],   # (file, func_name, lineno)
            "calls_function": [],     # (file, caller_func, callee_func, lineno)
            "imports_module": [],     # (file, imported_module)
            "defines_class": [],      # (file, class_name, lineno)
        }

    # --- AST Program Analysis Methods ---

    def index_file(self, filepath: str, code_content: str = None) -> Dict[str, Any]:
        """Parses Python AST and populates Datalog program analysis facts."""
        if code_content is None:
            if not os.path.exists(filepath):
                return {"error": f"File {filepath} not found."}
            with open(filepath, "r", encoding="utf-8") as f:
                code_content = f.read()

        try:
            tree = ast.parse(code_content, filename=filepath)
        except Exception as e:
            return {"error": f"Failed to parse AST: {e}"}

        rel_path = filepath
        engine_self = self

        class ASTVisitor(ast.NodeVisitor):
            def __init__(visitor_self):
                visitor_self.scope_stack = ["<global>"]

            def visit_FunctionDef(visitor_self, node):
                func_name = node.name
                engine_self.ast_facts["defines_function"].append((rel_path, func_name, node.lineno))
                engine_self.assert_fact("defines_function", rel_path, func_name, node.lineno)
                visitor_self.scope_stack.append(func_name)
                visitor_self.generic_visit(node)
                visitor_self.scope_stack.pop()

            def visit_AsyncFunctionDef(visitor_self, node):
                visitor_self.visit_FunctionDef(node)

            def visit_ClassDef(visitor_self, node):
                engine_self.ast_facts["defines_class"].append((rel_path, node.name, node.lineno))
                engine_self.assert_fact("defines_class", rel_path, node.name, node.lineno)
                visitor_self.generic_visit(node)

            def visit_Call(visitor_self, node):
                caller = visitor_self.scope_stack[-1]
                callee = None
                if isinstance(node.func, ast.Name):
                    callee = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    callee = node.func.attr
                if callee:
                    line = getattr(node, 'lineno', 0)
                    engine_self.ast_facts["calls_function"].append((rel_path, caller, callee, line))
                    engine_self.assert_fact("calls_function", rel_path, caller, callee, line)
                visitor_self.generic_visit(node)

            def visit_Import(visitor_self, node):
                for alias in node.names:
                    engine_self.ast_facts["imports_module"].append((rel_path, alias.name))
                    engine_self.assert_fact("imports_module", rel_path, alias.name)
                visitor_self.generic_visit(node)

            def visit_ImportFrom(visitor_self, node):
                if node.module:
                    engine_self.ast_facts["imports_module"].append((rel_path, node.module))
                    engine_self.assert_fact("imports_module", rel_path, node.module)
                visitor_self.generic_visit(node)

        visitor = ASTVisitor()
        visitor.visit(tree)

        return {
            "indexed_file": rel_path,
            "defines_count": len(self.ast_facts["defines_function"]),
            "calls_count": len(self.ast_facts["calls_function"]),
            "imports_count": len(self.ast_facts["imports_module"])
        }

    def query_callers(self, target_function: str) -> List[Dict[str, Any]]:
        """Finds all functions that call target_function."""
        results = []
        for file, caller, callee, lineno in self.ast_facts["calls_function"]:
            if callee == target_function:
                results.append({
                    "file": file,
                    "caller": caller,
                    "lineno": lineno
                })
        return results

    def query_transitive_calls(self, start_function: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Datalog transitive closure: finds all functions transitively reachable from start_function."""
        visited = set()
        call_chain = []

        def dfs(current: str, depth: int, path: List[str]):
            if depth > max_depth or current in visited:
                return
            visited.add(current)
            for file, caller, callee, lineno in self.ast_facts["calls_function"]:
                if caller == current and callee not in path:
                    new_path = path + [callee]
                    call_chain.append({
                        "caller": current,
                        "callee": callee,
                        "depth": depth,
                        "file": file,
                        "lineno": lineno,
                        "path": new_path
                    })
                    dfs(callee, depth + 1, new_path)

        dfs(start_function, 1, [start_function])
        return call_chain

    # --- Datalog Fixed-Point Engine Methods ---

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
            return False

        if key in self.support and len(self.support[key]) > 0:
            record.is_base = False
        else:
            del self.facts[key]

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
                head_args = tuple(bindings[var] for var in rule.head_args)
                head_key = (rule.head_predicate, head_args)

                v_from = max(p.valid_from for p in matched_premises)
                v_to = min(p.valid_to for p in matched_premises)

                if v_from >= v_to:
                    return

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
            for fact_key, fact in list(self.facts.items()):
                if fact.predicate != pred or len(fact.args) != len(patterns):
                    continue

                new_bindings = dict(bindings)
                match_possible = True
                for pat, arg in zip(patterns, fact.args):
                    if pat[0].isupper():
                        if pat in new_bindings:
                            if new_bindings[pat] != arg:
                                match_possible = False
                                break
                        else:
                            new_bindings[pat] = arg
                    else:
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

    def explain(self, predicate_or_symbol: str, *args: Any) -> Dict[str, Any]:
        """
        Builds an explicit provenance tree explaining why a fact or AST symbol is currently believed.
        Supports both Datalog fact tuples and AST symbol queries.
        """
        key = (predicate_or_symbol, tuple(args))
        if key in self.facts:
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

        if not args:
            # Symbol explanation for AST program analysis
            target_symbol = predicate_or_symbol
            defines = [f for f in self.ast_facts["defines_function"] if f[1] == target_symbol]
            callers = self.query_callers(target_symbol)
            transitive_callees = self.query_transitive_calls(target_symbol)

            return {
                "symbol": target_symbol,
                "definitions": [{"file": f[0], "lineno": f[2]} for f in defines],
                "direct_callers": callers,
                "transitive_call_graph": transitive_callees
            }

        return {"fact": f"{predicate_or_symbol}{args}", "status": "NOT_FOUND"}
