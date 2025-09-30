import pytest
from playwright.sync_api import Page, expect
import time

def test_code_runner_tool(page: Page):
    """
    Tests that the agent can successfully use the code_runner tool.
    """
    # Navigate to the web UI
    page.goto("http://localhost:8000")

    # Find the message input field and send a message
    message_input = page.locator("#message-input")
    expect(message_input).to_be_visible()
    message_input.fill("run python code: print(2+2)")
    message_input.press("Enter")

    # Wait for the agent's response
    # It might take a moment for the tool to run and the response to come back.
    # We will check for the response in the terminal.
    terminal = page.locator("#terminal")

    # The response from the agent should contain the result "4"
    expect(terminal).to_contain_text("4", timeout=30000)