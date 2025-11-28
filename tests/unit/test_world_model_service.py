import pytest
import os
import sys
from unittest.mock import MagicMock, patch, AsyncMock

# Add the ansible/roles directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ansible/roles')))

from world_model_service.files.app import app, on_connect, on_message, run_mqtt_client
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Fixture to create a TestClient for the FastAPI app."""
    with patch('world_model_service.files.app.run_mqtt_client'): # Prevent MQTT client from starting
        with TestClient(app) as test_client:
            yield test_client

@pytest.fixture
def mock_mqtt_client():
    """Fixture to mock the paho.mqtt.client."""
    with patch('world_model_service.files.app.mqtt.Client') as mock:
        yield mock.return_value

def test_health_check(client):
    """Tests that the /state endpoint returns the current world state."""
    response = client.get("/state")
    assert response.status_code == 200
    assert response.json() == {}

def test_on_connect_successful(mock_mqtt_client):
    """Tests the on_connect callback with a successful connection."""
    on_connect(mock_mqtt_client, None, None, 0)
    mock_mqtt_client.subscribe.assert_called_with("#")

def test_on_connect_failed(mock_mqtt_client):
    """Tests the on_connect callback with a failed connection."""
    on_connect(mock_mqtt_client, None, None, 1)
    mock_mqtt_client.subscribe.assert_not_called()

def test_on_message():
    """Tests the on_message callback."""
    msg = MagicMock()
    msg.topic = "home/livingroom/light"
    msg.payload = b'{"status": "on"}'
    on_message(None, None, msg)

@patch('world_model_service.files.app.time.sleep', return_value=None)
def test_run_mqtt_client_successful_connection(mock_sleep, mock_mqtt_client):
    """Tests the run_mqtt_client function with a successful connection."""
    mock_mqtt_client.connect.return_value = 0
    run_mqtt_client()
    mock_mqtt_client.connect.assert_called_once()
    mock_mqtt_client.loop_forever.assert_called_once()

@patch('world_model_service.files.app.os._exit')
@patch('world_model_service.files.app.time.sleep', return_value=None)
def test_run_mqtt_client_connection_refused(mock_sleep, mock_exit, mock_mqtt_client):
    """Tests the run_mqtt_client function with a ConnectionRefusedError."""
    mock_mqtt_client.connect.side_effect = ConnectionRefusedError
    run_mqtt_client()
    assert mock_mqtt_client.connect.call_count == 50
    mock_exit.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_dispatch_job(client):
    """Tests the /dispatch-job endpoint."""
    with patch('world_model_service.files.app.dispatch_job_func', new_callable=AsyncMock) as mock_dispatch_job:
        mock_dispatch_job.return_value = {"status": "success"}
        response = client.post("/dispatch-job", json={
            "model_name": "test-model",
            "prompt": "test-prompt"
        })
        assert response.status_code == 200
        assert response.json() == {"status": "success"}
