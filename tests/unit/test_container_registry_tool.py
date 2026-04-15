import pytest
import sys
from unittest.mock import patch, MagicMock

sys.modules['requests'] = MagicMock()

from pipecatapp.tools.container_registry_tool import ContainerRegistryTool

def test_container_registry_tool_initialization():
    tool = ContainerRegistryTool()
    assert tool.name == "container_registry"

def test_validate_repository():
    tool = ContainerRegistryTool()
    assert tool._validate_repository("myrepo") == True
    assert tool._validate_repository("my/repo/test") == True
    assert tool._validate_repository("../repo") == False
    assert tool._validate_repository("repo//test") == False

@patch('pipecatapp.tools.container_registry_tool.requests.get')
def test_list_repositories(mock_get):
    tool = ContainerRegistryTool("http://mock-registry:5000")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"repositories": ["repo1", "repo2"]}
    mock_get.return_value = mock_response

    res = tool.list_repositories()
    assert "repo1" in res
    assert "repo2" in res

@patch('pipecatapp.tools.container_registry_tool.requests.get')
def test_list_tags(mock_get):
    tool = ContainerRegistryTool("http://mock-registry:5000")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "myrepo", "tags": ["v1", "v2"]}
    mock_get.return_value = mock_response

    res = tool.list_tags("myrepo")
    assert "v1" in res
    assert "v2" in res

@patch('pipecatapp.tools.container_registry_tool.requests.get')
def test_search_images(mock_get):
    tool = ContainerRegistryTool("http://mock-registry:5000")

    # Needs two get calls, one for catalog, one for tags
    def side_effect(url, **kwargs):
        mock_response = MagicMock()
        mock_response.status_code = 200
        if "catalog" in url:
            mock_response.json.return_value = {"repositories": ["myrepo1", "otherrepo"]}
        else:
            mock_response.json.return_value = {"name": "myrepo1", "tags": ["latest"]}
        return mock_response

    mock_get.side_effect = side_effect

    res = tool.search_images("myrepo")
    assert "myrepo1" in res
    assert "latest" in res
    assert "otherrepo" not in res
