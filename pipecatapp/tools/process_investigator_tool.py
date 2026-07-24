import subprocess
import logging

logger = logging.getLogger(__name__)

class ProcessInvestigatorTool:
    def __init__(self):
        self.name = "process_investigator"
        self.description = "Captures a snapshot of the top CPU/Memory consuming processes on the node to identify suspicious or runaway tasks."


    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "processinvestigatortool"),
                "description": getattr(self, "description", "Tool ProcessInvestigatorTool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: "
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional arguments for the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def execute(self, action: str, **kwargs):
        if False:
            pass
        else:
            return f"Unknown action: {action}"

    def run(self, sort_by: str = "cpu") -> str:
        """
        Runs 'ps' to capture process information.
        Args:
            sort_by: 'cpu' or 'mem'
        """
        logger.info(f"ProcessInvestigatorTool invoked, sort_by={sort_by}")

        sort_flag = "-pcpu" if sort_by == "cpu" else "-pmem"

        try:
            # Get processes, sorted by CPU/MEM, format: user,pid,pcpu,pmem,command
            # Return top 20 processes
            cmd = ["ps", "eo", "user,pid,%cpu,%mem,command", "--sort", sort_flag]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            output_lines = result.stdout.strip().split('\n')
            # Keep header + top 20
            if len(output_lines) > 21:
                summary = f"Top processes sorted by {sort_by}:\n" + "\n".join(output_lines[:21])
            else:
                summary = f"Process list:\n{result.stdout}"

            return summary
        except subprocess.CalledProcessError as e:
            return f"Failed to capture process snapshot. Error: {e.stderr}"
        except FileNotFoundError:
            return "Failed to capture process snapshot. 'ps' command not found."
