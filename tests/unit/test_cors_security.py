import os
import sys
import unittest.mock
import pytest
import subprocess

def test_cors_production_wildcard_rejection():
    """
    Test that running the web_server in 'production' mode with a wildcard CORS
    origin correctly raises a RuntimeError at startup to prevent insecure deployment.
    """
    env = os.environ.copy()
    env["ENV"] = "production"
    env["ALLOWED_ORIGINS"] = "*"

    mock_script = """
import sys
import unittest.mock
import os

sys.modules['workflow'] = unittest.mock.MagicMock()
sys.modules['workflow.runner'] = unittest.mock.MagicMock()
sys.modules['workflow.history'] = unittest.mock.MagicMock()
sys.modules['api_keys'] = unittest.mock.MagicMock()
sys.modules['security'] = unittest.mock.MagicMock()
sys.modules['models'] = unittest.mock.MagicMock()
sys.modules['rate_limiter'] = unittest.mock.MagicMock()
sys.modules['net_utils'] = unittest.mock.MagicMock()

sys.path.insert(0, os.path.abspath('.'))

import pipecatapp.web_server
"""
    result = subprocess.run(
        [sys.executable, "-c", mock_script],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
    assert "RuntimeError: Insecure CORS Configuration: Wildcard origin ('*') is not allowed in production mode" in result.stderr

def test_cors_development_wildcard_warning():
    """
    Test that running the web_server in 'development' mode with a wildcard CORS
    origin successfully starts but issues a warning.
    """
    env = os.environ.copy()
    env["ENV"] = "development"
    env["ALLOWED_ORIGINS"] = "*"

    # To test without importing heavy dependencies in a separate process,
    # we can run a custom script that mocks the heavy parts.
    mock_script = """
import sys
import unittest.mock
import os

sys.modules['workflow'] = unittest.mock.MagicMock()
sys.modules['workflow.runner'] = unittest.mock.MagicMock()
sys.modules['workflow.history'] = unittest.mock.MagicMock()
sys.modules['api_keys'] = unittest.mock.MagicMock()
sys.modules['security'] = unittest.mock.MagicMock()
sys.modules['models'] = unittest.mock.MagicMock()
sys.modules['rate_limiter'] = unittest.mock.MagicMock()
sys.modules['net_utils'] = unittest.mock.MagicMock()

sys.path.insert(0, os.path.abspath('.'))

import pipecatapp.web_server
"""
    result = subprocess.run(
        [sys.executable, "-c", mock_script],
        env=env,
        capture_output=True,
        text=True
    )

    # It should exit gracefully
    assert result.returncode == 0
    assert "⚠️  Security Warning: CORS is configured to allow all origins" in result.stderr
