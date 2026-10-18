#!/usr/bin/env python3
"""
Python Reference Implementation for Proximity Challenge/Response

This script simulates a hardware token (or smart badge) communicating with
the Proximity Challenge-Response Daemon. It demonstrates:
1. Generating a local ECDSA keypair (simulating a Secure Element).
2. Fetching an ephemeral challenge nonce from the daemon.
3. Signing the challenge deterministically.
4. Sending the verification request to authenticate presence and allocate compute.

Requirements:
    pip install httpx cryptography
"""

import httpx
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

# Configuration
DAEMON_URL = "http://127.0.0.1:8011/api/v1"
ROOM_ID = "room_101"
DID = "did:example:alice-badge-001"
SECRET_HEADER = "secret" # Must match TAP_ORCHESTRATOR_SECRET

def generate_keypair():
    """Simulates a Secure Element generating a P-256 keypair."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    # Extract hex format as expected by the daemon
    public_key_hex = public_key.public_bytes(
        encoding=Encoding.X962,
        format=PublicFormat.UncompressedPoint
    ).hex()

    return private_key, public_key_hex

def deterministic_json(payload: dict) -> bytes:
    """Creates a deterministic JSON byte string for signing."""
    return json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')

def sign_payload(private_key, payload_dict: dict) -> str:
    """Signs the payload and returns a base64 encoded signature."""
    payload_bytes = deterministic_json(payload_dict)
    signature = private_key.sign(
        payload_bytes,
        ec.ECDSA(hashes.SHA256())
    )
    return base64.b64encode(signature).decode('utf-8')

def main():
    print(f"[*] Simulating hardware token for {DID} in {ROOM_ID}")

    # 1. Initialize "Secure Element"
    private_key, public_key_hex = generate_keypair()
    print(f"[+] Keypair generated. Public Key: {public_key_hex[:16]}...")

    headers = {"X-Tap-Secret": SECRET_HEADER}

    with httpx.Client(base_url=DAEMON_URL, headers=headers) as client:
        # 2. Fetch Challenge
        print(f"[*] Fetching challenge for {ROOM_ID}...")
        resp = client.get("/challenge", params={"room_id": ROOM_ID})
        resp.raise_for_status()
        challenge_data = resp.json()
        nonce = challenge_data["nonce"]
        print(f"[+] Received nonce: {nonce}")

        # 3. Sign the Challenge
        payload_to_verify = {
            "challenge_nonce": nonce,
            "room_id": ROOM_ID
        }
        signature = sign_payload(private_key, payload_to_verify)
        print(f"[+] Signed payload. Signature: {signature[:16]}...")

        # 4. Submit Verification
        verify_req = {
            "did": DID,
            "challenge_nonce": nonce,
            "signature": signature,
            "room_id": ROOM_ID,
            "public_key_hex": public_key_hex,
            "metadata": {"rssi": -45, "battery": 92} # Example spatial/hardware metadata
        }

        print(f"[*] Submitting verification payload...")
        verify_resp = client.post("/verify", json=verify_req)

        if verify_resp.status_code == 200:
            result = verify_resp.json()
            print("[✓] Presence Verified successfully!")
            print(f"[✓] Active Compute Weight: {result.get('weight')}")
        else:
            print(f"[!] Verification failed: {verify_resp.status_code}")
            print(verify_resp.text)

if __name__ == "__main__":
    main()
