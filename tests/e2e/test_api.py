import requests
import os
import hashlib
import secrets
import subprocess
import time
import pytest

# Base URL of the service to test
BASE_URL = "http://localhost:8000"

def get_api_key_hash(api_key: str) -> str:
    """Hashes an API key using SHA-256."""
    return hashlib.sha256(api_key.encode()).hexdigest()

@pytest.fixture(scope="module")
def api_key_and_hash():
    """Generate an API key and its hash for testing."""
    key = secrets.token_hex(32)
    hashed_key = get_api_key_hash(key)
    return key, hashed_key

@pytest.fixture(scope="module", autouse=True)
def start_service(api_key_and_hash):
    """
    A pytest fixture to manage the lifecycle of the pipecat application
    for the duration of the test module. It starts the service with a test
    API key and ensures it's terminated afterward.
    """
    _, hashed_key = api_key_and_hash

    # Set the environment variable for the subprocess
    env = os.environ.copy()
    env["PIECAT_API_KEYS"] = hashed_key
    env["PYTHONPATH"] = "./docker/pipecatapp"

    # Start the FastAPI server as a subprocess
    # We run it from the root directory to ensure all paths are correct
    process = subprocess.Popen(
        ["python", "-m", "uvicorn", "test_server:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=os.path.abspath("docker/pipecatapp"),
        env=env,
    )

    # Wait for the service to be ready
    for _ in range(10):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200 or response.status_code == 503: # 503 is also ok as it means server is up but agent not ready
                print("Service is up.")
                break
        except requests.ConnectionError:
            time.sleep(1)
    else:
        process.terminate()
        process.wait()
        pytest.fail("Service failed to start.")

    yield

    # Teardown: stop the server
    process.terminate()
    process.wait()
    print("Service terminated.")

def test_api_status_unauthorized_no_key():
    """Verify that accessing a protected endpoint without an API key fails."""
    response = requests.get(f"{BASE_URL}/api/status")
    assert response.status_code == 401
    assert "Missing API Key" in response.json()["detail"]

def test_api_status_unauthorized_invalid_key():
    """Verify that accessing a protected endpoint with an invalid API key fails."""
    headers = {"Authorization": "Bearer invalidkey"}
    response = requests.get(f"{BASE_URL}/api/status", headers=headers)
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["detail"]

def test_api_status_authorized(api_key_and_hash):
    """Verify that accessing a protected endpoint with a valid API key succeeds."""
    api_key, _ = api_key_and_hash
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(f"{BASE_URL}/api/status", headers=headers)
    assert response.status_code == 200
    # The agent isn't fully running, so we expect this specific status message
    assert "Agent not fully initialized" in response.json()["status"]