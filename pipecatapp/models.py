from pydantic import BaseModel, HttpUrl, Field, ConfigDict, model_validator
from typing import Optional, Dict, Any, Literal

class InternalChatRequest(BaseModel):
    """
    Schema for internal chat requests.
    Enforces presence of critical fields and limits input size.
    """
    text: Optional[str] = Field(None, min_length=0, max_length=10000, description="The chat message content.")
    request_id: str = Field(..., min_length=1, description="Unique identifier for the request.")
    response_url: HttpUrl = Field(..., description="The URL where the response should be sent.")

    # New fields for audio support
    audio_url: Optional[HttpUrl] = Field(None, description="URL to an audio file for the user's message.")
    audio_base64: Optional[str] = Field(None, description="Base64 encoded audio content.")

    # Allow passing through other metadata
    extra_fields: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra='allow')

    @model_validator(mode='after')
    def check_content_present(self) -> 'InternalChatRequest':
        if not self.text and not self.audio_url and not self.audio_base64:
            raise ValueError('At least one of text, audio_url, or audio_base64 must be provided.')
        return self

class SystemMessageRequest(BaseModel):
    """
    Schema for system alerts.
    Enforces text limit to prevent log flooding or memory issues.
    """
    text: str = Field(..., min_length=1, max_length=2000, description="The system alert message.")
    priority: Literal["low", "medium", "high", "critical"] = Field("medium", description="Priority level of the alert.")

    model_config = ConfigDict(extra='allow')
