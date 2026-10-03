import uvicorn
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import inspect
import os
import secrets
from typing import Optional

if __package__:
    from .rate_limiter import RateLimiter
else:
    from pipecatapp.rate_limiter import RateLimiter

import logging

logger = logging.getLogger("ToolServer")

app = FastAPI()

class ToolRequest(BaseModel):
    tool: str
    method: str
    args: dict = {}

tools = {}

def _safe_import_and_init(name: str, module_path: str, class_name: str, factory=None):
    """Safely import and initialize a tool, omitting it gracefully if dependencies or paths are missing."""
    try:
        import importlib
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        instance = factory(cls) if factory else cls()
        if instance is not None:
            tools[name] = instance
    except Exception as e:
        logger.warning(f"ToolServer: Optional tool '{name}' could not be initialized ({e}). It will be omitted.")

_safe_import_and_init("ssh", "pipecatapp.tools.ssh_tool", "SSH_Tool")
_safe_import_and_init("desktop_control", "pipecatapp.tools.desktop_control_tool", "DesktopControlTool")
_safe_import_and_init("code_runner", "pipecatapp.tools.code_runner_tool", "CodeRunnerTool")
_safe_import_and_init("web_browser", "pipecatapp.tools.web_browser_tool", "WebBrowserTool")
_safe_import_and_init("ansible", "pipecatapp.tools.ansible_tool", "Ansible_Tool")
_safe_import_and_init("power", "pipecatapp.tools.power_tool", "Power_Tool")
_safe_import_and_init("summarizer", "pipecatapp.tools.summarizer_tool", "SummarizerTool", lambda cls: cls(twin_service=None))
_safe_import_and_init("term_everything", "pipecatapp.tools.term_everything_tool", "TermEverythingTool",
                      lambda cls: cls(app_image_path=os.getenv("TERM_EVERYTHING_PATH", "/opt/mcp/tools/termeverything.AppImage")))
_safe_import_and_init("rag", "pipecatapp.tools.rag_tool", "RAG_Tool",
                      lambda cls: cls(pmm_memory=None, base_dir=os.getenv("RAG_BASE_DIR", "/mnt/host_repo" if os.path.exists("/mnt/host_repo") else os.getcwd())))
_safe_import_and_init("git", "pipecatapp.tools.git_tool", "Git_Tool")
_safe_import_and_init("orchestrator", "pipecatapp.tools.orchestrator_tool", "OrchestratorTool")
_safe_import_and_init("ocr", "pipecatapp.tools.ocr_tool", "OCRTool")
_safe_import_and_init("wasm", "pipecatapp.tools.wasm_tool", "WasmTool")
_safe_import_and_init("heretic", "pipecatapp.tools.heretic_tool", "HereticTool")

if os.getenv("HA_URL") and os.getenv("HA_TOKEN"):
    _safe_import_and_init("ha", "pipecatapp.tools.ha_tool", "HA_Tool",
                          lambda cls: cls(ha_url=os.getenv("HA_URL"), ha_token=os.getenv("HA_TOKEN")))

API_KEY = os.getenv("TOOL_SERVER_API_KEY")
strict_limiter = RateLimiter(limit=10, window=60)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Format Pydantic validation errors into LLM-friendly instructions.
    Instead of raw JSON schema errors, we provide explicit feedback
    (e.g., 'The required parameter X is missing').
    """
    errors = exc.errors()
    formatted_messages = []

    for error in errors:
        loc = ".".join(str(l) for l in error.get("loc", []))
        msg = error.get("msg", "")
        err_type = error.get("type", "")

        if err_type == "missing":
            formatted_messages.append(f"The required parameter `{loc}` is missing.")
        elif err_type == "extra_forbidden":
            formatted_messages.append(f"An unexpected parameter `{loc}` was provided.")
        elif "type" in err_type:
            formatted_messages.append(f"The parameter `{loc}` has an invalid type: {msg}.")
        else:
            formatted_messages.append(f"Validation error on `{loc}`: {msg}.")

    # LLMs handle a single string block of instructions better than complex JSON error arrays
    formatted_error_str = " ".join(formatted_messages)

    return JSONResponse(
        status_code=422,
        content={"detail": f"Tool argument validation failed: {formatted_error_str} Please verify the required tool parameters."}
    )

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.post("/run_tool/")
async def run_tool(request: ToolRequest, authorization: Optional[str] = Header(None), rate_limit: None = Depends(strict_limiter)):
    """
    Executes a method on a specified tool with the given arguments.
    """
    if not API_KEY:
        # If no API key is configured, we might want to fail open or closed. Failing closed for security.
        raise HTTPException(status_code=500, detail="API key not configured on server.")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing.")
    try:
        auth_type, token = authorization.split()
        if auth_type.lower() != "bearer" or not secrets.compare_digest(token, API_KEY):
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
        # Check if the method is a coroutine (async)
        if inspect.iscoroutinefunction(method):
            result = await method(**request.args)
        else:
            result = method(**request.args)
        return {"result": result}
    except TypeError as e:
        # Provide LLM-friendly error message for missing/unexpected arguments
        error_msg = str(e)
        formatted_error = f"Tool argument validation failed: {error_msg}. Please check the required and available parameters for '{request.tool}.{request.method}'."
        raise HTTPException(status_code=400, detail=formatted_error)
    except Exception as e:
        # Log the error potentially?
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")

@app.get("/tools/")
async def list_tools(authorization: Optional[str] = Header(None)):
    """
    Returns a list of available tools and their methods.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured on server.")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing.")
    try:
        auth_type, token = authorization.split()
        if auth_type.lower() != "bearer" or not secrets.compare_digest(token, API_KEY):
            raise HTTPException(status_code=403, detail="Invalid credentials.")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format.")

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
    uvicorn.run(app, host="0.0.0.0", port=8001)
