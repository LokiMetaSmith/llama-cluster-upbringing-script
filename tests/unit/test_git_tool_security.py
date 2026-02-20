import unittest
from unittest.mock import patch
from pipecatapp.tools.git_tool import Git_Tool

class TestGitToolSecurity(unittest.TestCase):
    def setUp(self):
        self.tool = Git_Tool()

    def test_allowed_protocols(self):
        """Test that safe protocols are allowed."""
        safe_urls = [
            "https://github.com/example/repo.git",
            "http://example.com/repo.git",
            "ssh://user@host/path/to/repo.git",
            "git://github.com/example/repo.git",
            "git@github.com:user/repo.git"
        ]
        for url in safe_urls:
            try:
                self.tool._validate_protocol(url)
            except ValueError:
                self.fail(f"Safe URL '{url}' was blocked.")

    def test_blocked_protocols(self):
        """Test that dangerous protocols are blocked."""
        dangerous_urls = [
            "file:///etc/passwd",
            "file:/etc/passwd",
            "ext::sh -c touch /tmp/pwn",
            "ftp://example.com/repo.git",
            "gopher://example.com/repo.git",
            "/etc/passwd", # Local path (implicit file://)
            "C:\\Windows\\System32\\cmd.exe" # Windows path
        ]
        for url in dangerous_urls:
            with self.assertRaises(ValueError, msg=f"Dangerous URL '{url}' was NOT blocked"):
                self.tool._validate_protocol(url)

    @patch("pipecatapp.tools.git_tool.subprocess.run")
    def test_clone_with_dangerous_protocol(self, mock_run):
        """Test that clone method respects protocol validation."""
        # This should return the error string, not raise exception (as per implementation)
        result = self.tool.clone("file:///etc/passwd", "dest")
        self.assertIn("Security Error: Protocol not allowed", result)
        mock_run.assert_not_called()

if __name__ == "__main__":
    unittest.main()
