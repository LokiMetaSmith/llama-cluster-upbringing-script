import asyncio
import json
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# Add pipecatapp to path so we can import tools and security
# Assuming we are running from repo root
sys.path.append(os.getcwd())

# Mock web_server BEFORE importing ShellTool
mock_web_server = MagicMock()
mock_web_server.manager = MagicMock()
mock_web_server.manager.broadcast = AsyncMock()
sys.modules["web_server"] = mock_web_server

from pipecatapp.tools.shell_tool import ShellTool

class TestShellToolLeak(unittest.TestCase):
    async def run_test(self):
        tool = ShellTool()
        tool._ensure_session = AsyncMock()

        # Patch asyncio.create_subprocess_exec inside ShellTool
        # ShellTool.execute_command calls create_subprocess_exec for "tmux send-keys" and "tmux capture-pane"
        with patch("asyncio.create_subprocess_exec") as mock_exec:
            mock_process = AsyncMock()
            mock_process.wait = AsyncMock(return_value=None)

            # The sentinel is generated randomly inside execute_command.
            # We need to ensure we return it.
            # However, execute_command uses UUID.
            # So we simulate the process returning output that contains the UUID.
            # But we don't know the UUID yet.
            # Wait, execute_command constructs full_command = "cmd; echo 'END_UUID'".
            # Then it sends keys.
            # Then it loops capturing pane.
            # The capture needs to return the sentinel.

            # Since we can't easily guess the UUID generated inside the function,
            # we'll patch uuid.uuid4 to return a fixed value.
            with patch("uuid.uuid4") as mock_uuid:
                mock_uuid.return_value.hex = "FIXED_UUID"
                sentinel = "END_FIXED_UUID"

                secret_output = "Secret: sk-1234567890abcdef1234567890abcdef\n"
                full_output = f"{secret_output}echo '{sentinel}'\n{sentinel}\n"

                # We need to distinguish calls.
                # 1. "tmux send-keys" -> just returns (wait)
                # 2. "tmux capture-pane" -> returns output

                def side_effect(*args, **kwargs):
                    if args[0] == "tmux" and args[1] == "capture-pane":
                        # Simulate capture pane output
                        proc = AsyncMock()
                        proc.communicate = AsyncMock(return_value=(full_output.encode(), b""))
                        return proc
                    else:
                        # Other commands (send-keys, new-session)
                        proc = AsyncMock()
                        proc.wait = AsyncMock(return_value=None)
                        return proc

                mock_exec.side_effect = side_effect

                command = "echo $SECRET"
                output = await tool.execute_command(command)

                # Check what was broadcasted
                # web_server.manager.broadcast is called twice:
                # 1. Command broadcast
                # 2. Output broadcast

                # Assert command broadcast (unredacted command)
                # Note: The command "echo $SECRET" doesn't contain the secret itself,
                # but if command was "export S=sk-..." it would be redacted.
                # Let's verify output broadcast first.

                broadcast_calls = mock_web_server.manager.broadcast.call_args_list
                # We expect at least one call with "shell_output"
                output_broadcast = None
                for call in broadcast_calls:
                    args, _ = call
                    msg = json.loads(args[0])
                    if msg["type"] == "shell_output":
                        output_broadcast = msg["data"]

                self.assertIsNotNone(output_broadcast, "Should have broadcasted shell_output")

                # Assert that the secret is REDACTED
                self.assertNotIn("sk-1234567890abcdef1234567890abcdef", output_broadcast)
                self.assertIn("sk-[REDACTED]", output_broadcast)
                print("Confirmed: Secret redacted in broadcast output")

    def test_leak(self):
        asyncio.run(self.run_test())

if __name__ == "__main__":
    unittest.main()
