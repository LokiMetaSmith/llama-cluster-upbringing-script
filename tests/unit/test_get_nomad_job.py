import pytest
import sys
import os
import requests
from unittest.mock import MagicMock, patch

# Update path to point to pipecatapp/tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp', 'tools')))

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
    # Verify timeout is passed
    mock_get.assert_called_once_with("http://localhost:4646/v1/job/test-job", timeout=10)

@patch('requests.get')
def test_get_nomad_job_definition_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    result = get_nomad_job_definition("test-job")
    assert result is None

def test_get_nomad_job_definition_invalid_id():
    # Test with invalid characters (path traversal attempt)
    result = get_nomad_job_definition("../../secrets")
    assert result is None

    # Test with invalid characters (injection attempt)
    result = get_nomad_job_definition("job; rm -rf /")
    assert result is None

    # Test with valid characters
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        result = get_nomad_job_definition("valid-job_1.2")
        assert result == {}
