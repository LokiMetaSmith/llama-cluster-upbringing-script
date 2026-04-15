import pytest
import socket
from unittest.mock import MagicMock, patch
from pipecatapp.tools.wol_tool import WOLTool

def test_wol_tool_initialization():
    tool = WOLTool()
    assert tool.name == "wol"

def test_validate_mac():
    tool = WOLTool()
    assert tool._validate_mac("00:11:22:33:44:55") == True
    assert tool._validate_mac("00-11-22-33-44-55") == True
    assert tool._validate_mac("invalid") == False
    assert tool._validate_mac("00:11:22:33:44:5Z") == False

def test_wake_invalid_mac():
    tool = WOLTool()
    res = tool.wake("invalid")
    assert "Invalid MAC address format" in res

@patch("socket.socket")
def test_wake_success(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    tool = WOLTool()
    res = tool.wake("00:11:22:33:44:55")

    assert "Success" in res
    assert "00:11:22:33:44:55" in res
    mock_socket.sendto.assert_called_once()
    args, kwargs = mock_socket.sendto.call_args
    assert args[1] == ("255.255.255.255", 9)
    assert b'\xff' * 6 in args[0]
    assert bytes.fromhex("001122334455") * 16 in args[0]

def test_execute():
    tool = WOLTool()

    with patch.object(tool, 'wake', return_value="Woke"):
        res = tool.execute({"mac_address": "00:11:22:33:44:55"})
        assert res == "Woke"

def test_execute_missing_arg():
    tool = WOLTool()
    res = tool.execute({})
    assert "mac_address is required" in res
