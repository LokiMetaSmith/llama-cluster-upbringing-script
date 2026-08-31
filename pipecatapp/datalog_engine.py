import ast
import os
from typing import List, Dict, Any

class DatalogEngine:
    """
    Lemmalog Datalog Program Analysis Engine.
    Parses Python source code into relational facts (calls, definitions, imports)
    and executes Datalog rules for dependency analysis and call graph querying.
    """
    def __init__(self):
        self.facts: Dict[str, List[tuple]] = {
            "defines_function": [],   # (file, func_name, lineno)
            "calls_function": [],     # (file, caller_func, callee_func, lineno)
            "imports_module": [],     # (file, imported_module)
            "defines_class": [],      # (file, class_name, lineno)
        }

    def index_file(self, filepath: str, code_content: str = None) -> Dict[str, Any]:
        """Parses Python AST and populates Datalog facts."""
        if code_content is None:
            if not os.path.exists(filepath):
                return {"error": f"File {filepath} not found."}
            with open(filepath, "r", encoding="utf-8") as f:
                code_content = f.read()

        try:
            tree = ast.parse(code_content, filename=filepath)
        except Exception as e:
            return {"error": f"Failed to parse AST: {e}"}

        rel_path = filepath
        current_func = "<global>"

        class ASTVisitor(ast.NodeVisitor):
            def __init__(visitor_self):
                visitor_self.scope_stack = ["<global>"]

            def visit_FunctionDef(visitor_self, node):
                func_name = node.name
                self.facts["defines_function"].append((rel_path, func_name, node.lineno))
                visitor_self.scope_stack.append(func_name)
                visitor_self.generic_visit(node)
                visitor_self.scope_stack.pop()

            def visit_AsyncFunctionDef(visitor_self, node):
                visitor_self.visit_FunctionDef(node)

            def visit_ClassDef(visitor_self, node):
                self.facts["defines_class"].append((rel_path, node.name, node.lineno))
                visitor_self.generic_visit(node)

            def visit_Call(visitor_self, node):
                caller = visitor_self.scope_stack[-1]
                callee = None
                if isinstance(node.func, ast.Name):
                    callee = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    callee = node.func.attr
                if callee:
                    self.facts["calls_function"].append((rel_path, caller, callee, getattr(node, 'lineno', 0)))
                visitor_self.generic_visit(node)

            def visit_Import(visitor_self, node):
                for alias in node.names:
                    self.facts["imports_module"].append((rel_path, alias.name))
                visitor_self.generic_visit(node)

            def visit_ImportFrom(visitor_self, node):
                if node.module:
                    self.facts["imports_module"].append((rel_path, node.module))
                visitor_self.generic_visit(node)

        visitor = ASTVisitor()
        visitor.visit(tree)

        return {
            "indexed_file": rel_path,
            "defines_count": len(self.facts["defines_function"]),
            "calls_count": len(self.facts["calls_function"]),
            "imports_count": len(self.facts["imports_module"])
        }

    def query_callers(self, target_function: str) -> List[Dict[str, Any]]:
        """Finds all functions that call target_function."""
        results = []
        for file, caller, callee, lineno in self.facts["calls_function"]:
            if callee == target_function:
                results.append({
                    "file": file,
                    "caller": caller,
                    "lineno": lineno
                })
        return results

    def query_transitive_calls(self, start_function: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Datalog transitive closure: finds all functions transitively reachable from start_function."""
        visited = set()
        call_chain = []

        def dfs(current: str, depth: int, path: List[str]):
            if depth > max_depth or current in visited:
                return
            visited.add(current)
            for file, caller, callee, lineno in self.facts["calls_function"]:
                if caller == current and callee not in path:
                    new_path = path + [callee]
                    call_chain.append({
                        "caller": current,
                        "callee": callee,
                        "depth": depth,
                        "file": file,
                        "lineno": lineno,
                        "path": new_path
                    })
                    dfs(callee, depth + 1, new_path)

        dfs(start_function, 1, [start_function])
        return call_chain

    def explain(self, target_symbol: str) -> Dict[str, Any]:
        """Provides a complete structural explanation of a symbol (defines, callers, callees, imports)."""
        defines = [f for f in self.facts["defines_function"] if f[1] == target_symbol]
        callers = self.query_callers(target_symbol)
        transitive_callees = self.query_transitive_calls(target_symbol)

        return {
            "symbol": target_symbol,
            "definitions": [{"file": f[0], "lineno": f[2]} for f in defines],
            "direct_callers": callers,
            "transitive_call_graph": transitive_callees
        }
