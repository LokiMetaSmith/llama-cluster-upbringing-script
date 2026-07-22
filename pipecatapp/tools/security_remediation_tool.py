import subprocess
import logging

logger = logging.getLogger(__name__)

class SecurityRemediationTool:
    def __init__(self):
        self.name = "security_remediation"
        self.description = "Takes restricted, safe remediation actions against security threats (e.g. stopping a Nomad allocation or cordoning a node)."

    def run(self, action: str, target: str) -> str:
        """
        Runs a predefined security action.
        Allowed actions:
        - stop_allocation: Stops a specific Nomad allocation. `target` should be the allocation ID.
        """
        logger.info(f"SecurityRemediationTool invoked: action={action}, target={target}")

        if action == "stop_allocation":
            # Very basic validation of the allocation ID format (alphanumeric/hyphen)
            if not target.replace("-", "").isalnum():
                return f"Error: Invalid allocation ID format: {target}"

            try:
                # Use nomad stop. Note: this requires the agent running it has nomad CLI and connectivity
                result = subprocess.run(["nomad", "alloc", "stop", target],
                                      capture_output=True, text=True, check=True)
                return f"Successfully stopped allocation {target}. Output: {result.stdout}"
            except subprocess.CalledProcessError as e:
                return f"Failed to stop allocation {target}. Error: {e.stderr}"
        else:
            return f"Error: Unsupported action '{action}'. Only 'stop_allocation' is currently permitted."
