import unittest
import os
import shutil
import tempfile
from ansible.roles.pipecatapp.files.tools.file_editor_tool import FileEditorTool

class TestFileEditorSecurity(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tool = FileEditorTool(root_dir=self.test_dir)
        self.sensitive_file = "/etc/hosts" # Should exist on most systems

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_read_file_outside_root(self):
        # Should return an error string, not raise exception
        result = self.tool.read_file(self.sensitive_file)
        # print(f"Read result: {result}")
        self.assertTrue(result.startswith("Error"))
        self.assertIn("Access denied", result)

    def test_write_file_outside_root(self):
        result = self.tool.write_file("../outside.txt", "content")
        # print(f"Write result: {result}")
        self.assertTrue(result.startswith("Error"))
        self.assertIn("Access denied", result)

    def test_apply_patch_outside_root(self):
        result = self.tool.apply_patch("../outside.txt", "search", "replace")
        # print(f"Patch result: {result}")
        self.assertTrue(result.startswith("Error"))
        self.assertIn("Access denied", result)

    def test_append_file_outside_root(self):
        result = self.tool.append_to_file("../outside.txt", "content")
        # print(f"Append result: {result}")
        self.assertTrue(result.startswith("Error"))
        self.assertIn("Access denied", result)

    def test_partial_path_match(self):
        # Test vulnerability where /tmp/test matches /tmp/test_suffix
        # Create a directory that shares a prefix with the allowed root
        # We need to construct this carefully.
        # Let's say root is self.test_dir.
        # We want to access a sibling directory that starts with self.test_dir's name.

        # This is tricky with mkdtemp names, so let's use a specific structure inside test_dir
        safe_dir = os.path.join(self.test_dir, "safe")
        unsafe_dir = os.path.join(self.test_dir, "safe_suffix")

        os.makedirs(safe_dir)
        os.makedirs(unsafe_dir)

        # Initialize tool with safe_dir
        tool = FileEditorTool(root_dir=safe_dir)

        # Try to access unsafe_dir/secret.txt
        secret_file = os.path.join(unsafe_dir, "secret.txt")
        with open(secret_file, 'w') as f:
            f.write("secret")

        # Try to read it using relative path from safe_dir
        # ../safe_suffix/secret.txt
        rel_path = "../safe_suffix/secret.txt"

        result = tool.read_file(rel_path)
        # print(f"Partial match result: {result}")
        self.assertTrue(result.startswith("Error"))
        self.assertIn("Access denied", result)

    def test_symlink_bypass(self):
        # Create a symlink inside root that points outside
        target_file = os.path.join(self.test_dir, "target.txt")
        with open(target_file, 'w') as f:
            f.write("target")

        # Tool root is a subdirectory
        tool_root = os.path.join(self.test_dir, "root")
        os.makedirs(tool_root)
        tool = FileEditorTool(root_dir=tool_root)

        # Create symlink in tool_root -> target_file (which is outside tool_root)
        link_path = os.path.join(tool_root, "link.txt")
        os.symlink(target_file, link_path)

        # Try to read the symlink
        result = tool.read_file("link.txt")
        # print(f"Symlink result: {result}")
        # With realpath check, this should be denied because the resolved path is outside root
        self.assertTrue(result.startswith("Error"))
        self.assertIn("Access denied", result)

if __name__ == '__main__':
    unittest.main()
