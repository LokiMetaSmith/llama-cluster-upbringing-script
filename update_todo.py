import re

with open('TODO.md', 'r') as f:
    todo_content = f.read()

# Add missing tests to Technical Debt
new_tech_debt = """- [ ] **Address Missing Tool Tests:** Create unit tests for tools lacking coverage (e.g., `atproto_tool.py`, `autoloop_tool.py`, `container_registry_tool.py`, `context_upload_tool.py`, `cq_tool.py`, `dependency_scanner_tool.py`, `document_tool.py`, `dynamic_skill_tool.py`, `openclaw_tool.py`, `save_skill_tool.py`, `scale_compute_tool.py`, `scheduler_tool.py`, `search_skills_tool.py`, `skill_builder_tool.py`, `spec_loader_tool.py`, `submit_solution_tool.py`, `update_litellm_tool.py`, `vr_tool.py`, `wol_tool.py`).
- [ ] **Fix Lazy Tests:** Address tests that contain only `pass` without actual assertions (e.g., `tests/unit/test_pipecat_app_unit.py`, `tests/test_event_bus.py`, `tests/verify_dlq.py`).
- [ ] **Decouple Subprocess Usage:** Refactor hardcoded `subprocess.run` calls in tools (like `heretic_tool.py`, `project_mapper_tool.py`, `autoresearch_tool.py`, `experiment_tool.py`, `ansible_tool.py`, etc.) to use a unified execution abstraction, enabling easier mocking and sandboxing.
"""
tech_debt_pattern = r'(## Technical Debt & Lazy Code\n)'
todo_content = re.sub(tech_debt_pattern, r'\1\n' + new_tech_debt, todo_content)

# Add security issues to Security Audit
new_sec_audit = """- [ ] **Audit Hardcoded Local IP Addresses:** Remove hardcoded `127.0.0.1` and `localhost` fallbacks in critical services (e.g., `app.py`, `workflow_nodes`, `web_server.py`) and replace them with robust environment-based configuration matching the cluster overlay architecture.
- [ ] **Audit Subprocess Injection Risks:** Thoroughly review all tools using `subprocess.run` (like `heretic_tool.py`, `experiment_tool.py`, `autoloop_tool.py`) for potential command injection vulnerabilities when interpolating user or LLM input into shell commands without `shlex.quote`.
- [ ] **Review Autoloop Tool Security:** The `autoloop_tool.py` executes code locally without a sandbox. Sandbox this tool or restrict its usage strictly to trusted, airgapped environments.
"""
sec_audit_pattern = r'(## Security Audit\n)'
todo_content = re.sub(sec_audit_pattern, r'\1\n' + new_sec_audit, todo_content)

# Add performance issues to Performance & I/O Optimization
new_perf = """- [ ] **Optimize Fast Path Security Redaction:** Evaluate the regex patterns in `security.py` (e.g., `_FAST_PATH_PATTERN`) under heavy concurrent load and consider implementing a Rust-based extension or a streaming redaction approach for large contexts.
"""
perf_pattern = r'(## Performance & I/O Optimization\n)'
todo_content = re.sub(perf_pattern, r'\1\n' + new_perf, todo_content)

# Add architecture enhancements
new_arch = """- [ ] **Decouple Task Supervisor from Subprocesses:** Consider replacing raw subprocess polling in `TaskSupervisor` with Nomad API task submission or a distributed task queue (like Celery) for better cluster-native fault tolerance.
"""
arch_pattern = r'(## Architecture 2\.0 \(Post 1\.0 Release\)\n.*?\n.*?\n)'
todo_content = re.sub(arch_pattern, r'\1\n' + new_arch, todo_content)


with open('TODO.md', 'w') as f:
    f.write(todo_content)
