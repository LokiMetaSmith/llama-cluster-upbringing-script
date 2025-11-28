import pytest
import sys
import os
import requests
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ansible', 'roles', 'pipecatapp', 'files', 'tools')))

from get_nomad_job import get_nomad_job_definition

@patch('requests.get')
@patch('os.environ.get')
def test_get_nomad_job_definition_success(mock_env_get, mock_get):
    mock_env_get.return_value = "http://localhost:4646"
    mock_response = MagicMock()
    mock_response.json.return_value = {"ID": "test-job"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_nomad_job_definition("test-job")
    assert result == {"ID": "test-job"}
    mock_get.assert_called_once_with("http://localhost:4646/v1/job/test-job")

@patch('requests.get')
def test_get_nomad_job_definition_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    result = get_nomad_job_definition("test-job")
    assert result is None
