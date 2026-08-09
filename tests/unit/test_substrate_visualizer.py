import pytest
import os
import shutil
from pipecatapp.tools.substrate_visualizer_tool import SubstrateVisualizerTool

@pytest.fixture
def visualizer():
    test_dir = "test_visualizations"
    tool = SubstrateVisualizerTool(output_dir=test_dir)
    yield tool
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

def test_visualizer_generates_html(visualizer):
    matrix_data = {
        "correlation_length": 0.9,
        "branches": 5,
        "substrate_state": "focused"
    }

    result = visualizer.run(matrix_data, "test_vis.html")
    assert "Successfully generated" in result

    file_path = os.path.join(visualizer.output_dir, "test_vis.html")
    assert os.path.exists(file_path)

    with open(file_path, "r") as f:
        content = f.read()

    assert "Glitter UI" in content
    assert "FOCUSED" in content
    assert "<svg" in content
    assert "path d=" in content # Ensures lines were drawn

def test_visualizer_sanitize_path(visualizer):
    matrix_data = {"branches": 2}
    visualizer.run(matrix_data, "../../../etc/shadow")

    file_path = os.path.join(visualizer.output_dir, "shadow.html")
    assert os.path.exists(file_path)
