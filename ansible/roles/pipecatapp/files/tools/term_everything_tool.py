import subprocess
import asyncio


class TermEverythingTool(object):
    """
    A tool for running GUI applications in the terminal using term.everything.
    """

    def __init__(self, app_image_path: str, **kwargs):
        super().__init__(**kwargs)
        self.app_image_path = app_image_path

    async def execute(self, command: str) -> str:
        """
        Executes the term.everything AppImage with the given command.
        The command string is split into arguments.
        """
        command_parts = command.split()
        try:
            process = await asyncio.create_subprocess_exec(
                self.app_image_path,
                *command_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                return f"Error: {stderr.decode().strip()}"
            return stdout.decode().strip()
        except Exception as e:
            return f"Error: {e}"