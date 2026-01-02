import unittest
from unittest.mock import MagicMock, patch, ANY
import os
import sys
import requests
import re

# Add the tools directory to sys.path so we can import the tool
sys.path.append(os.path.join(os.path.dirname(__file__), '../../ansible/roles/pipecatapp/files/tools'))

from open_workers_tool import OpenWorkersTool

class TestOpenWorkersTool(unittest.TestCase):

    def setUp(self):
        self.tool = OpenWorkersTool(api_url="http://mock-api:7000", token="mock-token")

    @patch('requests.delete')
    @patch('requests.put')
    @patch('requests.get')
    def test_run_javascript_success(self, mock_get, mock_put, mock_delete):
        # Mock successful script upload
        mock_put.return_value.status_code = 200
        mock_put.return_value.text = "Script updated"

        # Mock successful execution
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Hello from OpenWorkers"

        code = "console.log('Hello from OpenWorkers');"
        result = self.tool.run_javascript(code)

        self.assertEqual(result, "Hello from OpenWorkers")

        # Verify calls
        mock_put.assert_called_once()
        args, kwargs = mock_put.call_args
        self.assertRegex(args[0], r"http://mock-api:7000/api/workers/adhoc-runner-[a-f0-9\-]+/script")

        mock_get.assert_called_once()

        # Verify Cleanup
        mock_delete.assert_called_once()
        args_del, kwargs_del = mock_delete.call_args
        self.assertRegex(args_del[0], r"http://mock-api:7000/api/workers/adhoc-runner-[a-f0-9\-]+")

    @patch('requests.delete')
    @patch('requests.put')
    def test_run_javascript_upload_fail(self, mock_put, mock_delete):
        mock_put.return_value.status_code = 500
        mock_put.return_value.text = "Internal Server Error"

        result = self.tool.run_javascript("code")
        self.assertIn("Error uploading script", result)

        # Should still try to delete (or at least hit finally block)
        # Note: If upload fails, the worker might not exist, but our code tries to delete `worker_name` anyway
        # which is fine as "best effort".
        mock_delete.assert_called_once()

    @patch('requests.delete')
    @patch('requests.put')
    @patch('requests.get')
    def test_run_javascript_exec_exception(self, mock_get, mock_put, mock_delete):
        mock_put.return_value.status_code = 200
        mock_get.side_effect = requests.exceptions.RequestException("Connection refused")

        result = self.tool.run_javascript("code")
        self.assertIn("Network error", result)

        # Cleanup should happen
        mock_delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()
