import uvicorn
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import sys

# Ensure pipecatapp is in path so we can import RAG_Tool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from pipecatapp.tools.rag_tool import RAG_Tool

app = FastAPI(title="RAG Microservice")

# A simple security scheme if needed, though Consul Connect handles mTLS
security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    expected_token = os.getenv("RAG_SERVICE_API_KEY")
    if expected_token and (not credentials or credentials.credentials != expected_token):
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    return True

# Initialize the RAG Tool singleton
rag_tool_instance = None

@app.on_event("startup")
async def startup_event():
    global rag_tool_instance
    # Using defaults or env vars for initialization
    base_dir = os.getenv("RAG_BASE_DIR", ".")
    allowed_root = os.getenv("RAG_ALLOWED_ROOT", None)
    allow_root_scan = os.getenv("RAG_ALLOW_ROOT_SCAN", "False").lower() == "true"

    rag_tool_instance = RAG_Tool(
        base_dir=base_dir,
        allowed_root=allowed_root,
        allow_root_scan=allow_root_scan
    )

class AddDocumentRequest(BaseModel):
    filepath: str

class SearchRequest(BaseModel):
    query: str
    k: int = 5

class ScanDirectoryRequest(BaseModel):
    directory: str

@app.post("/add_document", dependencies=[Depends(verify_token)])
async def add_document(req: AddDocumentRequest):
    try:
        result = await rag_tool_instance.add_document(req.filepath)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", dependencies=[Depends(verify_token)])
async def search(req: SearchRequest):
    try:
        result = await rag_tool_instance.search(req.query, k=req.k)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan_directory", dependencies=[Depends(verify_token)])
async def scan_directory(req: ScanDirectoryRequest):
    try:
        result = await rag_tool_instance.scan_directory(req.directory)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("rag_server:app", host="0.0.0.0", port=port, reload=False)
