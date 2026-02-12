import os
import shutil
import pytest
import sys

# Ensure pipecatapp is in path
sys.path.append(os.getcwd())

from pipecatapp.tools.search_tool import SearchTool

class TestSearchToolSecurity:

    @pytest.fixture
    def setup_search_env(self, tmp_path):
        base_dir = tmp_path / "search_root"
        secret_dir = tmp_path / "secret_dir"
        base_dir.mkdir()
        secret_dir.mkdir()

        (base_dir / "safe.txt").write_text("This is safe content.")
        (secret_dir / "secret.txt").write_text("SECRET_DATA")

        # Symlink pointing outside
        try:
            (base_dir / "link_to_secret").symlink_to(secret_dir)
        except OSError:
            pytest.skip("Symlinks not supported")

        return base_dir, secret_dir

    def test_search_inside_root(self, setup_search_env):
        base_dir, _ = setup_search_env
        tool = SearchTool(root_dir=str(base_dir))

        # Should find safe content
        result = tool.grep("safe content", path="safe.txt")
        # Filename is not included when searching a single file without -H
        assert "This is safe content" in result

    def test_search_traversal_via_symlink(self, setup_search_env):
        base_dir, _ = setup_search_env
        tool = SearchTool(root_dir=str(base_dir))

        # Should be blocked
        result = tool.grep("SECRET_DATA", path="link_to_secret")
        assert "Access denied" in result or "outside allowed root" in result
        assert "SECRET_DATA" not in result

    def test_find_traversal_via_symlink(self, setup_search_env):
        base_dir, _ = setup_search_env
        tool = SearchTool(root_dir=str(base_dir))

        # Should be blocked
        result = tool.find_file("secret.txt", path="link_to_secret")
        assert "Access denied" in result or "outside allowed root" in result
