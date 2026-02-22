import json
import uuid
import logging
from typing import Dict, Any, List

class CanvasConverter:
    """
    Converts between Obsidian Canvas format (.canvas) and Pipecat Workflow format (.yaml).
    Handles the mapping of 2D Canvas nodes to 3D Workflow nodes (with default Z=0).
    """

    @staticmethod
    def canvas_to_workflow(canvas_path: str) -> Dict[str, Any]:
        """
        Parses an Obsidian Canvas file and converts it into a Pipecat Workflow definition.
        """
        try:
            with open(canvas_path, 'r', encoding='utf-8') as f:
                canvas_data = json.load(f)
        except Exception as e:
            logging.error(f"Failed to read canvas file {canvas_path}: {e}")
            return {}

        workflow = {
            "name": "Generated from Canvas", # Ideally filename
            "nodes": []
        }

        # 1. Map Nodes
        # Canvas Nodes: { "id": "...", "type": "text/file/group", "text": "...", "x": 0, "y": 0, "width": 0, "height": 0, "color": "..." }
        for canvas_node in canvas_data.get("nodes", []):
            workflow_node = {
                "id": canvas_node["id"],
                "type": CanvasConverter._infer_node_type(canvas_node),
                "config": CanvasConverter._extract_config(canvas_node),
                "position": {
                    "x": canvas_node.get("x", 0.0),
                    "y": canvas_node.get("y", 0.0),
                    "z": 0.0 # Default depth
                },
                "dimensions": {
                    "width": canvas_node.get("width", 400.0),
                    "height": canvas_node.get("height", 200.0),
                    "depth": 0.0 # Default visual depth
                },
                "style": {
                    "color": canvas_node.get("color", "#cccccc"),
                    "shape": "box"
                }
            }

            # Handle Grouping (Parent)
            # Obsidian Canvas uses implicit spatial containment for groups, or explicit "parent" if grouped.
            # We'll use the "group" type node as a parent container.
            if canvas_node["type"] == "group":
                # Groups are nodes too, but maybe with special type
                workflow_node["type"] = "scope" # Assuming a 'scope' node type exists or will exist

            workflow["nodes"].append(workflow_node)

        # 2. Map Edges (Connections)
        # Canvas Edges: { "id": "...", "fromNode": "...", "fromSide": "...", "toNode": "...", "toSide": "..." }
        # We need to add "inputs" to the target nodes based on these edges.
        # This is tricky because Canvas edges are just lines; Workflow inputs are named ports.
        # Convention: We'll use the 'fromNode' ID as the input name for now, or a generic 'input'.

        edges = canvas_data.get("edges", [])
        for edge in edges:
            source_id = edge["fromNode"]
            target_id = edge["toNode"]

            # Find the target node in our workflow list
            target_node = next((n for n in workflow["nodes"] if n["id"] == target_id), None)
            if target_node:
                if "inputs" not in target_node:
                    target_node["inputs"] = []

                # Append connection info
                # In Pipecat, inputs are usually dicts: { "name": "...", "value": "..." } or similar
                # For connections, it might be: { "name": "...", "connection": { "from_node": "..." } }
                target_node["inputs"].append({
                    "name": f"input_from_{source_id}", # Auto-generated name
                    "connection": {
                        "from_node": source_id,
                        "output_name": "output" # Default output port
                    }
                })

        return workflow

    @staticmethod
    def _infer_node_type(node: Dict[str, Any]) -> str:
        """
        Infers the Pipecat node type based on Canvas node content.

        Rules:
        - If text starts with '[TYPE: <type>]', use that.
        - If type is 'file', map to 'file_reader' (or 'rag' if strict).
        - If type is 'text', default to 'prompt' or 'note'.
        - If type is 'group', map to 'scope'.
        """
        if node["type"] == "text":
            text = node.get("text", "")
            # Check for explicit type hint
            if text.strip().startswith("[TYPE:"):
                # Extract type: [TYPE: python_code] -> python_code
                try:
                    type_hint = text.split("]")[0].split(":")[1].strip()
                    return type_hint
                except IndexError:
                    pass
            return "note" # Default for plain text

        if node["type"] == "file":
            return "file_reader"

        if node["type"] == "group":
            return "scope"

        return "unknown"

    @staticmethod
    def _extract_config(node: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts configuration from the node content.
        For text nodes, the text IS the content/config.
        """
        config = {}
        if node["type"] == "text":
            text = node.get("text", "")
            # Remove type hint if present
            if text.strip().startswith("[TYPE:"):
                 parts = text.split("]", 1)
                 if len(parts) > 1:
                     text = parts[1].strip()

            config["content"] = text
            config["raw_text"] = node.get("text", "")

        elif node["type"] == "file":
             config["filepath"] = node.get("file", "")

        return config

    @staticmethod
    def workflow_to_canvas(workflow: Dict[str, Any], output_path: str) -> None:
        """
        Converts a Pipecat Workflow back into an Obsidian Canvas file.
        Useful for visualizing the state or structure.
        """
        canvas = {
            "nodes": [],
            "edges": []
        }

        for node in workflow.get("nodes", []):
            # 1. Create Canvas Node
            canvas_node = {
                "id": node["id"],
                "x": node.get("position", {}).get("x", 0),
                "y": node.get("position", {}).get("y", 0),
                "width": node.get("dimensions", {}).get("width", 400),
                "height": node.get("dimensions", {}).get("height", 200),
                "color": node.get("style", {}).get("color", "#cccccc"),
                "type": "text" # Default to text for visualization
            }

            # Set content based on node type
            # We'll put the config in the text for now
            node_type = node.get("type", "unknown")
            config_str = json.dumps(node.get("config", {}), indent=2)
            canvas_node["text"] = f"**{node_type.upper()}**\n\n```json\n{config_str}\n```"

            # Map specific types if needed (e.g., file -> file node)
            # if node_type == "file_reader": ...

            canvas["nodes"].append(canvas_node)

            # 2. Create Edges from Inputs
            # In workflow: inputs -> connection -> from_node
            inputs = node.get("inputs", [])
            for inp in inputs:
                if "connection" in inp:
                    from_node = inp["connection"]["from_node"]
                    edge_id = str(uuid.uuid4())
                    canvas["edges"].append({
                        "id": edge_id,
                        "fromNode": from_node,
                        "fromSide": "right",
                        "toNode": node["id"],
                        "toSide": "left"
                    })

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(canvas, f, indent=2)
        except Exception as e:
             logging.error(f"Failed to write canvas file {output_path}: {e}")
