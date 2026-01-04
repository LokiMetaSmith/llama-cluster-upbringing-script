import os
import re
import logging

class FileEditorTool:
    """A tool for reading, writing, and patching files in the codebase.

    This tool allows the agent to modify the source code of the running application
    or other files in the repository.
    """
    def __init__(self, root_dir="/opt/pipecatapp"):
        """
        Args:
            root_dir (str): The root directory where the tool is allowed to operate.
                            Defaults to the app directory.
        """
        self.name = "file_editor"
        self.root_dir = os.path.realpath(root_dir)
        self.logger = logging.getLogger(__name__)

    def _validate_path(self, filepath: str) -> str:
        """Ensures the filepath is within the root directory."""
        # Handle relative paths by joining with root
        if not os.path.isabs(filepath):
            full_path = os.path.join(self.root_dir, filepath)
        else:
            full_path = filepath

        # Resolve symlinks and absolute path
        full_path = os.path.realpath(full_path)

        # Security check: Ensure we don't break out of the allowed root
        # Use commonpath to ensure full_path is a subdirectory of root_dir
        # This handles the case where root_dir is a prefix of full_path but not a parent directory
        # e.g., root_dir="/opt/app", full_path="/opt/app_backup"
        try:
            common = os.path.commonpath([self.root_dir, full_path])
        except ValueError:
            # Can happen on Windows if paths are on different drives
            common = ""

        if common != self.root_dir:
             raise ValueError(f"Access denied: {filepath} is outside the allowed root {self.root_dir}")

        return full_path

    def read_file(self, filepath: str) -> str:
        """Reads the content of a file."""
        try:
            path = self._validate_path(filepath)
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File not found at {filepath}"
        except Exception as e:
            return f"Error reading file {filepath}: {e}"

    def write_file(self, filepath: str, content: str) -> str:
        """Overwrites a file with new content. Creates directories if needed."""
        try:
            path = self._validate_path(filepath)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return f"Error writing to file {filepath}: {e}"

    def apply_patch(self, filepath: str, search_block: str, replace_block: str) -> str:
        """Replaces a specific block of text in a file with a new block.

        This acts like a targeted search-and-replace. The search_block must match exactly.
        """
        try:
            path = self._validate_path(filepath)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Normalize line endings for comparison if needed, but strict is safer for code.
            if search_block not in content:
                # Try to help with whitespace issues:
                # 1. Strip trailing spaces from lines in both
                # This is risky for python indentation.
                return f"Error: Search block not found in {filepath}. Ensure exact match."

            new_content = content.replace(search_block, replace_block, 1) # Replace first occurrence

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return f"Successfully patched {filepath}"
        except FileNotFoundError:
             return f"Error: File not found at {filepath}"
        except Exception as e:
            return f"Error patching file {filepath}: {e}"

    def append_to_file(self, filepath: str, content: str) -> str:
        """Appends content to the end of a file."""
        try:
            path = self._validate_path(filepath)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully appended to {filepath}"
        except Exception as e:
            return f"Error appending to file {filepath}: {e}"
