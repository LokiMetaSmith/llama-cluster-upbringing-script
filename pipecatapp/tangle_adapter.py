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


@tangle_router.get("/components", dependencies=[Depends(get_api_key)])
async def list_components():
    """Alias for /published_components/ to match standard component endpoint."""
    return await list_published_components()


def _map_status(internal_status: str) -> str:
    status = internal_status.lower()
    if status == "completed" or status == "succeeded":
        return "SUCCEEDED"
    elif status == "failed":
        return "FAILED"
    elif status == "running":
        return "RUNNING"
    elif status == "waiting":
        return "WAITING"
    return "UNKNOWN"


def _format_time(t) -> int:
    if t is None:
        return 0
    return int(t * 1000)


@tangle_router.get("/pipeline_runs/", dependencies=[Depends(get_api_key)])
async def list_pipeline_runs():
    """Dynamically fetches active and historical pipeline runs from WorkflowHistory and ActiveWorkflows."""
    from pipecatapp.workflow.history import WorkflowHistory
    from pipecatapp.workflow.runner import ActiveWorkflows
    import asyncio

    history = WorkflowHistory()
    loop = asyncio.get_running_loop()
    historical_runs = await loop.run_in_executor(
        None, lambda: history.get_all_runs(limit=50)
    )

    active_workflows = ActiveWorkflows()
    active_states = active_workflows.get_all_states(sanitize=True)

    runs = []

    # Process active runs
    for run_id, state in active_states.items():
        runs.append(
            {
                "id": run_id,
                "name": state.get("workflow_definition", {}).get(
                    "name", "Unnamed Workflow"
                ),
                "status": _map_status(state.get("status", "running")),
                "created_at": _format_time(state.get("start_time", 0)),
                "finished_at": None,
            }
        )

    # Process historical runs
    # To prevent duplicates if a run just finished but is still in active somehow
    active_ids = set([r["id"] for r in runs])
    for run in historical_runs:
        if run["id"] not in active_ids:
            runs.append(
                {
                    "id": run["id"],
                    "name": run.get("workflow_name", "Unnamed Workflow"),
                    "status": _map_status(run.get("status", "completed")),
                    "created_at": _format_time(run.get("start_time", 0)),
                    "finished_at": _format_time(run.get("end_time", 0)),
                }
            )

    # Sort by created_at descending
    runs.sort(key=lambda x: x["created_at"], reverse=True)
    return runs


@tangle_router.get("/pipeline_runs/{run_id}", dependencies=[Depends(get_api_key)])
async def get_pipeline_run(run_id: str):
    """Fetches specific run details for Tangle UI."""
    from pipecatapp.workflow.history import WorkflowHistory
    from pipecatapp.workflow.runner import ActiveWorkflows
    import asyncio

    active_workflows = ActiveWorkflows()
    active_runner = active_workflows.get_runner(run_id)

    if active_runner:
        state = active_runner.context_to_dict(sanitize=True)
        return {
            "id": run_id,
            "name": state.get("workflow_definition", {}).get(
                "name", "Unnamed Workflow"
            ),
            "status": _map_status(state.get("status", "running")),
            "created_at": _format_time(state.get("start_time", 0)),
            "finished_at": None,
            "details": state,
        }

    history = WorkflowHistory()
    loop = asyncio.get_running_loop()
    run_details = await loop.run_in_executor(None, lambda: history.get_run(run_id))

    if not run_details:
        raise HTTPException(status_code=404, detail="Pipeline run not found.")

    return {
        "id": run_id,
        "name": run_details.get("workflow_name", "Unnamed Workflow"),
        "status": _map_status(run_details.get("status", "completed")),
        "created_at": _format_time(run_details.get("start_time", 0)),
        "finished_at": _format_time(run_details.get("end_time", 0)),
        "details": run_details.get("final_state", {}),
    }


@tangle_router.get("/component_libraries/", dependencies=[Depends(get_api_key)])
async def list_component_libraries():
    """Mock component libraries list."""
    return []
