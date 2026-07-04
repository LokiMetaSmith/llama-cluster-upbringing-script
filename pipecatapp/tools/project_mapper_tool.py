import os
import json
from pathlib import Path
from typing import Optional, Dict, Any

from pipecatapp.tools.repo_map_impl.pipeline import extract_all
from pipecatapp.tools.repo_map_impl.config import RepoMapConfig, load_config
from pipecatapp.tools.repo_map_impl.discover import discover_files
from pipecatapp.tools.repo_map_impl.render.json_out import render_json

class ProjectMapperTool:
    """
    A tool to scan the codebase and generate a high-level map of the project structure,
    now using the upgraded repo-map implementation for richer metadata and deterministic results.
    """
    def __init__(self, root_dir: str = "/app"):
        self.root_dir = os.path.realpath(root_dir)

    def scan(self, sub_path: str = ".") -> Dict[str, Any]:
        """
        Scans the codebase starting from root_dir/sub_path.
        Returns a dictionary representing the file structure and intelligence catalog.
        """
        target_dir = os.path.realpath(os.path.join(self.root_dir, sub_path))

        # Security check: Ensure we don't break out of the allowed root
        try:
            common = os.path.commonpath([self.root_dir, target_dir])
        except ValueError:
            common = ""

        if common != self.root_dir:
            raise ValueError(f"Access denied: {sub_path} is outside the allowed root {self.root_dir}")

        target_path = Path(target_dir)

        try:
            config = load_config(target_path)
            # Override with defaults if needed
            paths = discover_files(target_path, extra_exclude_globs=config.exclude_globs)
            files = extract_all(target_path, paths, enrich_python_files=True)

            json_str = render_json(files)
            json_data = json.loads(json_str)

            return {
                "root": target_dir,
                "map_data": json_data
            }
        except Exception as e:
            return {
                "root": target_dir,
                "error": f"Failed to generate repo map: {str(e)}"
            }

    def run(self, sub_path: str = ".") -> Dict[str, Any]:
        """Standard tool execution method."""
        return self.scan(sub_path)
