import os
import json
import unittest
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipecatapp.workflow.node import Node
from pipecatapp.workflow.canvas_converter import CanvasConverter

class TestCanvasIntegration(unittest.TestCase):

    def test_node_schema_3d(self):
        """Verify the Node class supports 3D properties."""
        config = {
            "id": "test_node_1",
            "type": "code_runner",
            "position": {"x": 10.0, "y": 20.0, "z": 30.0},
            "dimensions": {"width": 100.0, "height": 200.0, "depth": 5.0}
        }

        # Create a dummy Node subclass since Node is abstract
        class ConcreteNode(Node):
            async def execute(self, context): pass

        node = ConcreteNode(config)

        self.assertEqual(node.position["x"], 10.0)
        self.assertEqual(node.position["y"], 20.0)
        self.assertEqual(node.position["z"], 30.0)
        self.assertEqual(node.dimensions["depth"], 5.0)

    def test_canvas_to_workflow(self):
        """Verify conversion from Canvas JSON to Workflow Schema."""
        canvas_data = {
            "nodes": [
                {
                    "id": "node1",
                    "type": "text",
                    "text": "[TYPE: code_runner]\nprint('Hello')",
                    "x": 100, "y": 100, "width": 400, "height": 200, "color": "#ff0000"
                },
                {
                    "id": "node2",
                    "type": "text",
                    "text": "Output Node",
                    "x": 600, "y": 100
                }
            ],
            "edges": [
                {
                    "id": "edge1",
                    "fromNode": "node1",
                    "fromSide": "right",
                    "toNode": "node2",
                    "toSide": "left"
                }
            ]
        }

        # Write to temp file
        with open("test_canvas.canvas", "w") as f:
            json.dump(canvas_data, f)

        try:
            workflow = CanvasConverter.canvas_to_workflow("test_canvas.canvas")

            # Verify Node Mapping
            self.assertEqual(len(workflow["nodes"]), 2)
            node1 = next(n for n in workflow["nodes"] if n["id"] == "node1")
            self.assertEqual(node1["type"], "code_runner") # Inferred type
            self.assertEqual(node1["position"]["z"], 0.0) # Default Z
            self.assertEqual(node1["style"]["color"], "#ff0000")

            # Verify Connection
            node2 = next(n for n in workflow["nodes"] if n["id"] == "node2")
            self.assertTrue("inputs" in node2)
            conn = node2["inputs"][0]["connection"]
            self.assertEqual(conn["from_node"], "node1")

        finally:
            if os.path.exists("test_canvas.canvas"):
                os.remove("test_canvas.canvas")

if __name__ == '__main__':
    unittest.main()
