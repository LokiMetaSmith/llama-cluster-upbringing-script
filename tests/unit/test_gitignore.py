import subprocess
import unittest
from pathlib import Path

class TestGitignore(unittest.TestCase):
    def test_temporary_certs_ignored(self):
        """Test that temporary cert directories are ignored by git."""
        repo_root = Path(__file__).resolve().parent.parent.parent
        paths_to_test = [
            ".tmp_certs_nomad/",
            "playbooks/.tmp_certs_nomad/",
            "playbooks/services/.tmp_certs_nomad/",
            ".tmp_certs_consul/",
            "playbooks/.tmp_certs_consul/",
            "playbooks/services/.tmp_certs_consul/",
        ]
        cmd = ["git", "check-ignore", "-v"] + paths_to_test
        result = subprocess.run(
            cmd,
            cwd=str(repo_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, f"git check-ignore failed: {result.stderr}")
        for path in paths_to_test:
            self.assertIn(
                path,
                result.stdout,
                f"Expected {path} to be ignored according to git check-ignore",
            )

if __name__ == "__main__":
    unittest.main()
