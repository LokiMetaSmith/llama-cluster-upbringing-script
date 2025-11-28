import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import base64

# Add tools directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from web_browser_tool import WebBrowserTool

@pytest.fixture
def mock_playwright():
    with patch('web_browser_tool.sync_playwright') as mock:
        yield mock

@pytest.fixture
def browser_tool(mock_playwright):
    # Setup mocks before instantiation
    mock_pw_instance = mock_playwright.return_value.start.return_value
    mock_browser = mock_pw_instance.chromium.launch.return_value
    mock_page = mock_browser.new_page.return_value

    tool = WebBrowserTool()
    # Attach mocks to tool for assertion.
    # Note: WebBrowserTool.__init__ calls sync_playwright().start(), chromium.launch(), new_page()
    # So our mock returns are already used.
    tool._mock_page = mock_page
    tool._mock_browser = mock_browser
    tool._mock_pw = mock_pw_instance
    return tool

def test_goto_success(browser_tool):
    result = browser_tool.goto("https://example.com")
    browser_tool._mock_page.goto.assert_called_once_with("https://example.com")
    assert result == "Successfully navigated to https://example.com."

def test_goto_failure(browser_tool):
    browser_tool._mock_page.goto.side_effect = Exception("Page not found")
    result = browser_tool.goto("https://invalid-url.com")
    assert "Error navigating to https://invalid-url.com: Page not found" in result

def test_get_page_content_success(browser_tool):
    browser_tool._mock_page.content.return_value = "<html><body><h1>Hello</h1></body></html>"
    result = browser_tool.get_page_content()
    assert result == "<html><body><h1>Hello</h1></body></html>"
    browser_tool._mock_page.content.assert_called_once()

def test_click_success(browser_tool):
    result = browser_tool.click("#my-button")
    browser_tool._mock_page.click.assert_called_once_with("#my-button")
    assert result == "Successfully clicked on element with selector '#my-button'."

def test_click_failure(browser_tool):
    browser_tool._mock_page.click.side_effect = Exception("Element not found")
    result = browser_tool.click("#nonexistent-button")
    assert "Error clicking on element with selector '#nonexistent-button': Element not found" in result

def test_type_success(browser_tool):
    result = browser_tool.type("#my-input", "hello world")
    browser_tool._mock_page.type.assert_called_once_with("#my-input", "hello world")
    assert result == "Successfully typed 'hello world' into element with selector '#my-input'."

def test_close(browser_tool):
    browser_tool.close()
    browser_tool._mock_browser.close.assert_called_once()
    browser_tool._mock_pw.stop.assert_called_once()

def test_get_screenshot(browser_tool):
    dummy_bytes = b'screenshot_data'
    browser_tool._mock_page.screenshot.return_value = dummy_bytes
    result = browser_tool.get_screenshot()
    browser_tool._mock_page.screenshot.assert_called_once()
    assert result == base64.b64encode(dummy_bytes).decode('utf-8')

def test_click_at(browser_tool):
    x, y = 100, 200
    result = browser_tool.click_at(x, y)
    browser_tool._mock_page.mouse.click.assert_called_once_with(x, y)
    assert result == "Successfully clicked at (100, 200)."

def test_type_text_at(browser_tool):
    x, y = 150, 250
    text = "hello vision"
    result = browser_tool.type_text_at(x, y, text)
    browser_tool._mock_page.mouse.click.assert_called_once_with(x, y)
    browser_tool._mock_page.keyboard.type.assert_called_once_with(text)
    assert result == f"Successfully typed '{text}' at ({x}, {y})."
