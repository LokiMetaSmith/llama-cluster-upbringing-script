import ast
import os
import logging
import re

class ASTEditorTool:
    """A tool for performing AST-aware structural edits on Python files.

    Provides structural commands:
    - extract_function
    - rename_symbol
    - add_import

    Ensures the resulting file is syntactically valid before writing.
    """
    def __init__(self, root_dir="/opt/pipecatapp"):
        self.name = "ast_editor"
        self.root_dir = os.path.realpath(root_dir)
        self.logger = logging.getLogger(__name__)

    def get_schema(self) -> dict:
        """Returns the schema for the AST editor tool."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Performs structural, AST-aware edits on Python files (extract_function, rename_symbol, add_import).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["extract_function", "rename_symbol", "add_import", "batch_edit"],
                            "description": "The AST edit action to perform."
                        },
                        "filepath": {
                            "type": "string",
                            "description": "The path to the Python file to modify. Optional for batch_edit."
                        },
                        "func_name": {
                            "type": "string",
                            "description": "The name of the function to extract (used for extract_function)."
                        },
                        "target_filepath": {
                            "type": "string",
                            "description": "The file to append the extracted function to (used for extract_function)."
                        },
                        "old_name": {
                            "type": "string",
                            "description": "The symbol name to replace (used for rename_symbol)."
                        },
                        "new_name": {
                            "type": "string",
                            "description": "The new symbol name (used for rename_symbol)."
                        },
                        "import_statement": {
                            "type": "string",
                            "description": "The full import statement to add (used for add_import)."
                        },
                        "batch_operations": {
                            "type": "array",
                            "description": "A list of operations across multiple files (used for batch_edit).",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "action": {
                                        "type": "string",
                                        "enum": ["extract_function", "rename_symbol", "add_import"],
                                        "description": "The AST edit action to perform."
                                    },
                                    "filepath": {
                                        "type": "string",
                                        "description": "The path to the Python file to modify."
                                    },
                                    "func_name": { "type": "string" },
                                    "target_filepath": { "type": "string" },
                                    "old_name": { "type": "string" },
                                    "new_name": { "type": "string" },
                                    "import_statement": { "type": "string" }
                                },
                                "required": ["action", "filepath"]
                            }
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    async def execute(self, action: str, filepath: str = "", **kwargs) -> str:
        """Executes the AST editor action."""
        if action == "extract_function":
            if not filepath: return "Error: filepath is required for extract_function action."
            func_name = kwargs.get("func_name")
            target_filepath = kwargs.get("target_filepath")
            if not func_name or not target_filepath:
                return "Error: extract_function requires func_name and target_filepath."
            return self.extract_function(filepath, func_name, target_filepath)
        elif action == "rename_symbol":
            if not filepath: return "Error: filepath is required for rename_symbol action."
            old_name = kwargs.get("old_name")
            new_name = kwargs.get("new_name")
            if not old_name or not new_name:
                return "Error: rename_symbol requires old_name and new_name."
            return self.rename_symbol(filepath, old_name, new_name)
        elif action == "add_import":
            if not filepath: return "Error: filepath is required for add_import action."
            import_statement = kwargs.get("import_statement")
            if not import_statement:
                return "Error: add_import requires import_statement."
            return self.add_import(filepath, import_statement)
        elif action == "batch_edit":
            batch_operations = kwargs.get("batch_operations", [])
            if not batch_operations:
                return "Error: batch_operations is required for batch_edit action."
            results = []
            for op in batch_operations:
                op_action = op.get("action")
                op_filepath = op.get("filepath")
                if not op_action or not op_filepath:
                    results.append("Error: action and filepath are required for each batch operation.")
                    continue

                if op_action == "extract_function":
                    func_name = op.get("func_name")
                    target_filepath = op.get("target_filepath")
                    if not func_name or not target_filepath:
                        results.append(f"[{op_filepath}] Error: extract_function requires func_name and target_filepath.")
                    else:
                        results.append(f"[{op_filepath}] " + self.extract_function(op_filepath, func_name, target_filepath))
                elif op_action == "rename_symbol":
                    old_name = op.get("old_name")
                    new_name = op.get("new_name")
                    if not old_name or not new_name:
                        results.append(f"[{op_filepath}] Error: rename_symbol requires old_name and new_name.")
                    else:
                        results.append(f"[{op_filepath}] " + self.rename_symbol(op_filepath, old_name, new_name))
                elif op_action == "add_import":
                    import_statement = op.get("import_statement")
                    if not import_statement:
                        results.append(f"[{op_filepath}] Error: add_import requires import_statement.")
                    else:
                        results.append(f"[{op_filepath}] " + self.add_import(op_filepath, import_statement))
                else:
                    results.append(f"[{op_filepath}] Error: Unknown action '{op_action}'")
            return "\n".join(results)
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

    def _parse_and_validate(self, content: str) -> bool:
        """Validates that the content is valid Python syntax."""
        try:
            ast.parse(content)
            return True
        except SyntaxError:
            return False

    def extract_function(self, filepath: str, func_name: str, target_filepath: str) -> str:
        """Extracts a function by name and moves it to a target file."""
        try:
            path = self._validate_path(filepath)
            target_path = self._validate_path(target_filepath)

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                return f"Error: Source file {filepath} has invalid syntax before edit: {e}"

            target_node = None
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name == func_name:
                        target_node = node
                        break

            if not target_node:
                return f"Error: Function '{func_name}' not found in {filepath}."

            lines = content.splitlines(keepends=True)

            # Identify the start and end line numbers (1-based index)
            start_line = target_node.lineno
            if target_node.decorator_list:
                start_line = min(d.lineno for d in target_node.decorator_list)
            end_line = target_node.end_lineno

            # Extract the function
            func_lines = lines[start_line - 1:end_line]
            extracted_code = "".join(func_lines)

            # Remove the function from the source file
            new_lines = lines[:start_line - 1] + lines[end_line:]
            new_content = "".join(new_lines)

            if not self._parse_and_validate(new_content):
                return "Error: Removing the function resulted in invalid syntax. Edit aborted."

            # Write the changes back to source file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Append the extracted function to target file
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, 'a', encoding='utf-8') as f:
                # Add a couple of blank lines before appending if file is not empty
                if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
                    f.write("\n\n")
                f.write(extracted_code)

            return f"Successfully extracted '{func_name}' from {filepath} to {target_filepath}."

        except Exception as e:
            return f"Error in extract_function: {e}"

    def rename_symbol(self, filepath: str, old_name: str, new_name: str) -> str:
        """Renames a symbol in the given Python file."""
        try:
            path = self._validate_path(filepath)

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            try:
                ast.parse(content)
            except SyntaxError as e:
                return f"Error: Source file {filepath} has invalid syntax before edit: {e}"

            # Simple regex replacement on word boundaries.
            # While this might affect strings/comments, standard AST read-only doesn't support writing.
            # We enforce AST validity as a safeguard.
            pattern = rf'\b{re.escape(old_name)}\b'
            new_content = re.sub(pattern, new_name, content)

            if not self._parse_and_validate(new_content):
                return "Error: Renaming symbol resulted in invalid syntax. Edit aborted."

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return f"Successfully renamed '{old_name}' to '{new_name}' in {filepath}."
        except Exception as e:
            return f"Error in rename_symbol: {e}"

    def add_import(self, filepath: str, import_statement: str) -> str:
        """Adds an import statement to the top of the file."""
        try:
            path = self._validate_path(filepath)

            if not import_statement.endswith('\n'):
                import_statement += '\n'

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                return f"Error: Source file {filepath} has invalid syntax before edit: {e}"

            # Check if import is already present by string matching (simple heuristic)
            if import_statement.strip() in [line.strip() for line in content.splitlines()]:
                return f"Import already exists in {filepath}."

            # Find the index to insert the new import
            # Generally after module docstring or future imports
            insert_idx = 0
            lines = content.splitlines(keepends=True)

            # If there are any imports or __future__ imports, we can just insert at line 0 or after the docstring
            # A more robust approach uses ast to find the end of __future__ imports
            last_future_lineno = 0
            for node in tree.body:
                if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                    last_future_lineno = node.lineno

            if last_future_lineno > 0:
                insert_idx = last_future_lineno
            else:
                # Check for module docstring
                if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str):
                    insert_idx = tree.body[0].end_lineno

            new_lines = lines[:insert_idx] + [import_statement] + lines[insert_idx:]
            new_content = "".join(new_lines)

            if not self._parse_and_validate(new_content):
                return "Error: Adding import resulted in invalid syntax. Edit aborted."

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return f"Successfully added import to {filepath}."

        except Exception as e:
            return f"Error in add_import: {e}"
