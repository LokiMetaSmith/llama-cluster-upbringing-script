import pytest
import json
import os
import asyncio
from unittest.mock import MagicMock, patch
from pipecatapp.tools.autoloop_tool import AutoloopTool

def test_autoloop_tool_initialization():
    tool = AutoloopTool()
    assert tool is not None

def test_autoloop_no_autoloop_package():
    tool = AutoloopTool()

    with patch.dict('sys.modules', {'autoloop': None}):
        res = asyncio.run(tool.run("fake.py", "echo 1", "test", 1))
        assert "autoloop-ai is not installed" in res

def test_autoloop_target_not_exist():
    tool = AutoloopTool()

    with patch('builtins.__import__') as mock_import:
        mock_import.return_value = MagicMock()

        with patch('os.path.exists', return_value=False):
            res = asyncio.run(tool.run("nonexistent.py", "echo 1", "test", 1))
            assert "does not exist" in res

@patch('os.path.exists', return_value=True)
@patch('tempfile.mkstemp', return_value=(1, "temp.md"))
@patch('os.fdopen')
@patch('tempfile.mkdtemp', return_value="tempdir")
@patch('os.remove')
def test_autoloop_run_success(mock_remove, mock_mkdtemp, mock_fdopen, mock_mkstemp, mock_exists):
    tool = AutoloopTool()

    class MockAutoLoop:
        def __init__(self, **kwargs):
            self.best_score = 1.0
            self.results = [MagicMock(improved=True)]
            self.config = MagicMock(results_dir="tempdir")

        def run(self, experiments):
            pass

    with patch.dict('sys.modules', {'autoloop': MagicMock(AutoLoop=MockAutoLoop)}):
        res = asyncio.run(tool.run("target.py", "echo 1", "directives", 1))
        res_json = json.loads(res)
        assert res_json["target_file"] == "target.py"
        assert res_json["total_experiments"] == 1
        assert res_json["best_score"] == 1.0
        assert res_json["improvements_found"] == 1
