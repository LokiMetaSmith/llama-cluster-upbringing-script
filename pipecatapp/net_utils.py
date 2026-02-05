import ipaddress
import urllib.parse
import socket
import asyncio
import logging

def ensure_ipv6_brackets(host: str) -> str:
    """
    Checks if the host is an IPv6 literal and wraps it in brackets if needed.
    """
    if not host:
        return ""

    # Remove existing brackets if present to normalize
    clean_host = host.strip("[]")

    try:
        ip = ipaddress.ip_address(clean_host)
        if isinstance(ip, ipaddress.IPv6Address):
            return f"[{clean_host}]"
    except ValueError:
        # Not an IP address (likely a hostname), so return as is
        # Note: If input was already "[...]" but invalid IP, we return original host
        # But here we stripped brackets. If it was "[hostname]", it's weird but let's assume valid hostname don't need brackets.
        pass

    return host

def format_url(scheme: str, host: str, port: int | str | None = None, path: str = "") -> str:
    """
    Constructs a URL ensuring IPv6 hosts are bracketed.
    """
    formatted_host = ensure_ipv6_brackets(host)

    url = f"{scheme}://{formatted_host}"

    if port:
        url += f":{port}"

    if path:
        if not path.startswith("/"):
            url += "/"
        url += path

    return url

async def validate_url(url: str) -> None:
    """Validates that the URL is safe to visit (SSRF protection).

    Args:
        url (str): The URL to validate.

    Raises:
        ValueError: If the URL is unsafe or invalid.
    """
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        raise ValueError("Invalid URL format.")

    if parsed.scheme not in ('http', 'https'):
        raise ValueError(f"Blocked: Scheme '{parsed.scheme}' is not allowed. Only http/https.")

    hostname = parsed.hostname
    if not hostname:
         raise ValueError("Blocked: Invalid hostname.")

    # Block localhost immediately
    if hostname.lower() in ('localhost', '127.0.0.1', '::1', '0.0.0.0'):
         raise ValueError(f"Blocked: Access to {hostname} is forbidden.")

    # Resolve IP to check for private ranges
    try:
        loop = asyncio.get_running_loop()
        # Use run_in_executor to avoid blocking the loop
        addr_info = await loop.run_in_executor(None, socket.getaddrinfo, hostname, None)
        # addr_info is list of (family, type, proto, canonname, sockaddr)
        # sockaddr is (address, port) for IPv4/IPv6
        ips = set(res[4][0] for res in addr_info)
    except socket.gaierror:
         # Fail closed if DNS fails
         raise ValueError(f"Blocked: Could not resolve hostname {hostname}.")

    for ip_str in ips:
         try:
            ip = ipaddress.ip_address(ip_str)
         except ValueError:
             continue

         # Check for private, loopback, link-local (169.254.x.x), unspecified (0.0.0.0)
         if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_unspecified:
            raise ValueError(f"Blocked: Host {hostname} resolves to restricted IP {ip_str}.")
