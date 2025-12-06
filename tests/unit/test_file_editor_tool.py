import unittest
import os
import shutil
import tempfile
from ansible.roles.pipecatapp.files.tools.file_editor_tool import FileEditorTool

class TestFileEditorTool(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tool = FileEditorTool(root_dir=self.test_dir)
        self.test_file = os.path.join(self.test_dir, "test.txt")
        with open(self.test_file, 'w') as f:
            f.write("Hello\nWorld\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_read_file(self):
        content = self.tool.read_file("test.txt")
        self.assertEqual(content, "Hello\nWorld\n")

    def test_write_file(self):
        result = self.tool.write_file("new.txt", "New Content")
        self.assertIn("Successfully wrote", result)
        with open(os.path.join(self.test_dir, "new.txt"), 'r') as f:
            self.assertEqual(f.read(), "New Content")

    def test_apply_patch(self):
        search = "World"
        replace = "Universe"
        result = self.tool.apply_patch("test.txt", search, replace)
        self.assertIn("Successfully patched", result)
        with open(self.test_file, 'r') as f:
            self.assertEqual(f.read(), "Hello\nUniverse\n")

    def test_apply_patch_fail(self):
        result = self.tool.apply_patch("test.txt", "Missing", "Replace")
        self.assertIn("not found in", result)

    def test_append_file(self):
        result = self.tool.append_to_file("test.txt", "END")
        self.assertIn("Successfully appended", result)
        with open(self.test_file, 'r') as f:
            self.assertEqual(f.read(), "Hello\nWorld\nEND")

if __name__ == '__main__':
    unittest.main()
