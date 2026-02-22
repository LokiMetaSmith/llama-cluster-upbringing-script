from abc import ABC, abstractmethod
from typing import Dict, Any, List

class Node(ABC):
    """Abstract base class for a node in the workflow graph."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.id = config.get("id")

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
        return context.get_input(self.id, name)

    def set_output(self, context: 'WorkflowContext', name: str, value: Any):
        """Set an output value in the context."""
        context.set_output(self.id, name, value)

    def get_spatial_data(self) -> Dict[str, Any]:
        """Returns the node's spatial properties for visualization/processing."""
        return {
            "position": self.position,
            "dimensions": self.dimensions,
            "style": self.style,
            "parent": self.parent
        }
