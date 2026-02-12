import subprocess
import shlex
import os
import logging

class SearchTool:
    """A tool for searching the codebase using grep and find.

    This tool allows the agent to semantically navigate the codebase by searching
    for text patterns (definitions, usages) and locating files by name.
    """

    def __init__(self, root_dir="/"):
        self.name = "search"
        self.description = "Search the codebase for text patterns or file names."
        self.root_dir = os.path.realpath(root_dir)

    def _validate_path(self, path: str) -> str:
        """Ensures the path is within the allowed root directory."""
        if not os.path.isabs(path):
            full_path = os.path.join(self.root_dir, path)
        else:
            full_path = path

        full_path = os.path.realpath(full_path)

        # Commonpath check is safer than startswith for symlinks/different drives
        try:
            common = os.path.commonpath([self.root_dir, full_path])
        except ValueError:
            common = ""

        if common != self.root_dir:
             raise ValueError(f"Access denied: Path '{path}' resolves to '{full_path}', which is outside allowed root '{self.root_dir}'")

        return full_path

    def grep(self, pattern: str, path: str = ".", include: str = None, exclude: str = None, context_lines: int = 0) -> str:
        """
        Searches for a text pattern in files using grep.

        Args:
            pattern (str): The regex pattern to search for.
            path (str): The directory to search in. Defaults to current directory.
            include (str): File pattern to include (e.g., "*.py").
            exclude (str): File pattern to exclude (e.g., "*.log").
            context_lines (int): Number of context lines to show (grep -C).

        Returns:
            str: The grep output, potentially truncated if too long.
        """
        if not pattern:
            return "Error: Pattern cannot be empty."

        try:
            safe_path = self._validate_path(path)
        except ValueError as e:
            return str(e)

        if not os.path.exists(safe_path):
            return f"Error: Path '{path}' does not exist."

        # Construct command
        # -r: recursive
        # -n: line numbers
        # -I: ignore binary files
        cmd = ["grep", "-r", "-n", "-I"]

        if context_lines > 0:
            cmd.extend(["-C", str(context_lines)])

        if include:
            cmd.extend(["--include", include])

        if exclude:
            cmd.extend(["--exclude", exclude])

        # Use -e to handle patterns starting with -
        cmd.extend(["-e", pattern])
        cmd.append(safe_path)

        try:
            logging.info(f"Running grep command: {shlex.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30 # Timeout to prevent hanging
            )

            output = result.stdout
            if result.stderr:
                output += f"\nStderr: {result.stderr}"

            if not output:
                if result.returncode == 1:
                    return "No matches found."
                elif result.returncode != 0:
                    return f"Error running grep (exit code {result.returncode})"

            # Truncate output if too long (e.g. 500 lines)
            lines = output.splitlines()
            if len(lines) > 500:
                truncated = "\n".join(lines[:500])
                return f"{truncated}\n... (Output truncated, {len(lines) - 500} more lines. Refine your search.)"

            return output

        except subprocess.TimeoutExpired:
            return "Error: Grep command timed out."
        except Exception as e:
            return f"Error executing grep: {e}"

    def find_file(self, filename_pattern: str, path: str = ".") -> str:
        """
        Locates files by name using the find command.

        Args:
            filename_pattern (str): The glob pattern for the filename (e.g., "*.py").
            path (str): The directory to start searching from.

        Returns:
            str: A list of matching file paths.
        """
        if not filename_pattern:
             return "Error: Filename pattern cannot be empty."

        try:
            safe_path = self._validate_path(path)
        except ValueError as e:
            return str(e)

        if not os.path.exists(safe_path):
            return f"Error: Path '{path}' does not exist."

        # Construct command
        # find path -name pattern
        cmd = ["find", safe_path, "-name", filename_pattern]

        try:
            logging.info(f"Running find command: {shlex.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout
            if result.stderr:
                output += f"\nStderr: {result.stderr}"

            if not output:
                return "No files found."

            lines = output.splitlines()
            if len(lines) > 500:
                truncated = "\n".join(lines[:500])
                return f"{truncated}\n... (Output truncated, {len(lines) - 500} more files found. Refine your search.)"

            return output

        except subprocess.TimeoutExpired:
             return "Error: Find command timed out."
        except Exception as e:
            return f"Error executing find: {e}"
