import pytest
from fastapi import HTTPException, status
from pipecatapp.api_keys import get_api_key, initialize_api_keys, get_api_key_hash

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
