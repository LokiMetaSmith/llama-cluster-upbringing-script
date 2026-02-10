import asyncio
import subprocess
import uuid
import logging
import json

try:
    from ..security import redact_sensitive_data
except ImportError:
    from security import redact_sensitive_data

class ShellTool:
    """A tool for running shell commands in a persistent tmux session.

    This allows the agent to maintain state (directories, environment variables, background processes)
    across multiple tool calls, unlike single-shot subprocess executions.
    """

    def __init__(self, session_name="agent_session"):
        self.session_name = session_name
        self.name = "shell"

    async def _ensure_session(self):
        """Ensures the tmux session exists."""
        check = await asyncio.create_subprocess_exec(
            "tmux", "has-session", "-t", self.session_name,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        await check.wait()
        if check.returncode != 0:
            logging.info(f"Creating new tmux session: {self.session_name}")
            create = await asyncio.create_subprocess_exec(
                "tmux", "new-session", "-d", "-s", self.session_name,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            await create.wait()

    async def execute_command(self, command: str, timeout: int = 30) -> str:
        """
        Executes a shell command in the persistent tmux session and returns the session output.

        Args:
            command (str): The command to execute.
            timeout (int): Max time to wait for the command to finish (in seconds). Default 30.

        Returns:
            str: The content of the tmux pane (last 200 lines) after execution.
        """
        await self._ensure_session()

        sentinel = f"END_{uuid.uuid4().hex}"
        # Combine command with sentinel echo. We use '|| true' to ensure sentinel prints even if command fails.
        full_command = f"{command}; echo '{sentinel}'"

        logging.info(f"Sending command to tmux session {self.session_name}: {command}")

        # Telepresence: Broadcast command to UI
        try:
            import web_server
            # Security: Redact sensitive data before broadcasting to UI
            safe_command = redact_sensitive_data(command)
            await web_server.manager.broadcast(json.dumps({
                "type": "shell_command",
                "data": f"$ {safe_command}"
            }))
        except Exception:
            pass

        # Send keys
        send = await asyncio.create_subprocess_exec(
            "tmux", "send-keys", "-t", self.session_name, full_command, "C-m"
        )
        await send.wait()

        # Poll for sentinel
        start_time = asyncio.get_event_loop().time()
        while (asyncio.get_event_loop().time() - start_time) < timeout:
            capture = await asyncio.create_subprocess_exec(
                "tmux", "capture-pane", "-t", self.session_name, "-p", "-S", "-200",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, _ = await capture.communicate()
            output = stdout.decode('utf-8', errors='replace')

            if sentinel in output:
                # Determine success/failure could be hard from just text,
                # but the agent can read the output.
                # We return the output up to the sentinel to keep it clean-ish?
                # Or just return the whole buffer. The agent is smart.
                # Let's strip the sentinel line to be nice.
                clean_output = output.replace(f"echo '{sentinel}'", "").replace(sentinel, "").strip()

                # Telepresence: Broadcast output to UI
                try:
                    import web_server
                    # Security: Redact sensitive data before broadcasting to UI
                    safe_output = redact_sensitive_data(clean_output)
                    await web_server.manager.broadcast(json.dumps({
                        "type": "shell_output",
                        "data": safe_output
                    }))
                except Exception:
                    pass

                return clean_output

            await asyncio.sleep(0.5)

        return f"Command timed out after {timeout} seconds. Output so far:\n{output}"
