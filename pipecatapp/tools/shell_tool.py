import asyncio
import subprocess
import uuid
import logging
import json
import os
import re

try:
    from ..security import redact_sensitive_data
except ImportError:
    from security import redact_sensitive_data

SAFE_COMMANDS = {"ls", "cat", "head", "tail", "wc", "date", "whoami", "echo", "pwd", "which"}
DANGEROUS_PATTERNS = [r"\brm\b", r"\bsudo\b", r"\bchmod\b", r"\bcurl.*\|.*sh"]
APPROVALS_FILE = "/opt/pipecatapp/exec-approvals.json"

class ShellTool:
    """A tool for running shell commands in a persistent tmux session.

    This allows the agent to maintain state (directories, environment variables, background processes)
    across multiple tool calls, unlike single-shot subprocess executions.
    """

    def __init__(self, session_name="agent_session", twin_service=None):
        self.session_name = session_name
        self.name = "shell"
        self.twin_service = twin_service
        self.description = "A tool for running shell commands in a persistent tmux session."

    def load_approvals(self):
        if os.path.exists(APPROVALS_FILE):
            try:
                with open(APPROVALS_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Error loading approvals file: {e}")
        return {"allowed": [], "denied": []}

    def save_approval(self, command, approved):
        approvals = self.load_approvals()
        key = "allowed" if approved else "denied"
        if command not in approvals[key]:
            approvals[key].append(command)

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(APPROVALS_FILE), exist_ok=True)
            with open(APPROVALS_FILE, "w") as f:
                json.dump(approvals, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving approval: {e}")

    def check_command_safety(self, command):
        base_cmd = command.strip().split()[0] if command.strip() else ""
        if base_cmd in SAFE_COMMANDS:
            return "safe"

        approvals = self.load_approvals()
        if command in approvals["allowed"]:
            return "approved"
        if command in approvals["denied"]:
            return "denied"

        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, command):
                return "needs_approval"

        return "needs_approval"

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
        safety = self.check_command_safety(command)
        if safety == "denied":
            return "Permission denied by previous user choice."
        elif safety == "needs_approval":
            if self.twin_service and getattr(self.twin_service, "approval_mode", False):
                logging.info(f"Command '{command}' requires approval.")
                is_approved = await self.twin_service._request_approval({
                    "name": self.name,
                    "arguments": {"command": command}
                })
                if not is_approved:
                    self.save_approval(command, False)
                    return "Permission denied by user."
                else:
                    self.save_approval(command, True)
            else:
                return "Permission denied. Command requires approval and approval mode is off or TwinService is not attached."

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
