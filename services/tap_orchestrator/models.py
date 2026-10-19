from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DesfireEvent(BaseModel):
    event: str
    user_id: str
    reader_id: str
    timestamp: int
    auth_type: str

class TapResponse(BaseModel):
    status: str
    message: str

class AuthentikUser(BaseModel):
    username: str
    name: Optional[str] = None
    is_active: bool
    groups: List[str] = []
    attributes: Dict[str, Any] = {}

class ChallengeResponse(BaseModel):
    nonce: str
    room_id: str
    expires_in: int

class VerifyRequest(BaseModel):
    did: str
    challenge_nonce: str
    signature: str
    room_id: str
    public_key_hex: str
    metadata: Optional[Dict[str, Any]] = None

class VerifyResponse(BaseModel):
    status: str
    message: str
    weight: Optional[float] = None

class RFSignalSample(BaseModel):
    device_id: str  # MAC address or hashed MAC identifier
    rssi: int  # Signal strength in dBm (e.g., -65)
    channel: Optional[int] = None
    frame_type: Optional[str] = "probe_request"  # probe_request, beacon, csi, iq_energy
    snr: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class RFTelemetryFrame(BaseModel):
    sensor_id: str  # ID of the ESP32 or Wi-Fi SDR sniffing node
    room_id: str
    timestamp: Optional[float] = None
    samples: List[RFSignalSample]

class RFPresenceResponse(BaseModel):
    status: str
    processed_samples: int
    active_devices_detected: int
    allocated_weight: Optional[float] = None
