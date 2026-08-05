import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/tap_orchestrator')))

from main import app, process_tap_event
from models import DesfireEvent, AuthentikUser
from config import settings
from deduplicator import deduplicator

client = TestClient(app)

@pytest.fixture
def sample_event():
    return DesfireEvent(
        event="desfire_authenticated",
        user_id="lawrence",
        reader_id="test_reader",
        timestamp=1785860545,
        auth_type="desfire_ev2_aes128"
    )

@pytest.fixture(autouse=True)
def set_env_vars():
    os.environ["TAP_ORCHESTRATOR_SECRET"] = "test_secret"
    yield
    if "TAP_ORCHESTRATOR_SECRET" in os.environ:
        del os.environ["TAP_ORCHESTRATOR_SECRET"]

@pytest.fixture(autouse=True)
def reset_deduplicator():
    deduplicator._last_tap = {}
    yield

def test_http_endpoint_unauthorized(sample_event):
    response = client.post(
        "/api/v1/tap-event",
        json=sample_event.model_dump(),
        headers={"X-Tap-Secret": "wrong_secret"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

@patch("main.process_tap_event")
def test_http_endpoint_authorized(mock_process, sample_event):
    # Setup mock
    mock_process.return_value = None

    response = client.post(
        "/api/v1/tap-event",
        json=sample_event.model_dump(),
        headers={"X-Tap-Secret": settings.tap_orchestrator_secret}
    )

    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Tap event queued for processing"}

def test_deduplicator():
    assert deduplicator.is_allowed("user1") == True
    assert deduplicator.is_allowed("user1") == False # Under cooldown
    assert deduplicator.is_allowed("user2") == True

@pytest.mark.asyncio
@patch("main.authentik_client.get_user")
@patch("main.cluster_orchestrator.execute_hot_load")
async def test_process_tap_event_success(mock_execute, mock_get_user, sample_event):
    mock_user = AuthentikUser(username="lawrence", is_active=True, groups=["admin"])
    mock_get_user.return_value = mock_user

    await process_tap_event(sample_event)

    mock_get_user.assert_called_once_with("lawrence")
    mock_execute.assert_called_once_with(mock_user)

@pytest.mark.asyncio
@patch("main.authentik_client.get_user")
@patch("main.publish_mqtt_status")
async def test_process_tap_event_user_not_found(mock_publish, mock_get_user, sample_event):
    mock_get_user.return_value = None
    mock_mqtt_client = MagicMock()

    await process_tap_event(sample_event, mqtt_client=mock_mqtt_client)

    mock_get_user.assert_called_once_with("lawrence")
    mock_publish.assert_called_once_with(mock_mqtt_client, settings.mqtt_topic_failure, "error", "User not found", "lawrence")

@pytest.mark.asyncio
@patch("main.authentik_client.get_user")
@patch("main.publish_mqtt_status")
async def test_process_tap_event_user_inactive(mock_publish, mock_get_user, sample_event):
    mock_user = AuthentikUser(username="lawrence", is_active=False)
    mock_get_user.return_value = mock_user
    mock_mqtt_client = MagicMock()

    await process_tap_event(sample_event, mqtt_client=mock_mqtt_client)

    mock_get_user.assert_called_once_with("lawrence")
    mock_publish.assert_called_once_with(mock_mqtt_client, settings.mqtt_topic_failure, "error", "User disabled", "lawrence")

@pytest.mark.asyncio
@patch("orchestrator.asyncio.create_subprocess_exec")
async def test_orchestrator_wake_node(mock_subprocess):
    from orchestrator import cluster_orchestrator

    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    mock_proc.communicate.return_value = (b'success', b'')
    mock_subprocess.return_value = mock_proc

    await cluster_orchestrator.wake_node("AA:BB:CC:DD:EE:FF")

    mock_subprocess.assert_called_once_with(
        "wakeonlan", "AA:BB:CC:DD:EE:FF",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

@pytest.mark.asyncio
@patch("orchestrator.httpx.AsyncClient.post")
async def test_authentik_get_token(mock_post):
    from authentik import AuthentikClient

    # Unset static token to test CCG flow
    with patch("authentik.settings.authentik_token", None), \
         patch("authentik.settings.authentik_client_id", "test_id"), \
         patch("authentik.settings.authentik_client_secret", "test_secret"):

        client = AuthentikClient()

        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "test_dynamic_token"}
        mock_post.return_value = mock_response

        token = await client._get_token()
        assert token == "test_dynamic_token"
        mock_post.assert_called_once()
        await client.close()
