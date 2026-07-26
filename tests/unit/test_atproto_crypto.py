import pytest
from pipecatapp.atproto_crypto import sign_payload, verify_payload

def test_sign_and_verify():
    # Use a dummy SECP256R1 private key (32 bytes)
    import os
    private_key_bytes = os.urandom(32)
    private_key_hex = private_key_bytes.hex()

    # Generate matching public key
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization
    private_key_int = int.from_bytes(private_key_bytes, byteorder='big')
    private_key = ec.derive_private_key(private_key_int, ec.SECP256R1())
    public_key = private_key.public_key()

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    public_key_hex = public_key_bytes.hex()

    payload = {"message": "hello", "severity": "high"}

    # Sign
    signature = sign_payload(payload, private_key_hex)
    assert signature is not None
    assert len(signature) > 0

    # Verify
    is_valid = verify_payload(payload, signature, public_key_hex)
    assert is_valid is True

    # Verify with tampered payload
    payload_tampered = {"message": "hello", "severity": "low"}
    is_valid_tampered = verify_payload(payload_tampered, signature, public_key_hex)
    assert is_valid_tampered is False
