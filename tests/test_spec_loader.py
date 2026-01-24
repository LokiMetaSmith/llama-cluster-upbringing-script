import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from pipecatapp.tools.spec_loader_tool import SpecLoaderTool

class TestSpecLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tool = SpecLoaderTool(work_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("subprocess.run")
    def test_clone_new_repo(self, mock_run):
        repo_url = "https://github.com/test/repo.git"

        # Simulate successful clone by creating a dummy file in the expected path
        def side_effect(*args, **kwargs):
            target_path = os.path.join(self.test_dir, "repo")
            os.makedirs(target_path, exist_ok=True)
            with open(os.path.join(target_path, "README.md"), "w") as f:
                f.write("# Test Repo")
            return MagicMock(returncode=0)

        mock_run.side_effect = side_effect

        result = self.tool.run("clone", repo_url=repo_url)

        self.assertIn("Successfully loaded spec 'repo'", result)
        self.assertIn("Found 1 relevant files", result)

        # Verify subprocess call
        expected_path = os.path.join(self.test_dir, "repo")
        mock_run.assert_called_with(
            ["git", "clone", "--depth", "1", repo_url, expected_path],
            check=True,
            capture_output=True
        )

    def test_list_specs(self):
        # Create some dummy directories
        os.makedirs(os.path.join(self.test_dir, "spec1"))
        os.makedirs(os.path.join(self.test_dir, "spec2"))

        result = self.tool.run("list")
        self.assertIn("spec1", result)
        self.assertIn("spec2", result)

    def test_scan_files_recursive(self):
        target_path = os.path.join(self.test_dir, "complex_repo")
        os.makedirs(os.path.join(target_path, "docs"))

        # Create files
        with open(os.path.join(target_path, "README.md"), "w") as f: f.write("test")
        with open(os.path.join(target_path, "docs", "api.txt"), "w") as f: f.write("test")
        with open(os.path.join(target_path, "ignore.exe"), "w") as f: f.write("binary")

        stats = self.tool._scan_files(target_path)
        self.assertEqual(stats["count"], 2)

if __name__ == "__main__":
    unittest.main()
