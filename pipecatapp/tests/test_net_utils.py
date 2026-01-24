import unittest
from pipecatapp.net_utils import ensure_ipv6_brackets, format_url

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

if __name__ == "__main__":
    unittest.main()
