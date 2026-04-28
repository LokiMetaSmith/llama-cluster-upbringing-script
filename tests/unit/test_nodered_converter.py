import json
import os
import asyncio
from pipecatapp.workflow.nodered_converter import NodeRedConverter

def test_nodered_conversion():
    sample_nodered = [
      {
        "id": "node_debug",
        "type": "debug",
        "name": "",
        "active": True,
        "complete": False,
        "x": 640,
        "y": 200,
        "wires": []
      },
      {
        "id": "node_inject",
        "type": "inject",
        "name": "",
        "topic": "",
        "payload": "",
        "repeat": "",
        "once": False,
        "x": 240,
        "y": 200,
        "wires": [
          [
            "node_function"
          ]
        ]
      },
      {
        "id": "node_function",
        "type": "function",
        "name": "Format timestamp",
        "func": "return msg;",
        "outputs": 1,
        "x": 440,
        "y": 200,
        "wires": [
          [
            "node_debug"
          ]
        ]
      }
    ]

    workflow = NodeRedConverter.nodered_to_workflow(nodered_data=sample_nodered)

    assert len(workflow["nodes"]) == 3, "Workflow should have 3 nodes"

    debug_node = next(n for n in workflow["nodes"] if n["id"] == "node_debug")
    assert debug_node["type"] == "output", "debug node mapped incorrectly"
    assert debug_node["inputs"][0]["connection"]["from_node"] == "node_function"

    inject_node = next(n for n in workflow["nodes"] if n["id"] == "node_inject")
    assert inject_node["type"] == "input", "inject node mapped incorrectly"

    function_node = next(n for n in workflow["nodes"] if n["id"] == "node_function")
    assert function_node["type"] == "python_code", "function node mapped incorrectly"
    assert function_node["inputs"][0]["connection"]["from_node"] == "node_inject"

    nr_out = NodeRedConverter.workflow_to_nodered(workflow)

    assert len(nr_out) == 3, "Converted back to Node-RED should have 3 nodes"

    nr_inject = next(n for n in nr_out if n["id"] == "node_inject")
    assert nr_inject["wires"][0] == ["node_function"], "Wires array missing or incorrect for inject node"

    nr_function = next(n for n in nr_out if n["id"] == "node_function")
    assert nr_function["wires"][0] == ["node_debug"], "Wires array missing or incorrect for function node"

if __name__ == "__main__":
    test_nodered_conversion()
    print("Node-RED conversion test passed.")
