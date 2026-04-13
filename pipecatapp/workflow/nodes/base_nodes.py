from .registry import registry
from ..node import Node
from ..context import WorkflowContext

@registry.register
class InputNode(Node):
    """A node that introduces global inputs into the workflow."""
    async def execute(self, context: WorkflowContext):
        outputs = self.config.get("config", {}).get("outputs", [])
        for output_config in outputs:
            if isinstance(output_config, str):
                output_name = output_config
            else:
                output_name = output_config["name"]
            value = context.global_inputs.get(output_name)
            self.set_output(context, output_name, value)

@registry.register
class OutputNode(Node):
    """A node that marks the final output of the workflow.
    It collects all connected inputs into a dictionary.
    """
    async def execute(self, context: WorkflowContext):
        result = {}
        # Iterate over configured inputs and collect their values
        if "inputs" in self.config:
            for input_config in self.config["inputs"]:
                name = input_config["name"]
                try:
                    val = self.get_input(context, name)
                    if val is not None:
                        result[name] = val
                except ValueError:
                    pass

        # If "final_output" is present in result, and it's the only one,
        # we might want to preserve legacy behavior?
        # But TwinService expects a dict with specific keys.
        # So we just return the result dict.

        # Fallback for workflows that might not have defined inputs correctly
        # or rely on the old behavior where only one input was allowed.
        if not result:
             try:
                 val = self.get_input(context, "final_output")
                 result = val # Legacy behavior: return value directly
             except ValueError:
                 pass

        context.final_output = result

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

@registry.register
class GateNode(Node):
    """A node that can pause the workflow to wait for external approval."""
    async def execute(self, context: WorkflowContext):
        import asyncio
        from ..workflow.runner import OpenGates

        input_value = self.get_input(context, "input_value")
        twin_service = context.global_inputs.get("twin_service")

        # Only gate if there is a tool call to approve and we are in approval mode
        if input_value and twin_service and twin_service.approval_mode:
            request_id = twin_service.current_request_meta.get("request_id")
            if request_id:
                open_gates = OpenGates()
                approval_event = asyncio.Event()
                open_gates.register_gate(request_id, approval_event)

                print(f"DEBUG: Workflow paused. Waiting for approval on request_id: {request_id}")
                await approval_event.wait()
                print(f"DEBUG: Workflow resumed for request_id: {request_id}")

        # Passthrough the input value
        self.set_output(context, "output", input_value)

@registry.register
class PostProcessorNode(Node):
    """A node that evaluates a Python expression on its input data securely.
    Input: 'data' (the data to process), 'expression' (a Python expression string, where 'data' is the input variable)
    Output: 'processed_data'
    """
    async def execute(self, context: WorkflowContext):
        data = self.get_input(context, "data")
        try:
            expression = self.get_input(context, "expression")
        except ValueError:
            expression = self.config.get("config", {}).get("expression", "data")

        if not expression or expression.strip() == "data":
            self.set_output(context, "processed_data", data)
            return

        try:
            import ast

            def evaluate_ast(node, local_vars):
                """A strict, recursive AST evaluator for simple data transformations."""
                if isinstance(node, ast.Expression):
                    return evaluate_ast(node.body, local_vars)
                elif isinstance(node, ast.Constant):
                    return node.value
                elif isinstance(node, ast.Name):
                    if node.id in local_vars:
                        return local_vars[node.id]
                    raise ValueError(f"Variable '{node.id}' is not defined.")
                elif isinstance(node, ast.Dict):
                    return {evaluate_ast(k, local_vars): evaluate_ast(v, local_vars) for k, v in zip(node.keys, node.values)}
                elif isinstance(node, ast.List):
                    return [evaluate_ast(x, local_vars) for x in node.elts]
                elif isinstance(node, ast.Subscript):
                    obj = evaluate_ast(node.value, local_vars)
                    key = evaluate_ast(node.slice, local_vars)
                    return obj[key]
                elif isinstance(node, ast.BinOp):
                    left = evaluate_ast(node.left, local_vars)
                    right = evaluate_ast(node.right, local_vars)
                    if isinstance(node.op, ast.Add): return left + right
                    if isinstance(node.op, ast.Sub): return left - right
                    if isinstance(node.op, ast.Mult): return left * right
                    if isinstance(node.op, ast.Div): return left / right
                    raise ValueError(f"Unsupported binary operator: {type(node.op)}")
                elif isinstance(node, ast.ListComp):
                    # Only support single comprehension with single target
                    if len(node.generators) != 1:
                        raise ValueError("Only single list comprehensions are supported.")
                    gen = node.generators[0]
                    if not isinstance(gen.target, ast.Name):
                        raise ValueError("List comprehension target must be a simple variable name.")

                    target_name = gen.target.id
                    iterable = evaluate_ast(gen.iter, local_vars)

                    result_list = []
                    for item in iterable:
                        # Create a new scope for the list comp
                        loop_vars = local_vars.copy()
                        loop_vars[target_name] = item
                        result_list.append(evaluate_ast(node.elt, loop_vars))
                    return result_list
                else:
                    raise ValueError(f"Unsupported expression type: {type(node)}")

            # Parse to AST and evaluate strictly
            tree = ast.parse(expression, mode='eval')
            result = evaluate_ast(tree, {"data": data})

            self.set_output(context, "processed_data", result)

        except Exception as e:
            print(f"PostProcessorNode execution error: {e}")
            self.set_output(context, "processed_data", {"error": str(e), "original_data": data})
