import pytest
import os
import tempfile
from pipecatapp.datalog_memory import DatalogMemory
from pipecatapp.tools.datalog_extraction_tool import DatalogExtractionTool
from pipecatapp.workflow.nodes.datalog_nodes import DatalogStateNode
from pipecatapp.pmm_memory import PMMMemory

def test_datalog_extraction_tool():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_extract.db")
        pmm = PMMMemory(db_path=db_path)
        mem = DatalogMemory(pmm=pmm)
        tool = DatalogExtractionTool(datalog_memory=mem)

        payload = {
            "rules": [
                {
                    "head_predicate": "controls_kernel_obj",
                    "head_args": ["Attacker"],
                    "body": [
                        {"predicate": "controls", "args": ["Attacker", "ObjA"]},
                        {"predicate": "points_to", "args": ["ObjA", "ObjB"]}
                    ]
                }
            ],
            "assert_facts": [
                {"predicate": "controls", "args": ["attacker", "obj1"]},
                {"predicate": "points_to", "args": ["obj1", "obj2"]}
            ]
        }

        res = tool.execute({"action": "extract_and_apply", "extraction": payload})
        assert res["status"] == "success"
        assert len(res["asserted"]) == 2

        # Check rule derivation
        derived = mem.query_state("controls_kernel_obj")
        assert len(derived) == 1
        assert derived[0]["args"] == ["attacker"]


def test_datalog_memory_hybrid_query():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_hybrid.db")
        pmm = PMMMemory(db_path=db_path)
        mem = DatalogMemory(pmm=pmm)

        mem.assert_fact("vulnerable_service", "apache", "httpd")
        pmm.add_event_sync("user_log", "Exploit attempt against apache server")

        hybrid_res = mem.query_hybrid("apache")
        assert len(hybrid_res["matching_datalog_facts"]) >= 1
        assert len(hybrid_res["matching_events"]) >= 1


def test_datalog_workflow_node():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_node.db")
        pmm = PMMMemory(db_path=db_path)
        mem = DatalogMemory(pmm=pmm)

        node = DatalogStateNode(
            config={
                "id": "test_node_1",
                "action": "assert",
                "predicate": "active_target",
                "args": ["host_10_0_0_1"],
                "datalog_memory": mem
            }
        )

        res = node.execute(context=None)
        assert res["status"] == "success"
        assert "active_target('host_10_0_0_1')" in res["fact"]
