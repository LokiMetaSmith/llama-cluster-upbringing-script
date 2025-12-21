import subprocess
import os
import shutil
import re
import ast

# This is a placeholder for the actual smolagents library.
# We will assume it's available in the environment. In a real scenario,
# this would be a dependency managed by our project's requirements.
try:
    from smolagents import CodeAgent, LiteLLMModel
except ImportError:
    # If smolagents is not installed, we create mock classes to allow
    # the application to load without crashing. The tool will return an
    # error message if it's actually used.
    class CodeAgent:
        def __init__(self, *args, **kwargs):
            raise ImportError("The 'smolagents' library is not installed.")
        def run(self, *args, **kwargs):
            pass

    class LiteLLMModel:
        def __init__(self, *args, **kwargs):
            pass


class SmolAgentTool:
    """
    A tool that uses a smolagents.CodeAgent to solve complex tasks
    by generating and executing Python code in a secure Deno/Pyodide sandbox.
    """

    def __init__(self):
        """Initializes the SmolAgentTool."""
        self.description = (
            "Solves complex, multi-step tasks that require logic, calculations, or data processing. "
            "Provide a clear, natural language description of the task to be performed."
        )
        self.name = "smol_agent_computer"
        self.sandbox_script_path = os.path.join(
            os.path.dirname(__file__), "sandbox.ts"
        )
        self._initialized = False
        self.agent = None

    def _initialize(self):
        """Initializes the agent on first use."""
        if not self._initialized:
            # This check ensures that 'deno' is available before trying to use the tool.
            if not shutil.which("deno"):
                raise FileNotFoundError("The 'deno' runtime is not installed or not in the system's PATH.")

            # This model will use the environment's LLM provider configuration (e.g., OPENAI_API_KEY).
            model = LiteLLMModel(model_id="gpt-4o")
            self.agent = CodeAgent(model=model, stream_outputs=False)
            self._initialized = True

    def _execute_in_sandbox(self, code: str) -> str:
        """Executes the given Python code in the Deno/Pyodide sandbox."""
        command = [
            "deno", "run",
            "--allow-read",       # Required for Deno to read the script itself.
            "--allow-net=cdn.jsdelivr.net", # Pyodide needs to fetch packages.
            self.sandbox_script_path,
        ]
        try:
            process = subprocess.run(
                command,
                input=code.encode("utf-8"),
                capture_output=True,
                text=True,
                check=True,
                timeout=120,
            )
            output = ""
            if process.stdout:
                output += f"Output:\\n{process.stdout.strip()}\\n"
            if process.stderr:
                output += f"Logs:\\n{process.stderr.strip()}\\n"
            return output.strip()
        except FileNotFoundError:
            return "Error: 'deno' command not found. Please ensure Deno is installed and in your PATH."
        except subprocess.CalledProcessError as e:
            return f"Error during code execution:\\n{e.stderr}"
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out after 120 seconds."
        except Exception as e:
            return f"An unexpected error occurred during sandbox execution: {e}"

    def run(self, task_description: str) -> str:
        """
        Takes a task, generates Python code using a CodeAgent, and executes it.
        """
        if not isinstance(task_description, str) or not task_description:
            return "Error: Task description must be a non-empty string."

        try:
            self._initialize()

            # Use the agent to generate a plan and code.
            self.agent.run(task_description)

            # Extract code using regex to handle variations (e.g. ```python, ```, ```py)
            # and to be less brittle than simple string splitting.
            # Updated regex:
            # 1. (?:python|py)? : matches optional 'python' or 'py', non-capturing group.
            # 2. \s* : matches any whitespace after the backticks/language identifier.
            # 3. (.*?) : matches the content (code) minimally.
            # 4. re.IGNORECASE : ensures PYTHON/Py are matched.
            code_pattern = re.compile(r"```(?:python|py)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)
            code_to_execute = ""

            for message in reversed(self.agent.memory):
                if message["role"] == "assistant":
                    matches = code_pattern.findall(message["content"])
                    if matches:
                        # Extract all code blocks from the message and concatenate them
                        # to form a complete workspace execution.
                        code_to_execute = "\n".join([m.strip() for m in matches])
                        break

            if not code_to_execute:
                return "Error: The agent did not generate any code to execute."

            # Verify syntax before execution
            try:
                ast.parse(code_to_execute)
            except SyntaxError as e:
                return f"Error: The generated code has a syntax error: {e}"

            return self._execute_in_sandbox(code_to_execute)

        except ImportError:
            return "Error: The 'smolagents' library is not installed. Please install it to use this tool."
        except FileNotFoundError as e:
             return f"Error: A required dependency is missing. {e}"
        except Exception as e:
            return f"An error occurred while running the smolagent: {e}"
