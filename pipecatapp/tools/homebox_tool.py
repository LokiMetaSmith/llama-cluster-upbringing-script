"""Homebox Tool providing agent support for cataloging physical containers in the world.

Integrates with Homebox and Homebox-mcp (https://github.com/LokiMetaSmith/Homebox-mcp).
Allows autonomous agents to:
- Catalog physical containers (boxes, bins, totes, shelves) and their contents from visual photos or descriptions
- Query container inventory and find where physical items are stored
- Manage labels, asset tags, and QR codes
- Interface seamlessly with Homebox MCP methods
"""

import os
import json
import logging
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error
import urllib.parse

logger = logging.getLogger("HomeboxTool")


class HomeboxTool:
    """Tool for interacting with Homebox inventory and LokiMetaSmith/Homebox-mcp server."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_token: Optional[str] = None,
        mcp_client: Optional[Any] = None,
    ):
        self.name = "homebox"
        self.description = (
            "Catalog, search, and manage physical storage containers, locations, and inventory items using Homebox and Homebox-mcp."
        )
        self.base_url = (base_url or os.getenv("HOMEBOX_URL") or "http://homebox.service.consul:7745").rstrip("/")
        self.api_token = api_token or os.getenv("HOMEBOX_TOKEN") or ""
        self.mcp_client = mcp_client

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers

    def _api_request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/api/v1/{endpoint.lstrip('/')}"
        encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=encoded_data, headers=self._get_headers(), method=method)

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp_body = resp.read().decode("utf-8")
                if resp_body:
                    try:
                        return json.loads(resp_body)
                    except json.JSONDecodeError:
                        return resp_body
                return {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else str(e)
            logger.error(f"Homebox HTTP error {e.code}: {err_body}")
            return {"error": f"HTTP {e.code}: {err_body}"}
        except Exception as e:
            logger.error(f"Homebox request failed: {e}")
            return {"error": str(e)}

    # MCP / Native tool methods
    def get_items(self) -> Any:
        """Retrieves all items from the Homebox inventory."""
        if self.mcp_client and hasattr(self.mcp_client, "get_items"):
            try:
                return self.mcp_client.get_items()
            except Exception as e:
                logger.warning(f"Homebox MCP call failed, falling back to direct API: {e}")
        return self._api_request("items")

    def get_item(self, item_id: str) -> Any:
        """Retrieves details of a specific item by its ID."""
        if self.mcp_client and hasattr(self.mcp_client, "get_item"):
            try:
                return self.mcp_client.get_item(id=item_id)
            except Exception as e:
                logger.warning(f"Homebox MCP call failed, falling back to direct API: {e}")
        return self._api_request(f"items/{item_id}")

    def create_item(
        self,
        name: str,
        description: str = "",
        location_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        quantity: int = 1,
        label_ids: Optional[List[str]] = None,
    ) -> Any:
        """Creates a new item in Homebox."""
        payload = {
            "name": name,
            "description": description,
            "quantity": quantity,
        }
        if location_id:
            payload["locationId"] = location_id
        if parent_id:
            payload["parentId"] = parent_id
        if label_ids:
            payload["labelIds"] = label_ids

        if self.mcp_client and hasattr(self.mcp_client, "create_item"):
            try:
                return self.mcp_client.create_item(**payload)
            except Exception as e:
                logger.warning(f"Homebox MCP call failed, falling back to direct API: {e}")

        return self._api_request("items", method="POST", data=payload)

    def get_locations(self) -> Any:
        """Retrieves all locations from the Homebox inventory."""
        if self.mcp_client and hasattr(self.mcp_client, "get_locations"):
            try:
                return self.mcp_client.get_locations()
            except Exception as e:
                logger.warning(f"Homebox MCP call failed, falling back to direct API: {e}")
        return self._api_request("locations")

    def create_location(self, name: str, description: str = "", parent_id: Optional[str] = None) -> Any:
        """Creates a new location or physical container in Homebox."""
        payload = {"name": name, "description": description}
        if parent_id:
            payload["parentId"] = parent_id

        if self.mcp_client and hasattr(self.mcp_client, "create_location"):
            try:
                return self.mcp_client.create_location(**payload)
            except Exception as e:
                logger.warning(f"Homebox MCP call failed, falling back to direct API: {e}")

        return self._api_request("locations", method="POST", data=payload)

    def get_location(self, location_id: str) -> Any:
        """Retrieves location details by ID."""
        if self.mcp_client and hasattr(self.mcp_client, "get_location"):
            try:
                return self.mcp_client.get_location(id=location_id)
            except Exception as e:
                logger.warning(f"Homebox MCP call failed, falling back to direct API: {e}")
        return self._api_request(f"locations/{location_id}")

    def get_labels(self) -> Any:
        """Retrieves all labels from the Homebox inventory."""
        if self.mcp_client and hasattr(self.mcp_client, "get_labels"):
            try:
                return self.mcp_client.get_labels()
            except Exception as e:
                logger.warning(f"Homebox MCP call failed, falling back to direct API: {e}")
        return self._api_request("labels")

    def create_label(self, name: str, description: str = "", color: Optional[str] = None) -> Any:
        """Creates a new label."""
        payload = {"name": name, "description": description}
        if color:
            payload["color"] = color

        if self.mcp_client and hasattr(self.mcp_client, "create_label"):
            try:
                return self.mcp_client.create_label(**payload)
            except Exception as e:
                logger.warning(f"Homebox MCP call failed, falling back to direct API: {e}")

        return self._api_request("labels", method="POST", data=payload)

    def get_qrcode(self, data: str) -> Any:
        """Generates a QR code image for a container or item."""
        if self.mcp_client and hasattr(self.mcp_client, "get_qrcode"):
            try:
                return self.mcp_client.get_qrcode(data=data)
            except Exception as e:
                logger.warning(f"Homebox MCP call failed: {e}")
        return self._api_request(f"qrcode?data={urllib.parse.quote(data)}")

    def get_location_label(self, location_id: str) -> Any:
        """Generates printable label image for a location or container."""
        if self.mcp_client and hasattr(self.mcp_client, "get_location_label"):
            try:
                return self.mcp_client.get_location_label(id=location_id)
            except Exception as e:
                logger.warning(f"Homebox MCP call failed: {e}")
        return self._api_request(f"labelmaker/location/{location_id}")

    # Physical Container Workflow Methods
    def catalog_container(
        self,
        container_name: str,
        items: List[Dict[str, Any]],
        description: str = "",
        parent_location: Optional[str] = None,
        photo_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Catalogs a physical container (box, tote, bin, shelf) in the physical world and registers its contents.

        Args:
            container_name: The name or identifier of the container (e.g. "Storage Box #4", "Blue Tool Tote").
            items: A list of dicts representing items found in the container, each having 'name' and optional 'quantity', 'description'.
            description: Optional description of the container.
            parent_location: Optional parent location name or ID (e.g., "Garage", "Attic", "Living Room").
            photo_metadata: Optional visual/camera details (timestamp, detected features).

        Returns:
            Dict containing the container location details and the list of cataloged item records.
        """
        # 1. Resolve or create parent location if specified
        parent_id = None
        if parent_location:
            existing_locs = self.get_locations()
            if isinstance(existing_locs, dict) and "locations" in existing_locs:
                loc_list = existing_locs["locations"]
            elif isinstance(existing_locs, list):
                loc_list = existing_locs
            else:
                loc_list = []

            for loc in loc_list:
                if loc.get("name", "").lower() == parent_location.lower() or loc.get("id") == parent_location:
                    parent_id = loc.get("id")
                    break

            if not parent_id:
                new_parent = self.create_location(name=parent_location, description="Auto-created parent location")
                if isinstance(new_parent, dict) and "id" in new_parent:
                    parent_id = new_parent["id"]

        # 2. Find or create the container location
        container_desc = description
        if photo_metadata:
            container_desc = f"{description}\nVisual metadata: {json.dumps(photo_metadata)}".strip()

        existing_locs = self.get_locations()
        container_id = None
        if isinstance(existing_locs, dict) and "locations" in existing_locs:
            loc_list = existing_locs["locations"]
        elif isinstance(existing_locs, list):
            loc_list = existing_locs
        else:
            loc_list = []

        for loc in loc_list:
            if loc.get("name", "").lower() == container_name.lower():
                container_id = loc.get("id")
                break

        if not container_id:
            loc_res = self.create_location(
                name=container_name,
                description=container_desc,
                parent_id=parent_id,
            )
            container_id = loc_res.get("id") if isinstance(loc_res, dict) else None

        # 3. Create or catalog each item inside this container
        cataloged_items = []
        for item in items:
            item_name = item.get("name", "Unknown Item")
            item_desc = item.get("description", "")
            item_qty = int(item.get("quantity", 1))

            created_item = self.create_item(
                name=item_name,
                description=item_desc,
                location_id=container_id,
                quantity=item_qty,
            )
            cataloged_items.append(created_item)

        return {
            "status": "success",
            "container": {
                "id": container_id,
                "name": container_name,
                "parent_id": parent_id,
                "description": container_desc,
            },
            "item_count": len(cataloged_items),
            "items": cataloged_items,
        }

    def get_container_inventory(self, container_name_or_id: str) -> Dict[str, Any]:
        """Retrieves all items cataloged inside a physical container or location."""
        # Check if container_name_or_id matches a location ID or name
        all_locs = self.get_locations()
        loc_list = []
        if isinstance(all_locs, dict) and "locations" in all_locs:
            loc_list = all_locs["locations"]
        elif isinstance(all_locs, list):
            loc_list = all_locs

        matched_loc = None
        for loc in loc_list:
            if loc.get("id") == container_name_or_id or loc.get("name", "").lower() == container_name_or_id.lower():
                matched_loc = loc
                break

        container_id = matched_loc.get("id") if matched_loc else container_name_or_id
        container_name = matched_loc.get("name", container_name_or_id) if matched_loc else container_name_or_id

        # Fetch all items and filter by locationId
        all_items = self.get_items()
        item_list = []
        if isinstance(all_items, dict) and "items" in all_items:
            item_list = all_items["items"]
        elif isinstance(all_items, list):
            item_list = all_items

        contained_items = []
        for it in item_list:
            loc_info = it.get("location")
            loc_id = loc_info.get("id") if isinstance(loc_info, dict) else it.get("location_id") or it.get("locationId")
            if loc_id == container_id:
                contained_items.append(it)

        return {
            "container_id": container_id,
            "container_name": container_name,
            "item_count": len(contained_items),
            "items": contained_items,
        }

    def search_containers(self, query: str) -> List[Dict[str, Any]]:
        """Searches across physical containers, locations, and items."""
        query_lower = query.lower()
        results = []

        # Search locations
        all_locs = self.get_locations()
        loc_list = all_locs.get("locations", []) if isinstance(all_locs, dict) else (all_locs if isinstance(all_locs, list) else [])
        for loc in loc_list:
            if query_lower in loc.get("name", "").lower() or query_lower in loc.get("description", "").lower():
                results.append({
                    "type": "container",
                    "id": loc.get("id"),
                    "name": loc.get("name"),
                    "description": loc.get("description", ""),
                    "item_count": loc.get("itemCount", 0),
                })

        # Search items
        all_items = self.get_items()
        item_list = all_items.get("items", []) if isinstance(all_items, dict) else (all_items if isinstance(all_items, list) else [])
        for it in item_list:
            if query_lower in it.get("name", "").lower() or query_lower in it.get("description", "").lower():
                results.append({
                    "type": "item",
                    "id": it.get("id"),
                    "name": it.get("name"),
                    "description": it.get("description", ""),
                    "location": it.get("location"),
                })

        return results
