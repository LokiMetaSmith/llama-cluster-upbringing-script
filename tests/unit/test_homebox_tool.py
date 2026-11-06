import unittest
from unittest.mock import MagicMock, patch
from pipecatapp.tools.homebox_tool import HomeboxTool


class TestHomeboxTool(unittest.TestCase):
    def setUp(self):
        self.tool = HomeboxTool(base_url="http://test-homebox:7745", api_token="secret-token")

    @patch("urllib.request.urlopen")
    def test_get_items(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"items": [{"id": "item-1", "name": "Screwdriver"}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        res = self.tool.get_items()
        self.assertIn("items", res)
        self.assertEqual(res["items"][0]["name"], "Screwdriver")

    @patch("urllib.request.urlopen")
    def test_catalog_container_and_contents(self, mock_urlopen):
        resp_empty_locs = MagicMock()
        resp_empty_locs.read.return_value = b'{"locations": []}'
        resp_empty_locs.__enter__.return_value = resp_empty_locs

        resp_create_box = MagicMock()
        resp_create_box.read.return_value = b'{"id": "loc-box-a", "name": "Garage Box A"}'
        resp_create_box.__enter__.return_value = resp_create_box

        resp_locs_after = MagicMock()
        resp_locs_after.read.return_value = b'{"locations": [{"id": "loc-box-a", "name": "Garage Box A"}]}'
        resp_locs_after.__enter__.return_value = resp_locs_after

        resp_item1 = MagicMock()
        resp_item1.read.return_value = b'{"id": "it-1", "name": "Wrench", "locationId": "loc-box-a"}'
        resp_item1.__enter__.return_value = resp_item1

        resp_item2 = MagicMock()
        resp_item2.read.return_value = b'{"id": "it-2", "name": "Pliers", "locationId": "loc-box-a"}'
        resp_item2.__enter__.return_value = resp_item2

        mock_urlopen.side_effect = [
            resp_empty_locs,
            resp_create_box,
            resp_locs_after,
            resp_item1,
            resp_item2,
        ]

        result = self.tool.catalog_container(
            container_name="Garage Box A",
            items=[
                {"name": "Wrench", "quantity": 1},
                {"name": "Pliers", "quantity": 2},
            ],
            description="Clear plastic tote in garage shelf 2",
            photo_metadata={"detected_objects": ["wrench", "pliers"], "confidence": 0.95},
        )

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["container"]["id"], "loc-box-a")
        self.assertEqual(result["item_count"], 2)
        self.assertEqual(len(result["items"]), 2)

    @patch("urllib.request.urlopen")
    def test_get_container_inventory(self, mock_urlopen):
        resp_locs = MagicMock()
        resp_locs.read.return_value = b'{"locations": [{"id": "loc-123", "name": "Blue Bin"}]}'
        resp_locs.__enter__.return_value = resp_locs

        resp_items = MagicMock()
        resp_items.read.return_value = b'{"items": [{"id": "it-1", "name": "Cables", "location": {"id": "loc-123"}}, {"id": "it-2", "name": "Monitor", "location": {"id": "loc-other"}}]}'
        resp_items.__enter__.return_value = resp_items

        mock_urlopen.side_effect = [resp_locs, resp_items]

        inv = self.tool.get_container_inventory("Blue Bin")
        self.assertEqual(inv["container_id"], "loc-123")
        self.assertEqual(inv["item_count"], 1)
        self.assertEqual(inv["items"][0]["name"], "Cables")

    @patch("urllib.request.urlopen")
    def test_search_containers(self, mock_urlopen):
        resp_locs = MagicMock()
        resp_locs.read.return_value = b'{"locations": [{"id": "loc-1", "name": "Storage Bin", "description": "Attic bin"}]}'
        resp_locs.__enter__.return_value = resp_locs

        resp_items = MagicMock()
        resp_items.read.return_value = b'{"items": [{"id": "it-1", "name": "Winter Coat", "description": "Heavy jacket"}]}'
        resp_items.__enter__.return_value = resp_items

        mock_urlopen.side_effect = [resp_locs, resp_items]

        results = self.tool.search_containers("bin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["type"], "container")
        self.assertEqual(results[0]["name"], "Storage Bin")

    def test_mcp_client_delegation(self):
        mock_mcp = MagicMock()
        mock_mcp.get_items.return_value = {"items": [{"id": "1", "name": "Hammer"}]}
        tool_with_mcp = HomeboxTool(mcp_client=mock_mcp)

        items = tool_with_mcp.get_items()
        self.assertEqual(items["items"][0]["name"], "Hammer")
        mock_mcp.get_items.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_get_qrcode_url_encoding(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"image": "base64encodedqr"}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        res = self.tool.get_qrcode("box: 123 & item: 456")
        self.assertEqual(res["image"], "base64encodedqr")
        self.assertIn("box%3A%20123%20%26%20item%3A%20456", mock_urlopen.call_args[0][0].full_url)


if __name__ == "__main__":
    unittest.main()
