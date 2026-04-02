import os
import re
import logging
import hashlib

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
        self._undo_history = {} # Maps filepath to list of previous contents
        self._file_metadata = {} # Maps filepath to metadata (e.g. line endings)

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

    def _calculate_line_hash(self, line: str) -> str:
        """Calculates a short hash for a line of text."""
        # Use full line content including whitespace for precision
        return hashlib.sha256(line.encode('utf-8')).hexdigest()[:2]

    def _save_for_undo(self, path: str):
        """Saves the current file content to the undo history."""
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if path not in self._undo_history:
                self._undo_history[path] = []
            self._undo_history[path].append(content)
        else:
             if path not in self._undo_history:
                self._undo_history[path] = []
             self._undo_history[path].append(None) # None means file didn't exist

    def undo_edit(self, filepath: str) -> str:
        """Reverts the last edit made to the specified file."""
        try:
            path = self._validate_path(filepath)
            if path not in self._undo_history or not self._undo_history[path]:
                return f"Error: No undo history available for {filepath}."

            previous_content = self._undo_history[path].pop()

            if previous_content is None:
                if os.path.exists(path):
                    os.remove(path)
                return f"Successfully reverted {filepath} (file deleted, as it didn't exist before the edit)."
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(previous_content)
                return f"Successfully reverted last edit to {filepath}."
        except Exception as e:
            return f"Error undoing edit to {filepath}: {e}"

    def read_file(self, filepath: str, use_hashlines: bool = False, view_range: list = None) -> str:
        """Reads the content of a file and detects line endings metadata.

        Args:
            filepath (str): The path to the file.
            use_hashlines (bool): If True, returns content with line numbers and hashes.
                                  Format: <line_number>:<hash>| <content>
            view_range (list): Optional [start_line, end_line] 1-based index to read only a portion of the file.
                               Setting [start_line, -1] reads to the end.
        """
        try:
            path = self._validate_path(filepath)
            with open(path, 'rb') as f_bin:
                sample = f_bin.read(4096)
                if b'\r\n' in sample:
                    self._file_metadata[path] = {'newline': '\r\n'}
                else:
                    self._file_metadata[path] = {'newline': '\n'}

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.splitlines()

            start_idx = 0
            end_idx = len(lines)

            if view_range and isinstance(view_range, list) and len(view_range) == 2:
                start_line = int(view_range[0])
                end_line = int(view_range[1])

                # Convert 1-based to 0-based
                start_idx = max(0, start_line - 1)

                if end_line != -1:
                    end_idx = min(len(lines), end_line)

            view_lines = lines[start_idx:end_idx]

            if use_hashlines:
                output = []
                for i, line in enumerate(view_lines):
                    line_hash = self._calculate_line_hash(line)
                    # i+start_idx is 0-based index of original line. +1 to get 1-based line number.
                    actual_line_num = i + start_idx + 1
                    output.append(f"{actual_line_num}:{line_hash}| {line}")
                result_str = "\n".join(output)
            else:
                result_str = "\n".join(view_lines)

            # Transparent Pagination Feedback
            if view_range and isinstance(view_range, list) and len(view_range) == 2:
                if end_idx < len(lines):
                     result_str += f"\n[Showing results with pagination = limit: {end_idx - start_idx}, offset: {start_idx}]"

            return result_str
        except FileNotFoundError:
            return f"Error: File not found at {filepath}"
        except Exception as e:
            return f"Error reading file {filepath}: {e}"

    def write_file(self, filepath: str, content: str) -> str:
        """Overwrites a file with new content preserving line endings metadata. Creates directories if needed."""
        try:
            path = self._validate_path(filepath)
            self._save_for_undo(path)
            os.makedirs(os.path.dirname(path), exist_ok=True)

            newline = self._file_metadata.get(path, {}).get('newline', None)
            with open(path, 'w', encoding='utf-8', newline=newline) as f:
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
            self._save_for_undo(path)
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

    def apply_hash_edits(self, filepath: str, edits: list) -> str:
        """Applies a list of edits using line hashes for verification.

        Args:
            filepath (str): Path to the file.
            edits (list): List of edit objects. Each object should have:
                          - type: "replace", "replace_range", "insert_after", "delete"
                          - id: "<line_number>:<hash>" (target line)
                          - end_id: "<line_number>:<hash>" (optional, for ranges)
                          - content: "new content" (for replace/insert)
        """
        try:
            path = self._validate_path(filepath)
            self._save_for_undo(path)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.splitlines()
            current_hashes = [self._calculate_line_hash(line) for line in lines]

            operations = []

            for edit in edits:
                edit_type = edit.get("type")
                target_id = edit.get("id")

                if not target_id:
                    return f"Error: Missing 'id' in edit: {edit}"

                try:
                    target_line_str, target_hash = target_id.split(':')
                    target_line_num = int(target_line_str)
                except ValueError:
                    return f"Error: Invalid id format '{target_id}'. Expected 'line_num:hash'."

                # Validation: Check if line exists and hash matches
                # Adjust to 0-based index
                idx = target_line_num - 1

                if idx < 0 or idx >= len(lines):
                    return f"Error: Line number {target_line_num} out of range."

                if current_hashes[idx] != target_hash:
                    return f"Error: Hash mismatch at line {target_line_num}. Expected {target_hash}, found {current_hashes[idx]}."

                # Resolve end_id for ranges
                end_idx = idx
                if edit_type == "replace_range":
                    end_id = edit.get("end_id")
                    if not end_id:
                         # Single line replace if end_id not provided? Treat as replace.
                         pass
                    else:
                        try:
                            end_line_str, end_hash = end_id.split(':')
                            end_line_num = int(end_line_str)
                            end_idx = end_line_num - 1
                        except ValueError:
                             return f"Error: Invalid end_id format '{end_id}'."

                        if end_idx < 0 or end_idx >= len(lines):
                            return f"Error: End line number {end_line_num} out of range."
                        if current_hashes[end_idx] != end_hash:
                            return f"Error: Hash mismatch at end line {end_line_num}. Expected {end_hash}, found {current_hashes[end_idx]}."

                operations.append({
                    "idx": idx,
                    "end_idx": end_idx,
                    "type": edit_type,
                    "content": edit.get("content", "")
                })

            # Sort operations by index descending to avoid shifting issues
            operations.sort(key=lambda x: x['idx'], reverse=True)

            # Apply edits
            for op in operations:
                idx = op['idx']
                end_idx = op['end_idx']
                op_type = op['type']
                new_content = op['content']

                # Split new content into lines. Keep empty list if content is empty (for deletes/replacements with empty)
                # Note: splitlines() on "" returns [].
                new_lines = new_content.splitlines()
                # If new_content ends with \n, splitlines ignores it by default.
                # Ideally, content provided by LLM has explicit structure.

                if op_type == "replace":
                    # Replace single line
                    lines[idx:idx+1] = new_lines
                elif op_type == "replace_range":
                    # Replace range [idx, end_idx] inclusive
                    lines[idx:end_idx+1] = new_lines
                elif op_type == "insert_after":
                    # Insert after idx
                    lines[idx+1:idx+1] = new_lines
                elif op_type == "delete":
                    # Delete single line
                    del lines[idx]
                else:
                    return f"Error: Unknown edit type '{op_type}'."

            # Write back
            with open(path, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))

            return f"Successfully applied {len(edits)} edits to {filepath}"

        except Exception as e:
            return f"Error applying edits to {filepath}: {e}"

    def append_to_file(self, filepath: str, content: str) -> str:
        """Appends content to the end of a file."""
        try:
            path = self._validate_path(filepath)
            self._save_for_undo(path)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully appended to {filepath}"
        except Exception as e:
            return f"Error appending to file {filepath}: {e}"
