import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import HTTPException
from pipecatapp.api_keys import (
    get_optional_api_key,
    get_api_key,
    initialize_api_keys,
    get_api_key_hash,
)
import pipecatapp.api_keys as api_keys_module
from pipecatapp.web_server import app


@pytest.mark.asyncio
async def test_get_optional_api_key_when_empty_keys():
    # Ensure API_KEYS is empty
    orig_keys = api_keys_module.API_KEYS
    try:
        api_keys_module.API_KEYS = set()

        # None header
        res = await get_optional_api_key(None)
        assert res is None

        # Empty string
        res = await get_optional_api_key("")
        assert res is None

        # "Bearer " with trailing space / no key
        res = await get_optional_api_key("Bearer ")
        assert res is None

        # Any token when API_KEYS is empty
        res = await get_optional_api_key("Bearer some_dummy_key")
        assert res is None
    finally:
        api_keys_module.API_KEYS = orig_keys


@pytest.mark.asyncio
async def test_get_optional_api_key_with_configured_keys():
    orig_keys = api_keys_module.API_KEYS
    try:
        valid_key = "secret_key_123"
        hashed = get_api_key_hash(valid_key)
        initialize_api_keys([hashed])

        # None header still returns None
        assert await get_optional_api_key(None) is None

        # "Bearer " empty returns None
        assert await get_optional_api_key("Bearer ") is None

        # Valid key returns key
        assert await get_optional_api_key(f"Bearer {valid_key}") == valid_key

        # Invalid key raises 401
        with pytest.raises(HTTPException) as exc_info:
            await get_optional_api_key("Bearer wrong_key")
        assert exc_info.value.status_code == 401
    finally:
        api_keys_module.API_KEYS = orig_keys


@pytest.mark.asyncio
async def test_web_uis_endpoint_accessible_unauthenticated():
    # Test that /api/web_uis can be accessed without Authorization header
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/web_uis")
        # Should not be 401
        assert response.status_code != 401
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
