from typing import Any, Callable, Dict, Optional
import inspect

class LangChainToolAdapter:
    """
    A generic adapter that wraps a LangChain BaseTool so it can be automatically
    discovered and executed by the custom Pipecat WorkflowRunner (specifically
    SystemPromptNode and ToolExecutorNode).

    The adapter exposes the LangChain tool's 'invoke' method as a dynamically
    named method (based on the tool's name) and sets its docstring to the tool's
    description so that the LLM understands how to use it.
    """
    def __init__(self, langchain_tool: Any):
        """
        Initializes the adapter with a LangChain tool.

        Args:
            langchain_tool (BaseTool): A LangChain tool instance (e.g., from
                @tool or a pre-built community tool).
        """
        self._langchain_tool = langchain_tool

        # Sanitize the tool name to be a valid Python method name
        method_name = langchain_tool.name.replace("-", "_").replace(" ", "_").lower()
        if not method_name.isidentifier():
             method_name = "execute_langchain_tool"

        self._method_name = method_name
        self._description = langchain_tool.description

        # Bind the wrapped execution function to the specific method name expected
        # by the pipecatapp system.
        setattr(self, self._method_name, self._create_execution_method())

    def _create_execution_method(self) -> Callable:
        """
        Creates a bound method that intercepts our custom framework's **args
        and passes them correctly to the LangChain tool's invoke method.
        """
        def wrapped_execute(**kwargs) -> str:
            try:
                # Langchain tools typically take a single string (query) or a dict (args).
                # We pass the unpacked kwargs. Langchain handles schema validation.
                if len(kwargs) == 1 and list(kwargs.keys())[0] in ["tool_input", "query", "__arg1"]:
                     # Fast path for single arg tools like DuckDuckGoSearch
                     result = self._langchain_tool.invoke(list(kwargs.values())[0])
                else:
                     result = self._langchain_tool.invoke(kwargs)
                return str(result)
            except Exception as e:
                return f"Error executing LangChain tool '{self._langchain_tool.name}': {str(e)}"

        # SystemPromptNode relies on docstrings to build the LLM instructions
        wrapped_execute.__doc__ = self._description

        # Optionally, we could attach the Langchain args_schema here if we wanted
        # to expose parameter types to our SystemPromptNode in the future.

        return wrapped_execute
