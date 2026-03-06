import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Mock out external dependencies so we don't need them installed
sys.modules['uvicorn'] = MagicMock()
sys.modules['paramiko'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['docker'] = MagicMock()
sys.modules['llm_sandbox'] = MagicMock()
sys.modules['playwright'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['faiss'] = MagicMock()

# Mock tools before importing
sys.modules['tools.ssh_tool'] = MagicMock()
sys.modules['tools.desktop_control_tool'] = MagicMock()
sys.modules['tools.code_runner_tool'] = MagicMock()
sys.modules['tools.web_browser_tool'] = MagicMock()
sys.modules['tools.ansible_tool'] = MagicMock()
sys.modules['tools.power_tool'] = MagicMock()
sys.modules['tools.summarizer_tool'] = MagicMock()
sys.modules['tools.term_everything_tool'] = MagicMock()
sys.modules['tools.rag_tool'] = MagicMock()
sys.modules['tools.ha_tool'] = MagicMock()
sys.modules['tools.git_tool'] = MagicMock()
sys.modules['tools.orchestrator_tool'] = MagicMock()
sys.modules['tools.search_tool'] = MagicMock()

# Now we can import the tool server safely
from fastapi.testclient import TestClient

with patch.dict('os.environ', {'TOOL_SERVER_API_KEY': 'test-key'}):
    with patch.dict('sys.modules'):
        import tool_server

        # Manually reset the API_KEY as it was evaluated during module load
        # before the mock if not mocked properly
        tool_server.API_KEY = "test-key"

        client = TestClient(tool_server.app)

class TestToolServer(unittest.TestCase):
    def test_run_tool_valid_auth(self):
        with patch.dict(tool_server.tools, {'search': MagicMock(grep=MagicMock(return_value="found"))}):
            response = client.post("/run_tool/", json={"tool": "search", "method": "grep", "args": {"pattern": "def test"}}, headers={"Authorization": "Bearer test-key"})
            self.assertEqual(response.status_code, 200)

    def test_run_tool_invalid_auth(self):
        response = client.post("/run_tool/", json={"tool": "search", "method": "grep", "args": {"pattern": "def test"}}, headers={"Authorization": "Bearer invalid-key"})
        self.assertEqual(response.status_code, 403)

    def test_run_tool_missing_auth(self):
        response = client.post("/run_tool/", json={"tool": "search", "method": "grep", "args": {"pattern": "def test"}})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
