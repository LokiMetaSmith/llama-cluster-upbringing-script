import asyncio
import logging

class DiracTool:
    """A tool for running Dirac CLI commands.

    Dirac is a token-saving coding agent that supports hash-anchored edits
    and multi-file batching.
    """
    def __init__(self, root_dir="/opt/pipecatapp"):
        self.name = "dirac"
        self.root_dir = root_dir
        self.logger = logging.getLogger(__name__)

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Executes a prompt using the Dirac CLI for complex coding tasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The coding task instruction to execute via Dirac."
                        },
                        "mode": {
                            "type": "string",
                            "description": "Optional run mode. Provide '-y' for auto-approval without user prompt.",
                            "default": "-y"
                        }
                    },
                    "required": ["prompt"]
                }
            }
        }

    async def execute(self, prompt: str, mode: str = "-y", **kwargs) -> str:
        """Executes the Dirac command with the given prompt."""
        try:
            self.logger.info(f"Executing Dirac command: dirac {mode} <prompt> in {self.root_dir}")

            process = await asyncio.create_subprocess_exec(
                "dirac",
                mode,
                prompt,
                cwd=self.root_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            stdout_str = stdout.decode('utf-8') if stdout else ""
            stderr_str = stderr.decode('utf-8') if stderr else ""

            result = f"Exit Code: {process.returncode}\n"
            if stdout_str:
                result += f"STDOUT:\n{stdout_str}\n"
            if stderr_str:
                result += f"STDERR:\n{stderr_str}\n"

            if process.returncode == 0:
                self.logger.info("Dirac execution successful.")
            else:
                self.logger.warning(f"Dirac execution failed with code {process.returncode}.")

            return result

        except Exception as e:
            error_msg = f"Failed to execute Dirac command: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
