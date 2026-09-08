import asyncio
import logging
import os

import httpx

from pipecatapp.net_utils import format_url
from pipecatapp.network_scanner import scan_network_for_llms
from pipecatapp.secret_manager import secret_manager


async def discover_services(service_names: list, consul_http_addr: str, delay=10):
    """Periodically queries Consul to find a healthy instance of a service, with failover support.

    Args:
        service_names (list): A list of service names to discover, in order of preference.
        consul_http_addr (str): The HTTP address of the Consul agent.
        delay (int): The number of seconds to wait between retries.

    Returns:
        The base URL (e.g., "http://1.2.3.4:5678/v1") of the first discovered service.
    """
    logging.info(f"Attempting to discover services: {service_names}")

    # Check for override URLs first
    override_map = {
        "llama-api-main": os.getenv("LLAMA_API_URL_OVERRIDE"),
        "llamacpp-rpc-api": os.getenv("LLAMA_API_URL_OVERRIDE"),
        "router-api": os.getenv("LLAMA_API_URL_OVERRIDE"),
        "tool-server-api": os.getenv("TOOL_SERVER_URL_OVERRIDE"),
        "memory-service": os.getenv("MEMORY_SERVICE_URL_OVERRIDE"),
    }

    for service_name in service_names:
        override_url = override_map.get(service_name)
        # also support generic naming OVERRIDE logic
        if not override_url:
            env_key = f"{service_name.replace('-', '_').upper()}_URL_OVERRIDE"
            override_url = os.getenv(env_key)

        if override_url:
            logging.info(f"Using override URL for {service_name}: {override_url}")
            return override_url

    token = secret_manager.get_secret("CONSUL_HTTP_TOKEN")
    headers = {"X-Consul-Token": token} if token else {}

    async with httpx.AsyncClient() as client:
        while True:
            for service_name in service_names:
                try:
                    logging.debug(f"Checking status of service: {service_name}")
                    url = f"{consul_http_addr}/v1/health/service/{service_name}?passing"
                    response = await client.get(url, headers=headers, timeout=5)

                    if response.status_code != 200:
                        logging.warning(f"Consul returned {response.status_code} for {service_name} at {url}: {response.text}")
                        continue

                    services = response.json()
                    if services:
                        address, port = services[0]['Service']['Address'], services[0]['Service']['Port']
                        base_url = format_url("http", address, port, "v1")
                        logging.info(f"Successfully discovered {service_name} at {base_url}")
                        return base_url
                    else:
                        logging.info(f"Consul returned empty list for {service_name} at {url}")
                except Exception as e:
                    logging.error(f"Unexpected error discovering {service_name}: {e}")

            # Fallback to local network scan before sleeping
            fallback_url = await scan_network_for_llms()
            if fallback_url:
                logging.info(f"Using fallback network LLM at {fallback_url}")
                return fallback_url

            logging.info(f"No healthy services found in list {service_names}, retrying in {delay} seconds...")
            await asyncio.sleep(delay)


async def discover_main_llm_service(consul_http_addr=None, delay=10):
    if consul_http_addr is None:
        consul_host = os.getenv("CONSUL_HOST", os.getenv("CLUSTER_IP", "127.0.0.1"))
        consul_port = os.getenv("CONSUL_PORT", "8500")
        consul_http_addr = f"http://{consul_host}:{consul_port}"
    """Discovers the main LLM service used for vision-related tasks.

    This is a specialized wrapper around `discover_service` for the primary
    vision-capable LLM.

    Args:
        consul_http_addr (str): The HTTP address of the Consul agent.
        delay (int): The number of seconds to wait between retries.

    Returns:
        The base URL of the discovered LLM service.
    """
    # This is useful for vision-specific LLM calls (used by TwinService._call_vision_llm)
    service_name = os.getenv("MAIN_API_SERVICE_NAME")
    if not service_name:
         logging.warning("MAIN_API_SERVICE_NAME not set, defaulting to llama-api-main")
         service_name = "llama-api-main"

    token = secret_manager.get_secret("CONSUL_HTTP_TOKEN")
    headers = {"X-Consul-Token": token} if token else {}

    async with httpx.AsyncClient() as client:
        while True:
            try:
                url = f"{consul_http_addr}/v1/health/service/{service_name}?passing"
                response = await client.get(url, headers=headers, timeout=5)

                if response.status_code != 200:
                    logging.warning(f"Consul returned {response.status_code} for {service_name} at {url}: {response.text}")
                else:
                    services = response.json()
                    if services:
                        address, port = services[0]['Service']['Address'], services[0]['Service']['Port']
                        base_url = format_url("http", address, port, "v1")
                        logging.info(f"Discovered main LLM service at {base_url}")
                        return base_url
                    else:
                        logging.info(f"Consul returned empty list for {service_name} at {url}")
            except Exception as e:
                logging.warning(f"Could not find service {service_name}: {e}")

            # Fallback to local network scan
            fallback_url = await scan_network_for_llms()
            if fallback_url:
                logging.info(f"Using fallback network LLM at {fallback_url}")
                return fallback_url

            await asyncio.sleep(delay)
