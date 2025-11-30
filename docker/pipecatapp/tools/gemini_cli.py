import asyncio
import websockets
import json
import argparse
import sys

async def send_message(message):
    """Connects to the WebSocket server and sends a user message."""
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            # The message format should match what the server expects
            await websocket.send(json.dumps({"type": "user_message", "data": message}))
            print(f"Sent: {message}")
    except Exception as e:
        print(f"Error connecting to WebSocket: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a message to the Pipecat agent.")
    parser.add_argument("message", type=str, help="The message to send.")
    args = parser.parse_args()

    asyncio.run(send_message(args.message))
