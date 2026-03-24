import pytest
import json
from pipecatapp.tools.cq_tool import CQ_Tool

def test_cq_query():
    tool = CQ_Tool()
    # Test existing tag
    res = json.loads(tool.cq_query(["api"]))
    assert res["status"] == "success"
    assert len(res["results"]) == 1
    assert res["results"][0]["id"] == "ku_mock_001"

    # Test non-existing tag
    res = json.loads(tool.cq_query(["nonexistent"]))
    assert res["status"] == "success"
    assert len(res["results"]) == 0

def test_cq_propose():
    tool = CQ_Tool()
    res = json.loads(tool.cq_propose(
        domain=["test"],
        summary="A test summary",
        detail="A test detail",
        action="Do a test action"
    ))

    assert res["status"] == "success"
    assert "id" in res

    # Verify it was added
    query_res = json.loads(tool.cq_query(["test"]))
    assert len(query_res["results"]) == 1
    assert query_res["results"][0]["id"] == res["id"]

def test_cq_confirm():
    tool = CQ_Tool()
    res = json.loads(tool.cq_confirm("ku_mock_001"))

    assert res["status"] == "success"
    assert res["total_confirmations"] == 848
    assert res["new_confidence"] == pytest.approx(0.99)

def test_cq_flag():
    tool = CQ_Tool()
    res = json.loads(tool.cq_flag("ku_mock_001", "stale", "It is old"))

    assert res["status"] == "success"

def test_cq_reflect():
    tool = CQ_Tool()
    res = json.loads(tool.cq_reflect("Some session context here"))

    assert res["status"] == "success"
    assert res["candidates_found"] == 1
