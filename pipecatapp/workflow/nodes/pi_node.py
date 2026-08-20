import json
import asyncio
import os
import shutil
import subprocess
from ..node import Node
from ..context import WorkflowContext
from .registry import registry

@registry.register
class PiAgentNode(Node):
    """
    A workflow node that delegates execution to the Pi agent CLI (@earendil-works/pi-coding-agent).
    It expects a prompt input and passes it to the `pi -p` command for JSON/print output mode.
    """
    async def execute(self, context: WorkflowContext):
        try:
            prompt = self.get_input(context, "prompt")
        except ValueError:
            prompt = None

        if not prompt:
            self.set_output(context, "result", "Error: 'prompt' input is required for PiAgentNode.")
            return

        # Check if pi is installed globally via npm or in PATH
        pi_executable = shutil.which("pi")
        if not pi_executable:
            self.set_output(context, "result", "Error: 'pi' executable not found. Ensure @earendil-works/pi-coding-agent is installed.")
            return

        timeout = self.config.get("timeout", 120)

        # Build the command: pi -p "prompt"
        # -p is for print/JSON mode, skipping the interactive TUI
        command = [pi_executable, "-p", prompt]

        try:
            # We run this in a thread executor to not block the async event loop
            loop = asyncio.get_running_loop()

            def run_subprocess():
                return subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=timeout,
                    env=os.environ.copy()
                )

            process = await loop.run_in_executor(None, run_subprocess)

            if process.returncode == 0:
                self.set_output(context, "result", process.stdout.strip())
            else:
                error_msg = f"Pi agent failed (code {process.returncode}):\nSTDOUT: {process.stdout}\nSTDERR: {process.stderr}"
                self.set_output(context, "result", error_msg)

        except subprocess.TimeoutExpired:
            self.set_output(context, "result", f"Error: Pi execution timed out after {timeout} seconds.")
        except Exception as e:
            self.set_output(context, "result", f"Error executing PiAgentNode: {e}")
