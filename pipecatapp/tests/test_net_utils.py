import unittest
import asyncio
from unittest.mock import patch, MagicMock
import socket
from pipecatapp.net_utils import ensure_ipv6_brackets, format_url, validate_url, resolve_and_validate_url

class TestNetUtils(unittest.TestCase):
    def test_ensure_ipv6_brackets(self):
        # IPv4
        self.assertEqual(ensure_ipv6_brackets("127.0.0.1"), "127.0.0.1")
        self.assertEqual(ensure_ipv6_brackets("0.0.0.0"), "0.0.0.0")

        # IPv6
        self.assertEqual(ensure_ipv6_brackets("::1"), "[::1]")
        self.assertEqual(ensure_ipv6_brackets("2001:db8::1"), "[2001:db8::1]")

        # Already bracketed IPv6
        self.assertEqual(ensure_ipv6_brackets("[::1]"), "[::1]")

        # Hostnames
        self.assertEqual(ensure_ipv6_brackets("localhost"), "localhost")
        self.assertEqual(ensure_ipv6_brackets("example.com"), "example.com")

        # Empty
        self.assertEqual(ensure_ipv6_brackets(""), "")

    def test_format_url(self):
        # Basic IPv4
        self.assertEqual(format_url("http", "127.0.0.1", 8000), "http://127.0.0.1:8000")
        self.assertEqual(format_url("http", "127.0.0.1", 8000, "/api"), "http://127.0.0.1:8000/api")

        # IPv6
        self.assertEqual(format_url("http", "::1", 8000), "http://[::1]:8000")
        self.assertEqual(format_url("http", "2001:db8::1", 80), "http://[2001:db8::1]:80")

        # Hostname
        self.assertEqual(format_url("https", "example.com", 443), "https://example.com:443")

        # Path handling
        self.assertEqual(format_url("http", "localhost", 8080, "v1/status"), "http://localhost:8080/v1/status")
        self.assertEqual(format_url("http", "localhost", 8080, "/v1/status"), "http://localhost:8080/v1/status")

        # No port
        self.assertEqual(format_url("http", "localhost"), "http://localhost")

class TestValidateUrl(unittest.IsolatedAsyncioTestCase):
    @patch("socket.getaddrinfo")
    async def test_validate_url_public(self, mock_getaddrinfo):
        # Mock public IP resolution
        mock_getaddrinfo.return_value = [
            (2, 1, 6, '', ('8.8.8.8', 0))
        ]

        url = "http://example.com"
        safe_url = await validate_url(url)
        self.assertEqual(safe_url, url)

        # Test resolve_and_validate_url
        safe_url, ip = await resolve_and_validate_url(url)
        self.assertEqual(safe_url, url)
        self.assertEqual(ip, '8.8.8.8')

    @patch("socket.getaddrinfo")
    async def test_validate_url_private(self, mock_getaddrinfo):
        # Mock private IP resolution
        mock_getaddrinfo.return_value = [
            (2, 1, 6, '', ('192.168.1.1', 0))
        ]

        url = "http://internal.local"
        with self.assertRaises(ValueError) as cm:
            await validate_url(url)
        self.assertIn("restricted IP", str(cm.exception))

    async def test_validate_url_localhost(self):
        # Localhost should be blocked before DNS resolution
        url = "http://localhost:8000"
        with self.assertRaises(ValueError) as cm:
            await validate_url(url)
        self.assertIn("Access to localhost is forbidden", str(cm.exception))

    async def test_validate_url_scheme(self):
        url = "ftp://example.com"
        with self.assertRaises(ValueError) as cm:
            await validate_url(url)
        self.assertIn("Scheme 'ftp' is not allowed", str(cm.exception))

    @patch("os.getenv")
    @patch("socket.getaddrinfo")
    async def test_validate_url_allowlist(self, mock_getaddrinfo, mock_getenv):
        # Allow specific internal domain
        mock_getenv.return_value = "*.internal,192.168.1.5"

        # This shouldn't even trigger DNS if hostname matches
        url = "http://my.internal"
        safe_url, ip = await resolve_and_validate_url(url)
        self.assertEqual(safe_url, url)
        self.assertIsNone(ip) # Should return None as it was allowed by name

        # Test IP allowlist
        mock_getaddrinfo.return_value = [
            (2, 1, 6, '', ('192.168.1.5', 0))
        ]
        url = "http://safe.internal.ip"
        safe_url, ip = await resolve_and_validate_url(url)
        self.assertEqual(safe_url, url)
        self.assertEqual(ip, '192.168.1.5')

    @patch("socket.getaddrinfo")
    async def test_validate_url_dns_failure(self, mock_getaddrinfo):
        mock_getaddrinfo.side_effect = socket.gaierror

        url = "http://doesnotexist.com"
        with self.assertRaises(ValueError) as cm:
            await validate_url(url)
        self.assertIn("Could not resolve hostname", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
