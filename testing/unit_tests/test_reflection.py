import unittest
import os
import sys
import json
import io
from unittest.mock import patch, mock_open, MagicMock

# Ensure the project root is in the path to allow `from reflection import reflect`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from reflection import reflect

# Sample LLM config to be returned by the mock
MOCK_LLM_CONFIG = {
    'base_url': 'https://api.fake-openai.com/v1',
    'api_key_env': 'FAKE_API_KEY',
    'model': 'gpt-fake',
    'api_key_plaintext': 'sk-fakekey'
}

class TestReflection(unittest.TestCase):

    @patch('reflection.reflect.load_llm_config', return_value=MOCK_LLM_CONFIG)
    @patch('requests.post')
    @patch('subprocess.run')
    def test_analyze_failure_out_of_memory_with_tool_use(self, mock_subprocess_run, mock_requests_post, mock_load_config):
        """
        Tests the full multi-turn flow:
        1. Initial analysis -> LLM requests a tool.
        2. Tool is run.
        3. Second analysis -> LLM provides the final action.
        """
        # --- Mock Setup ---
        # 1. Mock the first LLM response (requesting a tool)
        mock_response_tool_call = MagicMock()
        mock_response_tool_call.raise_for_status.return_value = None
        mock_response_tool_call.json.return_value = {
            "choices": [{"message": {"content": json.dumps({
                "tool_call": {"name": "get_nomad_job", "parameters": {"job_id": "job1"}}
            })}}]
        }

        # 2. Mock the subprocess call made by the tool runner
        mock_job_spec = {
            "ID": "job1", "Name": "job1",
            "TaskGroups": [{"Tasks": [{"Resources": {"MemoryMB": 256}}]}]
        }
        mock_subprocess_run.return_value.stdout = json.dumps(mock_job_spec)
        mock_subprocess_run.return_value.stderr = ""
        mock_subprocess_run.return_value.returncode = 0

        # 3. Mock the second LLM response (providing the final action)
        mock_response_final_action = MagicMock()
        mock_response_final_action.raise_for_status.return_value = None
        mock_response_final_action.json.return_value = {
            "choices": [{"message": {"content": json.dumps({
                "analysis": "Job failed due to OOM. Increased memory.",
                "action": "increase_memory",
                "parameters": {"job_id": "job1", "memory_mb": 512}
            })}}]
        }

        mock_requests_post.side_effect = [mock_response_tool_call, mock_response_final_action]

        # --- Test Execution ---
        diagnostic_data = {
            "job_id": "job1",
            "logs": {"stderr": "some error log with out of memory condition"}
        }
        solution = reflect.analyze_failure_with_llm(diagnostic_data)

        # --- Assertions ---
        self.assertEqual(mock_requests_post.call_count, 2)
        mock_subprocess_run.assert_called_once()
        self.assertEqual(solution["action"], "increase_memory")
        self.assertEqual(solution["parameters"]["job_id"], "job1")
        self.assertEqual(solution["parameters"]["memory_mb"], 512)

    @patch('reflection.reflect.load_llm_config', return_value=MOCK_LLM_CONFIG)
    @patch('requests.post')
    def test_analyze_failure_simple_restart(self, mock_requests_post, mock_load_config):
        """
        Tests the single-turn flow where the LLM can decide an action immediately.
        """
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": json.dumps({
                "analysis": "The job exited with a non-zero exit code...",
                "action": "restart",
                "parameters": {"job_id": "job2"}
            })}}]
        }
        mock_requests_post.return_value = mock_response

        diagnostic_data = {
            "job_id": "job2",
            "status": "Job finished with exit code 1",
            "logs": {"stderr": "Some other error"}
        }
        solution = reflect.analyze_failure_with_llm(diagnostic_data)

        mock_requests_post.assert_called_once()
        self.assertEqual(solution["action"], "restart")
        self.assertEqual(solution["parameters"]["job_id"], "job2")

    @patch('sys.argv', ['reflect.py', 'test.json'])
    @patch('builtins.open', new_callable=mock_open, read_data='{"job_id": "job4"}')
    @patch('json.load')
    @patch('reflection.reflect.analyze_failure_with_llm')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_success(self, mock_stdout, mock_analyze, mock_json_load, mock_open_file):
        mock_json_load.return_value = {"job_id": "job4"}
        mock_analyze.return_value = {"action": "restart", "parameters": {"job_id": "job4"}}

        reflect.main()

        mock_open_file.assert_called_with('test.json', 'r')
        mock_analyze.assert_called_once_with({"job_id": "job4"})
        self.assertIn('"action": "restart"', mock_stdout.getvalue())

    @patch('sys.argv', ['reflect.py'])
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit):
        # The function should call sys.exit(1)
        mock_exit.side_effect = SystemExit(1)
        with self.assertRaises(SystemExit) as cm:
            reflect.main()
        self.assertEqual(cm.exception.code, 1)

    @patch('sys.argv', ['reflect.py', 'nonexistent.json'])
    @patch('builtins.open', side_effect=IOError("File not found"))
    @patch('sys.exit')
    def test_main_file_not_found(self, mock_exit, mock_open):
        mock_exit.side_effect = SystemExit(1)
        with self.assertRaises(SystemExit) as cm:
            reflect.main()
        self.assertEqual(cm.exception.code, 1)

    @patch('sys.argv', ['reflect.py', 'malformed.json'])
    @patch('builtins.open', new_callable=mock_open, read_data='not a valid json')
    @patch('sys.exit')
    def test_main_malformed_json(self, mock_exit, mock_open):
        mock_exit.side_effect = SystemExit(1)
        with self.assertRaises(SystemExit) as cm:
            reflect.main()
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()