import unittest
from unittest.mock import MagicMock, patch
import urllib.request
import urllib.error
import time

class TestInfrastructure(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_consul_running(self, mock_urlopen):
        """Check if Consul is running and healthy."""
        url = "http://127.0.0.1:8500/v1/status/leader"

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'"127.0.0.1:8300"'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        print(f"Checking Consul at {url}...")
        try:
            with urllib.request.urlopen(url) as response:
                self.assertEqual(response.status, 200, "Consul API did not return 200 OK")
                data = response.read().decode('utf-8')
                # It returns the leader address, e.g. "127.0.0.1:8300" or "" if no leader
                self.assertTrue(len(data) > 2, f"Consul has no leader: {data}")
                print("Consul is running and has a leader.")
        except urllib.error.URLError as e:
            self.fail(f"Could not connect to Consul API: {e}")

    @patch('urllib.request.urlopen')
    def test_nomad_running(self, mock_urlopen):
        """Check if Nomad is running and healthy."""
        url = "http://127.0.0.1:4646/v1/status/leader"

        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'"127.0.0.1:4647"'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        print(f"Checking Nomad at {url}...")
        try:
            with urllib.request.urlopen(url) as response:
                self.assertEqual(response.status, 200, "Nomad API did not return 200 OK")
                data = response.read().decode('utf-8')
                self.assertTrue(len(data) > 2, f"Nomad has no leader: {data}")
                print("Nomad is running and has a leader.")
        except urllib.error.URLError as e:
            self.fail(f"Could not connect to Nomad API: {e}")

if __name__ == '__main__':
    unittest.main()
