from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Tool Server"}

@app.get("/health")
def read_health():
    return {"status": "ok"}
