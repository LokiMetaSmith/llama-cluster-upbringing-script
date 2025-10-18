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
        os.path.join(os.path.dirname(evolve.__file__), "..", "ansible", "roles", "pipecatapp", "files", "app.py")
    )

    # Assert that OpenEvolve was called with the correct initial_program_path
    mock_open_evolve.assert_called_once()
    called_args, called_kwargs = mock_open_evolve.call_args
    assert called_kwargs['initial_program_path'] == expected_path
    assert called_kwargs['evaluation_file'] == 'prompt_engineering/evaluator.py'

    # Clean up the environment variable
    del os.environ['OPENAI_API_KEY']


# Add create_evaluator to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'prompt_engineering')))
from prompt_engineering import create_evaluator

def test_create_evaluator_script():
    """
    Tests that the create_evaluator script generates a file with the correct content.
    """
    # Define test arguments
    test_args = {
        "app_job_template": "test/app.nomad.j2",
        "test_runner_job_template": "test/runner.nomad.j2",
        "app_source_dir": "test/src",
        "target_code_file": "test_app.py",
        "aux_startup_script": "/test/start.sh",
        "output_path": "/tmp/test_generated_evaluator.py"
    }

    # Use patch to simulate command-line arguments
    with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(**test_args)):
        create_evaluator.main()

    # Check if the file was created
    assert os.path.exists(test_args["output_path"])

    # Read the file and check if the content is correct
    with open(test_args["output_path"], 'r') as f:
        content = f.read()

    assert f'APP_JOB_TEMPLATE_PATH = "{test_args["app_job_template"]}"' in content
    assert f'TEST_RUNNER_JOB_TEMPLATE_PATH = "{test_args["test_runner_job_template"]}"' in content
    assert f'APP_SOURCE_DIR = "{test_args["app_source_dir"]}"' in content
    assert f'TARGET_CODE_FILE = "{test_args["target_code_file"]}"' in content
    assert f'AUXILIARY_STARTUP_SCRIPT = \'{test_args["aux_startup_script"]}\'' in content

    # Clean up the created file
    os.remove(test_args["output_path"])