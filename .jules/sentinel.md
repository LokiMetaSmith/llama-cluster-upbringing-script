## 2024-05-22 - Path Traversal Vulnerability
**Vulnerability:** `os.path.join` in Python allows absolute paths in the second argument to override the first argument (base directory), enabling path traversal if user input is not sanitized or validated.
**Learning:** Checking for `..` is insufficient to prevent path traversal when absolute paths can be supplied. Always validate the resolved absolute path.
**Prevention:** Use `os.path.abspath` to resolve the path and check if it starts with the expected base directory using `startswith`.

## 2026-01-08 - Fix Path Traversal in Ansible Tool
**Vulnerability:** Path traversal in `Ansible_Tool.run_playbook` allowed arbitrary file access via `..` sequences in the `playbook` argument.
**Learning:** Simply joining paths with `os.path.join` is insufficient for security when user input is involved.
**Prevention:** Use `os.path.abspath` and `os.path.commonpath` (or strictly check the prefix of the resolved path) to ensure the target file resides within the intended directory.
