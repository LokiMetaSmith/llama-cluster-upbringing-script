import os
import json
import base64
import logging
from typing import List, Dict, Any, Optional
import httpx

logger = logging.getLogger(__name__)

class ConsulKVBackend:
    """
    A stateless memory backend that persists coordination state into the Consul KV store.
    This manages session data and tracking to prevent failover issues, but DOES NOT store heavy vector embeddings.
    """
    def __init__(self, prefix: str = "pipecat/state/"):
        self.consul_url = os.getenv("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")
        if not self.consul_url.startswith("http"):
            self.consul_url = "http://" + self.consul_url
        self.prefix = prefix
        self.token = os.getenv("CONSUL_HTTP_TOKEN", "")
        if not self.token:
            for env_path in ["/opt/pipecatapp/pipecat.env", "/etc/environment"]:
                if os.path.exists(env_path):
                    try:
                        with open(env_path, "r") as f:
                            for line in f:
                                if "CONSUL_HTTP_TOKEN" in line:
                                    parts = line.strip().split("=", 1)
                                    if len(parts) == 2:
                                        self.token = parts[1].strip(" \"'")
                                        break
                    except Exception:
                        pass
                if self.token:
                    break
        headers = {}
        if self.token:
            headers["X-Consul-Token"] = self.token
        self.client = httpx.Client(base_url=self.consul_url, headers=headers)

    def put_kv(self, key: str, value: Any):
        try:
            val_str = json.dumps(value) if not isinstance(value, str) else value
            res = self.client.put(f"/v1/kv/{self.prefix}{key}", content=val_str)
            res.raise_for_status()
        except Exception as e:
            logger.error(f"Consul KV PUT failed for {key}: {e}")

    def get_kv(self, key: str) -> Optional[Any]:
        try:
            res = self.client.get(f"/v1/kv/{self.prefix}{key}")
            if res.status_code == 404:
                return None
            res.raise_for_status()
            data = res.json()
            if data and isinstance(data, list) and len(data) > 0:
                raw_val = base64.b64decode(data[0].get("Value", "")).decode("utf-8")
                try:
                    return json.loads(raw_val)
                except json.JSONDecodeError:
                    return raw_val
            return None
        except Exception as e:
            logger.error(f"Consul KV GET failed for {key}: {e}")
            return None

    def delete_kv(self, key: str) -> bool:
        try:
            res = self.client.delete(f"/v1/kv/{self.prefix}{key}")
            res.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Consul KV DELETE failed for {key}: {e}")
            return False
