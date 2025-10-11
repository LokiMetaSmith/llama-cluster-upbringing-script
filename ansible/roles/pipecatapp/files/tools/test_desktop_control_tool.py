import unittest
from unittest.mock import patch, MagicMock
from desktop_control_tool import DesktopControlTool

class TestDesktopControlTool(unittest.TestCase):
    def setUp(self):
        """Set up the test case."""
        self.tool = DesktopControlTool()

    @patch('pyautogui.screenshot')
    def test_get_desktop_screenshot(self, mock_screenshot):
        """Test that get_desktop_screenshot calls pyautogui.screenshot and returns base64."""
        # Configure the mock to return a dummy image and simulate the save method
        mock_image = MagicMock()
        def save_side_effect(buffer, format):
            buffer.write(b"dummy image data")
        mock_image.save.side_effect = save_side_effect
        mock_screenshot.return_value = mock_image

        # Call the method
        result = self.tool.get_desktop_screenshot()

        # Assert that pyautogui.screenshot was called
        mock_screenshot.assert_called_once()
        # Assert that the result is the correctly base64-encoded string
        import base64
        expected_result = base64.b64encode(b"dummy image data").decode('utf-8')
        self.assertEqual(result, expected_result)

    @patch('pyautogui.click')
    def test_click_at(self, mock_click):
        """Test that click_at calls pyautogui.click with the correct coordinates."""
        x, y = 123, 456
        self.tool.click_at(x, y)
        mock_click.assert_called_once_with(x, y)

    @patch('pyautogui.typewrite')
    def test_type_text(self, mock_typewrite):
        """Test that type_text calls pyautogui.typewrite with the correct text."""
        text = "hello world"
        self.tool.type_text(text)
        mock_typewrite.assert_called_once_with(text)

if __name__ == '__main__':
    unittest.main()