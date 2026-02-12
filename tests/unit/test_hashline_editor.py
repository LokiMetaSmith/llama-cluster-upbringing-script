import unittest
import os
import shutil
import tempfile
import hashlib
import sys

# Add parent directory to path to find pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from pipecatapp.tools.file_editor_tool import FileEditorTool

class TestHashlineEditor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tool = FileEditorTool(root_dir=self.test_dir)
        self.test_file_name = "test.txt"
        self.test_file_path = os.path.join(self.test_dir, self.test_file_name)
        self.initial_content = "Line 1\nLine 2\nLine 3"
        with open(self.test_file_path, 'w') as f:
            f.write(self.initial_content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def get_hash(self, s):
        return hashlib.sha256(s.encode('utf-8')).hexdigest()[:2]

    def test_read_with_hashlines(self):
        content = self.tool.read_file(self.test_file_name, use_hashlines=True)

        expected_lines = [
            f"1:{self.get_hash('Line 1')}| Line 1",
            f"2:{self.get_hash('Line 2')}| Line 2",
            f"3:{self.get_hash('Line 3')}| Line 3"
        ]
        self.assertEqual(content, "\n".join(expected_lines))

    def test_apply_hash_edits_replace(self):
        h2 = self.get_hash("Line 2")

        edits = [
            {
                "type": "replace",
                "id": f"2:{h2}",
                "content": "Line 2 Modified"
            }
        ]

        result = self.tool.apply_hash_edits(self.test_file_name, edits)
        self.assertIn("Successfully applied", result)

        with open(self.test_file_path, 'r') as f:
            new_content = f.read()

        expected = "Line 1\nLine 2 Modified\nLine 3"
        self.assertEqual(new_content, expected)

    def test_apply_hash_edits_delete(self):
        h2 = self.get_hash("Line 2")

        edits = [
            {
                "type": "delete",
                "id": f"2:{h2}"
            }
        ]

        result = self.tool.apply_hash_edits(self.test_file_name, edits)
        self.assertIn("Successfully applied", result)

        with open(self.test_file_path, 'r') as f:
            new_content = f.read()

        expected = "Line 1\nLine 3"
        self.assertEqual(new_content, expected)

    def test_apply_hash_edits_insert_after(self):
        h2 = self.get_hash("Line 2")

        edits = [
            {
                "type": "insert_after",
                "id": f"2:{h2}",
                "content": "Line 2.5"
            }
        ]

        result = self.tool.apply_hash_edits(self.test_file_name, edits)
        self.assertIn("Successfully applied", result)

        with open(self.test_file_path, 'r') as f:
            new_content = f.read()

        expected = "Line 1\nLine 2\nLine 2.5\nLine 3"
        self.assertEqual(new_content, expected)

    def test_apply_hash_edits_multiple(self):
        h1 = self.get_hash("Line 1")
        h3 = self.get_hash("Line 3")

        edits = [
            {
                "type": "replace",
                "id": f"1:{h1}",
                "content": "Line 1 Modified"
            },
            {
                "type": "delete",
                "id": f"3:{h3}"
            }
        ]

        result = self.tool.apply_hash_edits(self.test_file_name, edits)
        self.assertIn("Successfully applied", result)

        with open(self.test_file_path, 'r') as f:
            new_content = f.read()

        expected = "Line 1 Modified\nLine 2"
        self.assertEqual(new_content, expected)

    def test_apply_hash_edits_mismatch(self):
        edits = [
            {
                "type": "replace",
                "id": "2:xx", # Wrong hash
                "content": "Should not happen"
            }
        ]

        result = self.tool.apply_hash_edits(self.test_file_name, edits)
        self.assertIn("Error: Hash mismatch", result)

        with open(self.test_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.initial_content)

    def test_apply_hash_edits_range(self):
        h1 = self.get_hash("Line 1")
        h2 = self.get_hash("Line 2")

        edits = [
            {
                "type": "replace_range",
                "id": f"1:{h1}",
                "end_id": f"2:{h2}",
                "content": "Lines 1 and 2 replaced"
            }
        ]

        result = self.tool.apply_hash_edits(self.test_file_name, edits)
        self.assertIn("Successfully applied", result)

        with open(self.test_file_path, 'r') as f:
            new_content = f.read()

        expected = "Lines 1 and 2 replaced\nLine 3"
        self.assertEqual(new_content, expected)

    def test_read_without_hashlines(self):
        content = self.tool.read_file(self.test_file_name, use_hashlines=False)
        self.assertEqual(content, self.initial_content)

if __name__ == '__main__':
    unittest.main()
