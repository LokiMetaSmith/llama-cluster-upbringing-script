from .registry import registry
from ..node import Node
from ..context import WorkflowContext

@registry.register
class InputNode(Node):
    """A node that introduces global inputs into the workflow."""
    async def execute(self, context: WorkflowContext):
        for output_config in self.config.get("outputs", []):
            output_name = output_config["name"]
            value = context.global_inputs.get(output_name)
            self.set_output(context, output_name, value)

@registry.register
class OutputNode(Node):
    """A node that marks the final output of the workflow."""
    async def execute(self, context: WorkflowContext):
        final_output = self.get_input(context, "final_output")
        context.final_output = final_output

@registry.register
class MergeNode(Node):
    """A node that merges multiple inputs into a single output.
    It prioritizes the first non-None input."""
    async def execute(self, context: WorkflowContext):
        for i in range(1, 10): # Check for up to 9 inputs
            input_name = f"in{i}"
            try:
                value = self.get_input(context, input_name)
                if value is not None:
                    self.set_output(context, "merged_output", value)
                    return
            except ValueError:
                # This input is not configured, which is fine
                pass
        self.set_output(context, "merged_output", None)

@registry.register
class ConditionalBranchNode(Node):
    """A node that routes execution based on a condition."""
    async def execute(self, context: WorkflowContext):
        input_value = self.get_input(context, "input_value")

        condition_met = False
        if "check_if_tool_is" in self.config:
            tool_name_to_check = self.config["check_if_tool_is"]
            actual_tool_name = (input_value or {}).get("tool", "")
            condition_met = (actual_tool_name == tool_name_to_check)
        else:
            # Default to a simple truthiness check if no specific check is configured
            condition_met = bool(input_value)

        if condition_met:
            self.set_output(context, "output_true", input_value)
            self.set_output(context, "output_false", None)
        else:
            self.set_output(context, "output_true", None)
            self.set_output(context, "output_false", input_value)
