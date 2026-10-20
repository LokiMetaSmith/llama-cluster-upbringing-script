import base64
import hashlib
import hmac
import logging
import os
import struct
import time
from typing import Optional, Dict, Any

try:
    import urllib.request
    import urllib.parse
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

try:
    import pyotp
    HAS_PYOTP = True
except ImportError:
    HAS_PYOTP = False

logger = logging.getLogger("TOTPTool")


class TOTPTool:
    """Tool for generating 6-digit TOTP authentication codes for external agent tooling.

    Attributes:
        consul_url (str): Base URL for Consul KV store.
        local_seeds (dict): In-memory fallback cache for TOTP seeds.
    """

    def __init__(self, consul_url: Optional[str] = None):
        self.name = "totp"
        self.description = "Generate time-based one-time passwords (TOTP) for external agent MFA authentication."
        self.consul_url = consul_url or os.getenv("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")
        self.local_seeds: Dict[str, str] = {}

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "totp"),
                "description": getattr(self, "description", "TOTP authentication tool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform. Available: generate_totp_code, store_totp_seed"
                        },
                        "service_name": {
                            "type": "string",
                            "description": "The name of the external service (e.g. 'github', 'huggingface') or base32 seed."
                        },
                        "seed": {
                            "type": "string",
                            "description": "Base32 seed secret (used when storing a new seed)."
                        }
                    },
                    "required": ["action", "service_name"]
                }
            }
        }

    def execute(self, action: str, **kwargs) -> Any:
        params = kwargs.get("kwargs", kwargs)
        if action == "generate_totp_code":
            return self.generate_totp_code(params.get("service_name", ""))
        elif action == "store_totp_seed":
            return self.store_totp_seed(params.get("service_name", ""), params.get("seed", ""))
        else:
            return f"Unknown action: {action}"

    def _fetch_seed_from_consul(self, service_name: str) -> Optional[str]:
        if not HAS_URLLIB:
            return None
        url = f"{self.consul_url.rstrip('/')}/v1/kv/totp/{urllib.parse.quote(service_name)}?raw=true"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return response.read().decode("utf-8").strip()
        except Exception as e:
            logger.debug(f"Consul KV lookup for TOTP seed '{service_name}' failed: {e}")
        return None

    def _store_seed_in_consul(self, service_name: str, seed: str) -> bool:
        if not HAS_URLLIB:
            return False
        url = f"{self.consul_url.rstrip('/')}/v1/kv/totp/{urllib.parse.quote(service_name)}"
        try:
            req = urllib.request.Request(url, data=seed.encode("utf-8"), method="PUT")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status in (200, 201)
        except Exception as e:
            logger.debug(f"Failed to store TOTP seed in Consul KV for '{service_name}': {e}")
            return False

    def get_seed(self, service_or_seed: str) -> Optional[str]:
        # 1. Local memory cache
        if service_or_seed.lower() in self.local_seeds:
            return self.local_seeds[service_or_seed.lower()]

        # 2. Environment Variable (TOTP_SEED_<SERVICE>)
        env_var_name = f"TOTP_SEED_{service_or_seed.upper()}"
        if env_var_name in os.environ:
            return os.environ[env_var_name]

        # 3. Consul KV store
        consul_seed = self._fetch_seed_from_consul(service_or_seed.lower())
        if consul_seed:
            return consul_seed

        # 4. Direct Base32 seed string check (16+ chars, valid base32 chars A-Z, 2-7)
        clean_input = service_or_seed.strip().replace(" ", "").upper()
        if len(clean_input) >= 16 and all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=" for c in clean_input):
            return clean_input

        return None

    def store_totp_seed(self, service_name: str, seed: str) -> str:
        clean_service = service_name.strip().lower()
        clean_seed = seed.strip().replace(" ", "").upper()
        if not clean_service or not clean_seed:
            return "Error: service_name and seed must both be provided."

        self.local_seeds[clean_service] = clean_seed
        consul_ok = self._store_seed_in_consul(clean_service, clean_seed)

        if consul_ok:
            return f"Successfully stored TOTP seed for '{clean_service}' in Consul KV and local memory."
        else:
            return f"Stored TOTP seed for '{clean_service}' in local memory (Consul KV unavailable)."

    def generate_totp_code(self, service_or_seed: str) -> str:
        seed = self.get_seed(service_or_seed)
        if not seed:
            return f"Error: No TOTP seed found for service or key '{service_or_seed}'."

        try:
            if HAS_PYOTP:
                totp = pyotp.TOTP(seed)
                code = totp.now()
            else:
                code = self._generate_rfc6238_totp(seed)

            time_remaining = 30 - (int(time.time()) % 30)
            return f"TOTP Code for '{service_or_seed}': {code} (Valid for next {time_remaining} seconds)"
        except Exception as e:
            return f"Error generating TOTP code: {e}"

    def _generate_rfc6238_totp(self, secret: str, interval: int = 30, digits: int = 6) -> str:
        secret_clean = secret.upper().replace(" ", "")
        missing_padding = len(secret_clean) % 8
        if missing_padding:
            secret_clean += "=" * (8 - missing_padding)
        key = base64.b32decode(secret_clean, casefold=True)
        counter = int(time.time()) // interval
        msg = struct.pack(">Q", counter)
        digest = hmac.new(key, msg, hashlib.sha1).digest()
        offset = digest[-1] & 0x0F
        code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
        return str(code).zfill(digits)
