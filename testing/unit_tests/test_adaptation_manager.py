import unittest
import os
import json
import subprocess
import sys
from unittest.mock import patch, mock_open

# Ensure the reflection directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'reflection')))

class TestAdaptationManagerWithLLM(unittest.TestCase):

    def setUp(self):
        """Set up a dummy diagnostics file content."""
        self.diagnostics_data = {
            "job_id": "test-job-xyz",
            "logs": {"stderr": "Critical error: Task failed successfully."}
        }
        self.diagnostics_json = json.dumps(self.diagnostics_data)

    @patch('adaptation_manager.requests.post')
    @patch('adaptation_manager.subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_main_flow_with_llm_mock(self, mock_builtin_open, mock_subprocess_run, mock_requests_post):
        """Test the main flow, mocking the LLM API call."""
        import adaptation_manager

        # --- Mock Setup ---
        mock_read_handle = mock_open(read_data=self.diagnostics_json).return_value
        mock_write_handle = mock_open().return_value
        mock_builtin_open.side_effect = [mock_read_handle, mock_write_handle]

        # Define the expected content without the markdown wrapper
        llm_response_content = """tests:
  - name: test_reproduce_critical_error
    description: "Test generated from LLM based on job test-job-xyz"
    steps:
      - action: special_trigger
        payload:
          context: "Critical error: Task failed successfully."
"""
        # Mock the full LLM response, including the markdown wrapper with a correct newline
        mock_full_response = f"```yaml\n{llm_response_content}```"
        mock_requests_post.return_value.status_code = 200
        mock_requests_post.return_value.json.return_value = {
            'choices': [{'message': {'content': mock_full_response}}]
        }

        # Mock the subprocess call to be successful
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="Evolution complete.", stderr=""
        )

        # Mock the configuration loading
        dummy_config = {
            'model': 'grok/llama-test', 'base_url': 'https://api.test.com/v1',
            'api_key_env': 'TEST_API_KEY', 'api_key_plaintext': 'dummy-key'
        }
        with patch('adaptation_manager.load_llm_config', return_value=dummy_config):
            # --- Execution ---
            test_args = ['adaptation_manager.py', 'dummy_diagnostics.json']
            with patch.object(sys, 'argv', test_args):
                adaptation_manager.main()

        # --- Assertions ---
        # 1. Verify diagnostics file was read
        mock_builtin_open.assert_any_call('dummy_diagnostics.json', 'r')

        # 2. Verify the test case file was written with the *unwrapped* content
        expected_test_case_path = "/tmp/test_case_dummy_diagnostics.json.yaml"
        mock_builtin_open.assert_any_call(expected_test_case_path, 'w')
        mock_write_handle.write.assert_called_once_with(llm_response_content)

        # 3. Verify that the evolution script was called correctly
        mock_subprocess_run.assert_called_once()
        called_command = mock_subprocess_run.call_args[0][0]
        self.assertIn('prompt_engineering/evolve.py', called_command)
        self.assertIn(expected_test_case_path, called_command)

if __name__ == '__main__':
    unittest.main()
