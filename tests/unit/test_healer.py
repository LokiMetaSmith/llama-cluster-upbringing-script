import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Ensure project root is in sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.healer import (
    extract_repo_source_from_traceback,
    get_nomad_tls_kwargs,
    record_adaptation_case,
    NomadWatcher,
    HealerAgent,
)


class TestHealer(unittest.TestCase):

    def test_extract_repo_source_from_traceback(self):
        """Test extracting repository-relative Python files from tracebacks."""
        # Fake stderr with multiple stack frames
        stderr = """
Traceback (most recent call last):
  File "/usr/lib/python3.10/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/home/pipecatapp/.venv/lib/python3.10/site-packages/fastapi/applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "pipecatapp/chaos_module.py", line 12, in risky_math
    return 100 / x
ZeroDivisionError: division by zero
"""
        # Test with a mock repo root where pipecatapp/chaos_module.py is recognized
        with patch("os.path.isfile", side_effect=lambda path: "chaos_module.py" in path):
            result = extract_repo_source_from_traceback(stderr, repo_root=REPO_ROOT)
            self.assertIsNotNone(result)
            self.assertIn("chaos_module.py", result)

    def test_extract_repo_source_ignores_external(self):
        """Ensure external and venv tracebacks are not flagged as repo source files."""
        stderr = """
Traceback (most recent call last):
  File "/usr/lib/python3.10/subprocess.py", line 524, in run
    raise CalledProcessError(retcode, process.args)
CalledProcessError: Command '['consul', 'members']' returned non-zero exit status 1.
"""
        result = extract_repo_source_from_traceback(stderr, repo_root=REPO_ROOT)
        self.assertIsNone(result)

    def test_nomad_tls_kwargs_security(self):
        """Verify strict adherence to zero-bypass TLS rule for Nomad."""
        # HTTP URL should return empty kwargs (plain HTTP)
        http_kwargs = get_nomad_tls_kwargs("http://localhost:4646")
        self.assertEqual(http_kwargs, {})

        # HTTPS URL must NEVER set verify=False
        https_kwargs = get_nomad_tls_kwargs("https://100.64.0.1:4646")
        self.assertIn("verify", https_kwargs)
        self.assertNotEqual(https_kwargs["verify"], False)

    @patch("requests.get")
    def test_nomad_watcher_get_failed_allocs(self, mock_get):
        """Verify NomadWatcher accurately detects failed and crashed allocations."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "ID": "alloc-good-1",
                "JobID": "healthy-job",
                "ClientStatus": "running",
                "TaskStates": {"task1": {"State": "running", "Failed": False}}
            },
            {
                "ID": "alloc-fail-1",
                "JobID": "crashed-job",
                "ClientStatus": "failed",
                "TaskStates": {"worker": {"State": "dead", "Failed": True}}
            },
            {
                "ID": "alloc-fail-2",
                "JobID": "oom-job",
                "ClientStatus": "running",
                "TaskStates": {"oom_task": {"State": "dead", "Failed": True}}
            }
        ]
        mock_get.return_value = mock_response

        watcher = NomadWatcher("http://127.0.0.1:4646")
        failed = watcher.get_failed_allocs()

        self.assertEqual(len(failed), 2)
        failed_ids = [a["ID"] for a in failed]
        self.assertIn("alloc-fail-1", failed_ids)
        self.assertIn("alloc-fail-2", failed_ids)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_record_adaptation_case(self, mock_makedirs, mock_file):
        """Verify adaptation manager bridges runtime crashes into prompt_engineering."""
        diagnostic = {
            "job_id": "test_service",
            "alloc_id": "alloc-12345678",
            "task_name": "api",
            "logs": {"stderr": "ZeroDivisionError: division by zero"}
        }

        record_adaptation_case("test_service", "alloc-12345678", diagnostic, repo_root=REPO_ROOT)

        mock_makedirs.assert_called()
        mock_file.assert_called()
        handle = mock_file()
        written_content = handle.write.call_args[0][0]
        self.assertIn("test_failure_reproduction_test_service", written_content)
        self.assertIn("ZeroDivisionError", written_content)

    def test_healer_agent_mock_chat(self):
        """Verify mock responses generate valid reproduction and patch code blocks."""
        agent = HealerAgent()
        repro_prompt = [{"role": "user", "content": "Write a STANDALONE Python test file"}]
        repro_code = agent._mock_chat(repro_prompt)
        self.assertIn("def test_reproduction", repro_code)

        fix_prompt = [{"role": "user", "content": "rewrite the Source Code to fix the bug"}]
        fix_code = agent._mock_chat(fix_prompt)
        self.assertIn("def risky_math", fix_code)


if __name__ == "__main__":
    unittest.main()
