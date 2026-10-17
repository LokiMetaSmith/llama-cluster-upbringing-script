import pytest
import time
from fastapi.testclient import TestClient
from services.tap_orchestrator.main import app, challenge_store
from pipecatapp.atproto_crypto import generate_key_pair, sign_payload

client = TestClient(app)

@pytest.fixture
def keys():
    return generate_key_pair()

@pytest.fixture
def auth_headers():
    return {"X-Tap-Secret": "secret"}

def test_get_challenge():
    response = client.get("/api/v1/challenge?room_id=room_123")
    assert response.status_code == 200
    data = response.json()
    assert "nonce" in data
    assert data["room_id"] == "room_123"
    assert data["expires_in"] == 10

    # Check if stored
    assert data["nonce"] in challenge_store
    assert challenge_store[data["nonce"]]["room_id"] == "room_123"

def test_verify_presence_success(keys):
    priv, pub = keys

    # 1. Get challenge
    response = client.get("/api/v1/challenge?room_id=test_room")
    challenge_data = response.json()
    nonce = challenge_data["nonce"]

    # 2. Sign payload
    payload_to_verify = {
        "challenge_nonce": nonce,
        "room_id": "test_room"
    }
    signature = sign_payload(payload_to_verify, priv)

    # 3. Verify
    verify_payload = {
        "did": "did:example:123",
        "challenge_nonce": nonce,
        "signature": signature,
        "room_id": "test_room",
        "public_key_hex": pub
    }

    response = client.post("/api/v1/verify", json=verify_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "weight" in data

def test_verify_presence_invalid_signature(keys):
    priv, pub = keys
    # Use wrong public key to sign
    wrong_priv, wrong_pub = generate_key_pair()

    response = client.get("/api/v1/challenge?room_id=test_room")
    challenge_data = response.json()
    nonce = challenge_data["nonce"]

    payload_to_verify = {
        "challenge_nonce": nonce,
        "room_id": "test_room"
    }
    signature = sign_payload(payload_to_verify, wrong_priv)

    verify_payload = {
        "did": "did:example:123",
        "challenge_nonce": nonce,
        "signature": signature,
        "room_id": "test_room",
        "public_key_hex": pub # Presenting original pub key, but signed with wrong_priv
    }

    response = client.post("/api/v1/verify", json=verify_payload)
    assert response.status_code == 401
    assert "Invalid signature" in response.json()["detail"]

def test_verify_presence_expired_nonce(keys):
    priv, pub = keys
    response = client.get("/api/v1/challenge?room_id=test_room")
    challenge_data = response.json()
    nonce = challenge_data["nonce"]

    # Manually expire it
    challenge_store[nonce]["expires_at"] = time.time() - 10

    payload_to_verify = {
        "challenge_nonce": nonce,
        "room_id": "test_room"
    }
    signature = sign_payload(payload_to_verify, priv)

    verify_payload = {
        "did": "did:example:123",
        "challenge_nonce": nonce,
        "signature": signature,
        "room_id": "test_room",
        "public_key_hex": pub
    }

    response = client.post("/api/v1/verify", json=verify_payload)
    assert response.status_code == 400
    assert "expired" in response.json()["detail"].lower()
