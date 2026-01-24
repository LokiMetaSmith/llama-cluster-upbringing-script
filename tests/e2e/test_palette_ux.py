import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import os
import sys

# Define PYTHONPATH to include root and subdirectories as per instructions
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
# Use existing PYTHONPATH if set, append new paths
existing_pythonpath = os.environ.get("PYTHONPATH", "")
PYTHONPATH = f"{existing_pythonpath}:{REPO_ROOT}:{os.path.join(REPO_ROOT, 'pipecatapp')}:{os.path.join(REPO_ROOT, 'pipecatapp/tools')}:{os.path.join(REPO_ROOT, 'pipecatapp/workflow')}"

@pytest.fixture(scope="module")
def web_server():
    """Starts the web server for the duration of the test module."""
    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH

    # Start the server
    # We ignore the requirement for TwinService/Consul/Nomad for this UI test
    # as we only care about static file serving and JS logic.
    process = subprocess.Popen(
        [sys.executable, "-m", "pipecatapp.web_server"],
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    # We can try to poll the health endpoint or just sleep
    time.sleep(5)

    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print(f"Server failed to start:\nSTDOUT: {stdout.decode()}\nSTDERR: {stderr.decode()}")
        pytest.fail("Server failed to start")

    yield "http://localhost:8000"

    # Teardown
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

def test_save_load_buttons_state(page: Page, web_server):
    """
    Tests that Save/Load buttons are disabled when the input is empty
    and enabled when input is provided.
    """
    try:
        page.goto(web_server)
    except Exception as e:
         pytest.fail(f"Failed to navigate to {web_server}: {e}")

    save_input = page.locator("#save-name-input")
    save_btn = page.locator("#save-state-btn")
    load_btn = page.locator("#load-state-btn")

    # Initial state: Input is empty, buttons should be disabled
    expect(save_input).to_be_empty()
    expect(save_btn).to_be_disabled()
    expect(load_btn).to_be_disabled()

    # Type something
    save_input.fill("my_save")

    # Buttons should be enabled
    expect(save_btn).to_be_enabled()
    expect(load_btn).to_be_enabled()

    # Clear input
    save_input.fill("")

    # Buttons should be disabled again
    expect(save_btn).to_be_disabled()
    expect(load_btn).to_be_disabled()

    # Type whitespace
    save_input.fill("   ")

    # Buttons should be disabled (trim check)
    expect(save_btn).to_be_disabled()
    expect(load_btn).to_be_disabled()
