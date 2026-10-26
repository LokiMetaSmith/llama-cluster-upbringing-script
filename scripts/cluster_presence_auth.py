#!/usr/bin/env python3
"""
Cluster Presence & FIDO2 SSH Authentication Hook.
Designed to be invoked by OpenSSH sshd via:
    AuthorizedKeysCommand /usr/local/bin/cluster_presence_auth %u %k %t
    AuthorizedKeysCommandUser nobody

Workflow:
1. Queries Consul KV for an active, unexpired presence session under `swarm/sessions/<username>`
   or `swarm/sessions/active_operator`.
2. Validates that the session is active and grants 'terminal' target permission.
3. If valid, outputs the registered public keys associated with that session or user profile.
4. If invalid or presence expired, exits with code 1, denying touchless/presence admission.
"""

import sys
import json
import time
import urllib.request
import urllib.error
import os

CONSUL_ADDR = os.getenv("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")
CONSUL_TOKEN = os.getenv("CONSUL_HTTP_TOKEN", "")

def get_consul_token() -> str:
    global CONSUL_TOKEN
    if CONSUL_TOKEN:
        return CONSUL_TOKEN
    for env_path in ["/opt/pipecatapp/pipecat.env", "/etc/environment"]:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
                    for line in f:
                        if "CONSUL_HTTP_TOKEN" in line:
                            parts = line.strip().split("=", 1)
                            if len(parts) == 2:
                                CONSUL_TOKEN = parts[1].strip(" \"'")
                                return CONSUL_TOKEN
            except Exception:
                pass
    return ""

def get_consul_kv(key: str) -> dict | None:
    token = get_consul_token()
    url = f"{CONSUL_ADDR}/v1/kv/{key}?raw"
    headers = {}
    if token:
        headers["X-Consul-Token"] = token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            if resp.status == 200:
                content = resp.read().decode('utf-8')
                return json.loads(content)
    except Exception:
        return None
    return None

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    username = sys.argv[1]
    now = time.time()

    # 1. Lookup presence session in Consul KV
    session_data = get_consul_kv(f"swarm/sessions/{username}")
    if not session_data and username in ("pipecatapp", "operator", "root"):
        # Check active operator session fallback
        session_data = get_consul_kv("swarm/sessions/active_operator") or get_consul_kv("swarm/sessions/operator")

    if not session_data:
        sys.exit(1)

    # 2. Verify validity and expiration
    is_active = session_data.get("is_active", False)
    expires_at = session_data.get("expires_at", 0)
    allowed_targets = session_data.get("allowed_targets", [])

    if not is_active or expires_at <= now or "terminal" not in allowed_targets:
        sys.exit(1)

    # 3. Output public key if embedded in session
    keys_emitted = False
    public_key = session_data.get("public_key")
    if public_key and public_key.startswith(("ssh-", "sk-ssh-", "ecdsa-")):
        print(public_key)
        keys_emitted = True

    public_keys = session_data.get("public_keys")
    if isinstance(public_keys, list):
        for pk in public_keys:
            if isinstance(pk, str) and pk.startswith(("ssh-", "sk-ssh-", "ecdsa-")):
                print(pk)
                keys_emitted = True

    # 4. Lookup user's registered public keys from Consul KV ssh-keys/
    stored_key = get_consul_kv(f"ssh-keys/{username}")
    if stored_key:
        if isinstance(stored_key, str) and stored_key.startswith(("ssh-", "sk-ssh-", "ecdsa-")):
            print(stored_key)
            keys_emitted = True
        elif isinstance(stored_key, list):
            for pk in stored_key:
                if isinstance(pk, str) and pk.startswith(("ssh-", "sk-ssh-", "ecdsa-")):
                    print(pk)
                    keys_emitted = True

    if keys_emitted:
        sys.exit(0)

    # If session is active and authenticated, return success
    sys.exit(0)

if __name__ == "__main__":
    main()
