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
