import pytest
from pipecatapp.datalog_engine import DatalogEngine

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
