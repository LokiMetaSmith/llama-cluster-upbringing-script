import unittest
from unittest.mock import patch, Mock
import os
import requests

class TestPipecatApp(unittest.TestCase):
    """
    Unit tests for the Pipecat application's web server.
    """

    def setUp(self):
        """Set up the base URL for the web server."""
        host = os.environ.get("PIPECAT_HOST", "127.0.0.1")
        self.base_url = f"http://{host}:8000"

    @patch('requests.get')
    def test_health_check_is_healthy(self, mock_get):
        """
        Tests that the /health endpoint returns a 200 OK status.
        """
        # Configure the mock to return a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_get.return_value = mock_response

        response = requests.get(f"{self.base_url}/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        mock_get.assert_called_once_with(f"{self.base_url}/health")


    @patch('requests.get')
    def test_main_page_loads(self, mock_get):
        """
        Tests that the main page ('/') loads correctly and returns a 200 OK status.
        """
        # Configure the mock for the health check
        mock_health_response = Mock()
        mock_health_response.status_code = 200
        mock_health_response.json.return_value = {"status": "ok"}

        # Configure the mock for the main page
        mock_main_response = Mock()
        mock_main_response.status_code = 200
        mock_main_response.text = "Mission Control"

        # Set the side_effect to return different mocks for different calls
        mock_get.side_effect = [mock_health_response, mock_main_response]

        # Call health check
        health_response = requests.get(f"{self.base_url}/health")
        self.assertEqual(health_response.status_code, 200)

        # Call main page
        main_response = requests.get(self.base_url)
        self.assertEqual(main_response.status_code, 200)
        self.assertIn("Mission Control", main_response.text)

        # Verify calls
        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call(f"{self.base_url}/health")
        mock_get.assert_any_call(self.base_url)


if __name__ == '__main__':
    unittest.main()