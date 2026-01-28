import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure we can import from tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.container_registry_tool import ContainerRegistryTool

class TestContainerRegistryTool(unittest.TestCase):
    def setUp(self):
        self.tool = ContainerRegistryTool()

    @patch("tools.container_registry_tool.requests.get")
    @patch("tools.container_registry_tool.os.getenv")
    def test_discover_registry_consul_success(self, mock_getenv, mock_get):
        # Setup Consul mock
        mock_getenv.return_value = "localhost:8500"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"ServiceAddress": "10.0.0.5", "ServicePort": 5000}]
        mock_get.return_value = mock_response

        url = self.tool._discover_registry()
        self.assertEqual(url, "http://10.0.0.5:5000")
        mock_get.assert_called_with("http://localhost:8500/v1/catalog/service/docker-registry", timeout=2)

    @patch("tools.container_registry_tool.requests.get")
    @patch("tools.container_registry_tool.os.getenv")
    def test_discover_registry_consul_failure(self, mock_getenv, mock_get):
        # Setup Consul failure
        mock_getenv.return_value = "localhost:8500"
        mock_get.side_effect = Exception("Connection refused")

        url = self.tool._discover_registry()
        # Should fallback
        self.assertEqual(url, "http://localhost:5001")

    @patch("tools.container_registry_tool.requests.get")
    def test_list_repositories_success(self, mock_get):
        # Mock discovery via instance variable to avoid consul call
        self.tool._registry_url = "http://mock-registry"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"repositories": ["repo1", "repo2"]}
        mock_get.return_value = mock_response

        result = self.tool.list_repositories()
        self.assertIn("repo1", result)
        self.assertIn("repo2", result)
        mock_get.assert_called_with("http://mock-registry/v2/_catalog", timeout=5)

    @patch("tools.container_registry_tool.requests.get")
    def test_list_tags_success(self, mock_get):
        self.tool._registry_url = "http://mock-registry"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "repo1", "tags": ["v1", "latest"]}
        mock_get.return_value = mock_response

        result = self.tool.list_tags("repo1")
        self.assertIn("v1", result)
        self.assertIn("latest", result)
        mock_get.assert_called_with("http://mock-registry/v2/repo1/tags/list", timeout=5)

    @patch("tools.container_registry_tool.requests.get")
    def test_search_images_success(self, mock_get):
        self.tool._registry_url = "http://mock-registry"

        # Mock catalog response
        mock_catalog = MagicMock()
        mock_catalog.status_code = 200
        mock_catalog.json.return_value = {"repositories": ["pipecat", "python", "ubuntu"]}

        # Mock tags response
        mock_tags = MagicMock()
        mock_tags.status_code = 200
        mock_tags.json.return_value = {"tags": ["expert", "latest"]}

        mock_get.side_effect = [mock_catalog, mock_tags]

        result = self.tool.search_images("pipe")
        self.assertIn("pipecat", result)
        self.assertIn("expert", result)
        self.assertNotIn("ubuntu", result)

if __name__ == "__main__":
    unittest.main()
