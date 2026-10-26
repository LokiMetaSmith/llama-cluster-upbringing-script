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
    assert "session_token" in data
    assert data["session"]["user_id"] == "did:example:123"
    assert data["session"]["is_active"] is True
    assert "terminal" in data["session"]["allowed_targets"]

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

def test_session_status_and_lifecycle():
    # 1. Create a session explicitly
    create_payload = {
        "user_id": "operator",
        "did": "did:example:operator",
        "auth_method": "fido2",
        "ttl_seconds": 1800,
        "roles": ["operator", "admin"],
        "allowed_targets": ["terminal", "grafana", "nomad"]
    }
    create_resp = client.post("/api/v1/session/create", json=create_payload, headers={"X-Tap-Secret": "secret"})
    assert create_resp.status_code == 200
    create_data = create_resp.json()
    assert create_data["valid"] is True
    session_token = create_data["session"]["session_token"]
    assert session_token.startswith("swarm_st_")

    # 2. Check session status by token
    status_resp = client.get(f"/api/v1/session/status?token={session_token}")
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert status_data["valid"] is True
    assert status_data["status"] == "active"
    assert status_data["session"]["user_id"] == "operator"

    # 3. Check session status by Bearer header
    header_resp = client.get("/api/v1/session/status", headers={"Authorization": f"Bearer {session_token}"})
    assert header_resp.status_code == 200
    assert header_resp.json()["valid"] is True

    # 4. Check session status by user_id
    user_resp = client.get("/api/v1/session/status?user_id=operator")
    assert user_resp.status_code == 200
    assert user_resp.json()["valid"] is True

    # 5. Revoke session
    revoke_resp = client.post("/api/v1/session/revoke", json={"session_token": session_token})
    assert revoke_resp.status_code == 200
    assert revoke_resp.json()["status"] == "revoked"

    # 6. Verify session is no longer valid
    post_revoke = client.get(f"/api/v1/session/status?token={session_token}")
    assert post_revoke.status_code == 200
    assert post_revoke.json()["valid"] is False

def test_cluster_presence_auth_hook(monkeypatch):
    from scripts import cluster_presence_auth
    now = time.time()
    mock_session = {
        "user_id": "operator",
        "is_active": True,
        "expires_at": now + 600,
        "allowed_targets": ["terminal", "grafana"],
        "public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleValidKey operator@swarm"
    }

    monkeypatch.setattr(cluster_presence_auth, "get_consul_kv", lambda key: mock_session if "operator" in key else None)
    monkeypatch.setattr("sys.argv", ["cluster_presence_auth", "operator"])

    output_lines = []
    monkeypatch.setattr("builtins.print", lambda *args: output_lines.append(" ".join(str(a) for a in args)))

    with pytest.raises(SystemExit) as exc:
        cluster_presence_auth.main()
    assert exc.value.code == 0
    assert any("AAAAC3NzaC1lZDI1NTE5AAAAIExampleValidKey" in line for line in output_lines)

def test_cluster_presence_auth_expired(monkeypatch):
    from scripts import cluster_presence_auth
    mock_session = {
        "user_id": "operator",
        "is_active": True,
        "expires_at": time.time() - 100,  # Expired
        "allowed_targets": ["terminal"]
    }
    monkeypatch.setattr(cluster_presence_auth, "get_consul_kv", lambda key: mock_session)
    monkeypatch.setattr("sys.argv", ["cluster_presence_auth", "operator"])

    with pytest.raises(SystemExit) as exc:
        cluster_presence_auth.main()
    assert exc.value.code == 1

def test_cluster_presence_auth_no_terminal_target(monkeypatch):
    from scripts import cluster_presence_auth
    mock_session = {
        "user_id": "operator",
        "is_active": True,
        "expires_at": time.time() + 600,
        "allowed_targets": ["grafana"]  # Missing 'terminal'
    }
    monkeypatch.setattr(cluster_presence_auth, "get_consul_kv", lambda key: mock_session)
    monkeypatch.setattr("sys.argv", ["cluster_presence_auth", "operator"])

    with pytest.raises(SystemExit) as exc:
        cluster_presence_auth.main()
    assert exc.value.code == 1

