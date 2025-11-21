import pytest
import asyncio
import websockets
import json
import os
import sys

# Calculate path to gemini_cli.py
TOOL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools'))
SCRIPT_PATH = os.path.join(TOOL_DIR, 'gemini_cli.py')

@pytest.mark.asyncio
async def test_gemini_cli_interaction():
    """Runs the test with a mock server and the CLI as a subprocess."""
    received_message = None

    async def mock_server_handler(websocket, path=None):
        """The mock server logic to handle a single connection."""
        nonlocal received_message
        try:
            message = await websocket.recv()
            received_message = message
            await websocket.send("OK")
        except websockets.exceptions.ConnectionClosed:
            pass

    # Start the server on port 8000 because the script has it hardcoded
    try:
        async with websockets.serve(mock_server_handler, "localhost", 8000):
            test_message = "Hello, agent!"

            # Run the CLI script
            process = await asyncio.create_subprocess_exec(
                sys.executable, SCRIPT_PATH, test_message,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            assert process.returncode == 0, f"CLI exited with code {process.returncode}. Stderr: {stderr.decode()}"
            assert f"Sent: {test_message}" in stdout.decode(), "CLI output did not contain the sent message"
            assert received_message is not None, "Server did not receive a message"

            expected_message = json.dumps({"type": "user_message", "data": test_message})
            assert received_message == expected_message, f"Server received '{received_message}', expected '{expected_message}'"

    except OSError as e:
        if "Address already in use" in str(e):
            pytest.skip("Port 8000 is in use, skipping test")
        else:
            raise e
