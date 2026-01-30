import uvicorn
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import inspect
import os
from typing import Optional

from tools.ssh_tool import SSH_Tool
from tools.desktop_control_tool import DesktopControlTool
from tools.code_runner_tool import CodeRunnerTool
from tools.web_browser_tool import WebBrowserTool
from tools.ansible_tool import Ansible_Tool
from tools.power_tool import Power_Tool
from tools.summarizer_tool import SummarizerTool
from tools.term_everything_tool import TermEverythingTool
from tools.rag_tool import RAG_Tool
from tools.ha_tool import HA_Tool
from tools.git_tool import Git_Tool
from tools.orchestrator_tool import OrchestratorTool
from tools.search_tool import SearchTool

app = FastAPI()

class ToolRequest(BaseModel):
    tool: str
    method: str
    args: dict = {}

# Instantiate all available tools
tools = {
    "ssh": SSH_Tool(),
    "desktop_control": DesktopControlTool(),
    "code_runner": CodeRunnerTool(),
    "web_browser": WebBrowserTool(),
    "ansible": Ansible_Tool(),
    "power": Power_Tool(),
    "term_everything": TermEverythingTool(app_image_path="/opt/mcp/termeverything.AppImage"),
    "rag": RAG_Tool(base_dir="/"),
    "ha": HA_Tool(ha_url=None, ha_token=None), # These will be configured later if needed
    "git": Git_Tool(root_dir="/opt/pipecatapp"),
    "orchestrator": OrchestratorTool(),
    "search": SearchTool(root_dir="/opt/pipecatapp"),
}

API_KEY = os.getenv("TOOL_SERVER_API_KEY")

@app.post("/run_tool/")
async def run_tool(request: ToolRequest, authorization: Optional[str] = Header(None)):
    """
    Executes a method on a specified tool with the given arguments.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured on server.")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing.")

    try:
        auth_type, token = authorization.split()
        if auth_type.lower() != "bearer" or token != API_KEY:
            raise HTTPException(status_code=403, detail="Invalid credentials.")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format.")

    if request.tool not in tools:
        raise HTTPException(status_code=404, detail=f"Tool '{request.tool}' not found.")

    tool_instance = tools[request.tool]

    if not hasattr(tool_instance, request.method):
        raise HTTPException(status_code=404, detail=f"Method '{request.method}' not found on tool '{request.tool}'.")

    method = getattr(tool_instance, request.method)

    if not callable(method) or request.method.startswith("_"):
        raise HTTPException(status_code=403, detail=f"Method '{request.method}' is not a public callable method.")

    try:
        # For simplicity, this example assumes synchronous tool methods.
        # If any tool methods were async, this would need to be awaited.
        result = method(**request.args)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")

@app.get("/tools/")
async def list_tools():
    """
    Returns a list of available tools and their methods.
    """
    available_tools = {}
    for tool_name, tool_instance in tools.items():
        methods = {}
        for method_name, method in inspect.getmembers(tool_instance, predicate=inspect.ismethod):
            if not method_name.startswith('_'):
                methods[method_name] = {
                    "doc": method.__doc__,
                    "args": inspect.getfullargspec(method).args[1:] # Exclude 'self'
                }
        available_tools[tool_name] = methods
    return available_tools

if __name__ == "__main__":
    host_ip = os.getenv("HOST_IP", "::")
    uvicorn.run(app, host=host_ip, port=8001)
