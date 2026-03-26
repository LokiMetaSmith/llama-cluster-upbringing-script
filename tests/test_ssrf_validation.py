import asyncio
import sys
import os
from unittest.mock import patch

# Add repo root to path so we can import pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipecatapp.net_utils import validate_url

import pytest

@pytest.mark.asyncio
async def test_validate_url_safe():
    # Public URLs should pass and return ORIGINAL URL
    try:
        url_https = "https://google.com"
        res_https = await validate_url(url_https)
        assert res_https == url_https, f"FAILED: HTTPS URL was rewritten: {res_https}"

        url_http = "http://example.com"
        res_http = await validate_url(url_http)
        assert res_http == url_http, f"FAILED: HTTP URL was rewritten: {res_http}"

    except ValueError as e:
        if "Could not resolve" in str(e):
            pytest.skip(f"Skipping DNS test due to network issues: {e}")
        else:
            pytest.fail(f"FAILED: Safe URL rejected: {e}")

@pytest.mark.asyncio
async def test_validate_url_unsafe_ip():
    # Localhost and private IPs should fail
    unsafe_ips = [
        "http://localhost",
        "http://127.0.0.1",
        "http://0.0.0.0",
        "http://192.168.1.1",
        "http://10.0.0.1",
        "http://172.16.0.1",
        "http://169.254.169.254", # Cloud metadata
        "http://[::1]"
    ]
    for url in unsafe_ips:
        with pytest.raises(ValueError) as excinfo:
            await validate_url(url)
        assert "Blocked" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_url_unsafe_scheme():
    unsafe_schemes = [
        "ftp://google.com",
        "file:///etc/passwd",
        "gopher://google.com"
    ]
    for url in unsafe_schemes:
        with pytest.raises(ValueError) as excinfo:
            await validate_url(url)
        assert "Scheme" in str(excinfo.value)

@pytest.mark.asyncio
async def test_allowlist():
    # Simulate environment variable
    with patch.dict(os.environ, {"SSRF_ALLOWLIST": "192.168.1.5,*.internal.local,10.0.0.0/24"}):
        # Test allowed IP
        allowed_ip = "http://192.168.1.5"
        res = await validate_url(allowed_ip)
        assert res == allowed_ip

        # Test blocked IP (not in list)
        blocked_ip = "http://192.168.1.6"
        with pytest.raises(ValueError):
            await validate_url(blocked_ip)

        # Test CIDR
        cidr_ip = "http://10.0.0.42"
        res = await validate_url(cidr_ip)
        assert res == cidr_ip

        # Test Wildcard Domain (mock DNS resolution to unsafe IP)
        wildcard_domain = "http://service.internal.local"
        res = await validate_url(wildcard_domain)
        assert res == wildcard_domain
