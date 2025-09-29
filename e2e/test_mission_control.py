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

import time

def test_health_check_endpoint(page: Page):
    """
    Tests that the /health API endpoint eventually becomes healthy.
    The test will poll the endpoint for up to 60 seconds.
    """
    start_time = time.time()
    timeout = 60  # seconds

    while time.time() - start_time < timeout:
        response = page.request.get("http://localhost:8000/health", fail_on_error=False)
        if response.ok:
            json_response = response.json()
            assert json_response == {"status": "ok"}
            return  # Success
        time.sleep(2)

    pytest.fail(f"The /health endpoint did not return OK within {timeout} seconds.")