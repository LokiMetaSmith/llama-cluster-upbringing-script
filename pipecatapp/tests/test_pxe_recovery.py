"""
Unit tests for Autonomous PXE Recovery & Swarm Node Lifecycle.
"""

import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from pipecatapp.pxe_recovery import (
    PXERecoveryManager,
    normalize_mac,
    DEFAULT_TARGET_VERSION,
)
from pipecatapp.web_server import app

client = TestClient(app)


def test_normalize_mac():
    assert normalize_mac("00:25:AB:7A:0D:7E") == "00:25:ab:7a:0d:7e"
    assert normalize_mac("00-25-ab-7a-0d-7e") == "00:25:ab:7a:0d:7e"
    assert normalize_mac("0025ab7a0d7e") == "00:25:ab:7a:0d:7e"
    assert normalize_mac("") == ""
    assert normalize_mac(None) == ""


def test_pxe_recovery_manager_lifecycle():
    with tempfile.TemporaryDirectory() as tmpdir:
        state_path = os.path.join(tmpdir, "test_nodes.json")
        mgr = PXERecoveryManager(state_file=state_path)

        mac = "00:25:ab:7a:0d:7e"

        # Initially unknown -> Boot decision serves RAMOS maintenance boot
        decision = mgr.get_boot_decision(mac, server_ip="192.168.1.148")
        assert "#!ipxe" in decision
        assert "http://192.168.1.148/live/vmlinuz" in decision

        # Mark node as healthy -> Boot decision serves local chainload
        mgr.update_node_status(mac, status="HEALTHY")
        decision = mgr.get_boot_decision(mac, server_ip="192.168.1.148")
        assert "#!ipxe" in decision
        assert "exit 1" in decision

        # Quarantine node -> Boot decision serves halt
        mgr.quarantine_node(mac, reason="SMART test failed")
        decision = mgr.get_boot_decision(mac, server_ip="192.168.1.148")
        assert "QUARANTINED" in decision
        assert "SMART test failed" in decision
        assert "shell" in decision


def test_anti_flapping_quarantine():
    with tempfile.TemporaryDirectory() as tmpdir:
        state_path = os.path.join(tmpdir, "flapping_nodes.json")
        mgr = PXERecoveryManager(state_file=state_path)
        mac = "00:aa:bb:cc:dd:ee"

        # First and second reimage -> Healthy
        mgr.update_node_status(mac, status="REIMAGED")
        assert mgr.get_node(mac)["status"] == "HEALTHY"

        mgr.update_node_status(mac, status="REIMAGED")
        assert mgr.get_node(mac)["status"] == "HEALTHY"

        # Third reimage within short window -> Auto-quarantined
        mgr.update_node_status(mac, status="REIMAGED")
        node = mgr.get_node(mac)
        assert node["status"] == "QUARANTINED"
        assert "Excessive flapping" in node["quarantine_reason"]


def test_api_boot_decision_endpoint():
    mac = "00:11:22:33:44:55"
    resp = client.get(f"/api/pxe/boot-decision?mac={mac}")
    assert resp.status_code == 200
    assert "text/plain" in resp.headers["content-type"]
    assert "#!ipxe" in resp.text


def test_api_cluster_version_endpoints():
    # GET version
    resp = client.get("/api/cluster/target-version")
    assert resp.status_code == 200
    assert len(resp.text.strip()) > 0

    # POST version update
    new_version = "2026.10.06-vtest"
    resp = client.post("/api/cluster/target-version", json={"version": new_version})
    assert resp.status_code == 200
    assert resp.json()["target_version"] == new_version

    # Verify updated
    resp = client.get("/api/cluster/target-version")
    assert resp.text.strip() == new_version


def test_api_evict_and_quarantine_endpoints():
    mac = "aa:bb:cc:dd:ee:ff"

    # Evict
    resp = client.post("/api/cluster/evict", json={"mac": mac, "reason": "Test eviction"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "evicted"

    # Quarantine
    resp = client.post(
        "/api/cluster/quarantine",
        json={"mac": mac, "reason": "Drive SMART read failure", "details": {"reallocated": 50}},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "QUARANTINED"

    # Verify in nodes list
    resp = client.get("/api/cluster/nodes")
    assert resp.status_code == 200
    nodes = resp.json()["nodes"]
    matched = [n for n in nodes if n["mac"] == mac]
    assert len(matched) == 1
    assert matched[0]["status"] == "QUARANTINED"
