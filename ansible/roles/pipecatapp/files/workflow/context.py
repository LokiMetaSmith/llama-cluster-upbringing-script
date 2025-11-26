import logging
from typing import Dict, Any, List

class WorkflowContext:
    """Manages the state and data flow within a workflow execution."""

    def __init__(self, workflow_definition: Dict[str, Any]):
        self.workflow_definition = workflow_definition
        self.node_outputs: Dict[str, Dict[str, Any]] = {}
        self.global_inputs: Dict[str, Any] = {}
        self.final_output: Any = None

    def set_global_input(self, name: str, value: Any):
        """Set a global input value available to all nodes."""
        self.global_inputs[name] = value

    def get_input(self, node_id: str, input_name: str) -> Any:
        """Get the value for a specific input of a node.

        This method resolves the input by checking connections to other nodes'
        outputs. If not connected, it looks for a literal value in the node's
        configuration.
        """
        node_config = next((n for n in self.workflow_definition["nodes"] if n["id"] == node_id), None)
        if not node_config:
            raise ValueError(f"Node with id {node_id} not found in workflow definition.")

        input_config = next((i for i in node_config.get("inputs", []) if i["name"] == input_name), None)
        if not input_config:
            raise ValueError(f"Input '{input_name}' not found for node '{node_id}'.")

        # Check for a connection
        if "connection" in input_config:
            from_node_id = input_config["connection"]["from_node"]
            from_output_name = input_config["connection"]["from_output"]
            if from_node_id in self.node_outputs and from_output_name in self.node_outputs[from_node_id]:
                return self.node_outputs[from_node_id][from_output_name]
            else:
                # This can happen if the graph is not executed in topological order,
                # or if an expected output was not set.
                raise ValueError(f"Output '{from_output_name}' from node '{from_node_id}' not available for node '{node_id}'.")
        # Check for a literal value
        elif "value" in input_config:
            value = self._resolve_value(input_config["value"])
            # Check for a transform
            if "transform" in input_config:
                value = self._apply_transform(value, input_config["transform"])
            return value
        # Check for a global input
        elif "global_input" in input_config:
            global_input_name = input_config["global_input"]
            if global_input_name in self.global_inputs:
                return self.global_inputs[global_input_name]
            else:
                raise ValueError(f"Global input '{global_input_name}' not found.")

        return None

    def set_output(self, node_id: str, output_name: str, value: Any):
        """Set an output value for a specific node."""
        if node_id not in self.node_outputs:
            self.node_outputs[node_id] = {}
        self.node_outputs[node_id][output_name] = value
        logging.debug(f"Node '{node_id}' set output '{output_name}' to: {value}")

    def _resolve_value(self, value: Any) -> Any:
        """Recursively resolve a value, processing nested connections."""
        if isinstance(value, dict):
            if "connection" in value:
                from_node_id = value["connection"]["from_node"]
                from_output_name = value["connection"]["from_output"]
                if from_node_id in self.node_outputs and from_output_name in self.node_outputs[from_node_id]:
                    return self.node_outputs[from_node_id][from_output_name]
                else:
                    return None # Connection not yet available, return None
            else:
                # Recurse into dictionary values
                return {k: self._resolve_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            # Recurse into list items
            return [self._resolve_value(item) for item in value]
        else:
            # It's a literal value, return as is
            return value

    def _apply_transform(self, value: Any, transform: str) -> Any:
        """Applies a simple transformation to a value."""
        if transform == "extract_expert":
            return value.get("args", {}).get("expert")
        if transform == "extract_query":
            return value.get("args", {}).get("query")
        # Add more transforms here as needed
        raise ValueError(f"Unknown transform: {transform}")
