import asyncio
import sys
import os

# Add repo root to path so we can import pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipecatapp.net_utils import validate_url

async def test_validate_url_safe():
    print("Testing safe URLs...")
    # Public URLs should pass
    try:
        await validate_url("https://google.com")
        await validate_url("http://example.com")
        print("Safe URLs passed.")
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

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run_tests():
        await test_validate_url_safe()
        await test_validate_url_unsafe_ip()
        await test_validate_url_unsafe_scheme()
        print("All tests passed!")

    loop.run_until_complete(run_tests())
