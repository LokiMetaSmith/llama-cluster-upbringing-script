import pytest
import os
import sys

# Add the necessary path to import the workflow modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp')))

from workflow.crypto_receipts import ToolExecutionSigner

def test_sign_receipt():
    """Tests that a tool execution payload can be signed deterministically."""
    signer = ToolExecutionSigner(secret_key=b'test_secret')
    tool_name = "test_tool"
    args = {"arg1": "value1", "arg2": 42}
    result = "Success"

    signature = signer.sign(tool_name, args, result)
    assert isinstance(signature, str)
    assert len(signature) == 64  # HMAC-SHA256 hex string length

    # Ensure deterministic signatures for the same payload
    signature2 = signer.sign(tool_name, args, result)
    assert signature == signature2

def test_verify_receipt():
    """Tests that a generated signature can be verified correctly."""
    signer = ToolExecutionSigner(secret_key=b'test_secret')
    tool_name = "test_tool"
    args = {"arg1": "value1", "arg2": 42}
    result = "Success"

    signature = signer.sign(tool_name, args, result)

    # Valid verification
    assert signer.verify(tool_name, args, result, signature) is True

    # Invalid verification (wrong tool name)
    assert signer.verify("wrong_tool", args, result, signature) is False

    # Invalid verification (wrong args)
    assert signer.verify(tool_name, {"arg1": "wrong"}, result, signature) is False

    # Invalid verification (wrong result)
    assert signer.verify(tool_name, args, "Failed", signature) is False

    # Invalid signature
    assert signer.verify(tool_name, args, result, "invalid_signature_hex") is False
