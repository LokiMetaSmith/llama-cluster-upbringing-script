## 2024-05-22 - Path Traversal Vulnerability
**Vulnerability:** `os.path.join` in Python allows absolute paths in the second argument to override the first argument (base directory), enabling path traversal if user input is not sanitized or validated.
**Learning:** Checking for `..` is insufficient to prevent path traversal when absolute paths can be supplied. Always validate the resolved absolute path.
**Prevention:** Use `os.path.abspath` to resolve the path and check if it starts with the expected base directory using `startswith`.
