import aiohttp
from aiohttp import web
import os
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Map dummy keys to real keys
# In a real setup, this would be backed by a secure store (e.g., Vault, SOPS)
# For this proxy, we'll use environment variables for demonstration.
# DUMMY_KEY -> REAL_KEY mapping
KEY_MAPPINGS = {
    "FAKE_OPENAI_KEY": os.environ.get("REAL_OPENAI_KEY", "real_sk_placeholder"),
    "FAKE_ANTHROPIC_KEY": os.environ.get("REAL_ANTHROPIC_KEY", "real_ant_placeholder")
}

async def handle_proxy(request):
    """
    Intersects the request, swaps the DUMMY key for the REAL key if present,
    and forwards it to the intended destination.
    """
    # The client must send a custom header to indicate the real destination if acting as a pure reverse proxy,
    # OR we act as a true forward HTTP proxy.

    # Let's act as a forward proxy if full URL is passed, or use a custom header for destination.
    # A standard HTTP proxy receives the full URL in the path line.

    # In aiohttp web, request.url gives the full URL requested.
    target_url = str(request.url)

    # If the proxy is hit directly without full path, fallback to a header.
    if request.path == "/" and "X-Target-Url" in request.headers:
         target_url = request.headers["X-Target-Url"]

    if target_url.endswith("/proxy") or target_url.endswith("/"):
        return web.Response(text="OneCLI Python Proxy Running")

    logger.info(f"Proxying request to {target_url}")

    # Extract headers
    headers = dict(request.headers)

    # Strip hop-by-hop headers
    hop_by_hop = ['Host', 'Connection', 'Keep-Alive', 'Proxy-Authenticate',
                  'Proxy-Authorization', 'Te', 'Trailers', 'Transfer-Encoding', 'Upgrade']
    for h in hop_by_hop:
        headers.pop(h, None)
        headers.pop(h.lower(), None)

    # Swap keys
    auth_header = headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        dummy_key = auth_header.replace('Bearer ', '').strip()
        if dummy_key in KEY_MAPPINGS:
            logger.info("Swapping dummy key for real key")
            headers['Authorization'] = f"Bearer {KEY_MAPPINGS[dummy_key]}"
        else:
            logger.info("No key mapping found, passing through")
    elif 'X-API-Key' in headers:
         dummy_key = headers['X-API-Key']
         if dummy_key in KEY_MAPPINGS:
             logger.info("Swapping dummy key for real key")
             headers['X-API-Key'] = KEY_MAPPINGS[dummy_key]

    # Read body
    body = await request.read()

    # Forward the request
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=body,
                allow_redirects=False
            ) as resp:
                response_body = await resp.read()

                resp_headers = dict(resp.headers)
                # Strip headers that may conflict after aiohttp decompresses the payload
                for h in ['Content-Encoding', 'Content-Length', 'Transfer-Encoding', 'Connection']:
                    resp_headers.pop(h, None)
                    resp_headers.pop(h.lower(), None)

                proxy_resp = web.Response(
                    body=response_body,
                    status=resp.status,
                    headers=resp_headers
                )
                return proxy_resp
        except Exception as e:
            logger.error(f"Error proxying request: {e}")
            return web.Response(text=f"Proxy error: {str(e)}", status=502)

async def create_app():
    app = web.Application()
    # Catch all routes
    app.router.add_route('*', '/{tail:.*}', handle_proxy)
    return app

if __name__ == '__main__':
    web.run_app(create_app(), host='127.0.0.1', port=10255)
