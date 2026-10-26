from pipecatapp.utils.file_utils import calculate_line_hash
import os
import re
import logging
import hashlib
import asyncio
from typing import Optional
from pipecatapp.tools.code_graph_tool import CodeGraphTool

class FileEditorTool:
    """A tool for reading, writing, and patching files in the codebase.

    This tool allows the agent to modify the source code of the running application
    or other files in the repository. Integrated with CodeGraphTool for preflight checks.
    """
    def __init__(self, root_dir="/opt/pipecatapp", code_graph_tool: Optional[CodeGraphTool] = None):
        """
        Args:
            root_dir (str): The root directory where the tool is allowed to operate.
                            Defaults to the app directory.
            code_graph_tool (CodeGraphTool): Optional CodeGraphTool instance for preflight checks.
        """
        self.name = "file_editor"
        self.root_dir = os.path.realpath(root_dir)
        self.logger = logging.getLogger(__name__)
        self._undo_history = {} # Maps filepath to list of previous contents
        self._file_metadata = {} # Maps filepath to metadata (e.g. line endings)
        self.code_graph_tool = code_graph_tool or CodeGraphTool(root_dir=self.root_dir)


    def get_schema(self) -> dict:
        """Returns the schema for the file editor tool."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Reads, writes, and patches files in the codebase with optional preflight blast radius checks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["read", "write", "patch", "hash_replace", "batch_hash_replace", "undo", "find", "get_metadata", "flag_megafile"],
                            "description": "The action to perform on the file."
                        },
                        "filepath": {
                            "type": "string",
                            "description": "The path to the file to modify or read. Optional for batch_hash_replace."
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write or append to the file (used for write, append)."
                        },
                        "search_block": {
                            "type": "string",
                            "description": "The block of text to replace (used for patch)."
                        },
                        "replace_block": {
                            "type": "string",
                            "description": "The block of text to insert (used for patch)."
                        },
                        "verify_preflight": {
                            "type": "boolean",
                            "description": "Whether to perform code graph preflight checks prior to writing edits (default: False)."
                        },
                        "edits": {
                            "type": "array",
                            "description": "A list of edit objects (used for hash_replace).",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": { "type": "string", "enum": ["replace", "replace_range", "insert_after", "delete"] },
                                    "id": { "type": "string", "description": "The target line in format <line_number>:<hash>" },
                                    "end_id": { "type": "string", "description": "The end target line for replace_range" },
                                    "content": { "type": "string", "description": "The new content" }
                                },
                                "required": ["type", "id"]
                            }
                        },
                        "batch_edits": {
                            "type": "array",
                            "description": "A list of files and their edits (used for batch_hash_replace).",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "filepath": { "type": "string", "description": "The path to the file to modify." },
                                    "edits": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "type": { "type": "string", "enum": ["replace", "replace_range", "insert_after", "delete"] },
                                                "id": { "type": "string", "description": "The target line in format <line_number>:<hash>" },
                                                "end_id": { "type": "string", "description": "The end target line for replace_range" },
                                                "content": { "type": "string", "description": "The new content" }
                                            },
                                            "required": ["type", "id"]
                                        }
                                    }
                                },
                                "required": ["filepath", "edits"]
                            }
                        },
                        "use_hashlines": {
                            "type": "boolean",
                            "description": "Whether to return lines with line numbers and hashes (used for read). Defaults to False."
                        },
                        "view_range": {
                            "type": "array",
                            "items": { "type": "integer" },
                            "description": "Optional [start_line, end_line] 1-based index to read only a portion of the file."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    async def execute(self, action: str, filepath: str = "", verify_preflight: bool = False, **kwargs) -> str:
        """Executes the file editor action."""
        preflight_summary = ""
        if verify_preflight and filepath and action in ["write", "patch", "hash_replace"]:
            try:
                preflight_summary = self.code_graph_tool.preflight(filepath=filepath) + "\n\n"
            except Exception as e:
                self.logger.warning(f"Failed to run preflight check for {filepath}: {e}")

        if action == "read":
            if not filepath: return "Error: filepath is required for read action."
            use_hashlines = kwargs.get("use_hashlines", False)
            view_range = kwargs.get("view_range", None)
            return self.read_file(filepath, use_hashlines=use_hashlines, view_range=view_range)
        elif action == "write":
            if not filepath: return "Error: filepath is required for write action."
            content = kwargs.get("content", "")
            return preflight_summary + self.write_file(filepath, content)
        elif action == "patch":
            if not filepath: return "Error: filepath is required for patch action."
            search_block = kwargs.get("search_block", "")
            replace_block = kwargs.get("replace_block", "")
            return preflight_summary + self.apply_patch(filepath, search_block, replace_block)
        elif action == "hash_replace":
            if not filepath: return "Error: filepath is required for hash_replace action."
            edits = kwargs.get("edits", [])
            return preflight_summary + self.apply_hash_edits(filepath, edits)
        elif action == "batch_hash_replace":
            batch_edits = kwargs.get("batch_edits", [])
            if not batch_edits:
                return "Error: batch_edits is required for batch_hash_replace action."
            results = []
            for batch in batch_edits:
                path = batch.get("filepath")
                edits = batch.get("edits", [])
                if not path:
                    results.append("Error: filepath missing in batch edit.")
                else:
                    result = self.apply_hash_edits(path, edits)
                    results.append(f"[{path}] {result}")
            return "\n".join(results)
        elif action == "append":
            if not filepath: return "Error: filepath is required for append action."
            content = kwargs.get("content", "")
            return self.append_to_file(filepath, content)
        elif action == "flag_megafile":
            if not filepath: return "Error: filepath is required for flag_megafile action."
            return self.flag_megafile(filepath)
        elif action == "undo":
            if not filepath: return "Error: filepath is required for undo action."
            return self.undo_edit(filepath)
        else:
            return f"Error: Unknown action '{action}'"

    def _validate_path(self, filepath: str) -> str:
        """Ensures the filepath is within the root directory."""
        if not os.path.isabs(filepath):
            full_path = os.path.join(self.root_dir, filepath)
        else:
            full_path = filepath

        full_path = os.path.realpath(full_path)

        try:
            common = os.path.commonpath([self.root_dir, full_path])
        except ValueError:
            common = ""

        if common != self.root_dir:
             raise ValueError(f"Access denied: {filepath} is outside the allowed root {self.root_dir}")

        return full_path

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

    def flag_megafile(self, filepath: str) -> str:
        """Flags a file as bloated or highly contested by appending it to the Megafile queue."""
        try:
            full_path = self._validate_path(filepath)
        except Exception as e:
            return f"Error validating path: {e}"

        queue_path = os.path.join(self.root_dir, ".liminal", "megafiles_queue.json")
        try:
            import json
            os.makedirs(os.path.dirname(queue_path), exist_ok=True)
            queue = []
            if os.path.exists(queue_path):
                with open(queue_path, "r") as f:
                    queue = json.load(f)

            if filepath not in queue:
                queue.append(filepath)
                with open(queue_path, "w") as f:
                    json.dump(queue, f)
                return f"Successfully flagged '{filepath}' as a Megafile. It has been queued for decomposition."
            else:
                return f"'{filepath}' is already flagged in the Megafile queue."
        except Exception as e:
            self.logger.error(f"Failed to flag megafile: {e}")
            return f"Error flagging megafile: {e}"

    def read_file(self, filepath: str, use_hashlines: bool = False, view_range: list | None = None) -> str:
        """Reads the content of a file and detects line endings metadata."""
        try:
            path = self._validate_path(filepath)

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
            except Exception:
                line_count = 0

            start_line = view_range[0] if view_range and len(view_range) > 0 else 1
            end_line = view_range[1] if view_range and len(view_range) > 1 else -1

            lines_requested = line_count
            if end_line != -1:
                lines_requested = end_line - start_line + 1

            if lines_requested > 350:
                return f"Error: File is too large ({line_count} lines). Reading more than 350 lines directly into context is blocked to save tokens. Please use the `shunt` tool with action `bulk_read` to analyze this file, or use `view_range` to read a smaller, targeted portion."

            with open(path, 'rb') as f_bin:
                raw_content = f_bin.read()
                if b'\r\n' in raw_content:
                    self._file_metadata[path] = {'newline': '\r\n'}
                else:
                    self._file_metadata[path] = {'newline': '\n'}
                content = raw_content.decode('utf-8')

            lines = content.splitlines()

            start_idx = 0
            end_idx = len(lines)

            if view_range and isinstance(view_range, list) and len(view_range) == 2:
                start_line = int(view_range[0])
                end_line = int(view_range[1])

                start_idx = max(0, start_line - 1)

                if end_line != -1:
                    end_idx = min(len(lines), end_line)

            view_lines = lines[start_idx:end_idx]

            if use_hashlines:
                output = []
                for i, line in enumerate(view_lines):
                    line_hash = calculate_line_hash(line)
                    actual_line_num = i + start_idx + 1
                    output.append(f"{actual_line_num}:{line_hash}| {line}")
                result_str = "\n".join(output)
            else:
                result_str = "\n".join(view_lines)

            if view_range and isinstance(view_range, list) and len(view_range) == 2:
                if end_idx < len(lines) or start_idx > 0:
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
        """Replaces a specific block of text in a file with a new block."""
        try:
            path = self._validate_path(filepath)
            self._save_for_undo(path)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if search_block not in content:
                return f"Error: Search block not found in {filepath}. Ensure exact match."

            new_content = content.replace(search_block, replace_block, 1)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return f"Successfully patched {filepath}"
        except FileNotFoundError:
             return f"Error: File not found at {filepath}"
        except Exception as e:
            return f"Error patching file {filepath}: {e}"

    def apply_hash_edits(self, filepath: str, edits: list) -> str:
        """Applies a list of edits using line hashes for verification."""
        try:
            path = self._validate_path(filepath)
            self._save_for_undo(path)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.splitlines()
            current_hashes = [calculate_line_hash(line) for line in lines]

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

                idx = target_line_num - 1

                if idx < 0 or idx >= len(lines):
                    return f"Error: Line number {target_line_num} out of range."

                if current_hashes[idx] != target_hash:
                    return f"Error: Hash mismatch at line {target_line_num}. Expected {target_hash}, found {current_hashes[idx]}."

                end_idx = idx
                if edit_type == "replace_range":
                    end_id = edit.get("end_id")
                    if not end_id:
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

            operations.sort(key=lambda x: x['idx'], reverse=True)

            for op in operations:
                idx = op['idx']
                end_idx = op['end_idx']
                op_type = op['type']
                new_content = op['content']

                new_lines = new_content.splitlines()

                if op_type == "replace":
                    lines[idx:idx+1] = new_lines
                elif op_type == "replace_range":
                    lines[idx:end_idx+1] = new_lines
                elif op_type == "insert_after":
                    lines[idx+1:idx+1] = new_lines
                elif op_type == "delete":
                    del lines[idx]
                else:
                    return f"Error: Unknown edit type '{op_type}'."

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
