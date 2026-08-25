import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from pipecatapp.web_server import app, COMMUNITY_APPS_CATALOG

client = TestClient(app)

def test_get_apps_catalog():
    response = client.get("/api/apps/catalog")
    assert response.status_code == 200
    catalog = response.json()
    assert isinstance(catalog, list)
    assert len(catalog) == len(COMMUNITY_APPS_CATALOG)
    app_ids = [a["id"] for a in catalog]
    assert "pihole" in app_ids
    assert "nextcloud" in app_ids

@patch("pipecatapp.web_server.service_discovery_client.get")
def test_get_installed_apps(mock_get):
    # Mock Nomad jobs response
    mock_nomad_resp = MagicMock()
    mock_nomad_resp.status_code = 200
    mock_nomad_resp.json.return_value = [
        {"ID": "pihole", "Status": "running", "Type": "service", "CreateIndex": 100, "ModifyIndex": 101}
    ]
    mock_get.return_value = mock_nomad_resp

    response = client.get("/api/apps/installed")
    assert response.status_code == 200
    installed = response.json()
    assert isinstance(installed, list)
    assert len(installed) == 1
    assert installed[0]["id"] == "pihole"
    assert installed[0]["status"] == "running"

def test_install_community_app_rbac_denied():
    response = client.post(
        "/api/apps/install",
        json={"app_id": "pihole", "domain_name": "pihole.local"},
        headers={"X-User-Role": "viewer"}
    )
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

@patch("asyncio.create_subprocess_exec")
def test_install_community_app_success(mock_subproc):
    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    mock_proc.communicate.return_value = (b"Playbook execution successful", b"")
    mock_subproc.return_value = mock_proc

    response = client.post(
        "/api/apps/install",
        json={"app_id": "pihole", "domain_name": "pihole.local"},
        headers={"X-User-Role": "admin"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@patch("pipecatapp.web_server.service_discovery_client.delete")
def test_remove_community_app_success(mock_delete):
    mock_delete_resp = MagicMock()
    mock_delete_resp.status_code = 200
    mock_delete.return_value = mock_delete_resp

    response = client.delete(
        "/api/apps/remove/pihole",
        headers={"X-User-Role": "admin"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

@patch("asyncio.create_subprocess_exec")
def test_upgrade_community_app_success(mock_subproc):
    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    mock_proc.communicate.return_value = (b"Upgrade triggered", b"")
    mock_subproc.return_value = mock_proc

    response = client.post(
        "/api/apps/upgrade",
        json={"app_id": "pihole", "target_image": "pihole/pihole:v5.1"},
        headers={"X-User-Role": "admin"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
