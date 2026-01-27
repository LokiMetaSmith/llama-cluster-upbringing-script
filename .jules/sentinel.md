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
