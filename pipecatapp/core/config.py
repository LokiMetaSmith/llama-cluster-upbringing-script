import json
import logging
import os

import consul.aio

from pipecatapp.secret_manager import secret_manager


async def load_config_from_consul(consul_host, consul_port):
    """Loads application and model configuration from the Consul KV store.

    Args:
        consul_host (str): The hostname or IP address of the Consul agent.
        consul_port (int): The port of the Consul agent.

    Returns:
        A dictionary containing the loaded configuration.
    """
    logging.info("Loading configuration from Consul KV store...")
    config = {}
    token = secret_manager.get_secret("CONSUL_HTTP_TOKEN")
    c = consul.aio.Consul(host=consul_host, port=consul_port, token=token, scheme='http', verify=False)
    try:
        index, data = await c.kv.get('config/app/settings')
        if data:
            app_settings = json.loads(data['Value'].decode('utf-8'))
            config.update(app_settings)
            logging.info("Successfully loaded application settings from Consul.")
        else:
            logging.error("Could not find 'config/app/settings' in Consul KV.")

        index, data = await c.kv.get('config/models/tts_voices')
        if data:
            config['tts_voices'] = json.loads(data['Value'].decode('utf-8'))
            logging.info("Successfully loaded TTS voices from Consul.")
        else:
            logging.warning("Could not find 'config/models/tts_voices' in Consul KV.")

    except Exception as e:
        logging.error(f"Error loading configuration from Consul: {e}")

    if "TOOL_EXECUTION_MODE" in os.environ:
        config["tool_execution_mode"] = os.getenv("TOOL_EXECUTION_MODE")
    if "TOOL_SERVER_URL" in os.environ:
        config["tool_server_url"] = os.getenv("TOOL_SERVER_URL")

    return config
