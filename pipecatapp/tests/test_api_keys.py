import hashlib
import pytest
from fastapi import HTTPException, status

from pipecatapp.api_keys import get_api_key, initialize_api_keys, get_api_key_hash

def test_get_api_key_hash_known_value():
    """Test that hashing a known value produces the expected SHA-256 hash."""
    api_key = "my_super_secret_api_key"
    # Expected hash computed explicitly
    expected_hash = "ff423ebabb9aa1d9697a18088e5c00f790645c64c8269485cf3e8a248f7589f0"
    assert get_api_key_hash(api_key) == expected_hash

def test_get_api_key_hash_empty_string():
    """Test hashing an empty string."""
    api_key = ""
    # Expected hash computed explicitly for an empty string
    expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert get_api_key_hash(api_key) == expected_hash

def test_get_api_key_hash_unicode():
    """Test hashing a string with non-ASCII unicode characters."""
    api_key = "🚀🔑hello_worldñ"
    expected_hash = hashlib.sha256(api_key.encode()).hexdigest()
    assert get_api_key_hash(api_key) == expected_hash

def test_get_api_key_hash_deterministic():
    """Test that hashing the same string twice produces the same hash."""
    api_key = "deterministic_key"
    hash1 = get_api_key_hash(api_key)
    hash2 = get_api_key_hash(api_key)
    assert hash1 == hash2

@pytest.fixture(autouse=True)
def setup_api_keys():
    # Setup a valid known key
    valid_key = "test_valid_key_123"
    valid_hash = get_api_key_hash(valid_key)
    initialize_api_keys([valid_hash])

    yield valid_key

    # Teardown
    initialize_api_keys([])

@pytest.mark.asyncio
async def test_get_api_key_missing_header():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key_header=None)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Missing API Key"

@pytest.mark.asyncio
async def test_get_api_key_invalid_format_missing_bearer():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key_header="Token some_key")

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid authorization header format. Expected 'Bearer <key>'"

@pytest.mark.asyncio
async def test_get_api_key_invalid_format_too_many_parts():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key_header="Bearer some_key extra_part")

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid authorization header format. Expected 'Bearer <key>'"

@pytest.mark.asyncio
async def test_get_api_key_invalid_key():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key_header="Bearer invalid_key_456")

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid API Key"

@pytest.mark.asyncio
async def test_get_api_key_valid(setup_api_keys):
    valid_key = setup_api_keys
    result = await get_api_key(api_key_header=f"Bearer {valid_key}")
    assert result == valid_key
