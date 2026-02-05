## 2024-05-22 - Path Traversal Vulnerability
**Vulnerability:** `os.path.join` in Python allows absolute paths in the second argument to override the first argument (base directory), enabling path traversal if user input is not sanitized or validated.
**Learning:** Checking for `..` is insufficient to prevent path traversal when absolute paths can be supplied. Always validate the resolved absolute path.
**Prevention:** Use `os.path.abspath` to resolve the path and check if it starts with the expected base directory using `startswith`.

## 2026-01-08 - Fix Path Traversal in Ansible Tool
**Vulnerability:** Path traversal in `Ansible_Tool.run_playbook` allowed arbitrary file access via `..` sequences in the `playbook` argument.
**Learning:** Simply joining paths with `os.path.join` is insufficient for security when user input is involved.
**Prevention:** Use `os.path.abspath` and `os.path.commonpath` (or strictly check the prefix of the resolved path) to ensure the target file resides within the intended directory.

## 2026-06-15 - Robust Path Traversal Check in Web Server
**Vulnerability:** The `startswith` check for path traversal in `pipecatapp/web_server.py` was insufficient because it didn't account for partial directory name matches (e.g., `/app/workflows_secret` starts with `/app/workflows`).
**Learning:** `startswith` treats paths as simple strings. To ensure a file is strictly inside a directory, we must respect directory boundaries.
**Prevention:** Use `os.path.commonpath([base_dir, target_path]) == base_dir` to mathematically prove the target path is a child of the base directory.

## 2026-10-27 - Unrestricted Git Tool Access
**Vulnerability:** `Git_Tool` allowed executing git commands in arbitrary directories via `working_dir` argument, lacking any root directory restriction.
**Learning:** Tools that execute shell commands or file operations must be explicitly restricted to a safe root directory, even if they seem harmless like "git status".
**Prevention:** Enforce a `root_dir` in tool initialization and validate all path arguments using `os.path.commonpath` against this root.

## 2026-10-28 - SSRF in WebBrowserTool
**Vulnerability:** `WebBrowserTool` allowed navigating to arbitrary URLs, including internal services (localhost, 127.0.0.1) and Cloud Metadata services (169.254.169.254), enabling SSRF.
**Learning:** Tools that fetch URLs must treat user input as untrusted and strictly validate the destination, including resolving DNS to check for private IPs.
**Prevention:** Implemented `_validate_url` to check scheme, block local hostnames, and resolve IPs to reject private/link-local ranges using `ipaddress`.

## 2026-10-29 - Path Traversal in Project Mapper
**Vulnerability:** `ProjectMapperTool` allowed arbitrary directory scanning via path traversal in `sub_path` argument, as it only used `os.path.normpath` without `os.path.commonpath`.
**Learning:** `os.path.normpath` resolves `..` but does not enforce that the resulting path is within a base directory. Always verify the resolved path is a child of the intended root.
**Prevention:** Resolve both root and target paths to absolute paths using `os.path.abspath`, then use `os.path.commonpath([root, target]) == root` to strictly enforce containment.

## 2026-01-30 - Excessive Scope in RAG Tool
**Vulnerability:** `RAG_Tool` was initialized with `base_dir="/"`, granting it permission to scan and index the entire container filesystem, including sensitive system directories.
**Learning:** Default configurations for tools should obey the Principle of Least Privilege. Never default to the filesystem root (`/`) when a specific application directory (`/opt/pipecatapp`) is sufficient.
**Prevention:** Explicitly restrict file scanning tools to the application's root directory during initialization in the factory method.

## 2026-02-01 - Cross-Site WebSocket Hijacking
**Vulnerability:** Default configuration allowed all origins (*), enabling CSWSH.
**Learning:** "Secure by default" is critical. Convenience defaults (* for dev) often end up in production, leaving apps vulnerable.
**Prevention:** Default to restrictive policies (Same-Origin). Require explicit configuration for permissive modes. Use strict Origin vs Host validation for WebSockets.

## 2026-02-03 - Path Traversal in ExperimentTool Artifacts
**Vulnerability:** `ExperimentTool` allowed path traversal when writing solution artifacts from worker agents. This could allow a compromised worker (or LLM hallucination) to overwrite arbitrary files on the host.
**Learning:** Tools that accept file paths from LLM outputs must strictly validate that the resolved path stays within the intended sandbox/directory. `os.path.join` is not enough if the input can be absolute.
**Prevention:** Always use a validation helper (like `_validate_path`) that resolves absolute paths, checks `os.path.isabs`, and uses `os.path.commonpath` to ensure containment.

## 2026-02-04 - Unsanitized Active Workflow State
**Vulnerability:** The `/api/workflows/active` endpoint returned the raw state of active workflows, potentially leaking secrets (like API keys) stored in inputs or outputs.
**Learning:** Even internal monitoring endpoints must sanitize data before exposing it to the UI, as the UI is a client-side component. "Active" state is just as sensitive as "Historical" state.
**Prevention:** Apply `sanitize_data` to all endpoints returning workflow context or state, not just historical runs. Review all API endpoints for raw data exposure.

## 2026-02-05 - SSRF in Internal Chat Endpoint
**Vulnerability:** `web_server.py` allowed `response_url` to point to internal services (localhost, cloud metadata) enabling SSRF.
**Learning:** Validating `HttpUrl` in Pydantic only checks syntax, not safety (IP ranges).
**Prevention:** Use a dedicated `validate_url` helper that resolves DNS and checks against private IP ranges for all user-supplied URLs.
