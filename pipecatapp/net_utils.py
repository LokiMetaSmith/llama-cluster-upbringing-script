import ipaddress
import urllib.parse
import socket
import asyncio
import logging
import os
import fnmatch

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

async def _validate_url_logic(url: str) -> tuple[str, str | None]:
    """
    Internal logic for URL validation.
    Returns (url, resolved_ip) tuple. resolved_ip is None if skipped via allowlist.
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

    # Check against SSRF_ALLOWLIST env var
    # Format: comma-separated list of domains/IPs/CIDRs (e.g., "*.internal,192.168.1.5,10.0.0.0/8")
    allowlist_env = os.getenv("SSRF_ALLOWLIST", "")
    allowlist = [entry.strip() for entry in allowlist_env.split(",") if entry.strip()]

    is_allowed = False
    for entry in allowlist:
        if fnmatch.fnmatch(hostname, entry):
            is_allowed = True
            break
        # Check if entry is CIDR and hostname is IP
        try:
            if ipaddress.ip_address(hostname) in ipaddress.ip_network(entry, strict=False):
                is_allowed = True
                break
        except ValueError:
            pass

    if is_allowed:
        return url, None

    # Block localhost immediately unless allowed
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

         # Check allowlist for resolved IP as well
         ip_allowed = False
         for entry in allowlist:
             try:
                 if ip in ipaddress.ip_network(entry, strict=False):
                     ip_allowed = True
                     break
             except ValueError:
                 pass

         if ip_allowed:
             continue

         # Check for private, loopback, link-local (169.254.x.x), unspecified (0.0.0.0)
         if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_unspecified:
            raise ValueError(f"Blocked: Host {hostname} resolves to restricted IP {ip_str}.")

    # Return original URL and one of the safe IPs
    # We prefer IPv4 for compatibility if available, otherwise just take any
    safe_ip = None
    for ip in ips:
        if "." in ip: # simple check for IPv4
            safe_ip = ip
            break
    if not safe_ip and ips:
        safe_ip = list(ips)[0]

    return url, safe_ip

async def validate_url(url: str) -> str:
    """Validates that the URL is safe to visit (SSRF protection).

    Args:
        url (str): The URL to validate.

    Returns:
        str: The original URL if it passes validation.

    Raises:
        ValueError: If the URL is unsafe or invalid.
    """
    url, _ = await _validate_url_logic(url)
    return url

async def resolve_and_validate_url(url: str) -> tuple[str, str | None]:
    """Validates the URL and returns the resolved IP to prevent DNS rebinding.

    Args:
        url (str): The URL to validate.

    Returns:
        tuple[str, str | None]: (original_url, resolved_safe_ip).
                                resolved_safe_ip may be None if allowlisted.
    """
    return await _validate_url_logic(url)

def get_safe_url_and_headers(url: str, safe_ip: str | None) -> tuple[str, dict]:
    """
    Returns a URL that is safe against DNS rebinding (for HTTP), and necessary headers.

    If the scheme is HTTP and a safe IP is provided, it rewrites the URL to use the IP
    and returns a Host header.
    For HTTPS, it relies on SSL verification to prevent DNS rebinding, so it returns
    the original URL.
    """
    if not safe_ip:
        return url, {}

    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return url, {}

    # Only rewrite HTTP. HTTPS is protected by SSL certificate validation.
    if parsed.scheme != "http":
        return url, {}

    # Construct safe URL with IP
    # Handle IPv6 brackets if needed
    safe_host = f"[{safe_ip}]" if ":" in safe_ip else safe_ip

    if parsed.port:
        safe_netloc = f"{safe_host}:{parsed.port}"
    else:
        safe_netloc = safe_host

    # Reconstruct URL
    # usage of _replace is robust for namedtuple
    safe_url = parsed._replace(netloc=safe_netloc).geturl()

    return safe_url, {"Host": parsed.hostname}
