import yaml
import asyncio
from typing import Dict, Any, List
from .context import WorkflowContext
from .nodes import registry  # We will create this registry next

class WorkflowRunner:
    """Loads and executes a workflow defined in a YAML file."""

    def __init__(self, workflow_path: str):
        with open(workflow_path, 'r') as f:
            self.workflow_definition = yaml.safe_load(f)
        self.nodes = {}

    def _instantiate_nodes(self):
        """Instantiate all nodes defined in the workflow."""
        for node_config in self.workflow_definition["nodes"]:
            node_class = registry.get_node_class(node_config["type"])
            if not node_class:
                raise ValueError(f"Unknown node type: {node_config['type']}")
            self.nodes[node_config["id"]] = node_class(node_config)

    def _get_execution_order(self) -> List[str]:
        """Determine the execution order of nodes using Kahn's algorithm for topological sorting."""

        # 1. Initialize graph and in-degrees
        graph: Dict[str, List[str]] = {node["id"]: [] for node in self.workflow_definition["nodes"]}
        in_degree: Dict[str, int] = {node["id"]: 0 for node in self.workflow_definition["nodes"]}

        # 2. Build graph and in-degrees from connections
        for node in self.workflow_definition["nodes"]:
            node_id = node["id"]
            for input_config in node.get("inputs", []):
                if "connection" in input_config:
                    from_node_id = input_config["connection"]["from_node"]
                    # Add edge from the dependency to the current node
                    if from_node_id in graph:
                        graph[from_node_id].append(node_id)
                    # Increment in-degree of the current node
                    if node_id in in_degree:
                        in_degree[node_id] += 1

        # 3. Initialize the queue with all nodes having an in-degree of 0
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]

        # 4. Process the queue
        sorted_order = []
        while queue:
            current_node_id = queue.pop(0)
            sorted_order.append(current_node_id)

            # Decrement the in-degree of each neighbor
            if current_node_id in graph:
                for neighbor_id in graph[current_node_id]:
                    if neighbor_id in in_degree:
                        in_degree[neighbor_id] -= 1
                        # If in-degree becomes 0, add it to the queue
                        if in_degree[neighbor_id] == 0:
                            queue.append(neighbor_id)

        # 5. Check for cycles
        if len(sorted_order) != len(self.workflow_definition["nodes"]):
            raise ValueError("Workflow contains a cycle and cannot be executed.")

        return sorted_order

    async def run(self, global_inputs: Dict[str, Any]) -> Any:
        """Execute the workflow.

        Args:
            global_inputs (Dict[str, Any]): A dictionary of global inputs to the workflow.

        Returns:
            The final output of the workflow, from a designated "OutputNode".
        """
        self._instantiate_nodes()
        context = WorkflowContext(self.workflow_definition)
        for name, value in global_inputs.items():
            context.set_global_input(name, value)

        execution_order = self._get_execution_order()

        for node_id in execution_order:
            node = self.nodes[node_id]
            await node.execute(context)

        return context.final_output
