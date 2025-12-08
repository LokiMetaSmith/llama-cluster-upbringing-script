import pytest
import sys
import os
import shutil
import tempfile

# Adjust path to import the tool
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from project_mapper_tool import ProjectMapperTool

class TestProjectMapperTool:
    @pytest.fixture
    def tool(self):
        return ProjectMapperTool()

    @pytest.fixture
    def temp_project(self):
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Create structure:
        # /
        #   main.py
        #   utils.js
        #   README.md
        #   config.yaml
        #   node_modules/ (ignored)
        #     package.json
        #   __pycache__/ (ignored)
        #     main.cpython-38.pyc
        #   src/
        #     api.py

        os.makedirs(os.path.join(temp_dir, "node_modules"))
        os.makedirs(os.path.join(temp_dir, "__pycache__"))
        os.makedirs(os.path.join(temp_dir, "src"))

        # main.py
        with open(os.path.join(temp_dir, "main.py"), "w") as f:
            f.write("import os\nfrom sys import path\nprint('hello')")

        # utils.js
        with open(os.path.join(temp_dir, "utils.js"), "w") as f:
            f.write("import foo from 'bar';\nrequire('baz');")

        # README.md
        with open(os.path.join(temp_dir, "README.md"), "w") as f:
            f.write("# Test Project")

        # config.yaml
        with open(os.path.join(temp_dir, "config.yaml"), "w") as f:
            f.write("key: value")

        # Ignored file in ignored dir
        with open(os.path.join(temp_dir, "node_modules", "package.json"), "w") as f:
            f.write("{}")

        # File in src
        with open(os.path.join(temp_dir, "src", "api.py"), "w") as f:
            f.write("import requests")

        yield temp_dir

        # Cleanup
        shutil.rmtree(temp_dir)

    def test_is_ignored(self, tool):
        assert tool._is_ignored(".git")
        assert tool._is_ignored("node_modules")
        assert tool._is_ignored("__pycache__")
        assert tool._is_ignored("venv")
        assert tool._is_ignored("test.egg-info")
        assert tool._is_ignored(".coverage")

        assert not tool._is_ignored("main.py")
        assert not tool._is_ignored("src")

    def test_guess_type(self, tool):
        assert tool._guess_type("script.py") == "python"
        assert tool._guess_type("app.js") == "javascript"
        assert tool._guess_type("app.ts") == "javascript"
        assert tool._guess_type("config.yaml") == "yaml"
        assert tool._guess_type("config.yml") == "yaml"
        assert tool._guess_type("README.md") == "markdown"
        assert tool._guess_type("unknown.txt") == "unknown"

    def test_extract_imports_python(self, tool, temp_project):
        main_py = os.path.join(temp_project, "main.py")
        imports = tool._extract_imports(main_py)
        assert "os" in imports
        assert "sys" in imports # from sys import ... matches "sys" with the regex `from (\w+)`

    def test_extract_imports_js(self, tool, temp_project):
        utils_js = os.path.join(temp_project, "utils.js")
        imports = tool._extract_imports(utils_js)
        assert "bar" in imports
        assert "baz" in imports

    def test_scan(self, tool, temp_project):
        tool.root_dir = temp_project
        result = tool.scan()

        assert result["root"] == temp_project
        files = result["files"]

        # Check that we found the expected files
        paths = [f["path"] for f in files]
        assert "main.py" in paths
        assert "utils.js" in paths
        assert "README.md" in paths
        assert "config.yaml" in paths
        assert os.path.join("src", "api.py") in paths

        # Check that we ignored the expected files
        assert "node_modules/package.json" not in paths
        assert not any("node_modules" in p for p in paths)
        assert not any("__pycache__" in p for p in paths)

        # Verify details of a specific file
        main_py_info = next(f for f in files if f["path"] == "main.py")
        assert main_py_info["type"] == "python"
        assert "os" in main_py_info["imports"]
