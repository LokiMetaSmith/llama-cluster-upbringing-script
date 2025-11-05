import asyncio
import websockets
import json
import os
import sys

async def main():
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

    server = await websockets.serve(mock_server_handler, "localhost", 8000)

    test_message = "Hello, agent!"
    script_path = os.path.join(os.path.dirname(__file__), 'gemini_cli.py')

    process = await asyncio.create_subprocess_exec(
        sys.executable, script_path, test_message,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    server.close()
    await server.wait_closed()

    assert process.returncode == 0, f"CLI exited with code {process.returncode}"
    assert f"Sent: {test_message}" in stdout.decode(), "CLI output did not contain the sent message"
    assert received_message is not None, "Server did not receive a message"

    expected_message = json.dumps({"type": "user_message", "data": test_message})
    assert received_message == expected_message, f"Server received '{received_message}', expected '{expected_message}'"

    print("Test passed!")

if __name__ == "__main__":
    asyncio.run(main())
