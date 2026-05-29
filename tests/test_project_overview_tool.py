import unittest
import os
import sys

# Add project root to sys.path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipecatapp.tools.project_overview_tool import ProjectOverviewTool

class TestProjectOverviewTool(unittest.TestCase):
    def setUp(self):
        self.tool = ProjectOverviewTool()

    def test_execute(self):
        result = self.tool.execute()
        self.assertIsInstance(result, str)
        self.assertIn("=== Project Root Directory Structure ===", result)
        self.assertIn("=== AGENTS.md ===", result)
        self.assertIn("=== README.md ===", result)
        self.assertIn("=== docs/README.md ===", result)
        self.assertGreater(len(result), 100)  # Should return substantial content

if __name__ == '__main__':
    unittest.main()
