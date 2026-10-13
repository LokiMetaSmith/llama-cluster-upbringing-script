"""Unit tests for the autonomous PXE recovery manager."""
import os
import tempfile
import pytest
from pipecatapp.pxe_recovery import PXERecoveryManager, normalize_mac


def test_normalize_mac():
    assert normalize_mac("00:25:AB:7A:0D:7E") == "00:25:ab:7a:0d:7e"
    assert normalize_mac("0025ab7a0d7e") == "00:25:ab:7a:0d:7e"
    assert normalize_mac("00-25-ab-7a-0d-7e") == "00:25:ab:7a:0d:7e"
    assert normalize_mac("") == ""


def test_recovery_lifecycle():
    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = os.path.join(tmpdir, "test_nodes.json")
        mgr = PXERecoveryManager(state_file=state_file)

        mac = "00:25:ab:7a:0d:7e"
        assert mgr.get_node(mac) is None

        # Unknown node gets RAMOS audit boot decision
        decision = mgr.get_boot_decision(mac, "192.168.1.148")
        assert "http://192.168.1.148/live" in decision

        # Node reports healthy
        mgr.update_node_status(mac, "HEALTHY")
        node = mgr.get_node(mac)
        assert node["status"] == "HEALTHY"

        decision = mgr.get_boot_decision(mac, "192.168.1.148")
        assert "sanboot" in decision

        # Flapping protection test: 3 consecutive re-images triggers quarantine
        mgr.update_node_status(mac, "REIMAGED")
        mgr.update_node_status(mac, "REIMAGED")
        mgr.update_node_status(mac, "REIMAGED")
        node = mgr.get_node(mac)
        assert node["status"] == "QUARANTINED"
        assert "Excessive flapping" in node["quarantine_reason"]

        decision = mgr.get_boot_decision(mac, "192.168.1.148")
        assert "NODE QUARANTINED" in decision
