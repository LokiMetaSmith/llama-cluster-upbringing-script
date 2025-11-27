import pytest
import sys
import os

# Add the tools directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from final_answer_tool import FinalAnswerTool

def test_final_answer_tool_initialization():
    tool = FinalAnswerTool()
    assert tool.name == "final_answer"

def test_submit_task():
    tool = FinalAnswerTool()
    summary = "Task completed successfully."
    result = tool.submit_task(summary)
    assert result == f"Task submitted with summary: {summary}"
