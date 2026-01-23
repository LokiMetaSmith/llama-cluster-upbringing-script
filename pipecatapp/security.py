import re
import copy
from typing import Any, Dict, List

# Pre-compile regex for redaction to improve performance
# Matches "sk-" followed by 20+ alphanumeric/hyphen characters
# This targets OpenAI-style keys while avoiding common words like "task", "ask", "desk"
_API_KEY_PATTERN = re.compile(r'(sk-[a-zA-Z0-9-]{20,})')
# Matches "Bearer " followed by a token (alphanumeric and common token chars)
_BEARER_TOKEN_PATTERN = re.compile(r'(Bearer\s+)([a-zA-Z0-9\-\._~+/]+=*)')

def redact_sensitive_data(text: str) -> str:
    """
    Redacts sensitive information like API keys and Bearer tokens from a string.
    """
    if not text:
        return text

    # Redact generic API key patterns and Bearer tokens
    text = _API_KEY_PATTERN.sub(r'sk-[REDACTED]', text)
    text = _BEARER_TOKEN_PATTERN.sub(r'\1[REDACTED]', text)

    return text

def sanitize_data(data: Any) -> Any:
    """
    Recursively sanitizes a data structure (dict, list, etc.) by removing
    sensitive keys and redacting strings.

    Args:
        data: The data structure to sanitize.

    Returns:
        A new sanitized data structure (deep copy of the original where modified).
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Remove specific sensitive keys commonly found in global_inputs
            if key in ["external_experts_config", "tools_dict", "twin_service"]:
                continue

            new_dict[key] = sanitize_data(value)
        return new_dict

    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]

    elif isinstance(data, str):
        return redact_sensitive_data(data)

    else:
        # Return other types (int, float, None, bool) as is
        return data
