from mcp.server.fastmcp import FastMCP
import asyncio
import subprocess
import uuid
import logging
import os
from pipecatapp.utils.terminal_cleanup import clean_terminal_output

mcp = FastMCP("shell_server")

async def _ensure_session(session_name):
    """Ensures the tmux session exists."""
    check = await asyncio.create_subprocess_exec(
        "tmux", "has-session", "-t", session_name,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    await check.wait()
    if check.returncode != 0:
        logging.info(f"Creating new tmux session: {session_name}")
        create = await asyncio.create_subprocess_exec(
            "tmux", "new-session", "-d", "-s", session_name,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        await create.wait()

@mcp.tool()
async def execute_command(command: str, timeout: int = 30) -> str:
    """
    Executes a shell command in the persistent tmux session and returns the session output.

    Args:
        command (str): The command to execute.
        timeout (int): Max time to wait for the command to finish (in seconds). Default 30.

    Returns:
        str: The content of the tmux pane (last 200 lines) after execution.
    """
    session_name = "agent_session"

    await _ensure_session(session_name)

    sentinel = f"END_{uuid.uuid4().hex}"

    if "rg " in command or "ripgrep " in command:
        rg_fallback = (
            f"tmp_err=$(mktemp); "
            f"({command}) 2> $tmp_err; "
            f"if grep -qi 'os error 11\\|resource temporarily unavailable' $tmp_err; then "
            f"  echo 'EAGAIN detected, retrying ripgrep with -j 1...'; "
            f"  {command} -j 1; "
            f"fi; "
            f"cat $tmp_err >&2; "
            f"rm -f $tmp_err"
        )
        command = rg_fallback

    full_command = f"{command}; echo '{sentinel}'"
    logging.info(f"Sending command to tmux session {session_name}: {command}")

    send = await asyncio.create_subprocess_exec(
        "tmux", "send-keys", "-t", session_name, full_command, "C-m"
    )
    await send.wait()

    start_time = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - start_time) < timeout:
        capture = await asyncio.create_subprocess_exec(
            "tmux", "capture-pane", "-t", session_name, "-p", "-S", "-200",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, _ = await capture.communicate()
        output = stdout.decode('utf-8', errors='replace')

        if sentinel in output:
            clean_output = output.replace(f"echo '{sentinel}'", "").replace(sentinel, "").strip()
            return clean_terminal_output(clean_output)

        await asyncio.sleep(0.5)

    return f"Command timed out after {timeout} seconds. Output so far:\n{output}"

if __name__ == "__main__":
    mcp.run()
