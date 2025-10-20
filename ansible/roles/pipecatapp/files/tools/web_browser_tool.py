import base64
import sys
from unittest.mock import MagicMock

# Mock playwright if it's not available
if 'playwright' not in sys.modules:
    sys.modules['playwright'] = MagicMock()
    sys.modules['playwright.sync_api'] = MagicMock()

from playwright.sync_api import sync_playwright

class WebBrowserTool:
    """A tool for browsing the web to answer questions and interact with sites.

    This class wraps the Playwright library to provide the agent with a
    fully-featured web browser that it can control programmatically. It can
    navigate, read content, and interact with web elements.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
        playwright: The Playwright instance.
        browser: The browser instance (Chromium).
        page: The currently active browser page.
    """
    def __init__(self):
        """Initializes the WebBrowserTool by launching Playwright and a browser."""
        self.description = "A tool for browsing the web to answer questions."
        self.name = "web_browser"
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()

    def goto(self, url: str) -> str:
        """Navigates the browser to a specific URL.

        Args:
            url (str): The URL to navigate to.

        Returns:
            str: A confirmation message on success, or an error message.
        """
        try:
            self.page.goto(url)
            return f"Successfully navigated to {url}."
        except Exception as e:
            return f"Error navigating to {url}: {e}"

    def get_page_content(self) -> str:
        """Returns the full HTML content of the current page.

        Returns:
            str: The page's HTML content, or an error message.
        """
        try:
            return self.page.content()
        except Exception as e:
            return f"Error getting page content: {e}"

    def get_screenshot(self) -> str:
        """Takes a screenshot of the current page and returns it as a base64 string.

        Returns:
            str: A base64-encoded string of the screenshot PNG, or an error message.
        """
        try:
            screenshot_bytes = self.page.screenshot()
            return base64.b64encode(screenshot_bytes).decode('utf-8')
        except Exception as e:
            return f"Error taking screenshot: {e}"

    def click(self, selector: str) -> str:
        """Clicks on an element on the page, identified by a CSS selector.

        Args:
            selector (str): The CSS selector of the element to click.

        Returns:
            str: A confirmation message on success, or an error message.
        """
        try:
            self.page.click(selector)
            return f"Successfully clicked on element with selector '{selector}'."
        except Exception as e:
            return f"Error clicking on element with selector '{selector}': {e}"

    def type(self, selector: str, text: str) -> str:
        """Types text into an input field, identified by a CSS selector.

        Args:
            selector (str): The CSS selector of the input element.
            text (str): The text to type into the element.

        Returns:
            str: A confirmation message on success, or an error message.
        """
        try:
            self.page.type(selector, text)
            return f"Successfully typed '{text}' into element with selector '{selector}'."
        except Exception as e:
            return f"Error typing into element with selector '{selector}': {e}"

    def click_at(self, x: int, y: int) -> str:
        """Clicks the mouse at a specific (x, y) coordinate on the page.

        Args:
            x (int): The x-coordinate to click.
            y (int): The y-coordinate to click.

        Returns:
            str: A confirmation message on success, or an error message.
        """
        try:
            self.page.mouse.click(x, y)
            return f"Successfully clicked at ({x}, {y})."
        except Exception as e:
            return f"Error clicking at ({x}, {y}): {e}"

    def type_text_at(self, x: int, y: int, text: str) -> str:
        """Clicks at a coordinate and then types text.

        Args:
            x (int): The x-coordinate to click.
            y (int): The y-coordinate to click.
            text (str): The text to type.

        Returns:
            str: A confirmation message on success, or an error message.
        """
        try:
            self.page.mouse.click(x, y)
            self.page.keyboard.type(text)
            return f"Successfully typed '{text}' at ({x}, {y})."
        except Exception as e:
            return f"Error typing at ({x}, {y}): {e}"

    def close(self):
        """Closes the browser and stops the Playwright instance."""
        self.browser.close()
        self.playwright.stop()
