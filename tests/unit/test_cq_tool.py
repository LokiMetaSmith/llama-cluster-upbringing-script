import pytest
import json
from pipecatapp.tools.cq_tool import CQ_Tool

def test_cq_tool_initialization():
    tool = CQ_Tool()
    assert tool.name == "cq"

def test_cq_query():
    tool = CQ_Tool()
    # match on domain
    res_json = tool.cq_query(["payments"])
    res = json.loads(res_json)
    assert res["status"] == "success"
    assert len(res["results"]) == 1

def test_cq_propose():
    tool = CQ_Tool()
    res_json = tool.cq_propose(["test"], "sum", "det", "act")
    res = json.loads(res_json)
    assert res["status"] == "success"
    assert "id" in res

def test_cq_confirm():
    tool = CQ_Tool()
    res_json = tool.cq_confirm("ku_mock_001")
    res = json.loads(res_json)
    assert res["status"] == "success"
    assert "new_confidence" in res

def test_cq_flag():
    tool = CQ_Tool()
    res_json = tool.cq_flag("ku_mock_001", "stale")
    res = json.loads(res_json)
    assert res["status"] == "success"

def test_cq_reflect():
    tool = CQ_Tool()
    res_json = tool.cq_reflect("test context")
    res = json.loads(res_json)
    assert res["status"] == "success"
