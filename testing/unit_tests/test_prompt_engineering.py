import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock

# Add the project root to the Python path to allow importing evolve
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from prompt_engineering import evolve

@pytest.mark.asyncio
@patch('prompt_engineering.evolve.OpenEvolve')
async def test_run_evolution_initializes_openevolve_correctly(mock_open_evolve):
    """
    Tests that the run_evolution function initializes the OpenEvolve class
    with the correct path to the initial prompt.
    """
    # Mock the OpenEvolve instance and its run method
    mock_instance = MagicMock()
    # The run method is async, so it needs to be an AsyncMock
    mock_instance.run = AsyncMock(return_value=MagicMock())
    mock_open_evolve.return_value = mock_instance

    # Set the required environment variable
    os.environ['OPENAI_API_KEY'] = 'test-key'

    # Run the function
    await evolve.run_evolution()

    # Define the expected path
    expected_path = os.path.abspath(
        os.path.join(os.path.dirname(evolve.__file__), "..", "prompts", "router.txt")
    )

    # Assert that OpenEvolve was called with the correct initial_program_path
    mock_open_evolve.assert_called_once()
    called_args, called_kwargs = mock_open_evolve.call_args
    assert called_kwargs['initial_program_path'] == expected_path
    assert called_kwargs['evaluation_file'] == 'prompt_engineering/evaluator.py'

    # Clean up the environment variable
    del os.environ['OPENAI_API_KEY']