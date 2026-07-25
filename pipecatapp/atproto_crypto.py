import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives.serialization import load_der_private_key, load_der_public_key

def _get_deterministic_json(payload_dict: dict) -> bytes:
    """Returns a deterministic JSON byte representation of the payload."""
    # Ensure keys are sorted for consistent hashing
    return json.dumps(payload_dict, sort_keys=True, separators=(',', ':')).encode('utf-8')

def sign_payload(payload_dict: dict, private_key_hex: str) -> str:
    """
    Signs a dictionary payload deterministically using an ECDSA SECP256R1 private key in hex format.
    Returns the signature as a base64 encoded string.
    """
    payload_bytes = _get_deterministic_json(payload_dict)

    # Load private key from hex
    private_key_bytes = bytes.fromhex(private_key_hex)
    private_key_int = int.from_bytes(private_key_bytes, byteorder='big')
    private_key = ec.derive_private_key(private_key_int, ec.SECP256R1())

    signature = private_key.sign(
        payload_bytes,
        ec.ECDSA(hashes.SHA256())
    )

    return base64.b64encode(signature).decode('utf-8')

def verify_payload(payload_dict: dict, signature_b64: str, public_key_hex: str) -> bool:
    """
    Verifies the payload signature using the given public key in hex format.
    Returns True if valid, False otherwise.
    """
    try:
        payload_bytes = _get_deterministic_json(payload_dict)
        signature = base64.b64decode(signature_b64)

        public_key_bytes = bytes.fromhex(public_key_hex)
        public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), public_key_bytes)

        public_key.verify(
            signature,
            payload_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception:
        return False
