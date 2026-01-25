import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# Ensure we can import from pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.web_browser_tool import WebBrowserTool

@pytest.mark.asyncio
async def test_ssrf_protection():
    tool = WebBrowserTool()

    # Mock the internal playwright components to avoid real browser launch
    tool.playwright = MagicMock()
    tool.browser = MagicMock()
    tool.page = AsyncMock()
    # Mock goto to return success if called
    tool.page.goto.return_value = None

    # Test cases that should be BLOCKED
    blocked_urls = [
        "file:///etc/passwd",
        "http://localhost:8000/api/admin",
        "http://127.0.0.1:22",
        "http://0.0.0.0:8000",
        "http://169.254.169.254/latest/meta-data/",
        "http://[::1]/",
        "ftp://example.com",
    ]

    for url in blocked_urls:
        # Reset mock call count
        tool.page.goto.reset_mock()

        result = await tool.goto(url)

        # We expect a security error message, not a successful navigation
        # The result string usually starts with "Successfully navigated..." or "Error..."
        # If it navigated, it's a FAIL.
        assert "Security Error" in result or "blocked" in result.lower(), f"Security check failed! URL {url} was allowed. Result: {result}"

        # Ensure underlying goto was NOT called
        tool.page.goto.assert_not_called()

@pytest.mark.asyncio
async def test_valid_urls():
    tool = WebBrowserTool()
    tool.playwright = MagicMock()
    tool.browser = MagicMock()
    tool.page = AsyncMock()

    allowed_urls = [
        "https://www.google.com",
        "http://example.com",
        "https://github.com/pipecat-ai",
    ]

    for url in allowed_urls:
        # Reset mock
        tool.page.goto.reset_mock()
        await tool.goto(url)
        # Ensure underlying goto WAS called
        tool.page.goto.assert_called_with(url)
