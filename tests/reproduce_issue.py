
import logging
import json
import asyncio
import sys
import os

# Add pipecatapp to sys.path
sys.path.append(os.path.abspath("pipecatapp"))

import web_server
from pipecatapp.app import WebSocketLogHandler

# Mock WebSocket
class MockWebSocket:
    def __init__(self):
        self.sent_messages = []

    async def send_text(self, text: str):
        self.sent_messages.append(text)

    async def accept(self):
        pass

    async def receive_text(self):
        await asyncio.sleep(1)
        return ""

async def test_log_broadcasting():
    # Setup
    mock_ws = MockWebSocket()
    await web_server.manager.connect(mock_ws)

    handler = WebSocketLogHandler()
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Act
    secret = "sk-12345678901234567890secret" # Long enough to match {20,}
    short_fake = "sk-short" # Should NOT be redacted (false positive check)
    false_positive_word = "task" # Should NOT be redacted

    logger.info(f"Loaded API key: {secret}")
    logger.info(f"Short key: {short_fake}")
    logger.info(f"Running {false_positive_word}")
    logger.info("Bearer abcdef12345token")

    # Allow asyncio loop to process the broadcast task
    await asyncio.sleep(0.5)

    # Assert
    found_secret = False
    redaction_confirmed = False
    short_redacted = False
    task_redacted = False
    bearer_redacted = False

    print(f"Total messages received: {len(mock_ws.sent_messages)}")

    for msg in mock_ws.sent_messages:
        data = json.loads(msg)
        if data["type"] == "log":
            log_text = data["data"]
            print(f"Received log: {log_text}")

            if secret in log_text:
                found_secret = True

            if "sk-[REDACTED]" in log_text:
                redaction_confirmed = True

            if "sk-[REDACTED]" in log_text and "Short key" in log_text:
                short_redacted = True

            if "sk-[REDACTED]" in log_text and "Running" in log_text:
                task_redacted = True

            if "Bearer [REDACTED]" in log_text:
                bearer_redacted = True

    if found_secret:
        print("VULNERABILITY CONFIRMED: Secret found in WebSocket logs.")
        sys.exit(1)

    if not redaction_confirmed:
        print("FAILURE: Secret was NOT redacted.")
        sys.exit(1)

    if not bearer_redacted:
        print("FAILURE: Bearer token was NOT redacted.")
        sys.exit(1)

    if short_redacted:
        print("FAILURE: Short key (sk-short) was incorrectly redacted.")
        sys.exit(1)

    if task_redacted:
        print("FAILURE: Common word 'task' was incorrectly redacted.")
        sys.exit(1)

    print("SUCCESS: Secrets were redacted correctly and false positives avoided.")
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(test_log_broadcasting())
