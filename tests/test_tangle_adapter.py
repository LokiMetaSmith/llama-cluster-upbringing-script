import pytest
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI
from pipecatapp.tangle_adapter import tangle_router
from pipecatapp.api_keys import initialize_api_keys, get_api_key_hash

# Initialize a test API key for the tests
test_key = "test_key_123"
initialize_api_keys([get_api_key_hash(test_key)])

app = FastAPI()
app.include_router(tangle_router)

client = TestClient(app)

def test_get_current_user_auth_required():
    response = client.get("/api/users/me")
    assert response.status_code == 401

def test_get_current_user_authenticated():
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {test_key}"})
    assert response.status_code == 200
    assert response.json()["id"] == "admin"

def test_list_published_components_auth_required():
    response = client.get("/api/published_components/")
    assert response.status_code == 401

def test_list_published_components_authenticated():
    response = client.get("/api/published_components/", headers={"Authorization": f"Bearer {test_key}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Check if a known tool is in the list (e.g. search)
    assert any(c["name"] == "search" for c in data), "Expected 'search' tool to be converted and returned"

def test_list_pipeline_runs_auth_required():
    response = client.get("/api/pipeline_runs/")
    assert response.status_code == 401

def test_list_pipeline_runs_authenticated():
    response = client.get("/api/pipeline_runs/", headers={"Authorization": f"Bearer {test_key}"})
    assert response.status_code == 200
    assert response.json() == []
