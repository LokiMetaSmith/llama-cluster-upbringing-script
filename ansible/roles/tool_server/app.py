from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Tool Server"}

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.get("/tools/")
async def get_tools():
    return {"message": "Tools endpoint is healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
