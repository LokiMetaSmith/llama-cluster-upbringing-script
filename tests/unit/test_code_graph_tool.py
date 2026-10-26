import pytest
import os
import asyncio
import tempfile
from pipecatapp.tools.code_graph_tool import CodeGraphTool

@pytest.fixture
def temp_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a sample workspace with a module and test file
        src_dir = os.path.join(tmpdir, "src")
        tests_dir = os.path.join(tmpdir, "tests")
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(tests_dir, exist_ok=True)

        module_path = os.path.join(src_dir, "calculator.py")
        test_path = os.path.join(tests_dir, "test_calculator.py")

        with open(module_path, "w", encoding="utf-8") as f:
            f.write('''"""Calculator module docstring."""

def add_numbers(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b

def multiply_numbers(a: int, b: int) -> int:
    """Multiplies two integers using repeated addition."""
    total = 0
    for _ in range(b):
        total = add_numbers(total, a)
    return total
''')

        with open(test_path, "w", encoding="utf-8") as f:
            f.write('''from src.calculator import add_numbers, multiply_numbers

def test_add_numbers():
    assert add_numbers(2, 3) == 5

def test_multiply_numbers():
    assert multiply_numbers(3, 4) == 12
''')

        yield tmpdir

def test_code_graph_schema(temp_workspace):
    tool = CodeGraphTool(root_dir=temp_workspace)
    schema = tool.get_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "code_graph"
    assert "blast_radius" in schema["function"]["parameters"]["properties"]["action"]["enum"]

def test_blast_radius(temp_workspace):
    tool = CodeGraphTool(root_dir=temp_workspace)
    res = asyncio.run(tool.execute(action="blast_radius", symbol="add_numbers"))
    assert "Direct Call Sites:" in res
    assert "Risk Verdict:" in res
    assert "test_calculator.py" in res

def test_preflight(temp_workspace):
    tool = CodeGraphTool(root_dir=temp_workspace)
    res = asyncio.run(tool.execute(action="preflight", symbol="add_numbers", filepath="src/calculator.py"))
    assert "=== Preflight Edit Checklist ===" in res
    assert "Adds two integers together." in res
    assert "Definition Location: src/calculator.py:" in res

def test_repository_trace(temp_workspace):
    tool = CodeGraphTool(root_dir=temp_workspace)
    res = asyncio.run(tool.execute(action="repository_trace", symbol="add_numbers", max_depth=2))
    assert "=== Repository Dependency Trace ===" in res
    assert "Symbol: add_numbers" in res

def test_repository_tests(temp_workspace):
    tool = CodeGraphTool(root_dir=temp_workspace)
    res = asyncio.run(tool.execute(action="repository_tests", symbol="add_numbers"))
    assert "=== Connected Repository Tests for 'add_numbers' ===" in res
    assert "test_calculator.py" in res
