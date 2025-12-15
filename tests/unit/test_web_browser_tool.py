import unittest
import sys
import os
from unittest.mock import patch, MagicMock, AsyncMock
import base64

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from web_browser_tool import WebBrowserTool

class TestWebBrowserTool(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.patcher = patch('web_browser_tool.async_playwright')
        self.mock_async_playwright = self.patcher.start()

        # Configure mocks
        self.mock_playwright_instance = AsyncMock()
        self.mock_browser = AsyncMock()
        self.mock_page = AsyncMock()

        # Make the .start() method of the async_playwright return value an AsyncMock
        # When called, it will be awaited, and return self.mock_playwright_instance
        self.mock_async_playwright.return_value.start = AsyncMock(return_value=self.mock_playwright_instance)

        # Make chromium.launch an AsyncMock
        self.mock_playwright_instance.chromium.launch = AsyncMock(return_value=self.mock_browser)

        # Make browser.new_page an AsyncMock
        self.mock_browser.new_page = AsyncMock(return_value=self.mock_page)

        self.tool = WebBrowserTool()

    async def asyncTearDown(self):
        self.patcher.stop()

    async def test_goto_success(self):
        result = await self.tool.goto("https://example.com")

        # Verify initialization happened
        self.mock_async_playwright.return_value.start.assert_awaited()
        self.mock_playwright_instance.chromium.launch.assert_awaited()
        self.mock_browser.new_page.assert_awaited()

        # Verify action
        self.mock_page.goto.assert_awaited_with("https://example.com")
        self.assertEqual(result, "Successfully navigated to https://example.com.")

    async def test_goto_failure(self):
        self.mock_page.goto.side_effect = Exception("Page not found")
        result = await self.tool.goto("https://invalid-url.com")
        self.assertIn("Error navigating to https://invalid-url.com: Page not found", result)

    async def test_get_page_content_success(self):
        self.mock_page.content.return_value = "<html><body><h1>Hello</h1></body></html>"
        result = await self.tool.get_page_content()
        self.assertEqual(result, "<html><body><h1>Hello</h1></body></html>")
        self.mock_page.content.assert_awaited_once()

    async def test_click_success(self):
        result = await self.tool.click("#my-button")
        self.mock_page.click.assert_awaited_with("#my-button")
        self.assertEqual(result, "Successfully clicked on element with selector '#my-button'.")

    async def test_click_failure(self):
        self.mock_page.click.side_effect = Exception("Element not found")
        result = await self.tool.click("#nonexistent-button")
        self.assertIn("Error clicking on element with selector '#nonexistent-button': Element not found", result)

    async def test_type_success(self):
        result = await self.tool.type("#my-input", "hello world")
        self.mock_page.type.assert_awaited_with("#my-input", "hello world")
        self.assertEqual(result, "Successfully typed 'hello world' into element with selector '#my-input'.")

    async def test_close(self):
        # We need to initialize first to test close
        await self.tool.ensure_initialized()

        await self.tool.close()
        self.mock_browser.close.assert_awaited_once()
        self.mock_playwright_instance.stop.assert_awaited_once()

    async def test_get_screenshot(self):
        dummy_bytes = b'screenshot_data'
        self.mock_page.screenshot.return_value = dummy_bytes
        result = await self.tool.get_screenshot()
        self.mock_page.screenshot.assert_awaited_once()
        self.assertEqual(result, base64.b64encode(dummy_bytes).decode('utf-8'))

    async def test_click_at(self):
        x, y = 100, 200
        result = await self.tool.click_at(x, y)
        self.mock_page.mouse.click.assert_awaited_with(x, y)
        self.assertEqual(result, "Successfully clicked at (100, 200).")

    async def test_type_text_at(self):
        x, y = 150, 250
        text = "hello vision"
        result = await self.tool.type_text_at(x, y, text)
        self.mock_page.mouse.click.assert_awaited_with(x, y)
        self.mock_page.keyboard.type.assert_awaited_with(text)
        self.assertEqual(result, f"Successfully typed '{text}' at ({x}, {y}).")

if __name__ == '__main__':
    unittest.main()
