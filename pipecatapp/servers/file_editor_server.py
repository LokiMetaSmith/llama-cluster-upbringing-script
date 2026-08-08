from mcp.server.fastmcp import FastMCP
import os
import hashlib
from typing import List, Optional, Dict, Any

from pipecatapp.utils.file_utils import calculate_line_hash
import logging

mcp = FastMCP("file_editor_server")

ROOT_DIR = os.path.realpath("/opt/pipecatapp")
_undo_history: Dict[str, List[Optional[str]]] = {}
_file_metadata: Dict[str, Dict[str, Any]] = {}

def _validate_path(filepath: str) -> str:
    """Ensures the filepath is within the root directory."""
    if not os.path.isabs(filepath):
        full_path = os.path.join(ROOT_DIR, filepath)
    else:
        full_path = filepath
    full_path = os.path.realpath(full_path)
    try:
        common = os.path.commonpath([ROOT_DIR, full_path])
    except ValueError:
        common = ""
    if common != ROOT_DIR:
         raise ValueError(f"Access denied: {filepath} is outside the allowed root {ROOT_DIR}")
    return full_path

def _save_for_undo(path: str):
    """Saves the current file content to the undo history."""
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if path not in _undo_history:
            _undo_history[path] = []
        _undo_history[path].append(content)
    else:
         if path not in _undo_history:
            _undo_history[path] = []
         _undo_history[path].append(None) # None means file didn't exist

@mcp.tool()
def read_file(filepath: str, use_hashlines: bool = False, view_range: list = None) -> str:
    """Reads the content of a file and detects line endings metadata."""
    try:
        path = _validate_path(filepath)
        with open(path, 'rb') as f_bin:
            raw_content = f_bin.read()
            if b'\r\n' in raw_content:
                _file_metadata[path] = {'newline': '\r\n'}
            else:
                _file_metadata[path] = {'newline': '\n'}
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

@mcp.tool()
def write_file(filepath: str, content: str) -> str:
    """Overwrites a file with new content preserving line endings metadata. Creates directories if needed."""
    try:
        path = _validate_path(filepath)
        _save_for_undo(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        newline = _file_metadata.get(path, {}).get('newline', None)
        with open(path, 'w', encoding='utf-8', newline=newline) as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing to file {filepath}: {e}"

@mcp.tool()
def apply_patch(filepath: str, search_block: str, replace_block: str) -> str:
    """Replaces a specific block of text in a file with a new block."""
    try:
        path = _validate_path(filepath)
        _save_for_undo(path)
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

@mcp.tool()
def apply_hash_edits(filepath: str, edits: list) -> str:
    """Applies a list of edits using line hashes for verification."""
    try:
        path = _validate_path(filepath)
        _save_for_undo(path)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.splitlines()
        current_hashes = [calculate_line_hash(line) for line in lines]
        operations = []
        for edit in edits:
            edit_type = edit.get("type")
            target_id = edit.get("id")
            if not target_id: return f"Error: Missing 'id' in edit: {edit}"
            try:
                target_line_str, target_hash = target_id.split(':')
                target_line_num = int(target_line_str)
            except ValueError:
                return f"Error: Invalid id format '{target_id}'. Expected 'line_num:hash'."
            idx = target_line_num - 1
            if idx < 0 or idx >= len(lines): return f"Error: Line number {target_line_num} out of range."
            if current_hashes[idx] != target_hash: return f"Error: Hash mismatch at line {target_line_num}. Expected {target_hash}, found {current_hashes[idx]}."

            end_idx = idx
            if edit_type == "replace_range":
                end_id = edit.get("end_id")
                if end_id:
                    try:
                        end_line_str, end_hash = end_id.split(':')
                        end_line_num = int(end_line_str)
                        end_idx = end_line_num - 1
                    except ValueError:
                         return f"Error: Invalid end_id format '{end_id}'."
                    if end_idx < 0 or end_idx >= len(lines): return f"Error: End line number {end_line_num} out of range."
                    if current_hashes[end_idx] != end_hash: return f"Error: Hash mismatch at end line {end_line_num}. Expected {end_hash}, found {current_hashes[end_idx]}."

            operations.append({"idx": idx, "end_idx": end_idx, "type": edit_type, "content": edit.get("content", "")})

        operations.sort(key=lambda x: x['idx'], reverse=True)
        for op in operations:
            idx, end_idx, op_type, new_content = op['idx'], op['end_idx'], op['type'], op['content']
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

@mcp.tool()
def undo_edit(filepath: str) -> str:
    """Reverts the last edit made to the specified file."""
    try:
        path = _validate_path(filepath)
        if path not in _undo_history or not _undo_history[path]:
            return f"Error: No undo history available for {filepath}."
        previous_content = _undo_history[path].pop()
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

@mcp.tool()
def append_to_file(filepath: str, content: str) -> str:
    """Appends content to the end of a file."""
    try:
        path = _validate_path(filepath)
        _save_for_undo(path)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully appended to {filepath}"
    except Exception as e:
        return f"Error appending to file {filepath}: {e}"

@mcp.tool()
def flag_megafile(filepath: str) -> str:
    """Flags a file as bloated or highly contested by appending it to the Megafile queue."""
    full_path = _validate_path(filepath)
    if "Error" in full_path:
        return full_path
    queue_path = os.path.join(ROOT_DIR, ".liminal", "megafiles_queue.json")
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
        logging.getLogger(__name__).error(f"Failed to flag megafile: {e}")
        return f"Error flagging megafile: {e}"

if __name__ == "__main__":
    mcp.run()
