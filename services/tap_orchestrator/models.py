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
