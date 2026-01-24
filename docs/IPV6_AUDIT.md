# IPv6 Audit Report

## Executive Summary

The codebase has significant dependencies on IPv4-specific constructs that will prevent operation in an IPv6-only environment and may cause issues in dual-stack environments. The primary blockers are hardcoded URL construction (`http://{ip}:{port}`), explicit binding to `0.0.0.0` or `127.0.0.1`, and infrastructure scripts that assume single-value IPv4 returns from networking commands.

## Detailed Findings

### 1. URL Construction (Critical)

**Issue:** Python code frequently constructs URLs using `f"http://{address}:{port}"`.
**Impact:** If `address` is an IPv6 literal (e.g., `2001:db8::1`), the resulting URL is invalid (`http://2001:db8::1:8000`). IPv6 literals in URLs must be enclosed in brackets (`http://[2001:db8::1]:8000`).
**Locations:**

- `pipecatapp/web_server.py`: Service discovery logic constructs URLs for UI links.
- `pipecatapp/app.py`: `consul_http_addr` and LLM service discovery.
- `pipecatapp/tools/`: Multiple tools (Council, Prompt Improver, Open Workers) construct URLs for internal API calls.
- `pipecatapp/workflow/nodes/`: LLM nodes construct base URLs.

**Recommendation:** Implement a `format_url(host, port, protocol)` utility that detects IPv6 literals and adds brackets. Refactor all occurrences to use this utility.

### 2. Network Binding (High)

**Issue:** Services explicitly bind to `0.0.0.0` or `127.0.0.1`.
**Impact:** `0.0.0.0` is IPv4-only. While some OS configurations allow IPv4-mapped IPv6, it is not guaranteed. `127.0.0.1` is strictly IPv4 loopback.
**Locations:**

- `pipecatapp/web_server.py`: `uvicorn.run(..., host="0.0.0.0")`
- `pipecatapp/tool_server.py`, `archivist_service.py`: Similar `uvicorn` bindings.
- `bootstrap.sh`: `nc -z localhost 4646`.
- `ansible/inventory.yaml` & `local_inventory.ini`: Use `192.168.1.225` and `127.0.0.1`.

**Recommendation:**

- Change listen addresses to `::` (IPv6 "any") which supports dual-stack on most modern systems, or make it configurable.
- Update default configuration values to `localhost` (which can resolve to `::1`) but ensure downstream code handles `::1`.

### 3. Infrastructure & Provisioning (Medium)

**Issue:** Scripts and Ansible roles assume IPv4 formats or commands.
**Locations:**

- `bootstrap.sh`: `HOST_IP=$(hostname -I | awk '{print $1}')`. If the first IP is IPv6, it is passed raw to containers/scripts, breaking those that expect IPv4 or don't handle brackets.
- `initial-setup/update_inventory.sh`: Curls `127.0.0.1:8500`. It filters Consul nodes. If Consul reports IPv6 addresses, the script writes them to `inventory.yaml` without modification. Ansible handles IPv6 in inventory, but if these IPs are used later for URL construction, they will fail.
- `provisioning.py`: `check_port_open` uses `socket.AF_INET` (IPv4 only). It will fail to detect open ports if services bind only to IPv6.

**Recommendation:**

- Update `check_port_open` to try `AF_INET6` if `AF_INET` fails or use `getaddrinfo`.
- Update `bootstrap.sh` to handle multiple IPs and potentially prefer IPv6 or format it correctly.

### 4. Frontend (Medium)

**Issue:** JavaScript naive string replacement.
**Location:** `pipecatapp/static/cluster.html`
**Code:** `url = url.replace('localhost', window.location.hostname).replace('127.0.0.1', window.location.hostname);`
**Impact:** If `window.location.hostname` is an IPv6 address (e.g. `[::1]`), this replacement is fine. However, if the original `url` was constructed server-side with a raw IPv6 address (bug #1), the frontend receives an invalid URL before this code even runs. If the server sends `localhost`, and the browser is on IPv6, `window.location.hostname` might be `[::1]`. This replacement works, but relies on the browser providing brackets.

**Recommendation:** Ensure server-side URL generation is robust first. Frontend logic is likely passable but should be tested with IPv6 literals.

### 5. Ansible & Nomad (Low)

**Issue:** `address_mode = "host"` and `network_mode = "host"`.
**Impact:** Generally good for IPv6 as it uses the host stack. However, Nomad health checks often default to IPv4 if not explicitly told otherwise or if the service registers an IPv6 address without brackets in the check definition.

## Conclusion

The toolchain is currently **not compatible** with an IPv6-only environment and has significant bugs for dual-stack environments where services might resolve to IPv6 addresses. The most pervasive issue is the lack of bracket notation `[]` when constructing URLs with IP addresses.
