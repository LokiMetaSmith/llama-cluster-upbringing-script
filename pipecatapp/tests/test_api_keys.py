import hashlib
import sys
import os
import pytest

# Ensure pipecatapp is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api_keys import get_api_key_hash

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
