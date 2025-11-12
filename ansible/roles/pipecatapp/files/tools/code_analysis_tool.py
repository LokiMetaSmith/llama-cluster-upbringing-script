import os
import shlex
import ast

class Code_Analysis_Tool:
    """A tool for analyzing and modifying code.

    This class provides methods to analyze code, suggest modifications,
    and generate new code snippets.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self):
        """Initializes the Code_Analysis_Tool."""
        self.description = "Analyze and modify code."
        self.name = "code_analysis_tool"

    def _analyze_file(self, filepath: str) -> str:
        """Analyzes a single file.

        Args:
            filepath (str): The path to the file to analyze.

        Returns:
            str: A summary of the file's contents.
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                tree = ast.parse(content)
                num_lines = len(content.splitlines())
                num_classes = 0
                num_functions = 0
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        num_classes += 1
                    elif isinstance(node, ast.FunctionDef):
                        num_functions += 1
                return f"File: {filepath}\nLines: {num_lines}\nClasses: {num_classes}\nFunctions: {num_functions}"
        except FileNotFoundError:
            return f"Error: File not found at {filepath}"
        except SyntaxError:
            return f"Error: Invalid Python syntax in {filepath}"
        except Exception as e:
            return f"An unexpected error occurred while analyzing the file: {e}"

    def _modify_file(self, filepath: str, search: str, replace: str) -> str:
        """Modifies a single file.

        Args:
            filepath (str): The path to the file to modify.
            search (str): The string to search for.
            replace (str): The string to replace with.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read()

            new_content = content.replace(search, replace)

            with open(filepath, 'w') as f:
                f.write(new_content)

            return f"File {filepath} modified successfully."
        except FileNotFoundError:
            return f"Error: File not found at {filepath}"
        except Exception as e:
            return f"An unexpected error occurred while modifying the file: {e}"

    def _generate_file(self, filepath: str, content: str) -> str:
        """Generates a new file.

        Args:
            filepath (str): The path to the file to generate.
            content (str): The content of the new file.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            with open(filepath, 'w') as f:
                f.write(content)

            return f"File {filepath} generated successfully."
        except Exception as e:
            return f"An unexpected error occurred while generating the file: {e}"

    def run(self, command: str) -> str:
        """Runs a code analysis command.

        Args:
            command (str): The command to run.

        Returns:
            str: A string containing the output of the command, or an
                error message if the run fails.
        """
        if not command:
            return "Error: command cannot be empty."

        parts = shlex.split(command)
        if parts[0] == "analyze":
            if len(parts) > 1:
                return self._analyze_file(parts[1])
            else:
                return "Error: please specify a file to analyze."
        elif parts[0] == "modify":
            if len(parts) > 3:
                return self._modify_file(parts[1], parts[2], parts[3])
            else:
                return "Error: please specify a file, search string, and replace string."
        elif parts[0] == "generate":
            if len(parts) > 2:
                return self._generate_file(parts[1], " ".join(parts[2:]))
            else:
                return "Error: please specify a file path and content."
        else:
            return "Error: invalid command."
