import pytest
from pydantic import BaseModel, Field
import sys
import os

# Ensure the parent dir is in sys.path so we can import pipecatapp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pipecatapp.tools.langchain_adapter_tool import LangChainToolAdapter

class MockLangchainSchema(BaseModel):
    query: str = Field(description="Search query")

class MockLangChainTool:
    def __init__(self):
        self.name = "mock_tool"
        self.description = "A mock tool"
        self.args_schema = MockLangchainSchema

    def invoke(self, kwargs):
        return f"Mock result for {kwargs.get('query')}"

def test_langchain_adapter_schema():
    lc_tool = MockLangChainTool()
    adapter = LangChainToolAdapter(lc_tool)

    assert adapter.name == "mock_tool"
    assert adapter.description == "A mock tool"
    assert "query" in adapter.input_schema["properties"]

def test_langchain_adapter_run():
    lc_tool = MockLangChainTool()
    adapter = LangChainToolAdapter(lc_tool)

    result = adapter.run(query="hello")
    assert result == "Mock result for hello"

class MockLangChainToolNoSchema:
    def __init__(self):
        self.name = "mock_tool_no_schema"
        self.description = "A mock tool with no schema"

    def invoke(self, input_str):
        return f"Mock result string for {input_str}"

def test_langchain_adapter_run_no_schema():
    lc_tool = MockLangChainToolNoSchema()
    adapter = LangChainToolAdapter(lc_tool)

    result = adapter.run(tool_input="hello string")
    assert result == "Mock result string for hello string"
