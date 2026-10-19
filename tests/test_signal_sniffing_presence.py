import pytest
import time
from fastapi.testclient import TestClient
from services.tap_orchestrator.main import app, datalog
from services.tap_orchestrator.rf_sniffer import RFSnifferEngine
from services.tap_orchestrator.models import RFTelemetryFrame, RFSignalSample
from pipecatapp.datalog_memory import DatalogMemory

client = TestClient(app)

@pytest.fixture
def mock_datalog(tmp_path):
    db = str(tmp_path / "test_rf_datalog.db")
    return DatalogMemory(db_path=db)

def test_rf_sniffer_engine_anonymization():
    engine = RFSnifferEngine()
    mac = "AA:BB:CC:DD:EE:FF"
    hashed = engine.anonymize_device_id(mac)
    assert len(hashed) == 16
    assert hashed == engine.anonymize_device_id("aabbccddeeff")
    assert hashed != mac

def test_rf_sniffer_engine_rssi_confidence():
    engine = RFSnifferEngine(min_rssi_threshold=-90, max_rssi_ceiling=-30)
    assert engine.calculate_rssi_confidence(-100) == 0.0
    assert engine.calculate_rssi_confidence(-90) == 0.0
    assert engine.calculate_rssi_confidence(-30) == 1.0
    assert engine.calculate_rssi_confidence(-20) == 1.0
    assert engine.calculate_rssi_confidence(-60) == 0.5

def test_rf_sniffer_engine_processing(mock_datalog):
    engine = RFSnifferEngine(datalog=mock_datalog)
    frame = RFTelemetryFrame(
        sensor_id="test_sensor_01",
        room_id="room_101",
        timestamp=time.time(),
        samples=[
            RFSignalSample(device_id="11:22:33:44:55:66", rssi=-60, frame_type="probe_request"),
            RFSignalSample(device_id="77:88:99:AA:BB:CC", rssi=-95, frame_type="beacon"), # Below threshold
        ]
    )

    response = engine.process_telemetry_frame(frame)
    assert response.status == "success"
    assert response.processed_samples == 1
    assert response.active_devices_detected == 1
    assert response.allocated_weight > 0.0

    # Query datalog state for asserted facts
    facts = mock_datalog.query_state(predicate="rf_presence")
    assert len(facts) == 1
    assert facts[0]["args"][1] == "room_101"

def test_post_rf_telemetry_api():
    payload = {
        "sensor_id": "esp32-sniffer-node-01",
        "room_id": "room_202",
        "timestamp": time.time(),
        "samples": [
            {
                "device_id": "00:11:22:33:44:55",
                "rssi": -55,
                "channel": 6,
                "frame_type": "probe_request",
                "snr": 20.0
            }
        ]
    }

    response = client.post("/api/v1/telemetry/rf", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["processed_samples"] == 1
    assert data["active_devices_detected"] == 1
    assert data["allocated_weight"] is not None
