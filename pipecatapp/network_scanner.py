import socket
import asyncio
import logging
import httpx

logger = logging.getLogger(__name__)

async def check_llm_service(ip: str, port: int, timeout: float = 0.5) -> str | None:
    """Checks if a specific IP:Port hosts a reachable LLM service."""
    url = f"http://{ip}:{port}"
    try:
        # Check port first quickly
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()

        # If port is open, verify it's an LLM
        async with httpx.AsyncClient(timeout=timeout) as client:
            if port == 11434:
                # Ollama specific check
                try:
                    resp = await client.get(f"{url}/api/tags")
                    if resp.status_code == 200:
                        return f"{url}/v1" # Use OpenAI compatible endpoint for Ollama
                except Exception:
                    pass
            else:
                # Llama.cpp or other OpenAI compatible
                try:
                    resp = await client.get(f"{url}/v1/models")
                    if resp.status_code == 200 and "github" not in resp.headers.get("Server", "").lower() and "github" not in resp.headers.get("x-github-request-id", "").lower():
                         return f"{url}/v1"
                except Exception:
                    pass
                try:
                    resp = await client.get(f"{url}/health")
                    # Make sure it's not a generic 200 from a web server
                    if resp.status_code == 200 and "github" not in resp.headers.get("Server", "").lower() and "github" not in resp.headers.get("x-github-request-id", "").lower():
                        return f"{url}/v1"
                except Exception:
                    pass
    except Exception:
        pass

    return None

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

async def scan_network_for_llms(timeout: float = 0.5) -> str | None:
    """
    Scans localhost and the local subnet for instances of Ollama or Llama.cpp.
    Returns the first found base_url (e.g., http://192.168.1.100:11434/v1).
    """
    logger.info("Starting local network scan for LLM services...")
    local_ip = get_local_ip()
    ports = [11434, 8080] # Ollama, Llama.cpp/OpenAI

    # 1. Check localhost and local IP first (fast path)
    priority_tasks = []
    for ip in ['127.0.0.1', local_ip]:
        for port in ports:
            priority_tasks.append(check_llm_service(ip, port, timeout))

    priority_results = await asyncio.gather(*priority_tasks)
    for result in priority_results:
        if result:
            logger.info(f"Discovered local LLM at {result}")
            return result

    # 2. Check the rest of the /24 subnet
    if local_ip == '127.0.0.1':
        return None

    parts = local_ip.split('.')
    base_ip = f"{parts[0]}.{parts[1]}.{parts[2]}."

    logger.debug(f"Scanning subnet {base_ip}0/24")

    # Batch the tasks to avoid too many open sockets at once
    ips_to_check = [f"{base_ip}{i}" for i in range(1, 255) if f"{base_ip}{i}" != local_ip]

    batch_size = 50
    for i in range(0, len(ips_to_check), batch_size):
        batch_ips = ips_to_check[i:i+batch_size]
        tasks = []
        for ip in batch_ips:
            for port in ports:
                tasks.append(check_llm_service(ip, port, timeout))

        results = await asyncio.gather(*tasks)
        for result in results:
            if result:
                logger.info(f"Discovered network LLM at {result}")
                return result

    logger.info("No local network LLMs discovered.")
    return None
