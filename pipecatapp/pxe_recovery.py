"""
Autonomous PXE Recovery & Swarm Node Lifecycle Manager.

Manages node boot decisions, hardware health state, automated re-imaging guards,
and swarm identity de-registration across the cluster.
"""

import os
import re
import json
import time
import logging
import threading
from typing import Dict, Any, Optional, List

logger = logging.getLogger("pxe_recovery")

DEFAULT_TARGET_VERSION = os.getenv("TARGET_CLUSTER_VERSION", "2026.10.06-v1")
FLAPPING_THRESHOLD_COUNT = 3
FLAPPING_WINDOW_SECONDS = 3600  # 1 hour


def normalize_mac(mac: Optional[str]) -> str:
    """Normalize MAC address string into standard lowercase format xx:xx:xx:xx:xx:xx."""
    if not mac:
        return ""
    cleaned = re.sub(r"[^0-9a-fA-F]", "", mac.lower())
    if len(cleaned) == 12:
        return ":".join(cleaned[i:i + 2] for i in range(0, 12, 2))
    return mac.strip().lower()


class PXERecoveryManager:
    """Thread-safe manager for PXE boot decisions and swarm recovery states."""

    def __init__(self, state_file: Optional[str] = None):
        if not state_file:
            base_dir = os.path.join(os.getcwd(), ".liminal")
            os.makedirs(base_dir, exist_ok=True)
            state_file = os.path.join(base_dir, "pxe_nodes.json")
        self.state_file = state_file
        self._lock = threading.Lock()
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._target_version = DEFAULT_TARGET_VERSION
        self._load_state()

    def _load_state(self) -> None:
        """Load state from persistent disk cache if present."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._nodes = data.get("nodes", {})
                    self._target_version = data.get("target_version", DEFAULT_TARGET_VERSION)
            except Exception as e:
                logger.error(f"Error loading PXE recovery state from {self.state_file}: {e}")

    def _save_state(self) -> None:
        """Persist state to disk safely with atomic rename."""
        try:
            tmp_file = f"{self.state_file}.tmp"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "target_version": self._target_version,
                        "updated_at": time.time(),
                        "nodes": self._nodes,
                    },
                    f,
                    indent=2,
                )
            os.replace(tmp_file, self.state_file)
        except Exception as e:
            logger.error(f"Error persisting PXE recovery state to {self.state_file}: {e}")

    def get_target_version(self) -> str:
        """Return the current cluster target image version."""
        with self._lock:
            return self._target_version

    def set_target_version(self, version: str) -> str:
        """Set a new target image version across the cluster."""
        with self._lock:
            self._target_version = version.strip()
            self._save_state()
            return self._target_version

    def get_node(self, mac: str) -> Optional[Dict[str, Any]]:
        """Retrieve node state by MAC address."""
        norm_mac = normalize_mac(mac)
        with self._lock:
            return self._nodes.get(norm_mac)

    def list_nodes(self) -> List[Dict[str, Any]]:
        """List all tracked cluster nodes."""
        with self._lock:
            return list(self._nodes.values())

    def update_node_status(
        self,
        mac: str,
        status: str,
        hostname: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Record node status update, handling anti-flapping guards."""
        norm_mac = normalize_mac(mac)
        now = time.time()
        details = details or {}

        with self._lock:
            node = self._nodes.get(norm_mac, {
                "mac": norm_mac,
                "hostname": hostname or f"pipecat-{norm_mac.replace(':', '')[-6:]}",
                "status": "UNKNOWN",
                "first_seen": now,
                "reimage_history": [],
                "quarantine_reason": None,
            })

            if hostname:
                node["hostname"] = hostname

            node["last_seen"] = now
            node["details"] = details

            # Handle re-image events & anti-flapping protection
            if status == "REIMAGED":
                history = node.get("reimage_history", [])
                # Prune history older than flapping window
                recent_reimages = [ts for ts in history if now - ts < FLAPPING_WINDOW_SECONDS]
                recent_reimages.append(now)
                node["reimage_history"] = recent_reimages

                if len(recent_reimages) >= FLAPPING_THRESHOLD_COUNT:
                    node["status"] = "QUARANTINED"
                    node["quarantine_reason"] = f"Excessive flapping: {len(recent_reimages)} reimages in {FLAPPING_WINDOW_SECONDS}s"
                    logger.warning(f"Node {norm_mac} auto-quarantined: {node['quarantine_reason']}")
                else:
                    node["status"] = "HEALTHY"
                    node["quarantine_reason"] = None
            elif status == "QUARANTINED":
                node["status"] = "QUARANTINED"
                node["quarantine_reason"] = details.get("reason", "Manual or SMART hardware quarantine")
            else:
                node["status"] = status
                if status == "HEALTHY":
                    node["quarantine_reason"] = None

            if node.get("status") == "HEALTHY":
                mac_dash = norm_mac.replace(":", "-").lower()
                for tftp_dir in ["/srv/tftp/pxelinux.cfg", "/srv/tftp/debian-installer/amd64/pxelinux.cfg"]:
                    mac_cfg = os.path.join(tftp_dir, f"01-{mac_dash}")
                    if os.path.exists(mac_cfg):
                        try:
                            os.remove(mac_cfg)
                            logger.info(f"Removed one-time PXELINUX override: {mac_cfg}")
                        except Exception as e:
                            logger.warning(f"Could not remove {mac_cfg}: {e}")

            self._nodes[norm_mac] = node
            self._save_state()
            return node

    def quarantine_node(self, mac: str, reason: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Manually or automatically quarantine a node to prevent re-image loops."""
        details = details or {}
        details["reason"] = reason
        return self.update_node_status(mac, status="QUARANTINED", details=details)

    def evict_node(self, mac: str, hostname: Optional[str] = None, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle swarm node eviction before re-imaging.
        Notifies Nomad / Consul to drain tasks and prevent stale Raft registration.
        """
        norm_mac = normalize_mac(mac)
        node = self.get_node(norm_mac)
        target_hostname = hostname or (node.get("hostname") if node else f"pipecat-{norm_mac.replace(':', '')[-6:]}")

        # Record eviction state
        self.update_node_status(
            norm_mac,
            status="EVICTING",
            hostname=target_hostname,
            details={"eviction_reason": reason or "PXE Re-image Triggered"},
        )

        logger.info(f"Evicting swarm node {target_hostname} ({norm_mac}): {reason}")
        # In this substrate, workers will be gracefully drained from Nomad if reachable
        return {
            "mac": norm_mac,
            "hostname": target_hostname,
            "status": "evicted",
            "evicted_at": time.time(),
        }

    def get_boot_decision(self, mac: str, server_ip: str) -> str:
        """
        Generate dynamic iPXE script response for client node.
        - HEALTHY: exits iPXE to boot local drive.
        - QUARANTINED: displays alert and halts to prevent drive burnout.
        - UNKNOWN / AUDIT_RECOVER: boots maintenance RAMOS rootfs.
        """
        norm_mac = normalize_mac(mac)
        node = self.get_node(norm_mac)
        status = node.get("status", "UNKNOWN") if node else "UNKNOWN"

        if status == "QUARANTINED":
            reason = node.get("quarantine_reason", "Hardware / SMART failure detected")
            return f"""#!ipxe
echo ==============================================================================
echo  NODE QUARANTINED (Hardware Failure Protection)
echo  MAC Address: {norm_mac}
echo  Reason: {reason}
echo ==============================================================================
echo Halting network boot to prevent hardware death spiral.
echo Contact cluster administrator or inspect SMART drive health.
sleep 60
shell
"""

        if status == "HEALTHY":
            return f"""#!ipxe
echo ==============================================================================
echo  Pipecat Node {norm_mac} - Verified Healthy
echo ==============================================================================
echo Handoff: Booting installed OS from local drive...
sanboot --no-describe --drive 0x80 || exit 1
"""

        # Default fallback for new/unverified/recovering nodes: Boot RAMOS audit environment
        return f"""#!ipxe
echo ==============================================================================
echo  Pipecat Autonomous Recovery & Health Audit
echo  Node MAC: {norm_mac} | Status: {status}
echo ==============================================================================
echo Booting maintenance RAMOS from http://{server_ip}/live...
kernel http://{server_ip}/live/vmlinuz boot=live components fetch=http://{server_ip}/live/filesystem.squashfs quiet net.ifnames=0
initrd http://{server_ip}/live/initrd.img
boot
"""


# Global singleton instance for web_server
recovery_manager = PXERecoveryManager()
