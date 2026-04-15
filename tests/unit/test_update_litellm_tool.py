import pytest
import json
import os
from unittest.mock import patch, MagicMock
from pipecatapp.tools.update_litellm_tool import UpdateLitellmTool

def test_update_litellm_tool_initialization():
    tool = UpdateLitellmTool()
    assert tool.schema is not None

@patch("urllib.request.urlopen")
def test_fetch_releases_success(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps([{"tag_name": "v1.0", "published_at": "now", "name": "V1"}]).encode()
    mock_urlopen.return_value.__enter__.return_value = mock_response

    tool = UpdateLitellmTool()
    res = tool.execute("fetch_releases")
    res_json = json.loads(res)
    assert len(res_json) == 1
    assert res_json[0]["tag_name"] == "v1.0"

@patch("os.path.exists", return_value=False)
def test_update_nomad_file_missing(mock_exists):
    tool = UpdateLitellmTool()
    res = tool.execute("update_nomad_file", chosen_tag="v1.0")
    assert "not found" in res

@patch("os.path.exists", return_value=True)
@patch("builtins.open")
def test_update_nomad_file_success(mock_open, mock_exists):
    # Setup mock file reading and writing
    mock_file = MagicMock()
    mock_file.read.return_value = 'image = "ghcr.io/berriai/litellm:old-tag"'
    mock_open.return_value.__enter__.return_value = mock_file

    tool = UpdateLitellmTool()
    res = tool.execute("update_nomad_file", chosen_tag="v1.0")
    assert "Updated" in res
    assert "main-v1.0" in res

def test_execute_missing_tag():
    tool = UpdateLitellmTool()
    res = tool.execute("update_nomad_file")
    assert "chosen_tag is required" in res

def test_execute_unknown_action():
    tool = UpdateLitellmTool()
    res = tool.execute("unknown")
    assert "Unknown action" in res
