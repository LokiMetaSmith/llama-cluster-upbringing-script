from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict, Any
from pipecatapp.tools.homebox_tool import HomeboxTool

mcp = FastMCP("homebox_server")
_tool = HomeboxTool()


@mcp.tool()
def get_items() -> Any:
    """Retrieves all items from the Homebox inventory."""
    return _tool.get_items()


@mcp.tool()
def get_item(id: str) -> Any:
    """Retrieves a single item from the Homebox inventory by its ID."""
    return _tool.get_item(id)


@mcp.tool()
def create_item(
    name: str,
    description: str = "",
    location_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    quantity: int = 1,
    label_ids: Optional[List[str]] = None,
) -> Any:
    """Creates a new item in the Homebox inventory."""
    return _tool.create_item(
        name=name,
        description=description,
        location_id=location_id,
        parent_id=parent_id,
        quantity=quantity,
        label_ids=label_ids,
    )


@mcp.tool()
def get_locations() -> Any:
    """Retrieves all locations and physical containers from the Homebox inventory."""
    return _tool.get_locations()


@mcp.tool()
def create_location(name: str, description: str = "", parent_id: Optional[str] = None) -> Any:
    """Creates a new location or physical container in Homebox."""
    return _tool.create_location(name=name, description=description, parent_id=parent_id)


@mcp.tool()
def get_location(id: str) -> Any:
    """Retrieves a single location by its ID."""
    return _tool.get_location(id)


@mcp.tool()
def get_labels() -> Any:
    """Retrieves all labels from the Homebox inventory."""
    return _tool.get_labels()


@mcp.tool()
def create_label(name: str, description: str = "", color: Optional[str] = None) -> Any:
    """Creates a new label in the Homebox inventory."""
    return _tool.create_label(name=name, description=description, color=color)


@mcp.tool()
def catalog_container(
    container_name: str,
    items: List[Dict[str, Any]],
    description: str = "",
    parent_location: Optional[str] = None,
    photo_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Catalogs a physical container in the world along with its items."""
    return _tool.catalog_container(
        container_name=container_name,
        items=items,
        description=description,
        parent_location=parent_location,
        photo_metadata=photo_metadata,
    )


@mcp.tool()
def get_container_inventory(container_name_or_id: str) -> Dict[str, Any]:
    """Retrieves all items cataloged inside a physical container."""
    return _tool.get_container_inventory(container_name_or_id)


@mcp.tool()
def search_containers(query: str) -> List[Dict[str, Any]]:
    """Searches across physical containers and items."""
    return _tool.search_containers(query)


if __name__ == "__main__":
    mcp.run()
