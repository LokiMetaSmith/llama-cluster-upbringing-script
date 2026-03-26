from typing import Dict, Any
from langchain_core.runnables import RunnableConfig

from .registry import registry
from ..node import Node
from ..context import WorkflowContext


@registry.register
class LangGraphNode(Node):
    """
    A custom node for the Pipecat WorkflowRunner that executes a compiled LangGraph.

    This node acts as an interoperability bridge. It allows a complex, cyclic agentic
    reasoning loop built in LangGraph to be executed as a single step within our broader,
    hardware-aware orchestrator-driven DAG.
    """
    async def execute(self, context: WorkflowContext):
        # Retrieve the compiled LangGraph object from the global inputs
        compiled_graph = context.global_inputs.get("compiled_langgraph")

        if not compiled_graph:
            self.set_output(context, "error", "No compiled_langgraph provided in global inputs.")
            return

        # Prepare the initial state for the LangGraph. This can be constructed from
        # the inputs mapped to this node in the YAML workflow definition.
        initial_state: Dict[str, Any] = {}
        for input_config in self.config.get("inputs", []):
            name = input_config["name"]
            val = self.get_input(context, name)
            if val is not None:
                initial_state[name] = val

        # If no explicit inputs are mapped, fallback to standard agent inputs
        if not initial_state:
            initial_state = {
                "messages": context.global_inputs.get("user_text", ""),
                "tools": context.global_inputs.get("tools_dict", {})
            }

        config = RunnableConfig(
            # We could attach LangChain callbacks or tracing here in the future
            metadata={"workflow_runner_id": getattr(context, "runner_id", "unknown")}
        )

        try:
            # Execute the LangGraph.
            # Note: compiled_graph.ainvoke is expected for async graphs.
            if hasattr(compiled_graph, "ainvoke"):
                 final_state = await compiled_graph.ainvoke(initial_state, config)
            else:
                 # Fallback to synchronous invoke if the graph doesn't support async
                 final_state = compiled_graph.invoke(initial_state, config)

            # Extract the final result and push it to the Pipecat workflow context

            # Usually LangGraph agents return a 'messages' list where the last is the final response
            if isinstance(final_state, dict) and "messages" in final_state:
                last_message = final_state["messages"][-1]
                if hasattr(last_message, "content"):
                     self.set_output(context, "response", last_message.content)
                     self.set_output(context, "full_state", final_state)
                     return

            self.set_output(context, "response", str(final_state))

        except Exception as e:
            error_msg = f"LangGraph execution failed: {str(e)}"
            self.set_output(context, "error", error_msg)
            self.set_output(context, "response", error_msg)
