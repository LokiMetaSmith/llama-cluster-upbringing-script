from fastapi import FastAPI, Request, HTTPException
import subprocess
import json
import os
import asyncio

app = FastAPI(title="REA Tool Server")

# Basic HTTP wrap over the REA MCP CLI / Server
@app.post("/run_tool/{tool_name}")
async def run_tool(tool_name: str, request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    # We will invoke the CLI interface for now, or adapt to full MCP.
    # To keep it simple, we use the `npx rea-agents` commands if they map to the tool.

    # Since REA exposes MCP over stdio natively, the proper way is to have the python
    # client in pipecatapp talk to the `rea-agents` stdio directly via a custom script
    # or the MCP python SDK.

    cmd = ["npx", "rea-agents", "analyze-javascript-application", body.get("target_path", "."), "--json"]

    # As a simple wrapper for testing:
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="/tmp"
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        return {"error": stderr.decode()}

    try:
        return json.loads(stdout.decode())
    except json.JSONDecodeError:
        return {"result": stdout.decode()}

@app.get("/health")
def health():
    return {"status": "ok", "role": "rea"}
