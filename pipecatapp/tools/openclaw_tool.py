import logging
from integrations.openclaw import OpenClawClient
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

class OpenClawTool:
    """
    A tool for interacting with the OpenClaw Gateway to send messages via WhatsApp, Telegram, Discord, etc.
    """
    def __init__(self, gateway_url: str):
        self.client = OpenClawClient(gateway_url)
        self.description = "Send messages via OpenClaw Gateway to various channels (WhatsApp, Telegram, etc.)."
        self.name = "openclaw"

    async def send_message(self, target: str, message: str, channel: Optional[str] = None) -> str:
        """
        Sends a message to a target via OpenClaw.

        Args:
            target (str): The target recipient (e.g., phone number, username, channel ID).
            message (str): The text message to send.
            channel (str, optional): The specific channel provider to use (e.g., 'whatsapp', 'telegram').
                                     If omitted, OpenClaw attempts to route based on target.

        Returns:
            str: Result message indicating success or failure.
        """
        try:
            # We connect lazily or reconnect if disconnected
            await self.client.connect()

            # Send message
            response = await self.client.send_message(target, message, channel)

            # If response has a payload with result, format it
            if response.get("ok"):
                payload = response.get("payload", {})
                # payload might be the message object or just success
                return f"Message sent successfully."
            else:
                return f"Failed to send message. Error: {response.get('error') or response}"

        except Exception as e:
            logger.error(f"Error in OpenClawTool: {e}")
            return f"Error sending message: {str(e)}"
