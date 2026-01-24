## 2026-01-24 - Rate Limiting Behind Proxies
**Vulnerability:** The `RateLimiter` relied on `request.client.host` which, without `ProxyHeadersMiddleware`, reflects the proxy IP rather than the client IP. This causes all users to share the same rate limit bucket when deployed behind a proxy.
**Learning:** In containerized/Nomad environments, applications are almost always behind a load balancer or ingress. Defaulting to direct connection assumptions creates DoS risks.
**Prevention:** Always configure `ProxyHeadersMiddleware` in FastAPI/Uvicorn applications with a mechanism to specify trusted proxies (e.g., `TRUSTED_PROXIES` env var).
