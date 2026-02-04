# Security Audit Log

## Initial Audit: Hardcoded Secrets

**Date:** February 2026
**Auditor:** Jules (AI Agent)
**Scope:** `pipecatapp/` directory, including frontend (`static/js`), backend (`*.py`), workflows (`workflows/`), and tools (`tools/`).

### Methodology

Searched for common secret patterns and keywords using `grep`:

- **Regex Patterns:**
  - `sk-[a-zA-Z0-9-]{20,}` (OpenAI)
  - `gh[pousr]_[a-zA-Z0-9]{36,}` (GitHub)
  - `xox[baprs]-[a-zA-Z0-9-]{10,}` (Slack)
  - `AIza[0-9A-Za-z\-_]{35}` (Google)
- **Keywords:** `api_key`, `secret`, `token`, `password`

### Findings

1. **Frontend (`pipecatapp/static/js/*.js`):**
    - No hardcoded secrets found.

2. **Backend (`pipecatapp/**/*.py`):**
    - All API keys and tokens appear to be loaded via `os.getenv` or passed as arguments.
    - Examples:
        - `pipecatapp/tool_server.py`: `API_KEY = os.getenv("TOOL_SERVER_API_KEY")`
        - `pipecatapp/tools/remote_tool_proxy.py`: `self.api_key = api_key or os.getenv("TOOL_SERVER_API_KEY")`

3. **Tests (`pipecatapp/tests/`):**
    - Found dummy secrets (e.g., `"sk-abcdef..."`) in `test_uilogger_redaction.py` and `test_security.py`. These are intentional for testing the redaction logic and are safe.
    - `test_rag_tool.py` writes a temporary secret file for testing file exclusion; safe.

4. **Workflows (`workflows/`):**
    - `default_agent_loop.yaml` is currently empty (`nodes: []`).

### Conclusion

No active hardcoded secrets were found in the source code. The codebase follows the practice of using environment variables for sensitive credentials.

### Next Steps

- Continue with the Security Audit Plan in `TODO.md`.
- Ensure that new workflows or tools introduced in the future adhere to the same standard.
