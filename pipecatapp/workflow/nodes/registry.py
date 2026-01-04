from typing import Dict, Type
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

# Global registry instance
registry = NodeRegistry()
