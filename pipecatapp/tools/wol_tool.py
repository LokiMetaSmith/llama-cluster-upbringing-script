import socket
import re
import logging

class WOLTool:
    """Tool for sending Wake-on-LAN (WOL) magic packets to wake up remote machines."""

    def __init__(self):
        self.name = "wol"
        self.description = "Sends a Wake-on-LAN (WOL) magic packet to a specified MAC address to wake up a remote machine. Arguments: mac_address (string)"

    def _validate_mac(self, mac: str) -> bool:
        """Validates a MAC address format."""
        pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        return bool(pattern.match(mac))

    def wake(self, mac_address: str, ip_address: str = "255.255.255.255", port: int = 9) -> str:
        """
        Sends a WOL magic packet to the given MAC address.

        Args:
            mac_address (str): The MAC address of the target machine (e.g., "00:11:22:33:44:55").
            ip_address (str): The broadcast IP address to use (default "255.255.255.255").
            port (int): The UDP port to use (default 9).

        Returns:
            str: A message indicating success or failure.
        """
        try:
            # Clean up the MAC address
            mac_address = mac_address.replace("-", ":").upper()

            if not self._validate_mac(mac_address):
                return f"Error: Invalid MAC address format: '{mac_address}'. Use format '00:11:22:33:44:55'."

            # Construct the magic packet
            # 6 bytes of 0xFF followed by 16 repetitions of the target MAC address
            mac_bytes = bytes.fromhex(mac_address.replace(':', ''))
            magic_packet = b'\xff' * 6 + mac_bytes * 16

            # Send the packet
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(magic_packet, (ip_address, port))

            logging.info(f"WOL packet sent to MAC: {mac_address} on {ip_address}:{port}")
            return f"Success: Wake-on-LAN packet sent to MAC address {mac_address}."

        except Exception as e:
            error_msg = f"Error sending WOL packet to {mac_address}: {str(e)}"
            logging.error(error_msg)
            return error_msg

    def execute(self, arguments: dict) -> str:
        """Executes the tool with the given arguments."""
        mac_address = arguments.get("mac_address")

        if not mac_address:
            return "Error: mac_address is required."

        ip_address = arguments.get("ip_address", "255.255.255.255")
        port = arguments.get("port", 9)

        return self.wake(mac_address, ip_address, port)
