import os
import tempfile
import pytest
from fastapi.testclient import TestClient

from pipecatapp.security import redact_sensitive_data, sanitize_data
from pipecatapp.pmm_memory import PMMMemory
from pipecatapp.web_server import app
from pipecatapp.api_keys import get_api_key


def test_pii_redaction_email_ssn_card():
    # Test Email Redaction
    text_email = "User email is alice@example.com."
    redacted = redact_sensitive_data(text_email)
    assert "alice@example.com" not in redacted
    assert "[EMAIL_REDACTED]" in redacted

    # Test SSN Redaction
    text_ssn = "SSN is 123-45-6789."
    redacted_ssn = redact_sensitive_data(text_ssn)
    assert "123-45-6789" not in redacted_ssn
    assert "[SSN_REDACTED]" in redacted_ssn

    # Test Credit Card Redaction
    text_card = "Card number 4532 0123 4567 8910 for payment."
    redacted_card = redact_sensitive_data(text_card)
    assert "4532 0123 4567 8910" not in redacted_card
    assert "[CARD_REDACTED]" in redacted_card


def test_pmm_memory_pii_redaction_and_provenance(tmp_path):
    db_file = str(tmp_path / "test_gdpr.db")
    memory = PMMMemory(db_path=db_file)

    # Add event containing PII and test provenance auto-attachment
    meta = {"user_id": "user_123", "agent_id": "agent_test"}
    provenance_override = {"source_model": "gpt-4o", "prompt_version": "2.1.0"}

    memory.add_event_sync(
        kind="user_message",
        content="Contact me at bob@test.com with ssn 987-65-4321.",
        meta=meta,
        provenance=provenance_override
    )

    events = memory.get_events_sync(kind="user_message", limit=1)
    assert len(events) == 1
    event = events[0]

    # Check PII was redacted from content
    assert "bob@test.com" not in event["content"]
    assert "[EMAIL_REDACTED]" in event["content"]
    assert "987-65-4321" not in event["content"]
    assert "[SSN_REDACTED]" in event["content"]

    # Check Provenance tracking attached in meta
    prov = event["meta"].get("provenance", {})
    assert prov.get("agent_id") == "agent_test"
    assert prov.get("prompt_version") == "2.1.0"
    assert prov.get("source_model") == "gpt-4o"
    assert "timestamp" in prov


def test_pmm_memory_right_to_erasure_purge(tmp_path):
    db_file = str(tmp_path / "test_purge.db")
    memory = PMMMemory(db_path=db_file)

    user_id = "user_to_delete_999"

    # Add events and work items
    memory.add_event_sync("user_message", "Hello World", {"user_id": user_id})
    memory.add_event_sync("user_message", "Keep me", {"user_id": "other_user"})

    work_item_id = memory.create_work_item_sync("Task 1", created_by=user_id)
    other_work_item = memory.create_work_item_sync("Task 2", created_by="other_user")

    # Purge user data
    deleted_count = memory.purge_user_data_sync(user_id)
    assert deleted_count >= 2

    # Verify user_id records deleted
    remaining_events = memory.get_events_sync(limit=10)
    for evt in remaining_events:
        assert evt.get("meta", {}).get("user_id") != user_id

    assert memory.get_work_item_sync(work_item_id) is None
    assert memory.get_work_item_sync(other_work_item) is not None


def test_gdpr_purge_endpoint_and_provenance_headers(tmp_path):
    app.dependency_overrides[get_api_key] = lambda: "test_key"
    try:
        client = TestClient(app)

        # Test Provenance Headers on GET /
        res = client.get("/")
        assert res.status_code == 200
        assert "X-Agent-ID" in res.headers
        assert "X-Prompt-Version" in res.headers
        assert "X-Source-Model" in res.headers
        assert "X-Timestamp" in res.headers

        # Setup memory in app state
        db_file = str(tmp_path / "test_app_purge.db")
        memory = PMMMemory(db_path=db_file)

        class DummyTwin:
            def __init__(self, mem):
                self.long_term_memory = mem

        app.state.twin_service_instance = DummyTwin(memory)

        target_user = "gdpr_user_777"
        memory.add_event_sync("user_message", "Secret text", {"user_id": target_user})

        # Call Purge REST Endpoint
        resp = client.delete(f"/api/memory/gdpr/purge?identifier={target_user}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert data["identifier"] == target_user
        assert data["records_purged"] >= 1
    finally:
        app.dependency_overrides.clear()
