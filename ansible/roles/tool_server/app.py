from fastapi import FastAPI

app = FastAPI()

@app.get("/tools/")
async def get_tools():
    return {"message": "Tools endpoint is healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)