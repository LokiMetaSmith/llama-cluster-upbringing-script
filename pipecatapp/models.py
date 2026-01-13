from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional, Dict, Any, Literal

class InternalChatRequest(BaseModel):
    """
    Schema for internal chat requests.
    Enforces presence of critical fields and limits input size.
    """
    text: str = Field(..., min_length=1, max_length=10000, description="The chat message content.")
    request_id: str = Field(..., min_length=1, description="Unique identifier for the request.")
    response_url: HttpUrl = Field(..., description="The URL where the response should be sent.")
    # Allow passing through other metadata
    extra_fields: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra='allow')

class SystemMessageRequest(BaseModel):
    """
    Schema for system alerts.
    Enforces text limit to prevent log flooding or memory issues.
    """
    text: str = Field(..., min_length=1, max_length=2000, description="The system alert message.")
    priority: Literal["low", "medium", "high", "critical"] = Field("medium", description="Priority level of the alert.")

    model_config = ConfigDict(extra='allow')
