import subprocess
import threading
import fcntl
import time
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import yaml
import os
from datetime import datetime

app = FastAPI()

# --- Constants and Configuration ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
INVENTORY_PATH = os.path.join(PROJECT_ROOT, "inventory.yaml")
PLAYBOOK_PATH = os.path.join(PROJECT_ROOT, "playbook.yaml")
TODO_PATH = os.path.join(PROJECT_ROOT, "TODO.md")

# --- In-memory Job Tracking ---
provisioning_jobs = {}

# --- Helper Functions ---
def run_ansible_playbook(hostname: str, ip_address: str):
    job_id = f"{hostname}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    provisioning_jobs[hostname] = {
        "status": "running",
        "start_time": datetime.now().isoformat(),
        "end_time": None,
        "log": "",
        "job_id": job_id
    }

    ansible_command = ["ansible-playbook", "-l", hostname, PLAYBOOK_PATH]

    try:
        process = subprocess.Popen(
            ansible_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        log_buffer = []
        for line in process.stdout:
            log_buffer.append(line)
            provisioning_jobs[hostname]["log"] = "".join(log_buffer)

        process.wait()

        if process.returncode == 0:
            provisioning_jobs[hostname]["status"] = "success"
            print(f"Ansible playbook finished successfully for {hostname}")
        else:
            provisioning_jobs[hostname]["status"] = "failed"
            error_message = f"Ansible playbook failed for {hostname} with return code {process.returncode}."
            print(error_message)
            # Add to TODO list
            with open(TODO_PATH, "a") as f:
                f.write(f"\n---\n")
                f.write(f"### Provisioning Failed for `{hostname}`\n")
                f.write(f"- **IP Address:** {ip_address}\n")
                f.write(f"- **Timestamp:** {datetime.now().isoformat()}\n")
                f.write(f"- **Error Log:**\n")
                f.write("```\n")
                f.write("".join(log_buffer))
                f.write("\n```\n")

    except Exception as e:
        provisioning_jobs[hostname]["status"] = "failed"
        error_log = f"An exception occurred while running Ansible for {hostname}: {e}\n{provisioning_jobs[hostname]['log']}"
        provisioning_jobs[hostname]["log"] = error_log
        print(error_log)
    finally:
        provisioning_jobs[hostname]["end_time"] = datetime.now().isoformat()

@app.post("/api/ready-for-provisioning")
async def provision_node(request: Request, background_tasks: BackgroundTasks):
    try:
        payload = await request.json()
        new_ip = payload.get("ip_address")
        hostname = payload.get("hostname")

        if not all([new_ip, hostname]):
            raise HTTPException(status_code=400, detail="ip_address and hostname are required")

        if hostname in provisioning_jobs and provisioning_jobs[hostname]["status"] == "running":
            return JSONResponse(status_code=409, content={"message": f"Provisioning for {hostname} is already in progress."})

        print(f"Received provisioning request for hostname: {hostname} at IP: {new_ip}")

        # --- Update Inventory (with file locking) ---
        print(f"Updating inventory file: {INVENTORY_PATH}")
        with open(INVENTORY_PATH, 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                inventory = yaml.safe_load(f) or {'all': {'children': {'worker_nodes': {'hosts': {}}}}}

                # Ensure the structure is what we expect
                if 'all' not in inventory or 'children' not in inventory['all'] or 'worker_nodes' not in inventory['all']['children'] or 'hosts' not in inventory['all']['children']['worker_nodes']:
                    raise HTTPException(status_code=500, detail="Inventory file has an unexpected format.")

                worker_hosts = inventory['all']['children']['worker_nodes']['hosts']
                if hostname not in worker_hosts:
                    worker_hosts[hostname] = {'ansible_host': new_ip}
                    f.seek(0)
                    yaml.dump(inventory, f, default_flow_style=False)
                    f.truncate()
                    print(f"Added {hostname} to inventory.")
                else:
                    print(f"{hostname} already exists in inventory. Skipping inventory update.")
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

        # --- Run Ansible Playbook in Background ---
        background_tasks.add_task(run_ansible_playbook, hostname, new_ip)

        return JSONResponse(status_code=202, content={"message": f"Accepted provisioning request for {hostname}. Ansible playbook started."})

    except Exception as e:
        print(f"Error processing provisioning request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/provisioning/status")
async def get_all_statuses():
    """Returns the status of all known provisioning jobs."""
    return JSONResponse(content=provisioning_jobs)

@app.get("/api/provisioning/status/{hostname}")
async def get_status(hostname: str):
    """Returns the status of a specific provisioning job."""
    if hostname not in provisioning_jobs:
        raise HTTPException(status_code=404, detail="Job not found for this hostname.")
    return JSONResponse(content=provisioning_jobs[hostname])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
