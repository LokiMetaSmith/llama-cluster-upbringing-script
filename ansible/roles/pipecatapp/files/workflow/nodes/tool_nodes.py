from .registry import registry
from ..node import Node
from ..context import WorkflowContext
import json
import inspect

@registry.register
class SystemPromptNode(Node):
    """A node that constructs the system prompt with tool definitions."""
    async def execute(self, context: WorkflowContext):
        tools = context.global_inputs.get("tools", {})
        available_services = self.get_input(context, "available_services") or []

        prompt_file = "prompts/router.txt" # Hardcoded for now
        try:
            with open(prompt_file, "r") as f:
                base_prompt = f.read()
        except FileNotFoundError:
            base_prompt = "You are a helpful AI assistant."

        tools_prompt = "You have access to the following tools:\\n"
        for tool_name, tool in tools.items():
            if tool_name == "vision":
                tools_prompt += '- {"tool": "vision.get_observation"}: Get a real-time description of what is visible in the webcam.\\n'
            else:
                for method_name, method in inspect.getmembers(tool, predicate=inspect.ismethod):
                    if not method_name.startswith('_'):
                        tools_prompt += f'- {{"tool": "{tool_name}.{method_name}", "args": {{...}}}}: {method.__doc__}\\n'

        # Dynamically add available expert services to the prompt
        for service_name in available_services:
            tools_prompt += f'- {{"tool": "route_to_expert", "args": {{"expert": "{service_name}", "query": "<user_query>"}}}}: Use this for queries related to {service_name}.\\n'

        full_prompt = f"{base_prompt}\\n\\n{tools_prompt}\\n\\nIf the query doesn't fit a specific expert or tool, handle it yourself. Otherwise, respond with a JSON object with the 'tool' and 'args' keys."
        self.set_output(context, "system_prompt", full_prompt)

@registry.register
class ScreenshotNode(Node):
    """A node that captures a desktop screenshot."""
    async def execute(self, context: WorkflowContext):
        desktop_control_tool = context.global_inputs.get("tools", {}).get("desktop_control")
        if not desktop_control_tool:
            raise ValueError("DesktopControlTool not found in context.")
        screenshot = desktop_control_tool.get_desktop_screenshot()
        self.set_output(context, "screenshot_base64", screenshot)

@registry.register
class ToolParserNode(Node):
    """Parses the LLM response to determine if it's a tool call or a final text response."""
    async def execute(self, context: WorkflowContext):
        llm_response_text = self.get_input(context, "llm_response")
        try:
            tool_call = json.loads(llm_response_text)
            if "tool" in tool_call and "args" in tool_call:
                # It's a tool call
                self.set_output(context, "tool_call_data", tool_call)
                self.set_output(context, "final_response", None)
            else:
                # It's JSON, but not a tool call, treat as final response
                self.set_output(context, "tool_call_data", None)
                self.set_output(context, "final_response", llm_response_text)
        except (json.JSONDecodeError, TypeError):
            # It's not JSON, so it must be a final response
            self.set_output(context, "tool_call_data", None)
            self.set_output(context, "final_response", llm_response_text)

@registry.register
class ToolExecutorNode(Node):
    """Executes a tool call and returns the result."""
    async def execute(self, context: WorkflowContext):
        tool_call_data = self.get_input(context, "tool_call_data")
        tools = context.global_inputs.get("tools", {})

        if not tool_call_data:
            self.set_output(context, "tool_result", None)
            return

        tool_string = tool_call_data.get("tool", "")
        args = tool_call_data.get("args", {})

        try:
            tool_name, method_name = tool_string.split('.')
        except ValueError:
            raise ValueError(f"Invalid tool format: '{tool_string}'. Expected 'tool_name.method_name'.")

        tool = tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found.")

        method = getattr(tool, method_name)

        # Re-implement approval logic
        twin_service = context.global_inputs.get("twin_service")
        if twin_service and twin_service.approval_mode and tool_name in ["ssh", "code_runner", "ansible"]:
            if not await twin_service._request_approval({"tool": tool_string, "args": args}):
                result = f"Action denied. I cannot use the {tool_name} tool."
            else:
                result = method(**args)
        else:
            result = method(**args)
        if inspect.iscoroutine(result):
            result = await result

        # Quality control check for code-generating tools
        if tool_name in ["code_runner", "smol_agent_computer", "llxprt_code"]:
            if twin_service and hasattr(twin_service, 'quality_analyzer'):
                analysis_result = twin_service.quality_analyzer.analyze(result)
                # Format the structured result for the LLM
                combined_result = (
                    f"Tool output:\n```\n{result}\n```\n\n"
                    f"Quality Analysis:\n"
                    f"  - Score: {analysis_result['quality_score']}\n"
                    f"  - Report:\n{analysis_result['pylint_report']}"
                )
                self.set_output(context, "tool_result", combined_result)
                return

        self.set_output(context, "tool_result", str(result)) # Ensure result is a string
