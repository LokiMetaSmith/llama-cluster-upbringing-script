import os
import re
import fnmatch

class ProjectMapperTool:
    """
    A tool to scan the codebase and generate a high-level map of the project structure,
    including file paths and rough dependency inferences.
    """
    def __init__(self, root_dir: str = "/app"):
        self.root_dir = root_dir
        self.ignore_patterns = [
            ".git", "__pycache__", "node_modules", "venv", ".idea", ".vscode",
            "dist", "build", "*.egg-info", "htmlcov", ".coverage", ".pytest_cache"
        ]

    def _is_ignored(self, path: str) -> bool:
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
        return False

    def scan(self, sub_path: str = ".") -> dict:
        """
        Scans the codebase starting from root_dir/sub_path.
        Returns a dictionary representing the file structure and imports.
        """
        start_dir = os.path.normpath(os.path.join(self.root_dir, sub_path))
        project_map = {
            "root": start_dir,
            "files": [],
            "structure": {}
        }

        for root, dirs, files in os.walk(start_dir):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if not self._is_ignored(os.path.join(root, d))]

            for file in files:
                if self._is_ignored(file):
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start_dir)

                file_info = {
                    "path": rel_path,
                    "type": self._guess_type(file),
                    "imports": self._extract_imports(full_path)
                }
                project_map["files"].append(file_info)

        return project_map

    def _guess_type(self, filename: str) -> str:
        if filename.endswith(".py"): return "python"
        if filename.endswith(".js") or filename.endswith(".ts"): return "javascript"
        if filename.endswith(".yaml") or filename.endswith(".yml"): return "yaml"
        if filename.endswith(".md"): return "markdown"
        return "unknown"

    def _extract_imports(self, filepath: str) -> list:
        imports = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if filepath.endswith(".py"):
                # Simple regex for python imports
                imports.extend(re.findall(r'^import\s+(\w+)', content, re.MULTILINE))
                imports.extend(re.findall(r'^from\s+(\w+)', content, re.MULTILINE))
            elif filepath.endswith(".js") or filepath.endswith(".ts"):
                # Simple regex for JS imports
                imports.extend(re.findall(r'import\s+.*\s+from\s+[\'"](.+)[\'"]', content))
                imports.extend(re.findall(r'require\s*\(\s*[\'"](.+)[\'"]\s*\)', content))

        except Exception:
            pass # Ignore read errors

        return list(set(imports))
