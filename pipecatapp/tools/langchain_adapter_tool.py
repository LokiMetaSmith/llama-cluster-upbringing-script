import json
import logging
from typing import Any

logger = logging.getLogger("LangChainToolAdapter")

class LangChainToolAdapter:
    """
    Adapter class capable of ingesting any LangChain BaseTool and exposing it
    through the standard methods expected by our ToolExecutorNode.
    """
    def __init__(self, langchain_tool: Any):
        self.langchain_tool = langchain_tool
        self.name = getattr(langchain_tool, "name", "langchain_tool")
        self.description = getattr(langchain_tool, "description", "")

        # Convert LangChain args_schema (pydantic) to JSON Schema if available
        if hasattr(langchain_tool, "args_schema") and langchain_tool.args_schema:
            try:
                self.input_schema = langchain_tool.args_schema.model_json_schema()
            except Exception:
                try:
                    self.input_schema = langchain_tool.args_schema.schema()
                except Exception:
                    self.input_schema = {
                        "type": "object",
                        "properties": {
                            "tool_input": {
                                "type": "string",
                                "description": "Input for the tool"
                            }
                        }
                    }
        else:
            self.input_schema = {
                "type": "object",
                "properties": {
                    "tool_input": {
                        "type": "string",
                        "description": "Input for the tool"
                    }
                }
            }

    def run(self, **kwargs) -> Any:
        try:
            # LangChain tools usually accept either single string or kwargs
            if len(kwargs) == 1 and "tool_input" in kwargs and not hasattr(self.langchain_tool, "args_schema"):
                return self.langchain_tool.invoke(kwargs["tool_input"])
            return self.langchain_tool.invoke(kwargs)
        except Exception as e:
            logger.error(f"Error executing LangChain tool {self.name}: {e}")
            return f"Error executing LangChain tool {self.name}: {str(e)}"
