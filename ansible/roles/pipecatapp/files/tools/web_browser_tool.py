from playwright.sync_api import sync_playwright

class WebBrowserTool:
    def __init__(self):
        self.description = "A tool for browsing the web to answer questions."
        self.name = "web_browser"
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()

    def goto(self, url: str):
        """Navigates the browser to a specific URL."""
        try:
            self.page.goto(url)
            return f"Successfully navigated to {url}."
        except Exception as e:
            return f"Error navigating to {url}: {e}"

    def get_page_content(self):
        """Returns the full text content of the current page."""
        try:
            return self.page.content()
        except Exception as e:
            return f"Error getting page content: {e}"

    def click(self, selector: str):
        """Clicks on an element on the page, identified by a CSS selector."""
        try:
            self.page.click(selector)
            return f"Successfully clicked on element with selector '{selector}'."
        except Exception as e:
            return f"Error clicking on element with selector '{selector}': {e}"

    def type(self, selector: str, text: str):
        """Types text into an input field, identified by a CSS selector."""
        try:
            self.page.type(selector, text)
            return f"Successfully typed '{text}' into element with selector '{selector}'."
        except Exception as e:
            return f"Error typing into element with selector '{selector}': {e}"

    def close(self):
        """Closes the browser."""
        self.browser.close()
        self.playwright.stop()
