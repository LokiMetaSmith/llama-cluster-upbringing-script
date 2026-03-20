import pytest
from fastapi.testclient import TestClient
from pipecatapp.web_server import app

client = TestClient(app)

def test_get_personality():
    # Will fail unauthorized initially because of get_api_key security
    response = client.get("/api/personality")
    assert response.status_code == 401
