import pytest
from playwright.sync_api import Page, expect

def test_mission_control_ui_loads(page: Page):
    """
    Tests that the Mission Control UI loads correctly.
    """
    # Navigate to the web UI
    page.goto("http://localhost:8000")

    # Check that the page title is correct
    expect(page).to_have_title("Mission Control")

    # Check for the presence of the main heading
    heading = page.locator("h1")
    expect(heading).to_contain_text("Mission Control")

    # Check that the terminal container is visible
    terminal_div = page.locator("#terminal")
    expect(terminal_div).to_be_visible()

    # Check that the status light is present
    status_light = page.locator("#status-light")
    expect(status_light).to_be_visible()

def test_health_check_endpoint(page: Page):
    """
    Tests that the /health API endpoint is responsive.
    """
    # We can use Playwright to make API requests as well
    response = page.request.get("http://localhost:8000/health")
    expect(response).to_be_ok()

    # Verify the response body
    json_response = response.json()
    assert json_response == {"status": "ok"}