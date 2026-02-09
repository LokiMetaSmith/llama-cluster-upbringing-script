import asyncio
import sys
import os
from unittest.mock import patch

# Add repo root to path so we can import pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipecatapp.net_utils import validate_url

async def test_validate_url_safe():
    print("Testing safe URLs...")
    # Public URLs should pass and return ORIGINAL URL
    try:
        url_https = "https://google.com"
        res_https = await validate_url(url_https)
        if res_https != url_https:
            print(f"FAILED: HTTPS URL was rewritten: {res_https}")
            sys.exit(1)

        url_http = "http://example.com"
        res_http = await validate_url(url_http)
        if res_http != url_http:
             print(f"FAILED: HTTP URL was rewritten: {res_http}")
             sys.exit(1)

        print(f"Safe URLs passed. Original URL preserved: {res_http}")
    except ValueError as e:
        if "Could not resolve" in str(e):
            print(f"Skipping DNS test due to network issues: {e}")
        else:
            print(f"FAILED: Safe URL rejected: {e}")
            sys.exit(1)

async def test_validate_url_unsafe_ip():
    print("Testing unsafe IPs...")
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
        try:
            await validate_url(url)
            print(f"FAILED: {url} was NOT blocked")
            sys.exit(1)
        except ValueError as e:
            if "Blocked" not in str(e):
                print(f"FAILED: {url} raised wrong error: {e}")
                sys.exit(1)
    print("Unsafe IPs blocked correctly.")

async def test_validate_url_unsafe_scheme():
    print("Testing unsafe schemes...")
    unsafe_schemes = [
        "ftp://google.com",
        "file:///etc/passwd",
        "gopher://google.com"
    ]
    for url in unsafe_schemes:
        try:
            await validate_url(url)
            print(f"FAILED: {url} was NOT blocked")
            sys.exit(1)
        except ValueError as e:
            if "Scheme" not in str(e):
                print(f"FAILED: {url} raised wrong error: {e}")
                sys.exit(1)
    print("Unsafe schemes blocked correctly.")

async def test_allowlist():
    print("Testing SSRF_ALLOWLIST...")
    # Simulate environment variable
    with patch.dict(os.environ, {"SSRF_ALLOWLIST": "192.168.1.5,*.internal.local,10.0.0.0/24"}):

        # Test allowed IP
        allowed_ip = "http://192.168.1.5"
        try:
            res = await validate_url(allowed_ip)
            print(f"Allowed IP passed: {res}")
        except ValueError as e:
            print(f"FAILED: Allowed IP {allowed_ip} was blocked: {e}")
            sys.exit(1)

        # Test blocked IP (not in list)
        blocked_ip = "http://192.168.1.6"
        try:
            await validate_url(blocked_ip)
            print(f"FAILED: Blocked IP {blocked_ip} passed (should be blocked)")
            sys.exit(1)
        except ValueError:
            pass

        # Test CIDR
        cidr_ip = "http://10.0.0.42"
        try:
            res = await validate_url(cidr_ip)
            print(f"CIDR IP passed: {res}")
        except ValueError as e:
            print(f"FAILED: CIDR IP {cidr_ip} was blocked: {e}")
            sys.exit(1)

        # Test Wildcard Domain (mock DNS resolution to unsafe IP)
        wildcard_domain = "http://service.internal.local"
        # We need to mock socket.getaddrinfo to return a private IP for this domain
        # but since allowlist checks hostname first, it should pass regardless of IP resolution
        try:
            res = await validate_url(wildcard_domain)
            print(f"Wildcard domain passed: {res}")
        except ValueError as e:
            print(f"FAILED: Wildcard domain {wildcard_domain} was blocked: {e}")
            sys.exit(1)

    print("Allowlist tests passed.")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run_tests():
        await test_validate_url_safe()
        await test_validate_url_unsafe_ip()
        await test_validate_url_unsafe_scheme()
        await test_allowlist()
        print("All tests passed!")

    loop.run_until_complete(run_tests())
