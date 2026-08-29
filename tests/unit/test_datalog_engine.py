import pytest
import os
import tempfile
import time
from pipecatapp.datalog_engine import DatalogEngine
from pipecatapp.datalog_memory import DatalogMemory
from pipecatapp.pmm_memory import PMMMemory

def test_datalog_engine_basic_fact_and_rule():
    engine = DatalogEngine()

    # Rule: controls_kernel_object(Attacker) :- controls(Attacker, ObjA), points_to(ObjA, ObjB), kernel_object(ObjB)
    engine.add_rule(
        head_predicate="controls_kernel_object",
        head_args=("Attacker",),
        body=[
            ("controls", ("Attacker", "ObjA")),
            ("points_to", ("ObjA", "ObjB")),
            ("kernel_object", ("ObjB",))
        ]
    )

    engine.assert_fact("controls", "attacker", "object_a")
    engine.assert_fact("points_to", "object_a", "object_b")
    engine.assert_fact("kernel_object", "object_b")

    results = engine.query("controls_kernel_object")
    assert len(results) == 1
    assert results[0].args == ("attacker",)


def test_datalog_engine_retraction_propagation():
    engine = DatalogEngine()

    # Rule: reachable(X, Y) :- edge(X, Y)
    engine.add_rule("reachable", ("X", "Y"), [("edge", ("X", "Y"))])
    # Rule: reachable(X, Z) :- edge(X, Y), reachable(Y, Z)
    engine.add_rule("reachable", ("X", "Z"), [("edge", ("X", "Y")), ("reachable", ("Y", "Z"))])

    engine.assert_fact("edge", "node1", "node2")
    engine.assert_fact("edge", "node2", "node3")

    # Reachable: (node1, node2), (node2, node3), (node1, node3)
    results = engine.query("reachable")
    assert len(results) == 3

    # Retract edge(node1, node2)
    retracted = engine.retract_fact("edge", "node1", "node2")
    assert retracted is True

    # Remaining reachable: only (node2, node3)
    results_after = engine.query("reachable")
    assert len(results_after) == 1
    assert results_after[0].args == ("node2", "node3")


def test_datalog_engine_provenance_explain():
    engine = DatalogEngine()

    engine.add_rule("vulnerable", ("Obj",), [("freed", ("Obj",)), ("reused", ("Obj",))])

    engine.assert_fact("freed", "buf_1")
    engine.assert_fact("reused", "buf_1")

    explanation = engine.explain("vulnerable", "buf_1")
    assert explanation["type"] == "derived"
    assert len(explanation["derivations"]) == 1
    assert "freed('buf_1')" in str(explanation)
    assert "reused('buf_1')" in str(explanation)


def test_datalog_memory_integration():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_datalog.db")
        pmm = PMMMemory(db_path=db_path)
        mem = DatalogMemory(pmm=pmm)

        mem.add_rule("exploitable", ("Target",), [{"predicate": "vulnerable", "args": ["Target"]}])
        mem.assert_fact("vulnerable", "target_system_a")

        active_state = mem.query_state("exploitable")
        assert len(active_state) == 1
        assert active_state[0]["args"] == ["target_system_a"]

        # Verify event ledger recorded assertion and rule addition
        events = pmm.get_events_sync(limit=10)
        kinds = [e["kind"] for e in events]
        assert "datalog_rule_added" in kinds
        assert "datalog_fact_asserted" in kinds
