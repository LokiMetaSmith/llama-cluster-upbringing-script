import pytest
import sys
import os
import time
from unittest.mock import MagicMock, patch

# Add repo root to path to allow importing pipecatapp as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pipecatapp.tools.code_runner_tool import CodeRunnerTool

@patch('pipecatapp.tools.code_runner_tool.docker.from_env')
@patch('pipecatapp.tools.code_runner_tool.time.sleep') # Mock sleep to speed up
def test_execution_timeout_logic(mock_sleep, mock_docker_from_env):
    """
    Test that CodeRunnerTool runs containers in detached mode and implements timeout logic.
    """
    # Setup mock client and container
    mock_client = MagicMock()
    mock_docker_from_env.return_value = mock_client

    mock_container = MagicMock()
    mock_client.containers.run.return_value = mock_container

    # Configure mock container behavior
    # status is always running to force timeout logic
    mock_container.status = 'running'

    # Initialize tool
    tool = CodeRunnerTool()
    # Force docker mode
    tool.mode = "docker"
    tool.executor.client = mock_client

    # We want to break the loop quickly.
    # The loop condition is: while time.time() - start_time < timeout:
    # We can mock time.time but tricky.
    # Instead, we can just let it run but rely on mocked sleep so it spins fast?
    # No, if sleep is instant, it will loop MANY times until 30s passes in real time (via time.time()).

    # Better approach: Call execute_simple_python directly with short timeout
    # But we want to test run_python_code integration.

    # Let's mock time.time to simulate passage of time.
    with patch('pipecatapp.tools.code_runner_tool.time.time') as mock_time:
        # time() is called:
        # 1. start_time = time.time()
        # 2. inside while: time.time()
        # 3. inside while: time.time() again?

        # We want:
        # Call 1: 0 (start)
        # Call 2: 0 (check) -> 0 < 30 -> enter loop
        # Call 3: 31 (check) -> 31 > 30 -> exit loop

        mock_time.side_effect = [0, 0, 31, 31, 31]

        tool.run_python_code("import time; time.sleep(10)")

    # 1. Assert run was called with detach=True
    call_args = mock_client.containers.run.call_args
    assert call_args is not None
    kwargs = call_args[1]
    assert kwargs.get('detach') is True, "Container should be run in detached mode (detach=True)"

    # 2. Assert reload was called at least once
    mock_container.reload.assert_called()

    # 3. Assert kill was called (timeout happened)
    mock_container.kill.assert_called()
