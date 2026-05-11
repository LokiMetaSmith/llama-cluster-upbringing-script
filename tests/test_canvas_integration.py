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
                },
                {
                    "id": "node3",
                    "type": "file",
                    "file": "image.png",
                    "x": 100, "y": 300
                },
                {
                    "id": "node4",
                    "type": "file",
                    "file": "document.pdf",
                    "x": 100, "y": 400
                },
                {
                    "id": "node5",
                    "type": "file",
                    "file": "notes.md",
                    "x": 100, "y": 500
                },
                {
                    "id": "node6",
                    "type": "file",
                    "file": "video.mp4",
                    "x": 100, "y": 600
                },
                {
                    "id": "node7",
                    "type": "file",
                    "file": "unknown.xyz",
                    "x": 100, "y": 700
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
            self.assertEqual(len(workflow["nodes"]), 7)
            node1 = next(n for n in workflow["nodes"] if n["id"] == "node1")
            self.assertEqual(node1["type"], "code_runner") # Inferred type
            self.assertEqual(node1["position"]["z"], 0.0) # Default Z
            self.assertEqual(node1["style"]["color"], "#ff0000")

            # Verify inferred file node types
            node3 = next(n for n in workflow["nodes"] if n["id"] == "node3")
            self.assertEqual(node3["type"], "image_reader")
            self.assertEqual(node3["config"]["filepath"], "image.png")

            node4 = next(n for n in workflow["nodes"] if n["id"] == "node4")
            self.assertEqual(node4["type"], "pdf_reader")

            node5 = next(n for n in workflow["nodes"] if n["id"] == "node5")
            self.assertEqual(node5["type"], "markdown_reader")

            node6 = next(n for n in workflow["nodes"] if n["id"] == "node6")
            self.assertEqual(node6["type"], "media_reader")

            node7 = next(n for n in workflow["nodes"] if n["id"] == "node7")
            self.assertEqual(node7["type"], "file_reader")

            # Verify Connection
            node2 = next(n for n in workflow["nodes"] if n["id"] == "node2")
            self.assertTrue("inputs" in node2)
            conn = node2["inputs"][0]["connection"]
            self.assertEqual(conn["from_node"], "node1")

        finally:
            if os.path.exists("test_canvas.canvas"):
                os.remove("test_canvas.canvas")

    def test_workflow_to_canvas(self):
        """Verify conversion from Workflow Schema to Canvas JSON."""
        workflow = {
            "name": "Generated from Canvas",
            "nodes": [
                {
                    "id": "node1",
                    "type": "code_runner",
                    "config": {
                        "content": "print('Hello')",
                        "raw_text": "[TYPE: code_runner]\nprint('Hello')"
                    },
                    "position": {"x": 100.0, "y": 100.0, "z": 0.0},
                    "dimensions": {"width": 400.0, "height": 200.0, "depth": 0.0},
                    "style": {"color": "#ff0000", "shape": "box"}
                },
                {
                    "id": "node2",
                    "type": "note",
                    "config": {
                        "content": "Output Node",
                        "raw_text": "Output Node"
                    },
                    "position": {"x": 600.0, "y": 100.0, "z": 0.0},
                    "dimensions": {"width": 400.0, "height": 200.0, "depth": 0.0},
                    "style": {"color": "#cccccc", "shape": "box"},
                    "inputs": [
                        {
                            "name": "input_from_node1",
                            "connection": {
                                "from_node": "node1",
                                "output_name": "output"
                            }
                        }
                    ]
                }
            ]
        }

        output_path = "test_output.canvas"
        try:
            CanvasConverter.workflow_to_canvas(workflow, output_path)

            self.assertTrue(os.path.exists(output_path))
            with open(output_path, "r") as f:
                canvas_data = json.load(f)

            self.assertEqual(len(canvas_data["nodes"]), 2)
            self.assertEqual(len(canvas_data["edges"]), 1)

            node1 = next(n for n in canvas_data["nodes"] if n["id"] == "node1")
            self.assertEqual(node1["x"], 100.0)
            self.assertEqual(node1["color"], "#ff0000")

            edge = canvas_data["edges"][0]
            self.assertEqual(edge["fromNode"], "node1")
            self.assertEqual(edge["toNode"], "node2")

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)



    def test_canvas_to_workflow_with_groups(self):
        """Verify that Canvas groups map to Workflow scopes and infer parent-child relationships."""
        canvas_data = {
            "nodes": [
                {
                    "id": "group1",
                    "type": "group",
                    "x": 0, "y": 0, "width": 500, "height": 500
                },
                {
                    "id": "node1",
                    "type": "text",
                    "text": "Inside Group",
                    "x": 100, "y": 100, "width": 100, "height": 100
                },
                {
                    "id": "node2",
                    "type": "text",
                    "text": "Outside Group",
                    "x": 600, "y": 600, "width": 100, "height": 100
                }
            ],
            "edges": []
        }

        with open("test_canvas_groups.canvas", "w") as f:
            json.dump(canvas_data, f)

        try:
            workflow = CanvasConverter.canvas_to_workflow("test_canvas_groups.canvas")
            self.assertEqual(len(workflow["nodes"]), 3)

            group_node = next(n for n in workflow["nodes"] if n["id"] == "group1")
            self.assertEqual(group_node["type"], "scope")

            node1 = next(n for n in workflow["nodes"] if n["id"] == "node1")
            self.assertEqual(node1.get("parent"), "group1")

            node2 = next(n for n in workflow["nodes"] if n["id"] == "node2")
            self.assertIsNone(node2.get("parent"))
        finally:
            if os.path.exists("test_canvas_groups.canvas"):
                os.remove("test_canvas_groups.canvas")

    def test_workflow_to_canvas_with_scopes(self):
        """Verify that Workflow scopes map to Canvas groups."""
        workflow = {
            "name": "Generated from Canvas",
            "nodes": [
                {
                    "id": "scope1",
                    "type": "scope",
                    "position": {"x": 0, "y": 0},
                    "dimensions": {"width": 800, "height": 600}
                },
                {
                    "id": "node1",
                    "type": "note",
                    "parent": "scope1",
                    "position": {"x": 100, "y": 100},
                    "dimensions": {"width": 100, "height": 100}
                }
            ]
        }

        output_path = "test_output_scopes.canvas"
        try:
            CanvasConverter.workflow_to_canvas(workflow, output_path)

            with open(output_path, "r") as f:
                canvas_data = json.load(f)

            self.assertEqual(len(canvas_data["nodes"]), 2)
            group_node = next(n for n in canvas_data["nodes"] if n["id"] == "scope1")
            self.assertEqual(group_node["type"], "group")
            self.assertEqual(group_node["label"], "scope1")

            node_node = next(n for n in canvas_data["nodes"] if n["id"] == "node1")
            self.assertEqual(node_node["type"], "text")

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

if __name__ == '__main__':
    unittest.main()
