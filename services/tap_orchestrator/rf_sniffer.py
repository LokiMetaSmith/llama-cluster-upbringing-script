import hashlib
import time
import logging
from typing import Optional, Dict, Any, List
from services.tap_orchestrator.models import RFTelemetryFrame, RFPresenceResponse, RFSignalSample
from pipecatapp.datalog_memory import DatalogMemory
from pipecatapp.memory_backends_impl.consul_kv_backend import ConsulKVBackend

logger = logging.getLogger("rf_sniffer")

class RFSnifferEngine:
    """Processes RF/Wi-Fi/SDR signal telemetry for presence detection and REA compute weight allocation."""

    def __init__(
        self,
        datalog: Optional[DatalogMemory] = None,
        consul_backend: Optional[ConsulKVBackend] = None,
        min_rssi_threshold: int = -90,
        max_rssi_ceiling: int = -30
    ):
        self.datalog = datalog or DatalogMemory()
        self.consul_backend = consul_backend or ConsulKVBackend(prefix="swarm/")
        self.min_rssi_threshold = min_rssi_threshold
        self.max_rssi_ceiling = max_rssi_ceiling

    def anonymize_device_id(self, device_id: str) -> str:
        """Hash device identifiers (like MAC addresses) for privacy preserving presence tracking."""
        cleaned = device_id.replace(":", "").replace("-", "").strip().lower()
        if len(cleaned) == 64:
            # Already SHA256 hashed
            return cleaned
        return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()[:16]

    def calculate_rssi_confidence(self, rssi: int) -> float:
        """Convert RSSI (dBm) to a normalized presence confidence float between 0.0 and 1.0."""
        if rssi <= self.min_rssi_threshold:
            return 0.0
        if rssi >= self.max_rssi_ceiling:
            return 1.0
        range_span = self.max_rssi_ceiling - self.min_rssi_threshold
        return round((rssi - self.min_rssi_threshold) / range_span, 4)

    def process_telemetry_frame(self, frame: RFTelemetryFrame) -> RFPresenceResponse:
        """Processes a telemetry frame, updates REA datalog ledger, and syncs room presence to Consul."""
        now = frame.timestamp or time.time()
        processed_count = 0
        active_devices = 0
        total_confidence = 0.0

        for sample in frame.samples:
            if sample.rssi < self.min_rssi_threshold:
                logger.debug(f"Ignoring sample from {sample.device_id}: RSSI {sample.rssi} below threshold {self.min_rssi_threshold}")
                continue

            processed_count += 1
            device_hash = self.anonymize_device_id(sample.device_id)
            confidence = self.calculate_rssi_confidence(sample.rssi)
            total_confidence += confidence
            active_devices += 1

            # 1. Assert fact into Datalog REA ledger
            try:
                self.datalog.assert_fact(
                    "rf_presence",
                    device_hash,
                    frame.room_id,
                    now,
                    sample.rssi,
                    confidence,
                    meta={
                        "sensor_id": frame.sensor_id,
                        "frame_type": sample.frame_type,
                        "channel": sample.channel,
                        "snr": sample.snr
                    }
                )
            except Exception as e:
                logger.error(f"Failed to assert rf_presence fact for {device_hash}: {e}")

            # 2. Sync individual device state to Consul KV
            try:
                self.consul_backend.put_kv(
                    f"rf_presence/{frame.room_id}/{device_hash}",
                    {
                        "sensor_id": frame.sensor_id,
                        "rssi": sample.rssi,
                        "confidence": confidence,
                        "frame_type": sample.frame_type,
                        "last_seen": now
                    }
                )
            except Exception as e:
                logger.error(f"Failed to write rf_presence KV to Consul: {e}")

        # Calculate composite room compute weight
        composite_weight = round(min(100.0, total_confidence * 25.0), 2)

        # Sync aggregated room presence weight to Consul KV
        try:
            self.consul_backend.put_kv(
                f"compute_rights/rf_{frame.room_id}",
                {
                    "weight": composite_weight,
                    "room_id": frame.room_id,
                    "active_devices": active_devices,
                    "sensor_id": frame.sensor_id,
                    "last_updated": now
                }
            )
        except Exception as e:
            logger.error(f"Failed to write room compute rights to Consul: {e}")

        return RFPresenceResponse(
            status="success",
            processed_samples=processed_count,
            active_devices_detected=active_devices,
            allocated_weight=composite_weight
        )
