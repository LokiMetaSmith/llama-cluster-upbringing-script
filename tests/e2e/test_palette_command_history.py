import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import os
import sys

# Define PYTHONPATH to include root and subdirectories
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
existing_pythonpath = os.environ.get("PYTHONPATH", "")
PYTHONPATH = f"{existing_pythonpath}:{REPO_ROOT}:{os.path.join(REPO_ROOT, 'pipecatapp')}:{os.path.join(REPO_ROOT, 'pipecatapp/tools')}:{os.path.join(REPO_ROOT, 'pipecatapp/workflow')}"

@pytest.fixture(scope="module")
def web_server():
    """Starts the web server for the duration of the test module."""
    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH

    # Start the server
    process = subprocess.Popen(
        [sys.executable, "-m", "pipecatapp.web_server"],
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
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

def test_command_history(page: Page, web_server):
    """
    Tests the command history feature in the terminal.
    """
    try:
        page.goto(web_server)
    except Exception as e:
         pytest.fail(f"Failed to navigate to {web_server}: {e}")

    message_input = page.locator("#message-input")
    send_btn = page.locator("#send-btn")

    # Type and send first command
    message_input.fill("command1")
    send_btn.click()

    # Wait for input to clear (which happens in sendMessage)
    expect(message_input).to_be_empty()

    # Type and send second command
    message_input.fill("command2")
    send_btn.click()
    expect(message_input).to_be_empty()

    # Test Arrow Up (History)
    message_input.press("ArrowUp")
    expect(message_input).to_have_value("command2")

    message_input.press("ArrowUp")
    expect(message_input).to_have_value("command1")

    # Test Arrow Down
    message_input.press("ArrowDown")
    expect(message_input).to_have_value("command2")

    # Test Arrow Down (Back to empty/temp)
    message_input.press("ArrowDown")
    expect(message_input).to_be_empty()

    # Test Temp Input Preservation
    message_input.fill("temp_command")
    message_input.press("ArrowUp") # Go to history (command2)
    expect(message_input).to_have_value("command2")

    message_input.press("ArrowDown") # Go back
    expect(message_input).to_have_value("temp_command")
