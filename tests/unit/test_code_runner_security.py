import pytest
import sys
import os
from unittest.mock import MagicMock

# Add repo root to path to allow importing pipecatapp as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pipecatapp.tools.code_runner_tool import CodeRunnerTool, MAX_CODE_LENGTH

def test_code_runner_length_limit():
    """
    Test that CodeRunnerTool rejects code that exceeds the maximum length limit.
    This prevents Denial of Service (DoS) attacks via large payloads.
    """
    tool = CodeRunnerTool()
    # Mock executor to avoid actual execution if the check fails (which it shouldn't once fixed)
    tool.executor = MagicMock()
    tool.fast_executor = MagicMock() # For hybrid mode checks

    # Create a large string slightly larger than the limit
    large_code = "a" * (MAX_CODE_LENGTH + 1)

    # Test run_python_code
    result = tool.run_python_code(large_code)
    assert f"Error: Code length exceeds the maximum limit of {MAX_CODE_LENGTH} characters." in result

    # Test run_code_in_sandbox
    result = tool.run_code_in_sandbox(large_code)
    assert f"Error: Code length exceeds the maximum limit of {MAX_CODE_LENGTH} characters." in result

def test_code_runner_length_limit_ok():
    """
    Test that CodeRunnerTool accepts code within the limit.
    """
    tool = CodeRunnerTool()
    tool.executor = MagicMock()
    tool.executor.execute.return_value = "Success"

    # Mock fast executor for hybrid mode/Docker check
    tool.executor.execute_simple_python = MagicMock(return_value="Success")

    # Create a string exactly at the limit
    ok_code = "a" * MAX_CODE_LENGTH

    # We need to make sure run_python_code actually calls the executor if length is OK
    # Depending on mode (default is docker), run_python_code calls executor.execute_simple_python
    # or executor.execute.
    # We'll just mock both methods on the executor.

    result = tool.run_python_code(ok_code)
    # The result should be "Success" (from mock) or whatever the tool returns if it passes the check.
    # If the check fails, it returns "Error: Code length exceeds..."
    assert "Error: Code length exceeds" not in result

    result = tool.run_code_in_sandbox(ok_code)
    assert "Error: Code length exceeds" not in result
