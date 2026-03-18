import os
import json
import glob
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Prompt Engineering Archive Server")

ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "archive")
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

@app.get("/api/tree")
def get_tree():
    """
    Reads the archive directory and returns a JSON representation of the evolutionary tree.
    """
    if not os.path.isdir(ARCHIVE_DIR):
        return JSONResponse(status_code=404, content={"error": f"Archive directory not found at {ARCHIVE_DIR}"})

    meta_files = glob.glob(os.path.join(ARCHIVE_DIR, "*.json"))
    if not meta_files:
        return JSONResponse(content={"nodes": [], "edges": []})

    nodes = []
    edges = []
    all_agents = {}

    # First pass: Add all agents as nodes
    for meta_file in meta_files:
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
                agent_id = os.path.basename(meta_file).replace(".json", "")
                all_agents[agent_id] = meta

                fitness = meta.get("fitness", 0.0)
                rationale = meta.get("rationale", "N/A")

                # Attempt to read the corresponding python file
                py_file = os.path.join(ARCHIVE_DIR, f"{agent_id}.py")
                code = "Code not found."
                if os.path.isfile(py_file):
                    with open(py_file, 'r') as pf:
                        code = pf.read()

                nodes.append({
                    "id": agent_id,
                    "label": f"{agent_id}\n{fitness:.4f}",
                    "fitness": fitness,
                    "rationale": rationale,
                    "code": code
                })

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read or parse metadata file {meta_file}: {e}")

    # Second pass: Add edges
    root_added = False
    for agent_id, meta in all_agents.items():
        parent_id = meta.get("parent")
        if parent_id and parent_id in all_agents:
            edges.append({
                "from": parent_id,
                "to": agent_id
            })
        elif parent_id is None:
            # Connect to root
            edges.append({
                "from": "root",
                "to": agent_id
            })
            if not root_added:
                nodes.append({
                    "id": "root",
                    "label": "Initial Seed",
                    "fitness": 0.0,
                    "rationale": "Initial state",
                    "code": "Original app.py code"
                })
                root_added = True

    return JSONResponse(content={"nodes": nodes, "edges": edges})

# Ensure frontend dir exists
os.makedirs(FRONTEND_DIR, exist_ok=True)

# Mount the static files directory at the root URL
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
