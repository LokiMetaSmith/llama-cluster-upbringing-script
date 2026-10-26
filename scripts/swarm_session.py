#!/usr/bin/env python3
"""
Swarm Cluster Session Management CLI.
Provides unified operator and presence session control across cluster services
(Terminal SSH, Grafana, Nomad, Consul, Compute/MoE).

Usage:
    swarm_session.py status [--user USER] [--token TOKEN]
    swarm_session.py create --user USER [--ttl SECONDS] [--method METHOD] [--targets TARGETS] [--key-file PATH]
    swarm_session.py revoke [--user USER] [--token TOKEN]
    swarm_session.py list
"""

import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.error
import urllib.parse

DEFAULT_ORCHESTRATOR_URLS = [
    os.getenv("TAP_ORCHESTRATOR_URL", ""),
    "http://127.0.0.1:8011",
    "http://127.0.0.1:8012",
    "http://100.64.0.1:8011",
    "http://192.168.1.202:8011"
]
TAP_SECRET = os.getenv("TAP_ORCHESTRATOR_SECRET", "change_me_in_prod_tap_secret")
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

def get_orchestrator_base():
    for url in DEFAULT_ORCHESTRATOR_URLS:
        if not url:
            continue
        try:
            req = urllib.request.Request(f"{url}/docs", headers={"User-Agent": "swarm_session"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    return url
        except Exception:
            continue
    # Default to first non-empty or localhost:8011
    return [u for u in DEFAULT_ORCHESTRATOR_URLS if u][0] if any(DEFAULT_ORCHESTRATOR_URLS) else "http://127.0.0.1:8011"

def consul_request(path: str, method: str = "GET", data: dict | list | str = None):
    token = get_consul_token()
    url = f"{CONSUL_ADDR}/v1/{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["X-Consul-Token"] = token
    
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8") if isinstance(data, (dict, list)) else str(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            content = resp.read().decode("utf-8")
            if not content:
                return None
            try:
                return json.loads(content)
            except Exception:
                return content
    except Exception:
        return None

def orchestrator_request(endpoint: str, method: str = "GET", data: dict = None, token: str = None):
    base_url = get_orchestrator_base()
    url = f"{base_url}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "X-Tap-Secret": TAP_SECRET
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        try:
            return json.loads(err_msg)
        except Exception:
            return {"status": "error", "message": f"HTTP {e.code}: {err_msg}"}
    except Exception as e:
        return None

def cmd_status(args):
    user_id = args.user or os.getenv("USER", "operator")
    token = args.token

    # 1. Try tap_orchestrator API
    params = {}
    if token:
        params["token"] = token
    elif user_id:
        params["user_id"] = user_id

    query_str = urllib.parse.urlencode(params)
    resp = orchestrator_request(f"/api/v1/session/status?{query_str}", method="GET")

    if resp and resp.get("status") in ("active", "expired", "revoked", "success"):
        session = resp.get("session") or {}
        valid = resp.get("valid", False)
        remaining = resp.get("remaining_seconds", 0)
        print("=" * 60)
        print(f" Swarm Cluster Session Status: {'[ ACTIVE ]' if valid else '[ INACTIVE / EXPIRED ]'}")
        print("=" * 60)
        print(f" User ID:         {session.get('user_id', user_id)}")
        print(f" DID:             {session.get('did', 'N/A')}")
        print(f" Auth Method:     {session.get('auth_method', 'N/A')}")
        print(f" Session ID:      {session.get('session_id', 'N/A')}")
        print(f" Session Token:   {session.get('session_token', 'N/A')}")
        print(f" Roles:           {', '.join(session.get('roles', []))}")
        print(f" Allowed Targets: {', '.join(session.get('allowed_targets', []))}")
        print(f" Remaining TTL:   {remaining} seconds ({remaining // 60}m {remaining % 60}s)")
        print(f" Public Key:      {session.get('public_key') or 'None'}")
        print("=" * 60)
        return

    # 2. Fallback to Consul KV
    key = f"swarm/tokens/{token}" if token else f"swarm/sessions/{user_id}"
    kv_data = consul_request(f"kv/{key}?raw")
    if kv_data and isinstance(kv_data, dict):
        now = time.time()
        expires_at = kv_data.get("expires_at", 0)
        valid = kv_data.get("is_active", False) and expires_at > now
        remaining = max(0, int(expires_at - now))
        print("=" * 60)
        print(f" Swarm Cluster Session Status (Direct KV): {'[ ACTIVE ]' if valid else '[ INACTIVE / EXPIRED ]'}")
        print("=" * 60)
        print(f" User ID:         {kv_data.get('user_id', user_id)}")
        print(f" Auth Method:     {kv_data.get('auth_method', 'N/A')}")
        print(f" Session Token:   {kv_data.get('session_token', 'N/A')}")
        print(f" Allowed Targets: {', '.join(kv_data.get('allowed_targets', []))}")
        print(f" Remaining TTL:   {remaining} seconds")
        print("=" * 60)
        return

    print(f"No active session found for user '{user_id}' / token.")
    sys.exit(1)

def cmd_create(args):
    user_id = args.user or os.getenv("USER", "operator")
    ttl = args.ttl or 3600
    method = args.method or "fido2"
    targets = [t.strip() for t in args.targets.split(",")] if args.targets else ["terminal", "grafana", "nomad", "consul", "compute"]
    
    pub_key = None
    if args.key:
        pub_key = args.key.strip()
    elif args.key_file and os.path.exists(args.key_file):
        with open(args.key_file, "r") as f:
            pub_key = f.read().strip()
    elif os.path.exists(os.path.expanduser("~/.ssh/id_ed25519.pub")):
        with open(os.path.expanduser("~/.ssh/id_ed25519.pub"), "r") as f:
            pub_key = f.read().strip()
    elif os.path.exists(os.path.expanduser("~/.ssh/id_rsa.pub")):
        with open(os.path.expanduser("~/.ssh/id_rsa.pub"), "r") as f:
            pub_key = f.read().strip()

    payload = {
        "user_id": user_id,
        "did": f"did:key:{user_id}",
        "auth_method": method,
        "ttl_seconds": ttl,
        "allowed_targets": targets,
        "roles": ["operator", "admin"] if user_id in ("admin", "operator", "loki", "pipecatapp") else ["operator"],
        "public_key": pub_key
    }

    # 1. Try tap_orchestrator API
    resp = orchestrator_request("/api/v1/session/create", method="POST", data=payload)
    if resp and resp.get("valid"):
        sess = resp.get("session") or {}
        token = sess.get("session_token")
        print("Session successfully created via Tap Orchestrator!")
        print(f"User:          {user_id}")
        print(f"Session Token: {token}")
        print(f"Expires in:    {ttl}s")
        print(f"Targets:       {', '.join(targets)}")
        if pub_key:
            print(f"SSH Key:       {pub_key[:40]}...")
        return

    # 2. Fallback to direct Consul KV
    import secrets
    now = time.time()
    session_id = f"sess_{secrets.token_hex(12)}"
    session_token = f"swarm_st_{secrets.token_urlsafe(24)}"
    session_obj = {
        "session_id": session_id,
        "session_token": session_token,
        "user_id": user_id,
        "did": payload["did"],
        "auth_method": method,
        "roles": payload["roles"],
        "allowed_targets": targets,
        "created_at": now,
        "expires_at": now + ttl,
        "is_active": True,
        "public_key": pub_key,
        "metadata": {}
    }
    
    consul_request(f"kv/swarm/sessions/{user_id}", method="PUT", data=session_obj)
    consul_request(f"kv/swarm/tokens/{session_token}", method="PUT", data=session_obj)
    if user_id in ("admin", "operator", "pipecatapp"):
        consul_request("kv/swarm/sessions/active_operator", method="PUT", data=session_obj)

    print("Session created via Consul KV direct storage (Orchestrator offline/direct mode):")
    print(f"User:          {user_id}")
    print(f"Session Token: {session_token}")
    print(f"Expires in:    {ttl}s")
    print(f"Targets:       {', '.join(targets)}")

def cmd_revoke(args):
    user_id = args.user
    token = args.token

    payload = {"user_id": user_id, "session_token": token}
    resp = orchestrator_request("/api/v1/session/revoke", method="POST", data=payload)
    if resp and resp.get("status") == "revoked":
        print(f"Session revoked successfully via Orchestrator.")
        if user_id in ("admin", "operator", "pipecatapp"):
            consul_request("kv/swarm/sessions/active_operator", method="DELETE")
        return

    # Direct Consul deletion
    if user_id:
        consul_request(f"kv/swarm/sessions/{user_id}", method="DELETE")
        if user_id in ("admin", "operator", "pipecatapp"):
            consul_request("kv/swarm/sessions/active_operator", method="DELETE")
    if token:
        consul_request(f"kv/swarm/tokens/{token}", method="DELETE")
    print("Session revoked / purged from Consul KV.")

def cmd_list(args):
    keys = consul_request("kv/swarm/sessions/?keys")
    if not keys or not isinstance(keys, list):
        print("No active presence sessions found in cluster.")
        return

    print("=" * 70)
    print(f"{'USER / KEY':<25} {'STATUS':<12} {'EXPIRES IN':<15} {'AUTH METHOD':<15}")
    print("=" * 70)
    now = time.time()
    for k in keys:
        clean_k = k.removeprefix("swarm/sessions/")
        if not clean_k:
            continue
        data = consul_request(f"kv/{k}?raw")
        if isinstance(data, dict):
            active = data.get("is_active", False)
            exp = data.get("expires_at", 0)
            valid = active and exp > now
            rem = max(0, int(exp - now))
            method = data.get("auth_method", "unknown")
            status_str = "ACTIVE" if valid else "EXPIRED"
            rem_str = f"{rem}s ({rem//60}m)" if valid else "0s"
            print(f"{clean_k:<25} {status_str:<12} {rem_str:<15} {method:<15}")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Swarm Cluster Session CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    p_status = subparsers.add_parser("status", help="Get session status")
    p_status.add_argument("--user", "-u", help="Username or DID to query")
    p_status.add_argument("--token", "-t", help="Session token to query")
    p_status.set_defaults(func=cmd_status)

    # create
    p_create = subparsers.add_parser("create", help="Create a cluster presence session")
    p_create.add_argument("--user", "-u", required=True, help="Username or DID")
    p_create.add_argument("--ttl", type=int, default=3600, help="TTL in seconds (default 3600)")
    p_create.add_argument("--method", "-m", default="fido2", choices=["fido2", "ble_presence", "desfire_nfc", "challenge_attestation", "cli_bootstrap"], help="Auth method")
    p_create.add_argument("--targets", help="Comma-separated allowed targets (terminal,grafana,nomad,consul,compute)")
    p_create.add_argument("--key", help="SSH Public Key string to associate")
    p_create.add_argument("--key-file", help="Path to SSH Public Key file")
    p_create.set_defaults(func=cmd_create)

    # revoke
    p_revoke = subparsers.add_parser("revoke", help="Revoke a cluster session")
    p_revoke.add_argument("--user", "-u", help="Username to revoke")
    p_revoke.add_argument("--token", "-t", help="Session token to revoke")
    p_revoke.set_defaults(func=cmd_revoke)

    # list
    p_list = subparsers.add_parser("list", help="List all sessions recorded in Consul")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
