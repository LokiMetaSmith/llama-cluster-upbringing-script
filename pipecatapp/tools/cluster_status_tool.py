import logging
import subprocess
import os

logger = logging.getLogger(__name__)

class ClusterStatusTool:
    """
    A tool for querying the real-time status of the local compute cluster.
    """
    def __init__(self):
        self.name = "cluster_status"
        self.description = "Queries the live status of the local compute cluster (Consul/Nomad nodes and roles) to gain state awareness of hardware limitations. Takes no arguments."

    def get_status(self) -> str:
        """
        Runs the cluster_status playbook to query cluster nodes.
        Returns:
            str: Result message containing the cluster status output or an error.
        """
        try:
            # We assume playbooks/cluster_status.yaml is available
            # Find the path to the playbooks directory
            playbook_path = os.path.join(os.getcwd(), "playbooks", "cluster_status.yaml")

            if not os.path.exists(playbook_path):
                 playbook_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "playbooks", "cluster_status.yaml")

            if not os.path.exists(playbook_path):
                 return f"Error: Could not find playbooks/cluster_status.yaml."

            # Command to run the playbook
            command = ["ansible-playbook", playbook_path]

            result = subprocess.run(command, capture_output=True, text=True, check=False)

            if result.returncode == 0:
                # Ansible's default output might be noisy.
                # We can return the raw stdout, but it contains "TASK [Display Cluster Status]" which has the nice dict.
                # Returning the full stdout is usually fine for the LLM to parse.
                return f"Success: Cluster status retrieved.\n{result.stdout}"
            else:
                error_msg = f"Failed to retrieve cluster status. Exit code: {result.returncode}\nError Output:\n{result.stderr}"
                logger.error(error_msg)
                return error_msg

        except Exception as e:
            error_msg = f"Error executing cluster_status playbook: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def execute(self, arguments: dict = None) -> str:
        """Executes the tool with the given arguments."""
        # This tool requires no arguments
        return self.get_status()
