import re
import copy
from typing import Any, Dict, List

# Pre-compile regex for redaction to improve performance
# Matches "sk-" followed by 20+ alphanumeric/hyphen characters
# This targets OpenAI-style keys while avoiding common words like "task", "ask", "desk"
_OPENAI_KEY_PATTERN = re.compile(r'(sk-[a-zA-Z0-9-]{20,})')
# Matches "Bearer " followed by a token (alphanumeric and common token chars)
_BEARER_TOKEN_PATTERN = re.compile(r'(Bearer\s+)([a-zA-Z0-9\-\._~+/]+=*)')
# Matches Google API Keys (starts with AIza, 39 chars total)
_GOOGLE_KEY_PATTERN = re.compile(r'(AIza[0-9A-Za-z\-_]{35})')
# Matches AWS Access Key IDs (starts with AKIA, ASIA, ABIA, ACCA)
_AWS_KEY_PATTERN = re.compile(r'((?:AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16})')
# Matches Slack Tokens (starts with xoxb, xoxp, etc.)
_SLACK_KEY_PATTERN = re.compile(r'(xox[baprs]-[a-zA-Z0-9-]{10,})')
# Matches GitHub Tokens (starts with ghp, gho, etc.)
_GITHUB_KEY_PATTERN = re.compile(r'(gh[pousr]_[a-zA-Z0-9]{36,})')
# Matches GitLab Tokens (starts with glpat-, glptt-, etc.)
_GITLAB_KEY_PATTERN = re.compile(r'(glpat-[0-9a-zA-Z\-_]{20,})')

# Matches URL credentials (e.g. scheme://user:pass@host)
# Captures: 1=scheme separator "://", 2=user, 3=password
_URL_CREDENTIALS_PATTERN = re.compile(r'(://)([^:/]+):([^@]+)@')

def redact_sensitive_data(text: str) -> str:
    """
    Redacts sensitive information like API keys and Bearer tokens from a string.
    """
    if not text:
        return text

    # Fast path optimization: if potential triggers aren't present, skip regex
    # Bolt ⚡ Optimization: 'in' operator is much faster than regex
    # We check for the most common prefixes/indicators
    triggers = [
        "sk-", "Bearer", "AIza",
        "AKIA", "ASIA", "ABIA", "ACCA",
        "xox",
        "ghp_", "gho_", "ghu_", "ghs_", "ghr_", # GitHub prefixes
        "glpat", # GitLab
        "://"    # URL credentials
    ]
    if not any(trigger in text for trigger in triggers):
        return text

    # Redact generic API key patterns and Bearer tokens
    text = _OPENAI_KEY_PATTERN.sub(r'sk-[REDACTED]', text)
    text = _BEARER_TOKEN_PATTERN.sub(r'\1[REDACTED]', text)
    text = _GOOGLE_KEY_PATTERN.sub(r'AIza[REDACTED]', text)
    text = _AWS_KEY_PATTERN.sub(r'AWS-[REDACTED]', text)
    text = _SLACK_KEY_PATTERN.sub(r'xox-[REDACTED]', text)
    text = _GITHUB_KEY_PATTERN.sub(r'gh-[REDACTED]', text)
    text = _GITLAB_KEY_PATTERN.sub(r'glpat-[REDACTED]', text)

    # Redact credentials in URLs (e.g. for Bitbucket, generic git, etc.)
    # Replace with scheme://user:[REDACTED]@
    text = _URL_CREDENTIALS_PATTERN.sub(r'\1\2:[REDACTED]@', text)

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
