import sys
import os
import time
import asyncio
import threading
import uvicorn
import sqlite3
from contextlib import contextmanager

# Add repo root to path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(REPO_ROOT)
sys.path.append(os.path.join(REPO_ROOT, "pipecatapp"))
sys.path.append(os.path.join(REPO_ROOT, "ansible/roles/memory_service/files"))

from pipecatapp.pmm_memory_client import PMMMemoryClient
from pipecatapp.janitor_agent import JanitorAgent

PORT = 8123
DB_PATH = "test_dlq.db"

# Cleanup before import so the app initializes a fresh DB
if os.path.exists(DB_PATH):
    try:
        os.remove(DB_PATH)
    except:
        pass

# Set env before importing app to avoid PermissionError on /data
os.environ["MEMORY_DB_PATH"] = DB_PATH
from ansible.roles.memory_service.files.app import app

def run_server():
    # Disable access logs to keep output clean
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="critical")

@contextmanager
def test_server():
    # Start server
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(2) # Wait for startup

    try:
        yield f"http://127.0.0.1:{PORT}"
    finally:
        # Cleanup End
        if os.path.exists(DB_PATH):
            try:
                os.remove(DB_PATH)
            except:
                pass

async def run_test():
    with test_server() as url:
        print(f"--- Server started at {url} ---")
        client = PMMMemoryClient(base_url=url)

        # 1. Enqueue Item
        print("[1] Enqueueing item...")
        item_id = await client.enqueue_dlq_item(
            event_type="test_failure",
            payload={"foo": "bar"},
            error_reason="Something went wrong"
        )
        print(f"    Item enqueued: {item_id}")

        # 2. Verify it is there via Manual Claim
        print("[2] verifying existence via manual claim...")
        item = await client.claim_dlq_item("manual_tester", ["test_failure"])
        assert item is not None
        assert item['id'] == item_id
        assert item['status'] == 'PROCESSING'
        print("    Manual claim successful. Item is now PROCESSING.")

        # Reset to PENDING so Janitor can take it
        print("    Resetting item to PENDING...")
        # Note: We need to use update_dlq_item with status='PENDING'.
        # The method supports this.
        await client.update_dlq_item(item_id, status="PENDING")

        # 3. Run Janitor
        print("[3] Starting Janitor Agent...")
        os.environ["MEMORY_SERVICE_URL"] = url
        janitor = JanitorAgent()

        # Run janitor in background task
        janitor_task = asyncio.create_task(janitor.run())

        # Wait for janitor to process (it sleeps 5s if empty, but here it should find it immediately)
        # Give it a few seconds
        await asyncio.sleep(4)

        print("    Stopping Janitor...")
        janitor.stop()
        try:
             await asyncio.wait_for(janitor_task, timeout=1)
        except asyncio.TimeoutError:
            pass # Expected
        except Exception as e:
            print(f"Janitor error: {e}")

        # 4. Verify SUCCEEDED via SQLite direct inspection
        print("[4] Verifying final state in DB...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT status, error_reason FROM dlq WHERE id = ?", (item_id,))
        row = cursor.fetchone()

        print(f"    Final DB Row: {row}")

        if row[0] == 'SUCCEEDED':
            print("--- TEST PASSED: Item status is SUCCEEDED ---")
        else:
            print(f"--- TEST FAILED: Item status is {row[0]} ---")
            sys.exit(1)

        conn.close()

if __name__ == "__main__":
    asyncio.run(run_test())
