import os
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any, Optional

class Settings(BaseSettings):
    # MQTT
    mqtt_broker_host: str = "127.0.0.1"
    mqtt_broker_port: int = 1883
    mqtt_topic_success: str = "tagreader/auth/success"
    mqtt_topic_failure: str = "tagreader/auth/failure"

    # HTTP Server
    tap_orchestrator_port: int = 8011
    tap_orchestrator_secret: str = "change_me_secret"

    # Authentik
    authentik_api_url: str = "http://127.0.0.1:9000"
    authentik_client_id: Optional[str] = None
    authentik_client_secret: Optional[str] = None
    authentik_token: Optional[str] = None

    # Cluster Resource Map Path
    cluster_resource_map_file: str = "config.yaml"

    # APIs
    nomad_api_url: str = "http://127.0.0.1:4646"
    vault_api_url: str = "http://127.0.0.1:8200"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cluster_resource_map(self) -> Dict[str, Any]:
        if os.path.exists(self.cluster_resource_map_file):
            try:
                with open(self.cluster_resource_map_file, "r") as f:
                    config = yaml.safe_load(f)
                    return config.get("CLUSTER_RESOURCE_MAP", {})
            except Exception as e:
                import logging
                logging.error(f"Failed to load cluster resource map: {e}")
        return {}

settings = Settings()
