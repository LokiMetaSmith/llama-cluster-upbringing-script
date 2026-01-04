import asyncio
import os
from typing import Dict, Any

class ClaudeCloneTool:
    def __init__(self, config: Dict[str, Any] = None):
        self.name = "claude_clone_tool"
        self.claude_clone_dir = "/opt/claude_clone"
        self.node_executable = "node"  # Assumes node is in the PATH

    async def _run_command(self, command: str, *args: str) -> str:
        if not os.path.isdir(self.claude_clone_dir):
            return f"Error: Claude_Clone directory not found at {self.claude_clone_dir}"

        cli_path = os.path.join(self.claude_clone_dir, "dist/cli.js")
        if not os.path.isfile(cli_path):
            return f"Error: Claude_Clone CLI not found at {cli_path}. Please build the project first."

        try:
            process = await asyncio.create_subprocess_exec(
                self.node_executable, cli_path, command, *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.claude_clone_dir
            )

            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)

            if process.returncode != 0:
                return f"Error executing Claude_Clone command '{command}': {stderr.decode()}"

            return stdout.decode()
        except asyncio.TimeoutError:
            return f"Error: Claude_Clone command '{command}' timed out."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    async def explain(self, files: str) -> str:
        """
        Explains code using the AI.
        :param files: A space-separated list of one or more files to use as context.
        """
        file_list = files.split()
        return await self._run_command("explain", *file_list)

    async def report(self) -> str:
        """
        Generates a high-level analysis report for the entire project.
        """
        return await self._run_command("report")

    async def generate(self, type: str, prompt: str, output: str = "") -> str:
        """
        Generates a new code snippet.
        :param type: The type of code to generate (e.g., function, class, test).
        :param prompt: A detailed description of the code to generate.
        :param output: Optional file path to save the generated code.
        """
        args = ["generate", type, "--prompt", prompt]
        if output:
            args.extend(["--output", output])
        return await self._run_command(*args)

    async def test(self, file: str, symbol: str, framework: str = "jest", output: str = "") -> str:
        """
        Generates a unit test for a specific function or class.
        :param file: The file containing the code to test.
        :param symbol: The name of the function/class to test.
        :param framework: The test framework to use (e.g., jest, vitest).
        :param output: Optional file path to save the new test file.
        """
        args = ["test", file, "--symbol", symbol, "--framework", framework]
        if output:
            args.extend(["--output", output])
        return await self._run_command(*args)

    async def get_tool_config(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": "A tool for code analysis and modification using Claude_Clone.",
            "methods": [
                {
                    "name": "explain",
                    "description": "Explains code using the AI.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "files": {
                                "type": "string",
                                "description": "A space-separated list of one or more files to use as context.",
                            }
                        },
                        "required": ["files"],
                    },
                },
                {
                    "name": "report",
                    "description": "Generates a high-level analysis report for the entire project.",
                    "parameters": {"type": "object", "properties": {}},
                },
                {
                    "name": "generate",
                    "description": "Generates a new code snippet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "The type of code to generate (e.g., function, class, test).",
                            },
                            "prompt": {
                                "type": "string",
                                "description": "A detailed description of the code to generate.",
                            },
                            "output": {
                                "type": "string",
                                "description": "Optional file path to save the generated code.",
                            },
                        },
                        "required": ["type", "prompt"],
                    },
                },
                {
                    "name": "test",
                    "description": "Generates a unit test for a specific function or class.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file": {
                                "type": "string",
                                "description": "The file containing the code to test.",
                            },
                            "symbol": {
                                "type": "string",
                                "description": "The name of the function/class to test.",
                            },
                            "framework": {
                                "type": "string",
                                "description": "The test framework to use (e.g., jest, vitest).",
                                "default": "jest",
                            },
                            "output": {
                                "type": "string",
                                "description": "Optional file path to save the new test file.",
                            },
                        },
                        "required": ["file", "symbol"],
                    },
                },
            ],
        }
