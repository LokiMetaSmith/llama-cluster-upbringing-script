import pytest
import sys
from unittest.mock import patch, MagicMock

sys.modules['httpx'] = MagicMock()

from pipecatapp.tools.dependency_scanner_tool import DependencyScannerTool

def test_dependency_scanner_initialization():
    tool = DependencyScannerTool()
    assert tool.name == "dependency_scanner"

@patch("pipecatapp.tools.dependency_scanner_tool.httpx.Client")
def test_scan_package_no_version_success(mock_client_class):
    tool = DependencyScannerTool()

    mock_client = MagicMock()
    mock_client_class.return_value.__enter__.return_value = mock_client

    # Needs two calls: first for version, second for vulns
    mock_response_version = MagicMock()
    mock_response_version.status_code = 200
    mock_response_version.json.return_value = {"info": {"version": "1.0.0"}}

    mock_response_vulns = MagicMock()
    mock_response_vulns.status_code = 200
    mock_response_vulns.json.return_value = {"vulns": []}

    def side_effect(url, **kwargs):
        if "pypi.org" in url:
            return mock_response_version
        return mock_response_vulns

    mock_client.get.side_effect = side_effect
    mock_client.post.side_effect = side_effect

    res = tool.scan_package("mypackage")
    assert "Safe: No known vulnerabilities found" in res

@patch("pipecatapp.tools.dependency_scanner_tool.httpx.Client")
def test_scan_package_with_vulns(mock_client_class):
    tool = DependencyScannerTool()

    mock_client = MagicMock()
    mock_client_class.return_value.__enter__.return_value = mock_client

    mock_response_vulns = MagicMock()
    mock_response_vulns.status_code = 200
    mock_response_vulns.json.return_value = {
        "vulns": [
            {"id": "CVE-1", "summary": "Bad thing", "details": "Very bad"}
        ]
    }

    mock_client.post.return_value = mock_response_vulns

    res = tool.scan_package("mypackage", "1.0.0")
    assert "UNSAFE" in res
    assert "CVE-1" in res
