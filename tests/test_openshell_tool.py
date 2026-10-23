import pytest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.openshell_tool import OpenShellTool

def test_openshell_tool_schema():
    tool = OpenShellTool()
    schema = tool.get_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "openshell"
    assert "create_sandbox" in schema["function"]["parameters"]["properties"]["action"]["description"]

def test_openshell_tool_simulation():
    tool = OpenShellTool()
    # When openshell CLI is not installed or simulated
    with patch("shutil.which", return_value=None):
        res_create = tool.execute("create_sandbox", name="test-sbx")
        assert res_create["success"] is True
        assert res_create["simulated"] is True
        assert res_create["data"]["name"] == "test-sbx"

        res_list = tool.execute("list_sandboxes")
        assert res_list["success"] is True
        assert res_list["simulated"] is True

        res_policy = tool.execute("check_policy", policy_path="test_policy.yaml")
        assert res_policy["success"] is True
        assert res_policy["data"]["policy_status"] == "verified"

        res_exec = tool.execute("execute_command", sandbox_name="test-sbx", command="echo 123")
        assert res_exec["success"] is True

        res_status = tool.execute("get_status")
        assert res_status["success"] is True

        res_unknown = tool.execute("non_existent_action")
        assert res_unknown["success"] is False
        assert "Unknown action" in res_unknown["error"]

def test_openshell_tool_cli_execution():
    tool = OpenShellTool()
    mock_res = MagicMock()
    mock_res.returncode = 0
    mock_res.stdout = '{"status": "ok", "sandboxes": ["demo"]}'
    mock_res.stderr = ''

    with patch("shutil.which", return_value="/usr/local/bin/openshell"):
        with patch("pipecatapp.utils.command_runner.CommandRunner.run", return_value=mock_res) as mock_runner:
            res = tool.list_sandboxes()
            assert res["success"] is True
            assert res["data"]["status"] == "ok"
            mock_runner.assert_called_once()
