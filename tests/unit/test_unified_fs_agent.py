import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Mock fuse module before importing unified_fs_agent
mock_fuse = MagicMock()
mock_fuse.FUSE = MagicMock()
mock_fuse.FuseOSError = Exception
class DummyOperations:
    pass

class DummyLoggingMixIn:
    pass

mock_fuse.Operations = DummyOperations
mock_fuse.LoggingMixIn = DummyLoggingMixIn
sys.modules['fuse'] = mock_fuse

# Add unified_fs agent path to sys.path
agent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles/unified_fs/files'))
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

import unified_fs_agent

class TestUnifiedFSAgent(unittest.TestCase):
    def test_datacache(self):
        cache = unified_fs_agent.DataCache(ttl=1)
        cache.set("key1", "val1")
        self.assertEqual(cache.get("key1"), "val1")
        self.assertIsNone(cache.get("key2"))

    @patch('requests.get')
    def test_consul_backend(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"service1": []}
        mock_get.return_value = mock_resp

        backend = unified_fs_agent.ConsulBackend(base_url="http://localhost:8500/v1")
        services = backend.readdir('/services')
        self.assertIn("service1", services)

    @patch('requests.get')
    def test_memory_backend(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{"event": "test"}]
        mock_get.return_value = mock_resp

        backend = unified_fs_agent.MemoryBackend(base_url="http://localhost:8000")
        events = backend.readdir('/events')
        self.assertEqual(events, ['recent.json'])

    def test_unified_fs_readdir(self):
        ufs = unified_fs_agent.UnifiedFS(root_storage="/tmp")
        root_dirs = ufs.readdir('/', None)
        self.assertIn('consul', root_dirs)
        self.assertIn('memory', root_dirs)
        self.assertIn('fs', root_dirs)

if __name__ == '__main__':
    unittest.main()
