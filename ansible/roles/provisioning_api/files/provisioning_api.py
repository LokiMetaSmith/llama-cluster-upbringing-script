import subprocess
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import yaml
import os

app = FastAPI()

# Assuming this script is in ansible/roles/provisioning_api/files/
# The project root is 4 levels up.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
INVENTORY_PATH = os.path.join(PROJECT_ROOT, "inventory.yaml")
PLAYBOOK_PATH = os.path.join(PROJECT_ROOT, "playbook.yaml")

@app.post("/api/ready-for-provisioning")
async def provision_node(request: Request):
    try:
        payload = await request.json()
        new_ip = payload.get("ip_address")

        if not new_ip:
            raise HTTPException(status_code=400, detail="ip_address is required")

        print(f"Received provisioning request for IP: {new_ip}")

        # --- Update Inventory ---
        print(f"Updating inventory file: {INVENTORY_PATH}")
        with open(INVENTORY_PATH, 'r') as f:
            inventory = yaml.safe_load(f)

        # Ensure the structure is what we expect
        if 'all' not in inventory or 'children' not in inventory['all'] or 'worker_nodes' not in inventory['all']['children'] or 'hosts' not in inventory['all']['children']['worker_nodes']:
             raise HTTPException(status_code=500, detail="Inventory file has an unexpected format.")

        if new_ip not in inventory['all']['children']['worker_nodes']['hosts']:
            inventory['all']['children']['worker_nodes']['hosts'][new_ip] = {}
            with open(INVENTORY_PATH, 'w') as f:
                yaml.dump(inventory, f, default_flow_style=False)
            print(f"Added {new_ip} to inventory.")
        else:
            print(f"{new_ip} already exists in inventory. Skipping inventory update.")

        # --- Run Ansible Playbook ---
        ansible_command = [
            "ansible-playbook",
            "-l", new_ip,
            PLAYBOOK_PATH
        ]

        print(f"Running Ansible command: {' '.join(ansible_command)}")

        # Using subprocess.Popen to run in the background and not block the API
        process = subprocess.Popen(ansible_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # We can optionally log the output later or just let it run.
        # For now, we just fire and forget.

        return JSONResponse(status_code=202, content={"message": f"Accepted provisioning request for {new_ip}. Ansible playbook started."})

    except Exception as e:
        print(f"Error processing provisioning request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
