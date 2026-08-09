import pytest
import os
import json
import shutil
from pipecatapp.tools.holographic_memory_tool import HolographicMemoryTool

@pytest.fixture
def memory_tool():
    test_dir = "test_holographic_memory"
    tool = HolographicMemoryTool(memory_dir=test_dir)
    yield tool
    # Cleanup
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

def test_holographic_memory_save(memory_tool):
    matrix_data = {"dimensions": [128, 128], "branches": 5}
    result = memory_tool.run("save", "test_matrix", matrix_data, "test context")

    assert "Successfully saved" in result

    # Check file exists and contents
    file_path = os.path.join(memory_tool.memory_dir, "test_matrix.json")
    assert os.path.exists(file_path)

    with open(file_path, "r") as f:
        data = json.load(f)

    assert data["matrix_name"] == "test_matrix"
    assert data["matrix_data"]["branches"] == 5

def test_holographic_memory_recall(memory_tool):
    # Setup test file
    matrix_data = {"dimensions": [128, 128], "branches": 10}
    memory_tool.run("save", "test_recall_matrix", matrix_data, "test context")

    result = memory_tool.run("recall", "test_recall_matrix")

    assert "Recalled Holographic Memory" in result
    assert "test_recall_matrix" in result
    assert "10" in result # branches

def test_holographic_memory_missing():
    tool = HolographicMemoryTool(memory_dir="test_holographic_memory")
    result = tool.run("recall", "missing_matrix")

    assert "Error: Holographic memory" in result

def test_holographic_memory_sanitize(memory_tool):
    matrix_data = {"dimensions": [128, 128], "branches": 5}
    # Attempt directory traversal
    result = memory_tool.run("save", "../../../etc/passwd", matrix_data, "test context")

    assert "Successfully saved" in result

    # Check file exists and contents with sanitized name
    file_path = os.path.join(memory_tool.memory_dir, "etcpasswd.json")
    assert os.path.exists(file_path)

def test_holographic_memory_search(memory_tool):
    matrix_data = {"dimensions": [128, 128], "branches": 5}
    memory_tool.run("save", "test_matrix_1", matrix_data, "routes to python expert")
    memory_tool.run("save", "test_matrix_2", matrix_data, "routes to math expert")

    result = memory_tool.run("search", context_description="python")

    assert "Found 1 matching memories" in result
    assert "test_matrix_1" in result
    assert "test_matrix_2" not in result

def test_holographic_memory_search_not_found(memory_tool):
    result = memory_tool.run("search", context_description="nonexistent")
    assert "No holographic memory found" in result
