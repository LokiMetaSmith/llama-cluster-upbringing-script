import os
import logging
import shutil
import subprocess
import glob
from typing import List, Optional

class SpecLoaderTool:
    """
    A tool for cloning external Git repositories (e.g., documentation, specifications)
    and ingesting them into the agent's context or memory.
    """
    def __init__(self, work_dir: str = "/opt/pipecatapp/specs", memory_interface=None):
        self.work_dir = work_dir
        self.memory_interface = memory_interface
        self.logger = logging.getLogger(__name__)

        if not os.path.exists(self.work_dir):
            try:
                os.makedirs(self.work_dir)
            except OSError as e:
                self.logger.error(f"Failed to create spec directory: {e}")

    def _validate_protocol(self, url: str):
        """Validates that the URL uses a safe protocol."""
        if not url:
            return
        allowed_protocols = ("http://", "https://", "ssh://", "git://", "git@")
        if not any(url.startswith(proto) for proto in allowed_protocols):
            raise ValueError(f"Security Error: Protocol not allowed for URL '{url}'. Allowed protocols: http, https, ssh, git.")

    def _validate_arg(self, arg: str, arg_name: str):
        """Validates that an argument does not start with a dash to prevent injection."""
        if arg and arg.startswith("-"):
            raise ValueError(f"Security Error: Argument '{arg_name}' cannot start with '-'. Invalid value: {arg}")

    def _validate_path(self, path: str) -> str:
        """Ensures the path is within the work directory."""
        full_path = os.path.abspath(os.path.join(self.work_dir, path))
        try:
            common = os.path.commonpath([os.path.abspath(self.work_dir), full_path])
        except ValueError:
            common = ""

        if common != os.path.abspath(self.work_dir):
            raise ValueError(f"Security Error: Access denied: {path} is outside the allowed directory {self.work_dir}")
        return full_path

    def run(self, action: str, repo_url: str = None, repo_name: str = None) -> str:
        """
        Executes the spec loader action.

        Args:
            action (str): 'clone' or 'list'.
            repo_url (str): URL of the git repository.
            repo_name (str): Optional name for the local directory.
        """
        if action == "clone":
            return self.clone_and_ingest(repo_url, repo_name)
        elif action == "list":
            return self.list_specs()
        else:
            return f"Unknown action: {action}"

    def clone_and_ingest(self, repo_url: str, repo_name: str = None) -> str:
        if not repo_url:
            return "Error: repo_url is required for clone action."

        try:
            self._validate_protocol(repo_url)
            self._validate_arg(repo_url, "repo_url")
            if repo_name:
                 self._validate_arg(repo_name, "repo_name")
        except ValueError as e:
            return str(e)

        if not repo_name:
            # Infer name from URL
            repo_name = repo_url.split("/")[-1].replace(".git", "")

        try:
            # Validate target path to prevent traversal
            # We pass repo_name because _validate_path joins it with work_dir
            target_path = self._validate_path(repo_name)
        except ValueError as e:
            return str(e)

        # 1. Clone or Pull
        if os.path.exists(target_path):
            self.logger.info(f"Updating existing spec repo: {repo_name}")
            try:
                subprocess.run(["git", "-C", target_path, "pull"], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                return f"Failed to pull repo: {e.stderr.decode()}"
        else:
            self.logger.info(f"Cloning new spec repo: {repo_url}")
            try:
                subprocess.run(["git", "clone", "--depth", "1", repo_url, target_path], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                return f"Failed to clone repo: {e.stderr.decode()}"

        # 2. Ingest (Simple text scan for now)
        # In a full RAG system, this would push to vector DB.
        # Here we just index the files found for the agent to read later.
        file_stats = self._scan_files(target_path)

        return f"Successfully loaded spec '{repo_name}'. Found {file_stats['count']} relevant files. Path: {target_path}"

    def list_specs(self) -> str:
        if not os.path.exists(self.work_dir):
            return "No specs directory found."

        repos = [d for d in os.listdir(self.work_dir) if os.path.isdir(os.path.join(self.work_dir, d))]
        return f"Loaded Specs: {', '.join(repos)}"

    def _scan_files(self, path: str) -> dict:
        """Scans for readable documentation files."""
        count = 0
        extensions = ['*.md', '*.txt', '*.rst', '*.html']

        for ext in extensions:
            # Recursive glob
            files = glob.glob(os.path.join(path, '**', ext), recursive=True)
            count += len(files)

        return {"count": count}
