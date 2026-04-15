import pytest
import json
from pipecatapp.tools.submit_solution_tool import SubmitSolutionTool

def test_submit_solution_tool_initialization():
    tool = SubmitSolutionTool()
    assert tool is not None

def test_submit_solution_success():
    tool = SubmitSolutionTool()

    res = tool.run("print('Hello')", "hello.py", "A test script")

    res_json = json.loads(res)
    assert res_json["type"] == "solution_artifact"
    assert res_json["file_path"] == "hello.py"
    assert res_json["content"] == "print('Hello')"
    assert res_json["description"] == "A test script"
