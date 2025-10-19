import unittest
from unittest.mock import patch

# Import the class to be tested
from web_browser_tool import WebBrowserTool

class TestWebBrowserTool(unittest.TestCase):

    def setUp(self):
        """Set up fresh mocks for each test."""
        # Start the patcher for the playwright dependency and keep a reference to stop it later
        self.playwright_patcher = patch('web_browser_tool.sync_playwright')
        self.mock_sync_playwright = self.playwright_patcher.start()
        self.addCleanup(self.playwright_patcher.stop)

        # Configure the entire mock hierarchy for this specific test run
        self.mock_playwright = self.mock_sync_playwright.return_value.start.return_value
        self.mock_browser = self.mock_playwright.chromium.launch.return_value
        self.mock_page = self.mock_browser.new_page.return_value

        # Now instantiate the tool. It will use the fresh mocks we just configured.
        self.browser_tool = WebBrowserTool()

    def test_goto_success(self):
        """Test successful navigation to a URL."""
        result = self.browser_tool.goto("https://example.com")
        self.mock_page.goto.assert_called_once_with("https://example.com")
        self.assertEqual(result, "Successfully navigated to https://example.com.")

    def test_goto_failure(self):
        """Test failed navigation."""
        self.mock_page.goto.side_effect = Exception("Page not found")
        result = self.browser_tool.goto("https://invalid-url.com")
        self.assertIn("Error navigating to https://invalid-url.com: Page not found", result)

    def test_get_page_content_success(self):
        """Test successfully getting page content."""
        self.mock_page.content.return_value = "<html><body><h1>Hello</h1></body></html>"
        result = self.browser_tool.get_page_content()
        self.assertEqual(result, "<html><body><h1>Hello</h1></body></html>")
        self.mock_page.content.assert_called_once()

    def test_click_success(self):
        """Test successfully clicking an element."""
        result = self.browser_tool.click("#my-button")
        self.mock_page.click.assert_called_once_with("#my-button")
        self.assertEqual(result, "Successfully clicked on element with selector '#my-button'.")

    def test_click_failure(self):
        """Test failing to click an element."""
        self.mock_page.click.side_effect = Exception("Element not found")
        result = self.browser_tool.click("#nonexistent-button")
        self.assertIn("Error clicking on element with selector '#nonexistent-button': Element not found", result)

    def test_type_success(self):
        """Test successfully typing into an element."""
        result = self.browser_tool.type("#my-input", "hello world")
        self.mock_page.type.assert_called_once_with("#my-input", "hello world")
        self.assertEqual(result, "Successfully typed 'hello world' into element with selector '#my-input'.")

    def test_close(self):
        """Test that the close method calls the underlying browser and playwright close methods."""
        self.browser_tool.close()
        self.mock_browser.close.assert_called_once()
        self.mock_playwright.stop.assert_called_once()

    def test_get_screenshot(self):
        """Test taking a screenshot."""
        dummy_bytes = b'screenshot_data'
        self.mock_page.screenshot.return_value = dummy_bytes
        result = self.browser_tool.get_screenshot()
        self.mock_page.screenshot.assert_called_once()
        import base64
        self.assertEqual(result, base64.b64encode(dummy_bytes).decode('utf-8'))

    def test_click_at(self):
        """Test clicking at a specific coordinate."""
        x, y = 100, 200
        result = self.browser_tool.click_at(x, y)
        self.mock_page.mouse.click.assert_called_once_with(x, y)
        self.assertEqual(result, "Successfully clicked at (100, 200).")

    def test_type_text_at(self):
        """Test typing text at a specific coordinate."""
        x, y = 150, 250
        text = "hello vision"
        result = self.browser_tool.type_text_at(x, y, text)
        self.mock_page.mouse.click.assert_called_once_with(x, y)
        self.mock_page.keyboard.type.assert_called_once_with(text)
        self.assertEqual(result, f"Successfully typed '{text}' at ({x}, {y}).")

if __name__ == '__main__':
    unittest.main()