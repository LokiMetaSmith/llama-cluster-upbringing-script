import unittest
from unittest.mock import patch, MagicMock
import os
import json
from pipecatapp.tools.p2p_sync_tool import P2PSyncTool

class TestP2PSyncTool(unittest.TestCase):

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('subprocess.Popen')
    @patch('subprocess.run')
    @patch('requests.get')
    def test_initialize_and_start(self, mock_get, mock_run, mock_popen, mock_getsize, mock_exists, mock_makedirs):
        mock_exists.return_value = True
        mock_getsize.return_value = 6000000  # Assume binary exists and is valid size

        # Mock API key extraction
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            mock_tree = MagicMock()
            mock_root = MagicMock()
            mock_gui = MagicMock()
            mock_apikey = MagicMock()
            mock_apikey.text = "dummy_api_key"

            mock_device = MagicMock()
            mock_device.attrib = {"id": "dummy_device_id"}

            mock_gui.find.return_value = mock_apikey
            mock_root.find.return_value = mock_gui
            mock_root.findall.return_value = [mock_device]
            mock_tree.getroot.return_value = mock_root
            mock_parse.return_value = mock_tree

            # Mock network responses
            mock_ping_res = MagicMock()
            mock_ping_res.status_code = 200

            mock_status_res = MagicMock()
            mock_status_res.json.return_value = {"myID": "dummy_device_id"}

            mock_get.side_effect = [mock_ping_res, mock_status_res]

            tool = P2PSyncTool(name="test_node")
            result = tool.initialize_and_start()

            self.assertIn("Syncthing started successfully", result)
            self.assertIn("dummy_device_id", result)

    @patch('requests.get')
    def test_check_sync_status(self, mock_get):
        # Setup mocks
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = {"completion": 99.5}
        mock_get.return_value = mock_res

        tool = P2PSyncTool()
        tool.process = MagicMock() # Simulate running
        tool.api_key = "dummy"

        result = tool.check_sync_status("peer_id", "folder123")

        self.assertIn("99.50%", result)
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()
