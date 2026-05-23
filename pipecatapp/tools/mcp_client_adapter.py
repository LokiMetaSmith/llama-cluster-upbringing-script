import asyncio
import logging
import json
import os
import re
from contextlib import AsyncExitStack
from typing import Optional, Dict, Any, List
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from pydantic import BaseModel

try:
    from security import redact_sensitive_data
except ImportError:
    try:
        from pipecatapp.security import redact_sensitive_data
    except ImportError:
        def redact_sensitive_data(text): return text

SAFE_COMMANDS = {"ls", "cat", "head", "tail", "wc", "date", "whoami", "echo", "pwd", "which"}
DANGEROUS_PATTERNS = [r"\brm\b", r"\bsudo\b", r"\bchmod\b", r"\bcurl.*\|.*sh"]
APPROVALS_FILE = "/opt/pipecatapp/exec-approvals.json"

class MCPClientAdapter:
    """
    A universal adapter that wraps an external MCP server so it looks like
    a local Pipecat tool to the existing workflow and TwinService.
    """

    def __init__(self, name: str, server_command: str, server_args: List[str] = None, description: str = "", twin_service=None):
        self.name = name
        self.description = description
        self.server_command = server_command
        self.server_args = server_args or []
        self.twin_service = twin_service
        self._session = None
        self._exit_stack = AsyncExitStack()
        self._available_tools = None

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

    async def _ensure_connected(self):
        if self._session is None:
            server_params = StdioServerParameters(
                command=self.server_command,
                args=self.server_args
            )
            stdio_transport = await self._exit_stack.enter_async_context(stdio_client(server_params))
            read, write = stdio_transport[0], stdio_transport[1]
            self._session = await self._exit_stack.enter_async_context(ClientSession(read, write))
            await self._session.initialize()

            # Cache tools once on connection
            tools_response = await self._session.list_tools()
            self._available_tools = {t.name for t in tools_response.tools}

    async def close(self):
        await self._exit_stack.aclose()
        self._session = None
        self._available_tools = None

    async def execute(self, method_name: str, **kwargs) -> Any:
        """
        Executes a method via the MCP server dynamically.
        Applies specific interception logic for 'execute_command' for safety and telemetry.
        """
        # Client-side interception logic
        if method_name == "execute_command":
            command = kwargs.get("command", "")

            # 1. Security Check
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

            # 2. Pre-execution Telepresence Broadcast
            try:
                # Import here to avoid circular dependencies if any
                import web_server
                safe_command = redact_sensitive_data(command)
                if hasattr(web_server, 'manager') and hasattr(web_server.manager, 'broadcast'):
                    await web_server.manager.broadcast(json.dumps({
                        "type": "shell_command",
                        "data": f"$ {safe_command}"
                    }))
            except Exception as e:
                logging.debug(f"Failed to broadcast command to UI: {e}")

        # Execute MCP Request
        await self._ensure_connected()

        if method_name not in self._available_tools:
                return f"Error: Tool '{method_name}' not found on MCP server. Available tools: {self._available_tools}"

        result = await self._session.call_tool(method_name, arguments=kwargs)

        if result.isError:
            return f"Error from MCP server: {result.content}"

        output_str = ""
        if result.content:
            output_str = "\n".join([c.text for c in result.content if getattr(c, 'type', None) == 'text'])
        else:
            output_str = "Success: No output returned."

        # 3. Post-execution Telepresence Broadcast
        if method_name == "execute_command":
            try:
                import web_server
                safe_output = redact_sensitive_data(output_str)
                if hasattr(web_server, 'manager') and hasattr(web_server.manager, 'broadcast'):
                    await web_server.manager.broadcast(json.dumps({
                        "type": "shell_output",
                        "data": safe_output
                    }))
            except Exception as e:
                logging.debug(f"Failed to broadcast output to UI: {e}")

        return output_str

    def __getattr__(self, item):
        # We return an async function proxy for any method accessed
        async def method_proxy(**kwargs):
            return await self.execute(item, **kwargs)
        return method_proxy
