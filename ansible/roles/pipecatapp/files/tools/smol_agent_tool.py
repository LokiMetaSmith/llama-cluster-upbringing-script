import subprocess
import os
import shutil

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

            # TODO: The following code extraction logic is brittle, as it relies on
            # parsing the internal `memory` log of the `smolagents` library.
            # This should be replaced with a more stable method if the library
            # provides a direct way to access the final generated code.
            code_to_execute = ""
            for message in reversed(self.agent.memory):
                if message["role"] == "assistant" and "```python" in message["content"]:
                    # This reliably extracts the code from the markdown block.
                    code_block = message["content"].split("```python\\n", 1)[1]
                    code_to_execute = code_block.split("```", 1)[0]
                    break

            if not code_to_execute:
                return "Error: The agent did not generate any code to execute."

            return self._execute_in_sandbox(code_to_execute)

        except ImportError:
            return "Error: The 'smolagents' library is not installed. Please install it to use this tool."
        except FileNotFoundError as e:
             return f"Error: A required dependency is missing. {e}"
        except Exception as e:
            return f"An error occurred while running the smolagent: {e}"
