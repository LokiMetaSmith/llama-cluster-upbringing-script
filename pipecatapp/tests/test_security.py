import sys
import os
import pytest

# Ensure pipecatapp is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from security import redact_sensitive_data

def test_redact_openai_key():
    text = "Here is my key sk-1234567890abcdef1234567890abcdef"
    redacted = redact_sensitive_data(text)
    assert "sk-[REDACTED]" in redacted
    assert "sk-1234567890abcdef1234567890abcdef" not in redacted

def test_redact_github_key():
    text = "My token is ghp_1234567890abcdef1234567890abcdef3636"
    redacted = redact_sensitive_data(text)
    assert "gh-[REDACTED]" in redacted
    assert "ghp_1234567890abcdef1234567890abcdef3636" not in redacted

def test_redact_bearer_token():
    text = "Authorization: Bearer abcdef12345-token"
    redacted = redact_sensitive_data(text)
    assert "Bearer [REDACTED]" in redacted
    assert "abcdef12345-token" not in redacted

def test_redact_gitlab_key():
    # This should fail initially
    text = "My gitlab token is glpat-1234567890abcdef1234"
    redacted = redact_sensitive_data(text)
    # Expectation
    if "glpat-" in redacted and "1234567890abcdef1234" in redacted:
        pytest.fail("GitLab token was not redacted")

def test_redact_url_credentials():
    # This should fail initially
    # Covers Bitbucket, GitHub, GitLab, etc. when used in URLs
    urls = [
        "https://user:password123@github.com/repo.git",
        "https://user:glpat-12345@gitlab.com/repo.git",
        "https://x-token-auth:ATATT-bitbucket-token@bitbucket.org/repo.git"
    ]

    for url in urls:
        redacted = redact_sensitive_data(url)
        if "password123" in redacted or "glpat-12345" in redacted or "ATATT-bitbucket-token" in redacted:
            pytest.fail(f"URL credentials were not redacted in: {redacted}")

        # Verify structure is preserved
        assert "@" in redacted
        assert "://" in redacted
