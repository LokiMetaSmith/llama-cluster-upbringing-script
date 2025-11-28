import unittest
from unittest.mock import patch, mock_open
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import supervisor
import json
import subprocess

class TestSupervisor(unittest.TestCase):

    @patch('subprocess.run')
    def test_run_playbook_success(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="Playbook success", stderr="")
        self.assertTrue(supervisor.run_playbook("test.yaml"))
        mock_run.assert_called_with(["ansible-playbook", "test.yaml"], capture_output=True, text=True)

    @patch('subprocess.run')
    def test_run_playbook_failure(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="Playbook failure", stderr="Error")
        self.assertFalse(supervisor.run_playbook("test.yaml"))

    @patch('subprocess.run')
    def test_run_playbook_with_extra_vars(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="Playbook success", stderr="")
        extra_vars = {"key": "value"}
        self.assertTrue(supervisor.run_playbook("test.yaml", extra_vars=extra_vars))
        mock_run.assert_called_with(["ansible-playbook", "test.yaml", "-e", json.dumps(extra_vars)], capture_output=True, text=True)

    @patch('subprocess.run')
    def test_run_script_success(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="Script success", stderr="")
        self.assertEqual(supervisor.run_script("test.py"), "Script success")
        mock_run.assert_called_with(["python", "test.py"], capture_output=True, text=True)

    @patch('subprocess.run')
    def test_run_script_failure(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="Error")
        self.assertIsNone(supervisor.run_script("test.py"))

    @patch('subprocess.run')
    def test_run_script_with_args(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="Script success", stderr="")
        args = ["arg1", "arg2"]
        self.assertEqual(supervisor.run_script("test.py", args=args), "Script success")
        mock_run.assert_called_with(["python", "test.py", "arg1", "arg2"], capture_output=True, text=True)

    @patch('os.path.exists')
    @patch('os.remove')
    def test_cleanup_files(self, mock_remove, mock_exists):
        files_to_clean = ["file1.txt", "file2.txt"]
        mock_exists.side_effect = [True, False]
        supervisor.cleanup_files(files_to_clean)
        mock_exists.assert_any_call("file1.txt")
        mock_exists.assert_any_call("file2.txt")
        mock_remove.assert_called_once_with("file1.txt")

    @patch('supervisor.run_playbook')
    @patch('os.path.exists')
    @patch('time.sleep')
    def test_main_no_failed_jobs(self, mock_sleep, mock_exists, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.return_value = True
        mock_exists.return_value = False
        with self.assertRaises(StopIteration):
            supervisor.main()
        mock_run_playbook.assert_called_once_with("health_check.yaml")
        mock_exists.assert_called_once_with("failed_jobs.json")

    @patch('supervisor.run_playbook')
    @patch('time.sleep')
    def test_main_health_check_fails(self, mock_sleep, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.return_value = False
        with self.assertRaises(StopIteration):
            supervisor.main()
        mock_run_playbook.assert_called_once_with("health_check.yaml")

    @patch('supervisor.run_playbook')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('supervisor.cleanup_files')
    @patch('time.sleep')
    def test_main_failed_jobs_file_unreadable(self, mock_sleep, mock_cleanup, mock_open_file, mock_exists, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.return_value = True
        mock_exists.return_value = True
        mock_open_file.side_effect = IOError("File not found")
        with self.assertRaises(StopIteration):
            supervisor.main()
        mock_cleanup.assert_called_once_with(["failed_jobs.json"])

    @patch('supervisor.run_playbook')
    @patch('supervisor.run_script')
    @patch('supervisor.cleanup_files')
    @patch('os.path.exists')
    @patch('time.sleep')
    @patch('builtins.open')
    def test_main_full_successful_cycle(self, mock_open, mock_sleep, mock_exists, mock_cleanup, mock_run_script, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.side_effect = [True, True, True]
        mock_exists.return_value = True
        failed_jobs_data = {"unhealthy_jobs": [{"ID": "job123"}]}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(failed_jobs_data)
        solution_json = '{"action": "restart"}'
        mock_run_script.return_value = solution_json

        with self.assertRaises(StopIteration):
            supervisor.main()

        self.assertEqual(mock_run_playbook.call_count, 3)
        mock_run_playbook.assert_any_call('health_check.yaml')
        mock_run_playbook.assert_any_call('diagnose_failure.yaml', extra_vars={'job_id': 'job123'})
        mock_run_playbook.assert_any_call('heal_job.yaml', extra_vars={'solution_json': solution_json})
        mock_run_script.assert_called_once_with('reflection/reflect.py', ['job123.diagnostics.json'])
        self.assertEqual(mock_cleanup.call_count, 2)
        mock_cleanup.assert_any_call(['job123.diagnostics.json'])
        mock_cleanup.assert_any_call(['failed_jobs.json'])

    @patch('supervisor.run_playbook')
    @patch('supervisor.cleanup_files')
    @patch('os.path.exists')
    @patch('time.sleep')
    @patch('builtins.open')
    def test_main_empty_unhealthy_jobs_list(self, mock_open, mock_sleep, mock_exists, mock_cleanup, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.return_value = True
        mock_exists.return_value = True
        failed_jobs_data = {"unhealthy_jobs": []}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(failed_jobs_data)

        with self.assertRaises(StopIteration):
            supervisor.main()

        mock_run_playbook.assert_called_once_with('health_check.yaml')
        mock_cleanup.assert_called_once_with(['failed_jobs.json'])

    @patch('supervisor.run_playbook')
    @patch('supervisor.run_script')
    @patch('supervisor.cleanup_files')
    @patch('os.path.exists')
    @patch('time.sleep')
    @patch('builtins.open')
    def test_main_job_missing_id(self, mock_open, mock_sleep, mock_exists, mock_cleanup, mock_run_script, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.side_effect = [True, True, True]
        mock_exists.return_value = True
        failed_jobs_data = {"unhealthy_jobs": [{"Name": "job-no-id"}, {"ID": "job456"}]}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(failed_jobs_data)
        solution_json = '{"action": "restart"}'
        mock_run_script.return_value = solution_json

        with self.assertRaises(StopIteration):
            supervisor.main()

        self.assertEqual(mock_run_playbook.call_count, 3)
        mock_run_playbook.assert_any_call('health_check.yaml')
        mock_run_playbook.assert_any_call('diagnose_failure.yaml', extra_vars={'job_id': 'job456'})
        mock_run_playbook.assert_any_call('heal_job.yaml', extra_vars={'solution_json': solution_json})
        mock_run_script.assert_called_once_with('reflection/reflect.py', ['job456.diagnostics.json'])
        self.assertEqual(mock_cleanup.call_count, 2)
        mock_cleanup.assert_any_call(['job456.diagnostics.json'])
        mock_cleanup.assert_any_call(['failed_jobs.json'])

    @patch('supervisor.run_playbook')
    @patch('supervisor.run_script')
    @patch('supervisor.cleanup_files')
    @patch('os.path.exists')
    @patch('time.sleep')
    @patch('builtins.open')
    def test_main_diagnose_failure_playbook_fails(self, mock_open, mock_sleep, mock_exists, mock_cleanup, mock_run_script, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.side_effect = [True, False]  # health_check.yaml passes, diagnose_failure.yaml fails
        mock_exists.return_value = True
        failed_jobs_data = {"unhealthy_jobs": [{"ID": "job789"}]}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(failed_jobs_data)

        with self.assertRaises(StopIteration):
            supervisor.main()

        self.assertEqual(mock_run_playbook.call_count, 2)
        mock_run_playbook.assert_any_call('health_check.yaml')
        mock_run_playbook.assert_any_call('diagnose_failure.yaml', extra_vars={'job_id': 'job789'})
        mock_run_script.assert_not_called()
        mock_cleanup.assert_called_once_with(['failed_jobs.json'])

    @patch('supervisor.run_playbook')
    @patch('supervisor.run_script')
    @patch('supervisor.cleanup_files')
    @patch('os.path.exists')
    @patch('time.sleep')
    @patch('builtins.open')
    def test_main_reflection_script_fails(self, mock_open, mock_sleep, mock_exists, mock_cleanup, mock_run_script, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.side_effect = [True, True]  # health_check.yaml and diagnose_failure.yaml pass
        mock_exists.return_value = True
        failed_jobs_data = {"unhealthy_jobs": [{"ID": "job101"}]}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(failed_jobs_data)
        mock_run_script.return_value = None  # reflection/reflect.py fails

        with self.assertRaises(StopIteration):
            supervisor.main()

        self.assertEqual(mock_run_playbook.call_count, 2)
        mock_run_playbook.assert_any_call('health_check.yaml')
        mock_run_playbook.assert_any_call('diagnose_failure.yaml', extra_vars={'job_id': 'job101'})
        mock_run_script.assert_called_once_with('reflection/reflect.py', ['job101.diagnostics.json'])
        self.assertEqual(mock_cleanup.call_count, 2)
        mock_cleanup.assert_any_call(['job101.diagnostics.json'])
        mock_cleanup.assert_any_call(['failed_jobs.json'])

    @patch('supervisor.run_playbook')
    @patch('supervisor.run_script')
    @patch('supervisor.cleanup_files')
    @patch('os.path.exists')
    @patch('time.sleep')
    @patch('builtins.open')
    def test_main_heal_job_playbook_fails(self, mock_open, mock_sleep, mock_exists, mock_cleanup, mock_run_script, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        mock_run_playbook.side_effect = [True, True, False]  # health_check.yaml and diagnose_failure.yaml pass, heal_job.yaml fails
        mock_exists.return_value = True
        failed_jobs_data = {"unhealthy_jobs": [{"ID": "job112"}]}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(failed_jobs_data)
        solution_json = '{"action": "restart"}'
        mock_run_script.return_value = solution_json

        with self.assertRaises(StopIteration):
            supervisor.main()

        self.assertEqual(mock_run_playbook.call_count, 3)
        mock_run_playbook.assert_any_call('health_check.yaml')
        mock_run_playbook.assert_any_call('diagnose_failure.yaml', extra_vars={'job_id': 'job112'})
        mock_run_playbook.assert_any_call('heal_job.yaml', extra_vars={'solution_json': solution_json})
        mock_run_script.assert_called_once_with('reflection/reflect.py', ['job112.diagnostics.json'])
        self.assertEqual(mock_cleanup.call_count, 2)
        mock_cleanup.assert_any_call(['job112.diagnostics.json'])
        mock_cleanup.assert_any_call(['failed_jobs.json'])

    @patch('supervisor.run_playbook')
    @patch('supervisor.run_script')
    @patch('supervisor.cleanup_files')
    @patch('os.path.exists')
    @patch('time.sleep')
    @patch('builtins.open')
    def test_main_multiple_failed_jobs(self, mock_open, mock_sleep, mock_exists, mock_cleanup, mock_run_script, mock_run_playbook):
        mock_sleep.side_effect = StopIteration
        # health_check, diagnose job1, heal job1, diagnose job2, heal job2
        mock_run_playbook.side_effect = [True, True, True, True, True]
        mock_exists.return_value = True
        failed_jobs_data = {"unhealthy_jobs": [{"ID": "job-multi-1"}, {"ID": "job-multi-2"}]}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(failed_jobs_data)
        solution_json = '{"action": "restart"}'
        mock_run_script.return_value = solution_json

        with self.assertRaises(StopIteration):
            supervisor.main()

        self.assertEqual(mock_run_playbook.call_count, 5)
        mock_run_playbook.assert_any_call('health_check.yaml')
        mock_run_playbook.assert_any_call('diagnose_failure.yaml', extra_vars={'job_id': 'job-multi-1'})
        mock_run_playbook.assert_any_call('heal_job.yaml', extra_vars={'solution_json': solution_json})
        mock_run_playbook.assert_any_call('diagnose_failure.yaml', extra_vars={'job_id': 'job-multi-2'})
        mock_run_playbook.assert_any_call('heal_job.yaml', extra_vars={'solution_json': solution_json})

        self.assertEqual(mock_run_script.call_count, 2)
        mock_run_script.assert_any_call('reflection/reflect.py', ['job-multi-1.diagnostics.json'])
        mock_run_script.assert_any_call('reflection/reflect.py', ['job-multi-2.diagnostics.json'])

        self.assertEqual(mock_cleanup.call_count, 3)
        mock_cleanup.assert_any_call(['job-multi-1.diagnostics.json'])
        mock_cleanup.assert_any_call(['job-multi-2.diagnostics.json'])
        mock_cleanup.assert_any_call(['failed_jobs.json'])

if __name__ == '__main__':
    unittest.main()