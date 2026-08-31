import os
import tempfile
import pytest
from pipecatapp.datalog_engine import DatalogEngine
from pipecatapp.datalog_memory import DatalogMemory
from pipecatapp.pmm_memory import PMMMemory

def test_datalog_indexing_and_explain():
    engine = DatalogEngine()
    sample_code = """
import os

def helper_a():
    return 42

def helper_b(x):
    return helper_a() + x

class Calculator:
    def compute(self, val):
        return helper_b(val)
"""
    res = engine.index_file("test_calc.py", sample_code)
    assert res["indexed_file"] == "test_calc.py"
    assert res["defines_count"] == 3
    assert res["calls_count"] == 2

    # Query callers of helper_a
    callers = engine.query_callers("helper_a")
    assert len(callers) == 1
    assert callers[0]["caller"] == "helper_b"

    # Query transitive calls from helper_b
    transitive = engine.query_transitive_calls("helper_b")
    assert len(transitive) >= 1
    assert transitive[0]["callee"] == "helper_a"

    # Explain symbol
    exp = engine.explain("helper_a")
    assert exp["symbol"] == "helper_a"
    assert len(exp["definitions"]) == 1
    assert len(exp["direct_callers"]) == 1

def test_datalog_engine_basic_fact_and_rule():
    engine = DatalogEngine()

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

    engine.add_rule("reachable", ("X", "Y"), [("edge", ("X", "Y"))])
    engine.add_rule("reachable", ("X", "Z"), [("edge", ("X", "Y")), ("reachable", ("Y", "Z"))])

    engine.assert_fact("edge", "node1", "node2")
    engine.assert_fact("edge", "node2", "node3")

    results = engine.query("reachable")
    assert len(results) == 3

    retracted = engine.retract_fact("edge", "node1", "node2")
    assert retracted is True

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

        events = pmm.get_events_sync(limit=10)
        kinds = [e["kind"] for e in events]
        assert "datalog_rule_added" in kinds
        assert "datalog_fact_asserted" in kinds
