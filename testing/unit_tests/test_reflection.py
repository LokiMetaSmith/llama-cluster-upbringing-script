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
        solution = reflect.analyze_failure_with_llm(diagnostic_data)
        self.assertIn("analysis", solution)
        self.assertIn("action", solution)
        self.assertIn("parameters", solution)
        self.assertEqual(solution["action"], "increase_memory")
        self.assertIn("job_id", solution["parameters"])
        self.assertIn("memory_mb", solution["parameters"])
        self.assertEqual(solution["parameters"]["job_id"], "job1")

    def test_analyze_failure_exit_code_1(self):
        diagnostic_data = {
            "job_id": "job2",
            "status": "Job finished with exit code 1",
            "logs": {"stderr": "Some other error"}
        }
        solution = reflect.analyze_failure_with_llm(diagnostic_data)
        self.assertIn("analysis", solution)
        self.assertIn("action", solution)
        self.assertIn("parameters", solution)
        self.assertEqual(solution["action"], "restart")
        self.assertIn("job_id", solution["parameters"])
        self.assertEqual(solution["parameters"]["job_id"], "job2")

    def test_analyze_failure_default_case(self):
        diagnostic_data = {
            "job_id": "job3",
            "status": "failed",
            "logs": {"stderr": "An unknown error"}
        }
        solution = reflect.analyze_failure_with_llm(diagnostic_data)
        self.assertIn("analysis", solution)
        self.assertIn("action", solution)
        self.assertIn("parameters", solution)
        self.assertEqual(solution["action"], "restart")
        self.assertIn("job_id", solution["parameters"])
        self.assertEqual(solution["parameters"]["job_id"], "job3")

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