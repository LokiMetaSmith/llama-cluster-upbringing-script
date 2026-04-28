import json
import logging
from typing import Dict, Any, List

class NodeRedConverter:
    """
    Converts between Node-RED Flow format (.json) and Pipecat Workflow format (.yaml).
    """

    @staticmethod
    def nodered_to_workflow(nodered_path: str = None, nodered_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Parses a Node-RED flow and converts it into a Pipecat Workflow definition.
        Accepts either a file path or direct JSON data.
        """
        if nodered_data is None:
            if nodered_path is None:
                logging.error("Either nodered_path or nodered_data must be provided.")
                return {}
            try:
                with open(nodered_path, 'r', encoding='utf-8') as f:
                    nodered_data = json.load(f)
            except Exception as e:
                logging.error(f"Failed to read Node-RED file {nodered_path}: {e}")
                return {}

        workflow = {
            "name": "Generated from Node-RED",
            "nodes": []
        }

        # 1. Map Nodes
        for nr_node in nodered_data:
            # Skip special global config nodes or flows if any (usually don't have x, y)
            if "x" not in nr_node and "y" not in nr_node:
                # Sometimes subflows or configs. We can skip or keep them depending on needs.
                if nr_node.get("type") == "tab":
                     continue # Skip flow tabs

            workflow_node = {
                "id": nr_node.get("id"),
                "type": NodeRedConverter._infer_node_type(nr_node),
                "config": NodeRedConverter._extract_config(nr_node),
                "position": {
                    "x": nr_node.get("x", 0.0),
                    "y": nr_node.get("y", 0.0),
                    "z": nr_node.get("z", 0.0) # Flow/tab ID usually
                },
                "dimensions": {
                    "width": 200.0, # Default width
                    "height": 50.0, # Default height
                    "depth": 0.0
                },
                "style": {
                    "color": "#cccccc",
                    "shape": "box"
                }
            }
            workflow["nodes"].append(workflow_node)

        # 2. Map Edges (Connections)
        # Node-RED format: "wires": [ ["target1", "target2"], ["target3"] ]
        # outer index is the output port. inner elements are target node IDs.
        for nr_node in nodered_data:
            source_id = nr_node.get("id")
            wires = nr_node.get("wires", [])

            for port_idx, targets in enumerate(wires):
                for target_id in targets:
                    target_node = next((n for n in workflow["nodes"] if n["id"] == target_id), None)
                    if target_node:
                        if "inputs" not in target_node:
                            target_node["inputs"] = []

                        target_node["inputs"].append({
                            "name": f"input_from_{source_id}_{port_idx}",
                            "connection": {
                                "from_node": source_id,
                                "output_name": f"output_{port_idx}"
                            }
                        })

        return workflow

    @staticmethod
    def _infer_node_type(node: Dict[str, Any]) -> str:
        """
        Infers the Pipecat node type based on Node-RED node type.
        """
        nr_type = node.get("type", "")
        if nr_type == "inject":
            return "input"
        elif nr_type == "debug":
            return "output"
        elif nr_type == "function":
            return "python_code"
        elif nr_type == "http in":
            return "http_server"
        elif nr_type == "http request":
            return "http_client"
        return nr_type # Default to the Node-RED type as fallback

    @staticmethod
    def _extract_config(node: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts configuration from the Node-RED node content.
        """
        config = {}
        for key, value in node.items():
            if key not in ["id", "type", "x", "y", "z", "wires"]:
                config[key] = value
        return config

    @staticmethod
    def workflow_to_nodered(workflow: Dict[str, Any], output_path: str = None) -> List[Dict[str, Any]]:
        """
        Converts a Pipecat Workflow back into a Node-RED Flow format.
        """
        nodered_nodes = []

        # 1. Map Nodes
        for wf_node in workflow.get("nodes", []):
            nr_node = {
                "id": wf_node.get("id"),
                "type": wf_node.get("type", "unknown"),
                "x": wf_node.get("position", {}).get("x", 0.0),
                "y": wf_node.get("position", {}).get("y", 0.0),
                "wires": []
            }

            # Map config back (flatten it)
            for k, v in wf_node.get("config", {}).items():
                nr_node[k] = v

            # Add z (tab ID) if present
            z_pos = wf_node.get("position", {}).get("z")
            if z_pos:
                 nr_node["z"] = z_pos

            nodered_nodes.append(nr_node)

        # 2. Map Edges (Connections)
        # We need to look at each target node's inputs and map it back to the source node's `wires` array.
        for wf_node in workflow.get("nodes", []):
            target_id = wf_node.get("id")
            for inp in wf_node.get("inputs", []):
                if "connection" in inp:
                    source_id = inp["connection"]["from_node"]
                    # Usually "output_name" looks like "output_0" or "output". Try to infer index.
                    output_name = inp["connection"].get("output_name", "output_0")
                    port_idx = 0
                    if output_name.startswith("output_"):
                         try:
                             port_idx = int(output_name.split("_")[1])
                         except ValueError:
                             pass

                    # Find the source node in our Node-RED nodes list
                    nr_source_node = next((n for n in nodered_nodes if n["id"] == source_id), None)
                    if nr_source_node:
                        # Ensure the `wires` array has enough sub-arrays to reach `port_idx`
                        while len(nr_source_node["wires"]) <= port_idx:
                            nr_source_node["wires"].append([])

                        nr_source_node["wires"][port_idx].append(target_id)

        if output_path:
             try:
                 with open(output_path, 'w', encoding='utf-8') as f:
                     json.dump(nodered_nodes, f, indent=2)
             except Exception as e:
                 logging.error(f"Failed to write Node-RED file {output_path}: {e}")

        return nodered_nodes
