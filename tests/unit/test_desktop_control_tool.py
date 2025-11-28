import pytest
import sys
import os
from unittest.mock import MagicMock
import base64

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from desktop_control_tool import DesktopControlTool

@pytest.fixture
def tool():
    return DesktopControlTool()

@pytest.fixture
def mock_pyautogui():
    # Get the global mock from conftest
    return sys.modules['pyautogui']

def test_get_desktop_screenshot(mock_pyautogui, tool):
    """Test that get_desktop_screenshot calls pyautogui.screenshot and returns base64."""
    # Configure the mock
    mock_image = MagicMock()
    def save_side_effect(buffer, format):
        buffer.write(b"dummy image data")
    mock_image.save.side_effect = save_side_effect
    mock_pyautogui.screenshot.return_value = mock_image

    # Call the method
    result = tool.get_desktop_screenshot()

    # Assertions
    mock_pyautogui.screenshot.assert_called_once()
    expected_result = base64.b64encode(b"dummy image data").decode('utf-8')
    assert result == expected_result

def test_click_at(mock_pyautogui, tool):
    """Test that click_at calls pyautogui.click with the correct coordinates."""
    x, y = 123, 456
    tool.click_at(x, y)
    mock_pyautogui.click.assert_called_once_with(x, y)

def test_type_text(mock_pyautogui, tool):
    """Test that type_text calls pyautogui.typewrite with the correct text."""
    text = "hello world"
    tool.type_text(text)
    mock_pyautogui.typewrite.assert_called_once_with(text)
