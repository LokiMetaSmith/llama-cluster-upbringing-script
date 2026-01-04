import secrets
import hashlib
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

# This is where we will store the hashed API keys.
# In a real-world application, this would be a database or a secure secret manager.
API_KEYS = set()

# Define the API key header
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def generate_api_key(length: int = 32) -> str:
    """Generates a cryptographically secure random API key.

    Args:
        length (int): The length of the API key to generate.

    Returns:
        str: The generated API key.
    """
    return secrets.token_urlsafe(length)

def get_api_key_hash(api_key: str) -> str:
    """Hashes an API key using SHA-256.

    Args:
        api_key (str): The API key to hash.

    Returns:
        str: The SHA-256 hash of the API key.
    """
    return hashlib.sha256(api_key.encode()).hexdigest()

def initialize_api_keys(hashed_keys: list[str]):
    """Initializes the set of valid API keys from a list of hashes.

    This function is called at startup to load the API keys from the
    environment configuration into memory.

    Args:
        hashed_keys (list[str]): A list of pre-hashed API keys.
    """
    global API_KEYS
    API_KEYS = set(hashed_keys)
    if API_KEYS:
        print(f"Loaded {len(API_KEYS)} API key(s).")

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """A FastAPI dependency to authenticate requests using an API key.

    This function checks for the presence of an "Authorization" header and
    validates the provided API key against the list of known keys.

    Args:
        api_key_header (str): The value of the "Authorization" header.

    Raises:
        HTTPException: If the API key is missing or invalid.

    Returns:
        str: The valid API key if authentication is successful.
    """
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )

    # The key is expected to be prefixed with "Bearer "
    parts = api_key_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <key>'",
        )

    provided_key = parts[1]
    hashed_provided_key = get_api_key_hash(provided_key)

    if hashed_provided_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return provided_key