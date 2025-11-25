from .registry import registry
from ..node import Node
from ..context import WorkflowContext

@registry.register
class InputNode(Node):
    """A node that introduces global inputs into the workflow."""
    async def execute(self, context: WorkflowContext):
        # This node doesn't need to do anything, its purpose is to be a starting point.
        # Outputs are implicitly handled by connections from it.
        # We can pass through the global inputs as its outputs.
        for output_config in self.config.get("outputs", []):
            output_name = output_config["name"]
            global_input_name = self.config.get("global_input_map", {}).get(output_name, output_name)
            value = context.global_inputs.get(global_input_name)
            self.set_output(context, output_name, value)


@registry.register
class OutputNode(Node):
    """A node that marks the final output of the workflow."""
    async def execute(self, context: WorkflowContext):
        final_output = self.get_input(context, "final_output")
        context.final_output = final_output
