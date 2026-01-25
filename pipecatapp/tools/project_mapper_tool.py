import os
import re
import fnmatch
import subprocess
import shutil
from typing import Optional, List

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

        # Optimization: Use git ls-files if available to avoid slow os.walk
        git_files = self._list_files_git(start_dir)
        if git_files is not None:
            for rel_path in git_files:
                full_path = os.path.join(start_dir, rel_path)
                # Still check ignores in case git tracks files we want to skip
                if self._is_ignored(full_path):
                    continue

                file_info = {
                    "path": rel_path,
                    "type": self._guess_type(rel_path),
                    "imports": self._extract_imports(full_path)
                }
                project_map["files"].append(file_info)
            return project_map

        # Fallback to os.walk
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

    def _list_files_git(self, start_dir: str) -> Optional[List[str]]:
        """Lists files using git ls-files if possible. Returns None if not a git repo."""
        if not shutil.which("git"):
            return None

        try:
            # Check if inside git repo
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                           cwd=start_dir, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # git ls-files returns paths relative to cwd
            res = subprocess.run(["git", "ls-files"], cwd=start_dir, check=True, capture_output=True, text=True)
            files = res.stdout.splitlines()
            return files
        except Exception:
            return None

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
