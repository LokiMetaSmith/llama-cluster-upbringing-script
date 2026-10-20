import os
import pytest
from pipecatapp.tools.totp_tool import TOTPTool

TEST_SEED = "JBSWY3DPEHPK3PXP" # Base32 seed for "Hello!"


def test_totp_tool_direct_seed():
    tool = TOTPTool()
    res = tool.generate_totp_code(TEST_SEED)
    assert "TOTP Code for 'JBSWY3DPEHPK3PXP':" in res
    assert "Valid for next" in res


def test_totp_tool_local_store():
    tool = TOTPTool()
    store_res = tool.store_totp_seed("github", TEST_SEED)
    assert "Stored TOTP seed for 'github'" in store_res

    res = tool.generate_totp_code("github")
    assert "TOTP Code for 'github':" in res


def test_totp_tool_env_var(monkeypatch):
    monkeypatch.setenv("TOTP_SEED_HUGGINGFACE", TEST_SEED)
    tool = TOTPTool()
    res = tool.generate_totp_code("huggingface")
    assert "TOTP Code for 'huggingface':" in res


def test_totp_tool_missing_seed():
    tool = TOTPTool()
    res = tool.generate_totp_code("nonexistent_service_123")
    assert "Error: No TOTP seed found" in res


def test_totp_tool_execute():
    tool = TOTPTool()
    tool.store_totp_seed("testservice", TEST_SEED)
    res = tool.execute("generate_totp_code", service_name="testservice")
    assert "TOTP Code for 'testservice':" in res


def test_totp_schema():
    tool = TOTPTool()
    schema = tool.get_schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "totp"
