import logging
import subprocess
import os

logger = logging.getLogger(__name__)

class ScaleComputeTool:
    """
    A tool for dynamically adding more compute power to the local cluster by offloading inference to other machines.
    """
    def __init__(self):
        self.name = "scale_compute"
        self.description = "Use this to add more GPU power if inference is slow or context is full. Runs bootstrap.sh to add a worker node. Arguments: node_ip (string)"

    def scale(self, node_ip: str) -> str:
        """
        Runs the cluster upbrining script to add a worker node to the cluster.

        Args:
            node_ip (str): The IP address of the controller node.

        Returns:
            str: Result message indicating success or failure.
        """
        try:
            # We assume bootstrap.sh is in the root directory relative to the current working directory of the process
            script_path = os.path.join(os.getcwd(), "bootstrap.sh")
            if not os.path.exists(script_path):
                # Try finding it relative to this file's directory (assuming pipecatapp/tools/...)
                script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "bootstrap.sh")

            if not os.path.exists(script_path):
                 return f"Error: Could not find bootstrap.sh script."

            # Construct the command
            # Based on user requirements, we want to run: bash bootstrap.sh --role worker --controller-ip <node_ip>
            command = ["bash", script_path, "--role", "worker", "--controller-ip", node_ip]

            # Execute the command
            result = subprocess.run(command, capture_output=True, text=True, check=False)

            if result.returncode == 0:
                logger.info(f"Successfully added node {node_ip} to the cluster.")
                return f"Success: Added node with IP {node_ip} to the cluster.\nOutput:\n{result.stdout}"
            else:
                error_msg = f"Failed to add node {node_ip}. Exit code: {result.returncode}\nError Output:\n{result.stderr}"
                logger.error(error_msg)
                return error_msg

        except Exception as e:
            error_msg = f"Error executing bootstrap.sh: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def execute(self, arguments: dict) -> str:
        """Executes the tool with the given arguments."""
        node_ip = arguments.get("node_ip")

        if not node_ip:
            return "Error: node_ip is required."

        return self.scale(node_ip)
