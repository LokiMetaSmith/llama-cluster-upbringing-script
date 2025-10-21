import subprocess
import asyncio


class TermEverythingTool(object):
    """A tool for running GUI applications in the terminal.

    This tool uses the `term.everything` AppImage to execute commands that would
    typically require a graphical user interface, capturing their output from
    the terminal.

    Attributes:
        app_image_path (str): The path to the term.everything AppImage.
    """

    def __init__(self, app_image_path: str, **kwargs):
        """Initializes the TermEverythingTool.

        Args:
            app_image_path (str): The file path to the term.everything AppImage.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.app_image_path = app_image_path

    async def execute(self, command: str) -> str:
        """Executes a command using the term.everything AppImage.

        The provided command string is split into arguments and executed as a
        subprocess.

        Args:
            command (str): The command to execute.

        Returns:
            str: The standard output of the command on success, or an error
                 message on failure.
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