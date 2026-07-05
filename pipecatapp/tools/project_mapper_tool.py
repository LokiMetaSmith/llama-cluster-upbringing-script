import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger("ProjectMapperTool")

try:
    from pipecatapp.tools.repo_map_impl.pipeline import extract_all
    from pipecatapp.tools.repo_map_impl.config import load_config
    from pipecatapp.tools.repo_map_impl.discover import discover_files
    from pipecatapp.tools.repo_map_impl.render.json_out import render_json
    HAS_REPO_MAP = True
except ImportError:
    HAS_REPO_MAP = False

from pipecatapp.tools.lightweight_project_mapper_tool import LightweightProjectMapperTool

class ProjectMapperTool:
    """
    A tool to scan the codebase and generate a high-level map of the project structure.
    It uses the sophisticated repo-map implementation (tree-sitter based) when available,
    and falls back to a lightweight regex-based mapper in constrained environments.
    """
    def __init__(self, root_dir: str = "/app"):
        self.root_dir = os.path.realpath(root_dir)
        self.lightweight_mapper = LightweightProjectMapperTool(root_dir=root_dir)

    def scan(self, sub_path: str = ".") -> Dict[str, Any]:
        """
        Scans the codebase starting from root_dir/sub_path.
        Attempts to use the heavy repo-map first, falls back to lightweight if it fails or is unavailable.
        Maintains a consistent interface by returning results in the 'files' key.
        """
        target_dir = os.path.realpath(os.path.join(self.root_dir, sub_path))

        # Security check: Ensure we don't break out of the allowed root
        try:
            common = os.path.commonpath([self.root_dir, target_dir])
        except ValueError:
            common = ""

        if common != self.root_dir:
            raise ValueError(f"Access denied: {sub_path} is outside the allowed root {self.root_dir}")

        if HAS_REPO_MAP:
            try:
                target_path = Path(target_dir)
                config = load_config(target_path)
                paths = discover_files(target_path, extra_exclude_globs=config.exclude_globs)
                files_metadata = extract_all(target_path, paths, enrich_python_files=True)

                json_str = render_json(files_metadata)
                files_data = json.loads(json_str)

                return {
                    "root": target_dir,
                    "files": files_data,
                    "mapper_type": "repo-map-heavy"
                }
            except Exception as e:
                logger.warning(f"Heavy repo-map failed, falling back to lightweight: {e}")

        # Fallback
        res = self.lightweight_mapper.scan(sub_path)
        # LightweightProjectMapperTool already returns {root, files}
        res["mapper_type"] = "lightweight-regex"
        return res

    def run(self, sub_path: str = ".") -> Dict[str, Any]:
        """Standard tool execution method."""
        return self.scan(sub_path)
