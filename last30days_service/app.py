import os
import subprocess
import tempfile
import json
import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Last30DaysService")

app = FastAPI(title="Last30Days Research Service")

# Authentication key shared with the cluster
API_KEY = os.getenv("TOOL_SERVER_API_KEY")

class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The core subject to research")
    query_type: Optional[str] = Field(None, description="Specific framing/type")
    days: Optional[int] = Field(30, description="The lookback window")
    depth: Optional[int] = Field(None, description="Scrape depth/breadth")

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.post("/research")
def perform_research(req: ResearchRequest, authorization: Optional[str] = Header(None)):
    """
    Executes the last30days engine via subprocess and returns the compact synthesis.
    """
    if API_KEY:
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header is missing.")
        try:
            auth_type, token = authorization.split()
            if auth_type.lower() != "bearer" or token != API_KEY:
                raise HTTPException(status_code=403, detail="Invalid credentials.")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header format.")

    # We will build the command arguments
    engine_path = "/app/last30days-skill/skills/last30days/scripts/last30days.py"
    if not os.path.exists(engine_path):
        # Fallback if local dev paths or different structure
        engine_path = "last30days-skill/skills/last30days/scripts/last30days.py"

    cmd = [
        "python3",
        engine_path,
        req.topic,
        "--emit=compact"
    ]

    if req.days:
        cmd.append(f"--days={req.days}")

    if req.depth:
        # Depth mapping: 1 -> quick, 2 -> balanced, 3 -> deep
        if req.depth == 1:
            cmd.append("--quick")
        elif req.depth == 3:
            cmd.append("--deep")

    # The engine has an internal planner. Since we are in headless/microservice mode,
    # it will plan internally using configured web keys.
    env = os.environ.copy()
    env["SETUP_COMPLETE"] = "true"  # Bypass first-run setup wizard prompts
    env["LAST30DAYS_MEMORY_DIR"] = "/tmp/last30days"

    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            timeout=300 # 5 minutes maximum
        )
        if result.returncode != 0:
            logger.error(f"Engine failed with exit code {result.returncode}. Stderr: {result.stderr}")
            raise HTTPException(
                status_code=500,
                detail=f"Research engine execution failed: {result.stderr or result.stdout}"
            )

        return {"result": result.stdout}
    except subprocess.TimeoutExpired:
        logger.error("Engine execution timed out")
        raise HTTPException(status_code=504, detail="Research engine execution timed out.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
