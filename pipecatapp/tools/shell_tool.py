import asyncio
import subprocess
import uuid
import logging
from pipecatapp.utils.terminal_cleanup import clean_terminal_output

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
                result = output.replace(f"echo '{sentinel}'", "").replace(sentinel, "").strip()

                # EAGAIN Handling for ripgrep
                if ("os error 11" in result.lower() or "resource temporarily unavailable" in result.lower()) and \
                   (command.strip().startswith("rg ") or command.strip().startswith("ripgrep ")):

                    logging.warning("EAGAIN encountered during ripgrep in shell_tool. Retrying with -j 1...")

                    # Ensure -j 1 is added
                    if "-j 1" not in command and "-j1" not in command:
                        retry_command = command.replace("rg ", "rg -j 1 ", 1).replace("ripgrep ", "ripgrep -j 1 ", 1)
                        return await self.execute_command(retry_command, timeout)


                try:
                    import web_server
                    import json
                    # Redact output if security module is present
                    redacted_output = result
                    try:
                        from pipecatapp.security import redact_sensitive_data_stream
                        import inspect
                        res = redact_sensitive_data_stream(result)
                        if inspect.isasyncgen(res):
                            # It's an async generator, we need to collect it
                            async def collect_gen(gen):
                                parts = []
                                async for part in gen:
                                    parts.append(part)
                                return "".join(parts)
                            redacted_output = str(await collect_gen(res))
                        else:
                            redacted_output = str(res)
                    except ImportError:
                        pass
                    except Exception:
                        pass

                    asyncio.create_task(web_server.manager.broadcast(json.dumps({
                        "type": "shell_output",
                        "data": redacted_output
                    })))
                except ImportError:
                    pass

                return result




            await asyncio.sleep(0.5)

        return f"Command timed out after {timeout} seconds. Output so far:\n{output}"
