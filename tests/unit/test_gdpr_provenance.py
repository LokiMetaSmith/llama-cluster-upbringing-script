import os
import tempfile
import pytest
from fastapi.testclient import TestClient

from pipecatapp.security import redact_sensitive_data, sanitize_data
from pipecatapp.pmm_memory import PMMMemory
from pipecatapp.web_server import app
from pipecatapp.api_keys import get_api_key
from pipecatapp.atproto_crypto import verify_payload


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


def test_pmm_memory_pii_redaction_and_signed_provenance(tmp_path):
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

    # Check Provenance tracking attached and signed
    prov = event["meta"].get("provenance", {})
    assert prov.get("agent_id") == "agent_test"
    assert prov.get("prompt_version") == "2.1.0"
    assert prov.get("source_model") == "gpt-4o"
    assert "timestamp" in prov
    assert "signature" in prov
    assert "public_key" in prov

    # Verify cryptographic signature
    signable_payload = {k: v for k, v in prov.items() if k not in ("signature", "public_key")}
    is_valid = verify_payload(signable_payload, prov["signature"], prov["public_key"])
    assert is_valid is True


def test_pmm_memory_gdpr_export_and_purge_audit(tmp_path):
    db_file = str(tmp_path / "test_gdpr_export.db")
    memory = PMMMemory(db_path=db_file)

    user_id = "user_export_123"

    # Add events and work items
    memory.add_event_sync("user_message", "Hello Export", {"user_id": user_id})
    memory.create_work_item_sync("Task 101", created_by=user_id)

    # Export user data
    exported = memory.export_user_data_sync(user_id)
    assert exported["identifier"] == user_id
    assert len(exported["events"]) >= 1
    assert len(exported["work_items"]) >= 1

    # Purge user data
    res = memory.purge_user_data_sync(user_id)
    assert res["records_deleted"] >= 2

    # Check audit logs recorded
    erasure_audits = memory.get_events_sync(kind="gdpr_erasure_audit", limit=10)
    export_audits = memory.get_events_sync(kind="gdpr_export_audit", limit=10)

    assert len(erasure_audits) >= 1
    assert len(export_audits) >= 1


def test_multi_party_consensus_discussion_retention(tmp_path):
    db_file = str(tmp_path / "test_multi_party.db")
    memory = PMMMemory(db_path=db_file)

    user_a = "alice"
    user_b = "bob"

    # Add multi-party discussion event
    memory.add_event_sync("discussion", "Alice and Bob's collaborative proposal", {
        "participant_ids": [user_a, user_b],
        "user_id": user_a
    })

    # Add single-party blog entry
    memory.add_event_sync("personal_blog", "Alice's private blog post", {
        "user_id": user_a
    })

    # User Alice requests removal
    res = memory.purge_user_data_sync(user_a)

    # Single-party blog post should be deleted, multi-party discussion should be anonymized
    assert res["records_anonymized"] == 1
    assert res["records_deleted"] == 1

    events = memory.get_events_sync(limit=10)
    discussion_events = [e for e in events if e["kind"] == "discussion"]
    blog_events = [e for e in events if e["kind"] == "personal_blog"]

    assert len(blog_events) == 0 # Fully deleted
    assert len(discussion_events) == 1 # Retained & Anonymized
    assert discussion_events[0]["content"] == "[REDACTED_BY_USER_REQUEST]"

    # Now Bob requests removal as well (Consensus reached!)
    res_b = memory.purge_user_data_sync(user_b)
    assert res_b["records_deleted"] == 1

    events_after = memory.get_events_sync(limit=10)
    discussion_after = [e for e in events_after if e["kind"] == "discussion"]
    assert len(discussion_after) == 0 # Fully deleted now that all parties consented!


def test_gdpr_api_endpoints_and_signed_headers(tmp_path):
    app.dependency_overrides[get_api_key] = lambda: "test_key"
    try:
        client = TestClient(app)

        # Test Provenance Headers and Signature on GET /
        res = client.get("/")
        assert res.status_code == 200
        assert "X-Agent-ID" in res.headers
        assert "X-Prompt-Version" in res.headers
        assert "X-Source-Model" in res.headers
        assert "X-Timestamp" in res.headers
        assert "X-Provenance-Signature" in res.headers
        assert "X-Agent-Public-Key" in res.headers

        # Verify response header signature
        payload_to_verify = {
            "agent_id": res.headers["X-Agent-ID"],
            "prompt_version": res.headers["X-Prompt-Version"],
            "source_model": res.headers["X-Source-Model"],
            "timestamp": float(res.headers["X-Timestamp"])
        }
        assert verify_payload(payload_to_verify, res.headers["X-Provenance-Signature"], res.headers["X-Agent-Public-Key"]) is True

        # Setup memory in app state
        db_file = str(tmp_path / "test_app_gdpr.db")
        memory = PMMMemory(db_path=db_file)

        class DummyTwin:
            def __init__(self, mem):
                self.long_term_memory = mem

        app.state.twin_service_instance = DummyTwin(memory)

        target_user = "gdpr_user_888"
        memory.add_event_sync("user_message", "Export & Purge text", {"user_id": target_user})

        # Test Export Endpoint
        exp_resp = client.get(f"/api/memory/gdpr/export?identifier={target_user}")
        assert exp_resp.status_code == 200
        exp_data = exp_resp.json()
        assert exp_data["identifier"] == target_user
        assert len(exp_data["events"]) >= 1

        # Test Purge Endpoint
        purge_resp = client.delete(f"/api/memory/gdpr/purge?identifier={target_user}")
        assert purge_resp.status_code == 200
        purge_data = purge_resp.json()
        assert purge_data["records_deleted"] >= 1

        # Test Audit Logs Endpoint
        audit_resp = client.get("/api/memory/gdpr/audit_logs")
        assert audit_resp.status_code == 200
        audit_logs = audit_resp.json()
        assert len(audit_logs) >= 2

    finally:
        app.dependency_overrides.clear()
