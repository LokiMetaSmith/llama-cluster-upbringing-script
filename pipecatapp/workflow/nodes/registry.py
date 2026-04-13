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


    def get_all_nodes_metadata(self) -> Dict[str, Any]:
        """Get metadata for all registered nodes."""
        metadata = {}
        for type_name, node_class in self._registry.items():
            # For now just return name and basic empty inputs/outputs,
            # If the node has a get_metadata classmethod, we could use that.
            if hasattr(node_class, 'get_metadata'):
                metadata[type_name] = node_class.get_metadata()
            else:
                metadata[type_name] = {
                    "name": type_name,
                    "description": node_class.__doc__ or f"A {type_name} node."
                }
        return metadata

# Global registry instance

registry = NodeRegistry()
