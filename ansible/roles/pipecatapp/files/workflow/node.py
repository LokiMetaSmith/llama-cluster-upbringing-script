from abc import ABC, abstractmethod
from typing import Dict, Any, List

class Node(ABC):
    """Abstract base class for a node in the workflow graph."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.id = config.get("id")

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
