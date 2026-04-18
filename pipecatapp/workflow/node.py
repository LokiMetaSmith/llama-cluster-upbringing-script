from abc import ABC, abstractmethod
from typing import Dict, Any, List, Set, Optional

class Node(ABC):
    """Abstract base class for a node in the workflow graph."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.id = config.get("id")

        # Explicit I/O Typing (Haystack Concept)
        # Nodes should explicitly define what inputs they expect and what outputs they produce.
        # This allows for pre-runtime graph validation.
        self.expected_inputs: Set[str] = set()
        self.expected_outputs: Set[str] = set()

        # Enhanced 3D Spatial Properties
        # These default values ensure backward compatibility with existing workflows
        self.position = config.get("position", {"x": 0.0, "y": 0.0, "z": 0.0})
        self.dimensions = config.get("dimensions", {"width": 100.0, "height": 100.0, "depth": 0.0})
        self.style = config.get("style", {"color": "#cccccc", "shape": "box"})
        self.parent = config.get("parent", None) # For grouping/hierarchy

    @abstractmethod
    async def execute(self, context: 'WorkflowContext') -> None:
        """Execute the node's logic."""
        pass

    def get_input(self, context: 'WorkflowContext', name: str) -> Any:
        """Retrieve an input value from the context."""
        if self.expected_inputs and name not in self.expected_inputs:
            # We don't raise an exception yet to avoid breaking existing nodes that haven't been updated
            print(f"Warning: Node '{self.id}' retrieved undeclared input '{name}'")
        return context.get_input(self.id, name)

    def set_output(self, context: 'WorkflowContext', name: str, value: Any):
        """Set an output value in the context."""
        if self.expected_outputs and name not in self.expected_outputs:
            print(f"Warning: Node '{self.id}' set undeclared output '{name}'")
        context.set_output(self.id, name, value)

    def validate_io(self) -> List[str]:
        """Validates that the node's config satisfies its explicit I/O contracts.
        Returns a list of error messages, or an empty list if valid."""
        errors = []
        if not self.config:
            return errors

        configured_inputs = [inp.get("name") for inp in self.config.get("inputs", []) if isinstance(inp, dict)]
        for expected in self.expected_inputs:
            if expected not in configured_inputs and f"{expected}_from_global" not in self.config:
                 # Check if maybe it's in a config dict directly (legacy)
                 if not self.config.get("config", {}).get(expected):
                     errors.append(f"Node '{self.id}' is missing required input mapping for '{expected}'.")

        return errors

    def get_spatial_data(self) -> Dict[str, Any]:
        """Returns the node's spatial properties for visualization/processing."""
        return {
            "position": self.position,
            "dimensions": self.dimensions,
            "style": self.style,
            "parent": self.parent
        }
