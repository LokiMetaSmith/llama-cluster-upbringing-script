import pytest
import os
import json
from pipecatapp.tools.field_guide_tool import FieldGuideTool
from pipecatapp.tools.file_editor_tool import FileEditorTool

def test_field_guide_auto_condense(tmp_path):
    guide_file = str(tmp_path / "field_guide.md")
    tool = FieldGuideTool(filepath=guide_file, line_budget=20)

    # Generate content over line budget (30 lines)
    over_lines = [f"Line {i}: context details" for i in range(30)]
    content = "\n".join(over_lines)

    res = tool.execute(action="update", content=content)
    assert "Successfully updated" in res
    assert "automatically condensed/truncated" in res

    with open(guide_file, "r") as f:
        read_lines = f.readlines()
    assert len(read_lines) <= 20

def test_file_editor_flag_megafile(tmp_path):
    editor = FileEditorTool(root_dir=str(tmp_path))
    res = editor.flag_megafile("heavy_legacy_module.py")
    assert "Successfully flagged" in res

    queue_path = tmp_path / ".liminal" / "megafiles_queue.json"
    assert os.path.exists(queue_path)
    with open(queue_path, "r") as f:
        data = json.load(f)
    assert "heavy_legacy_module.py" in data
