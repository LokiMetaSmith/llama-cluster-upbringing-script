import subprocess
import os
import shlex
from dotenv import load_dotenv

class LLxprt_Code_Tool:
    """A tool for running llxprt-code commands.

    This class provides a method to execute `llxprt` commands from
    within the agent's environment.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self):
        """Initializes the LLxprt_Code_Tool."""
        self.description = "Run a llxprt-code command."
        self.name = "llxprt_code_tool"

    def run(self, command: str) -> str:
        """Runs a llxprt-code command.

        Args:
            command (str): The command to run.

        Returns:
            str: A string containing the output of the command, or an
                error message if the run fails or times out.
        """
        if not command:
            return "Error: command cannot be empty."

        try:
            load_dotenv("/opt/llxprt-code/.env")
            command_parts = ["llxprt"] + shlex.split(command)
            process = subprocess.run(
                command_parts,
                capture_output=True,
                text=True,
                timeout=300
            )

            if process.returncode == 0:
                return f"llxprt-code command run completed successfully.\nOutput:\n{process.stdout}"
            else:
                return f"llxprt-code command run failed with return code {process.returncode}.\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"

        except subprocess.TimeoutExpired as e:
            return f"Error: llxprt-code command run timed out after 5 minutes.\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        except FileNotFoundError:
            return "Error: `llxprt` command not found. Is it installed and in the system's PATH?"
        except Exception as e:
            return f"An unexpected error occurred while trying to run llxprt-code: {e}"
