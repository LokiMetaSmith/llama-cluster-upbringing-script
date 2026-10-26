import ast
import os
import logging
import re
from typing import Dict, List, Set, Any, Optional

class CodeGraphTool:
    """A tool for querying workspace code structure, caller graphs, blast radius,

    and preflight checks using AST analysis ("Tools over Tokens").
    """

    def __init__(self, root_dir="/opt/pipecatapp"):
        self.name = "code_graph"
        self.root_dir = os.path.realpath(root_dir)
        self.logger = logging.getLogger(__name__)

    def get_schema(self) -> dict:
        """Returns the JSON schema for CodeGraphTool."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": (
                    "Query code structure, blast radius, callers, dependencies, "
                    "and preflight checks without reading full files."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["blast_radius", "preflight", "repository_trace", "repository_tests"],
                            "description": "The code graph action to perform."
                        },
                        "symbol": {
                            "type": "string",
                            "description": "The function, class, or variable symbol to query."
                        },
                        "filepath": {
                            "type": "string",
                            "description": "Target file path relative to workspace root (optional if symbol is unique)."
                        },
                        "max_depth": {
                            "type": "integer",
                            "description": "Maximum depth for dependency tracing (default: 3)."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    async def execute(self, action: str, symbol: str = "", filepath: str = "", max_depth: int = 3, **kwargs) -> str:
        """Executes code graph analysis actions."""
        try:
            if action == "blast_radius":
                if not symbol and not filepath:
                    return "Error: blast_radius action requires 'symbol' or 'filepath'."
                return self.blast_radius(symbol=symbol, filepath=filepath)
            elif action == "preflight":
                if not symbol and not filepath:
                    return "Error: preflight action requires 'symbol' or 'filepath'."
                return self.preflight(symbol=symbol, filepath=filepath)
            elif action == "repository_trace":
                if not symbol and not filepath:
                    return "Error: repository_trace action requires 'symbol' or 'filepath'."
                return self.repository_trace(symbol=symbol, filepath=filepath, max_depth=max_depth)
            elif action == "repository_tests":
                if not symbol and not filepath:
                    return "Error: repository_tests action requires 'symbol' or 'filepath'."
                return self.repository_tests(symbol=symbol, filepath=filepath)
            else:
                return f"Error: Unknown action '{action}'"
        except Exception as e:
            self.logger.error(f"Error executing code_graph action '{action}': {e}", exc_info=True)
            return f"Error executing code graph query: {e}"

    def _validate_path(self, filepath: str) -> str:
        """Validates that filepath is within the root directory."""
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
            raise ValueError(f"Access denied: {filepath} is outside allowed root {self.root_dir}")
        return full_path

    def _scan_py_files(self) -> List[str]:
        """Scans workspace for Python files, ignoring common hidden/build dirs."""
        ignore_dirs = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules", ".liminal", "dist", "build"}
        py_files = []
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))
        return py_files

    def _find_symbol_references(self, symbol: str) -> List[Dict[str, Any]]:
        """Finds all call sites or symbol references across workspace Python files."""
        refs = []
        if not symbol:
            return refs

        py_files = self._scan_py_files()
        pattern = re.compile(rf'\b{re.escape(symbol)}\b')

        for fpath in py_files:
            rel_path = os.path.relpath(fpath, self.root_dir)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                if not pattern.search(content):
                    continue

                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Function/method call
                        func_name = ""
                        if isinstance(node.func, ast.Name):
                            func_name = node.func.id
                        elif isinstance(node.func, ast.Attribute):
                            func_name = node.func.attr

                        if func_name == symbol:
                            refs.append({
                                "file": rel_path,
                                "line": getattr(node, "lineno", 0),
                                "type": "call"
                            })
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        if node.name == symbol:
                            refs.append({
                                "file": rel_path,
                                "line": getattr(node, "lineno", 0),
                                "type": "definition"
                            })
            except Exception:
                continue

        return refs

    def blast_radius(self, symbol: str = "", filepath: str = "") -> str:
        """Calculates blast radius count, affected callers, test files, and risk verdict."""
        refs = self._find_symbol_references(symbol) if symbol else []

        if filepath:
            full_path = self._validate_path(filepath)
            rel_file = os.path.relpath(full_path, self.root_dir)
        else:
            rel_file = ""

        caller_files: Set[str] = set()
        test_files: Set[str] = set()
        call_sites = 0

        for ref in refs:
            f = ref["file"]
            if ref["type"] == "call":
                call_sites += 1
                caller_files.add(f)
                if "test" in f.lower() or f.startswith("tests/"):
                    test_files.add(f)

        if rel_file and rel_file in caller_files:
            caller_files.remove(rel_file)

        # Risk assessment
        total_callers = len(caller_files)
        if total_callers == 0 and call_sites == 0:
            risk = "LOW (symbol has no external callers detected)"
        elif total_callers < 3 and len(test_files) > 0:
            risk = "MODERATE (contained caller count with connected unit tests)"
        elif total_callers >= 3 or len(test_files) == 0:
            risk = "HIGH (multiple external callers or missing test coverage)"
        else:
            risk = "MODERATE"

        output = [
            f"=== Blast Radius Report ===",
            f"Target Symbol: {symbol or '(File-level)'}",
            f"Target File: {rel_file or 'Workspace-wide'}",
            f"Direct Call Sites: {call_sites}",
            f"Affected Caller Files ({len(caller_files)}): " + (", ".join(sorted(caller_files)) if caller_files else "None"),
            f"Connected Test Files ({len(test_files)}): " + (", ".join(sorted(test_files)) if test_files else "None"),
            f"Risk Verdict: {risk}"
        ]
        return "\n".join(output)

    def preflight(self, symbol: str = "", filepath: str = "") -> str:
        """Generates decision-ready preflight checklist before editing a symbol or file."""
        refs = self._find_symbol_references(symbol) if symbol else []
        def_loc = "Unknown"
        docstring = "None"

        if filepath:
            full_path = self._validate_path(filepath)
            rel_file = os.path.relpath(full_path, self.root_dir)
            if os.path.exists(full_path):
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    tree = ast.parse(content)
                    if symbol:
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == symbol:
                                def_loc = f"{rel_file}:{node.lineno}"
                                docstring = ast.get_docstring(node) or "None"
                                break
                    else:
                        def_loc = rel_file
                        docstring = ast.get_docstring(tree) or "None"
                except Exception:
                    pass
        else:
            for ref in refs:
                if ref["type"] == "definition":
                    def_loc = f"{ref['file']}:{ref['line']}"
                    break

        blast = self.blast_radius(symbol=symbol, filepath=filepath)

        output = [
            f"=== Preflight Edit Checklist ===",
            f"Symbol: {symbol or '(N/A)'}",
            f"Definition Location: {def_loc}",
            f"Docstring: {docstring.strip()}",
            "",
            blast
        ]
        return "\n".join(output)

    def repository_trace(self, symbol: str = "", filepath: str = "", max_depth: int = 3) -> str:
        """Traces import and call dependencies starting from a symbol up to max_depth."""
        visited = set()
        trace_lines = []

        def trace(sym: str, depth: int):
            if depth > max_depth or sym in visited:
                return
            visited.add(sym)
            indent = "  " * (depth - 1)
            refs = self._find_symbol_references(sym)
            calls = [r for r in refs if r["type"] == "call"]
            trace_lines.append(f"{indent}- Symbol: {sym} ({len(calls)} call sites)")

            # Trace caller files
            for c in calls[:5]: # Limit fan-out
                trace_lines.append(f"{indent}  ↳ Called in {c['file']}:{c['line']}")

        trace(symbol if symbol else "main", 1)
        return "=== Repository Dependency Trace ===\n" + "\n".join(trace_lines)

    def repository_tests(self, symbol: str = "", filepath: str = "") -> str:
        """Finds all unit test files and test functions referencing the target symbol or file."""
        refs = self._find_symbol_references(symbol) if symbol else []
        test_refs = []

        for ref in refs:
            f = ref["file"]
            if "test" in f.lower() or f.startswith("tests/"):
                test_refs.append(f"{f}:{ref['line']} ({ref['type']})")

        if not test_refs:
            return f"No unit tests found referencing symbol '{symbol}'."

        output = [
            f"=== Connected Repository Tests for '{symbol}' ===",
            *test_refs
        ]
        return "\n".join(output)
