import ipaddress

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
