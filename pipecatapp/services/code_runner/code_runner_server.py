import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
import os
import sys

# Ensure pipecatapp is in path so we can import tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from pipecatapp.tools.code_runner_tool import CodeRunnerTool

app = FastAPI(title="Code Runner Microservice")

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    expected_token = os.getenv("CODE_RUNNER_API_KEY")
    if expected_token and (not credentials or credentials.credentials != expected_token):
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    return True

# Initialize the CodeRunnerTool
code_runner_instance = None

@app.on_event("startup")
async def startup_event():
    global code_runner_instance
    # Uses nomad or docker based on env setup in the job
    code_runner_instance = CodeRunnerTool()

class ExecuteCodeRequest(BaseModel):
    code: str
    language: str = "python"
    libraries: Optional[List[str]] = None
    timeout: Optional[int] = None

@app.post("/execute", dependencies=[Depends(verify_token)])
def execute_code(req: ExecuteCodeRequest):
    try:
        result = code_runner_instance.execute(
            code=req.code,
            language=req.language,
            libraries=req.libraries,
            timeout=req.timeout
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("code_runner_server:app", host="0.0.0.0", port=port, reload=False)
