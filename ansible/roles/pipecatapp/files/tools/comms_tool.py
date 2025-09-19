import logging

class CommsTool:
    """A tool for broadcasting messages over the ship-wide intercom."""

    def broadcast_message(self, message: str) -> str:
        """
        Broadcasts a message to all intruders in the installation.
        :param message: The message to broadcast.
        """
        logging.info(f"COMMS: Broadcasting message: '{message}'")
        return f"Message broadcasted: '{message}'"
