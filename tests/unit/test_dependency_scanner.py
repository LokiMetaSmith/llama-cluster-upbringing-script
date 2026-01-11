import unittest
from unittest.mock import MagicMock, patch
from pipecatapp.tools.dependency_scanner_tool import DependencyScannerTool
from pipecatapp.tools.code_runner_tool import CodeRunnerTool

class TestDependencyScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = DependencyScannerTool()

    @patch('httpx.Client')
    def test_scan_safe_package(self, mock_client_cls):
        # Mock PyPI response
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.get.return_value.status_code = 200
        mock_client.get.return_value.json.return_value = {"info": {"version": "2.31.0"}}

        # Mock OSV response
        mock_client.post.return_value.status_code = 200
        mock_client.post.return_value.json.return_value = {"vulns": []}

        result = self.scanner.scan_package("requests")
        self.assertIn("Safe", result)
        self.assertIn("requests==2.31.0", result)

    @patch('httpx.Client')
    def test_scan_vulnerable_package(self, mock_client_cls):
        # Mock PyPI response for an old vulnerable version if we were to ask for latest (but here we pass explicit version)
        # Mock OSV response for vulnerable package
        mock_client = mock_client_cls.return_value.__enter__.return_value

        # Setup for scan_package("django", "1.0") -> Calls OSV directly
        mock_client.post.return_value.status_code = 200
        mock_client.post.return_value.json.return_value = {
            "vulns": [
                {
                    "id": "GHSA-xxxx-xxxx-xxxx",
                    "summary": "Cross-site scripting",
                    "details": "A serious vulnerability."
                }
            ]
        }

        result = self.scanner.scan_package("django", "1.0")
        self.assertIn("UNSAFE", result)
        self.assertIn("django==1.0", result)
        self.assertIn("Cross-site scripting", result)

    @patch('pipecatapp.tools.code_runner_tool.DependencyScannerTool')
    @patch('pipecatapp.tools.code_runner_tool.SandboxSession')
    @patch('pipecatapp.tools.code_runner_tool.docker.from_env')
    def test_code_runner_blocks_unsafe_lib(self, mock_docker_env, MockSandbox, MockScanner):
        # Setup Mock Scanner
        mock_scanner_instance = MockScanner.return_value
        mock_scanner_instance.scan_package.return_value = "⚠️ UNSAFE: Found 1 vulnerabilities..."

        runner = CodeRunnerTool()

        result = runner.run_code_in_sandbox("print('hello')", libraries=["vulnerable-lib"])

        # Debugging output if assertion fails
        if "Operation blocked by security policy" not in result:
             print(f"\nDEBUG: Result was: {result}")

        self.assertIn("Operation blocked by security policy", result)
        self.assertIn("vulnerable-lib", result)
        # Ensure scan was called
        mock_scanner_instance.scan_package.assert_called_with("vulnerable-lib", None)

    @patch('pipecatapp.tools.code_runner_tool.DependencyScannerTool')
    @patch('pipecatapp.tools.code_runner_tool.SandboxSession')
    @patch('pipecatapp.tools.code_runner_tool.docker.from_env')
    def test_code_runner_allows_safe_lib(self, mock_docker_env, MockSandbox, MockScanner):
         # Setup Mock Scanner
        mock_scanner_instance = MockScanner.return_value
        mock_scanner_instance.scan_package.return_value = "Safe: No known vulnerabilities."

        # Setup Mock Sandbox result
        mock_result = MagicMock()
        mock_result.exit_code = 0
        mock_result.stdout = "Success"
        mock_result.stderr = ""
        mock_result.plots = [] # Ensure plots attribute exists

        mock_session = MockSandbox.return_value.__enter__.return_value
        mock_session.run.return_value = mock_result

        runner = CodeRunnerTool()
        result = runner.run_code_in_sandbox("print('hello')", libraries=["safe-lib"])

        self.assertEqual(result, "Success")
        mock_scanner_instance.scan_package.assert_called_with("safe-lib", None)

if __name__ == '__main__':
    unittest.main()
