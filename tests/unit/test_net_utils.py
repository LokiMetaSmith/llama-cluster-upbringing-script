import sys
import os
import pytest

# Add repo root to path so we can import pipecatapp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pipecatapp.net_utils import ensure_ipv6_brackets

def test_ensure_ipv6_brackets_empty():
    assert ensure_ipv6_brackets("") == ""
    assert ensure_ipv6_brackets(None) == ""

def test_ensure_ipv6_brackets_ipv4():
    assert ensure_ipv6_brackets("127.0.0.1") == "127.0.0.1"
    assert ensure_ipv6_brackets("192.168.1.1") == "192.168.1.1"

def test_ensure_ipv6_brackets_ipv6_no_brackets():
    assert ensure_ipv6_brackets("::1") == "[::1]"
    assert ensure_ipv6_brackets("2001:0db8:85a3:0000:0000:8a2e:0370:7334") == "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]"
    assert ensure_ipv6_brackets("fe80::1ff:fe23:4567:890a") == "[fe80::1ff:fe23:4567:890a]"

def test_ensure_ipv6_brackets_ipv6_with_brackets():
    assert ensure_ipv6_brackets("[::1]") == "[::1]"
    assert ensure_ipv6_brackets("[2001:db8:85a3::8a2e:370:7334]") == "[2001:db8:85a3::8a2e:370:7334]"

def test_ensure_ipv6_brackets_hostname():
    assert ensure_ipv6_brackets("example.com") == "example.com"
    assert ensure_ipv6_brackets("localhost") == "localhost"

def test_ensure_ipv6_brackets_hostname_with_brackets():
    # As per implementation, invalid IPs wrapped in brackets should be returned as-is
    assert ensure_ipv6_brackets("[example.com]") == "[example.com]"
    assert ensure_ipv6_brackets("[localhost]") == "[localhost]"

def test_ensure_ipv6_brackets_invalid_ip():
    assert ensure_ipv6_brackets("256.256.256.256") == "256.256.256.256"
    assert ensure_ipv6_brackets("not_an_ip") == "not_an_ip"
