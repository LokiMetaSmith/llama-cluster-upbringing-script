import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to sys.path to allow importing pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from pipecatapp.tools.container_registry_tool import ContainerRegistryTool

class TestContainerRegistrySecurity(unittest.TestCase):
    def setUp(self):
        self.tool = ContainerRegistryTool(registry_url="http://localhost:5001")

    @patch('pipecatapp.tools.container_registry_tool.requests.get')
    def test_list_tags_path_traversal(self, mock_get):
        """Test that list_tags blocks path traversal attempts."""
        # Exploitable input
        repo_name = "../secret"

        # Call the method
        result = self.tool.list_tags(repo_name)

        # Verify that the request was NOT made
        mock_get.assert_not_called()

        # Verify error message
        self.assertIn("Error: Invalid repository name", result)

    @patch('pipecatapp.tools.container_registry_tool.requests.get')
    def test_search_images_blocks_invalid_repos(self, mock_get):
        """Test that search_images blocks invalid repositories from the catalog."""
        # Mock catalog response with one valid and one invalid repo
        mock_catalog_response = MagicMock()
        mock_catalog_response.status_code = 200
        mock_catalog_response.json.return_value = {"repositories": ["valid-repo", "../invalid-repo"]}

        # Mock tags response for valid repo
        mock_tags_response = MagicMock()
        mock_tags_response.status_code = 200
        mock_tags_response.json.return_value = {"tags": ["latest"]}

        mock_get.side_effect = [mock_catalog_response, mock_tags_response]

        # Call the method
        result = self.tool.search_images("repo")

        # Verify requests
        # First request to catalog
        mock_get.assert_any_call("http://localhost:5001/v2/_catalog", timeout=5)

        # Second request to valid-repo tags
        mock_get.assert_any_call("http://localhost:5001/v2/valid-repo/tags/list", timeout=2)

        # Verify NO request to invalid-repo tags
        # We need to ensure call args check
        call_args_list = mock_get.call_args_list
        invalid_url = "http://localhost:5001/v2/../invalid-repo/tags/list"
        for call in call_args_list:
            args, _ = call
            if args and args[0] == invalid_url:
                self.fail("Request was made to invalid repository URL")

        self.assertIn("Skipped due to invalid name", result)

    @patch('pipecatapp.tools.container_registry_tool.requests.get')
    def test_list_tags_valid(self, mock_get):
        """Test that list_tags works for valid repository names."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"tags": ["latest"]}
        mock_get.return_value = mock_response

        repo_name = "my-image"
        self.tool.list_tags(repo_name)

        mock_get.assert_called_with("http://localhost:5001/v2/my-image/tags/list", timeout=5)

if __name__ == '__main__':
    unittest.main()
