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
        # Don't provide API URL to force discovery
        self.tool = OpenWorkersTool(token="mock-token")

    @patch('requests.delete')
    @patch('requests.put')
    @patch('requests.get')
    def test_run_javascript_full_discovery(self, mock_get, mock_put, mock_delete):
        # Sequence of GET calls:
        # 1. Discover API
        # 2. Discover Runner
        # 3. Execute Runner

        # Mock API Discovery
        api_discovery = MagicMock()
        api_discovery.status_code = 200
        api_discovery.json.return_value = [{"ServiceAddress": "10.0.0.10", "ServicePort": 7100}]

        # Mock Upload (PUT)
        mock_put.return_value.status_code = 200
        mock_put.return_value.text = "Script updated"

        # Mock Runner Discovery
        runner_discovery = MagicMock()
        runner_discovery.status_code = 200
        runner_discovery.json.return_value = [{"ServiceAddress": "10.0.0.50", "ServicePort": 25001}]

        # Mock Execution
        execution_response = MagicMock()
        execution_response.status_code = 200
        execution_response.text = "Hello Dynamic World"

        mock_get.side_effect = [api_discovery, runner_discovery, execution_response]

        code = "console.log('Hello');"
        result = self.tool.run_javascript(code)

        self.assertEqual(result, "Hello Dynamic World")

        # Check API Discovery
        args_api = mock_get.call_args_list[0]
        self.assertIn("/v1/catalog/service/openworkers-api", args_api[0][0])

        # Check Upload URL used discovered API
        args_put = mock_put.call_args
        self.assertRegex(args_put[0][0], r"http://10.0.0.10:7100/api/workers/adhoc-runner-[a-f0-9\-]+/script")

        # Check Runner Discovery
        args_runner = mock_get.call_args_list[1]
        self.assertIn("/v1/catalog/service/openworkers-runner", args_runner[0][0])

        # Check Execution used discovered Runner
        args_exec = mock_get.call_args_list[2]
        self.assertEqual(args_exec[0][0], "http://10.0.0.50:25001")

        # Check Cleanup used discovered API
        args_del = mock_delete.call_args
        self.assertRegex(args_del[0][0], r"http://10.0.0.10:7100/api/workers/adhoc-runner-[a-f0-9\-]+")

if __name__ == '__main__':
    unittest.main()
