import subprocess
import logging

logger = logging.getLogger(__name__)

class NetworkInvestigatorTool:
    def __init__(self):
        self.name = "network_investigator"
        self.description = "Temporarily captures a brief snapshot of active network connections (using netstat/ss) on the current node to investigate suspicious traffic."

    def run(self, duration_seconds: int = 5) -> str:
        """
        Runs a quick network snapshot to identify active connections and listening ports.
        Args:
            duration_seconds: How long to wait/sample (unused for netstat, but kept for future tcpdump expansion).
        """
        logger.info("NetworkInvestigatorTool invoked")

        try:
            # Using 'ss' (socket statistics) which is modern, fast, and pre-installed on Debian
            # -t (TCP), -u (UDP), -p (processes), -n (numeric, no DNS resolution to save time), -a (all sockets)
            result = subprocess.run(["ss", "-tupna"], capture_output=True, text=True, check=True)

            # Truncate output if it's too massive for the LLM context window
            output_lines = result.stdout.strip().split('\n')
            if len(output_lines) > 50:
                summary = f"Captured {len(output_lines)} active connections. Showing top 50:\n" + "\n".join(output_lines[:50])
            else:
                summary = f"Active connections:\n{result.stdout}"

            return summary
        except subprocess.CalledProcessError as e:
            return f"Failed to capture network snapshot. Error: {e.stderr}"
        except FileNotFoundError:
            return "Failed to capture network snapshot. 'ss' command not found."
