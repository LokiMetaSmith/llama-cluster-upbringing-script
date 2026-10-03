from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from pipecatapp.tools import __all__ as all_tools
from pipecatapp.tools import get_component_spec_for_tool
from pipecatapp.api_keys import get_api_key
import pipecatapp.tools
import uuid

tangle_router = APIRouter(prefix="/api", tags=["tangle_ui"])


@tangle_router.get("/users/me", dependencies=[Depends(get_api_key)])
async def get_current_user():
    """Mock auth for the Tangle UI to allow local editing."""
    return {"id": "admin", "permissions": ["read", "write", "admin"]}


@tangle_router.get("/published_components/", dependencies=[Depends(get_api_key)])
async def list_published_components():
    """Dynamically loads Pipecat tools and returns them as Tangle components."""
    components = []
    for tool_name in all_tools:
        try:
            tool_class = getattr(pipecatapp.tools, tool_name)
            tool_instance = tool_class()
            spec = get_component_spec_for_tool(tool_instance)
            if spec:
                components.append(
                    {
                        "digest": str(
                            uuid.uuid5(uuid.NAMESPACE_OID, spec.name or "unknown")
                        ),
                        "name": spec.name,
                        "text": spec.to_json_dict(),  # Tangle expects the YAML/JSON spec here
                        "is_deleted": False,
                    }
                )
        except Exception as e:
            # Skip tools that fail to initialize (e.g., missing env vars)
            continue
    return components


@tangle_router.get("/pipeline_runs/", dependencies=[Depends(get_api_key)])
async def list_pipeline_runs():
    """Returns an empty list for now until Consul integration is complete."""
    return []


@tangle_router.get("/component_libraries/", dependencies=[Depends(get_api_key)])
async def list_component_libraries():
    """Mock component libraries list."""
    return []
