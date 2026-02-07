import os
import logging
from typing import Dict, Optional, Set

class SecretManager:
    """
    A singleton class to manage sensitive secrets (API keys, tokens) in memory.
    It captures secrets from environment variables at startup and removes them
    from os.environ to prevent accidental leakage via child processes or
    unintentional exposure.
    """
    _instance = None
    _secrets: Dict[str, str] = {}
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecretManager, cls).__new__(cls)
        return cls._instance

    def initialize_from_env(self, sensitive_keys: Set[str]):
        """
        Captures specified keys from os.environ, stores them securely, and
        removes them from the environment.
        """
        if self._initialized:
            logging.warning("SecretManager already initialized.")
            return

        captured_count = 0
        for key in sensitive_keys:
            value = os.environ.get(key)
            if value:
                self._secrets[key] = value
                del os.environ[key]
                captured_count += 1
            else:
                # Check if it was already manually set (e.g. testing)
                if key not in self._secrets:
                    logging.debug(f"Secret key {key} not found in environment.")

        self._initialized = True
        logging.info(f"SecretManager initialized. Captured and secured {captured_count} secrets from environment.")

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieves a secret by key."""
        return self._secrets.get(key, default)

    def set_secret(self, key: str, value: str):
        """Manually sets a secret."""
        self._secrets[key] = value

    def get_all_secrets(self) -> Dict[str, str]:
        """Returns a copy of all secrets (use with caution)."""
        return self._secrets.copy()

# Global instance
secret_manager = SecretManager()
