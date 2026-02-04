import time
import json
import pytest
from pipecatapp.workflow.runner import make_serializable

class NonSerializable:
    def __str__(self):
        return "<NonSerializable>"

def test_make_serializable_primitives():
    assert make_serializable(1) == 1
    assert make_serializable("test") == "test"
    assert make_serializable(True) is True
    assert make_serializable(None) is None
    assert make_serializable(1.5) == 1.5

def test_make_serializable_dict():
    obj = {"a": 1, "b": "test"}
    assert make_serializable(obj) == obj

def test_make_serializable_list():
    obj = [1, "test", True]
    assert make_serializable(obj) == obj

def test_make_serializable_nested():
    obj = {"a": [1, {"b": 2}]}
    assert make_serializable(obj) == obj

def test_make_serializable_non_serializable():
    obj = {"a": NonSerializable()}
    expected = {"a": "<NonSerializable>"}
    assert make_serializable(obj) == expected

def test_make_serializable_list_non_serializable():
    obj = [1, NonSerializable()]
    expected = [1, "<NonSerializable>"]
    assert make_serializable(obj) == expected

def test_make_serializable_depth():
    # Create a deep structure
    obj = {"a": {"b": {"c": 1}}}
    # Depth 0: obj
    # Depth 1: a
    # Depth 2: b -> Recurses to c
    # Depth 3: value 1 -> hit max_depth (3 > 2) -> str(1)
    assert make_serializable(obj, max_depth=2) == {'a': {'b': {'c': '1'}}}

def test_make_serializable_cycle():
    a = {}
    b = {"a": a}
    a["b"] = b
    # This should not crash but return string at max depth
    res = make_serializable(a, max_depth=5)
    # Just check it returns a dict and doesn't crash
    assert isinstance(res, dict)

def test_performance_vs_json_dumps():
    # Create a large string (10MB)
    large_string = "a" * 10 * 1024 * 1024
    large_dict = {"data": large_string, "meta": {"id": 123}}

    start = time.time()
    # Run a few times to warmup/average
    for _ in range(5):
        make_serializable(large_dict)
    duration_make = (time.time() - start) / 5

    start = time.time()
    for _ in range(5):
        try:
            json.dumps(large_dict)
        except:
            pass
    duration_json = (time.time() - start) / 5

    print(f"make_serializable: {duration_make:.6f}s")
    print(f"json.dumps: {duration_json:.6f}s")

    # Expect make_serializable to be significantly faster
    # We use a conservative 10x factor for the assertion to be safe in CI environments
    assert duration_make < (duration_json / 10)
