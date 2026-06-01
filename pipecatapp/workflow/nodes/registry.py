from typing import Dict, Type, Any
from ..node import Node

class NodeRegistry:
    """A registry for mapping node type names to node classes."""

    def __init__(self):
        self._registry: Dict[str, Type[Node]] = {}

    def register(self, node_class: Type[Node]):
        """Register a node class."""
        type_name = node_class.__name__
        if type_name in self._registry:
            raise ValueError(f"Node type '{type_name}' is already registered.")
        self._registry[type_name] = node_class
        return node_class

    def get_node_class(self, type_name: str) -> Type[Node]:
        """Get a node class by its type name."""
        return self._registry.get(type_name)

    def get_all_nodes_metadata(self) -> list:
        """Returns metadata for all registered nodes for UI generation."""
        metadata = []
        for name, cls in self._registry.items():
            doc = cls.__doc__ or ""

            # Extract inputs/outputs if defined on the class or via generic config
            # (Fallback to empty arrays if not defined to prevent UI crashes)
            inputs = []
            outputs = []

            # Temporary hack: Instantiate a dummy node to inspect its expected inputs/outputs.
            # In a real system, these should be static class attributes or Pydantic models.
            try:
                dummy_instance = cls({"id": "dummy"})
                if hasattr(dummy_instance, "expected_inputs"):
                    inputs = [{"name": i, "type": "any"} for i in dummy_instance.expected_inputs]
                if hasattr(dummy_instance, "expected_outputs"):
                    outputs = [{"name": o, "type": "any"} for o in dummy_instance.expected_outputs]
            except Exception:
                pass # Ignore if dummy instantiation fails

            node_info = {
                "name": name,
                "description": doc.strip().split("\n")[0] if doc else "No description available.",
                "category": getattr(cls, "category", "General"),
                "icon": getattr(cls, "icon", "node.svg"),
                "inputs": inputs,
                "outputs": outputs,
                "properties": {} # Placeholder for future dynamic properties schema
            }
            metadata.append(node_info)
        return metadata
        return metadata

# Global registry instance

registry = NodeRegistry()
