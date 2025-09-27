import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import json
from unittest.mock import patch, mock_open
from reflection import reflect

class TestReflection(unittest.TestCase):

    def test_analyze_failure_out_of_memory(self):
        diagnostic_data = {
            "job_id": "job1",
            "logs": {"stderr": "Some error log with out of memory condition"}
        }
        expected_solution = {
            "analysis": "The job failed due to an out-of-memory error.",
            "action": "increase_memory",
            "parameters": {"job_id": "job1", "memory_mb": 512}
        }
        solution = reflect.analyze_failure_with_llm(diagnostic_data)
        self.assertEqual(solution, expected_solution)

    def test_analyze_failure_exit_code_1(self):
        diagnostic_data = {
            "job_id": "job2",
            "status": "Job finished with exit code 1",
            "logs": {"stderr": "Some other error"}
        }
        expected_solution = {
            "analysis": "The job exited with a non-zero exit code, suggesting a runtime error.",
            "action": "restart",
            "parameters": {"job_id": "job2"}
        }
        solution = reflect.analyze_failure_with_llm(diagnostic_data)
        self.assertEqual(solution, expected_solution)

    def test_analyze_failure_default_case(self):
        diagnostic_data = {
            "job_id": "job3",
            "status": "failed",
            "logs": {"stderr": "An unknown error"}
        }
        expected_solution = {
            "analysis": "The cause of failure could not be determined from the logs. A restart is recommended as a first step.",
            "action": "restart",
            "parameters": {"job_id": "job3"}
        }
        solution = reflect.analyze_failure_with_llm(diagnostic_data)
        self.assertEqual(solution, expected_solution)

    @patch('sys.argv', ['reflect.py', 'test.json'])
    @patch('builtins.open', new_callable=mock_open, read_data='{"job_id": "job4"}')
    @patch('json.load')
    @patch('reflection.reflect.analyze_failure_with_llm')
    @patch('sys.stdout')
    def test_main_success(self, mock_stdout, mock_analyze, mock_json_load, mock_open_file):
        mock_json_load.return_value = {"job_id": "job4"}
        mock_analyze.return_value = {"action": "restart"}
        reflect.main()
        mock_open_file.assert_called_once_with('test.json', 'r')
        mock_analyze.assert_called_once_with({"job_id": "job4"})

    @patch('sys.argv', ['reflect.py'])
    @patch('sys.exit')
    @patch('sys.stdout')
    def test_main_no_args(self, mock_stdout, mock_exit):
        mock_exit.side_effect = SystemExit
        with self.assertRaises(SystemExit):
            reflect.main()
        mock_exit.assert_called_with(1)

    @patch('sys.argv', ['reflect.py', 'nonexistent.json'])
    @patch('builtins.open', side_effect=IOError("File not found"))
    @patch('sys.exit')
    @patch('sys.stdout')
    def test_main_file_not_found(self, mock_stdout, mock_exit, mock_open):
        mock_exit.side_effect = SystemExit
        with self.assertRaises(SystemExit):
            reflect.main()
        mock_exit.assert_called_with(1)

    @patch('sys.argv', ['reflect.py', 'malformed.json'])
    @patch('builtins.open', new_callable=mock_open, read_data='not json')
    @patch('sys.exit')
    @patch('sys.stdout')
    def test_main_malformed_json(self, mock_stdout, mock_exit, mock_open):
        mock_exit.side_effect = SystemExit
        with self.assertRaises(SystemExit):
            reflect.main()
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()