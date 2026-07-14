import os
import sys
import json
import yaml
import httpx
import logging
import subprocess
from typing import Dict, List, Any, Optional

logger = logging.getLogger("AnsibleTriage")
logging.basicConfig(level=logging.INFO)

class AnsibleTriageHandler:
    def __init__(self, context_dir: str, task_id: str):
        self.context_dir = os.path.realpath(context_dir)
        self.task_id = task_id
        self.repo_root = os.path.realpath(os.getcwd())

        # Load inputs
        self.failure_log = self._read_file_raw(os.path.join(self.context_dir, "failure_log.txt"))
        self.failing_task = self._read_file_raw(os.path.join(self.context_dir, "failing_task.yml"))
        self.host_vars = self._read_json_file(os.path.join(self.context_dir, "host_vars.json"))
        self.rendered_artifacts = self._load_rendered_artifacts()

    def _read_file_raw(self, filepath: str) -> str:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _read_json_file(self, filepath: str) -> Dict[str, Any]:
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to parse JSON file {filepath}: {e}")
        return {}

    def _load_rendered_artifacts(self) -> Dict[str, str]:
        artifacts = {}
        artifacts_dir = os.path.join(self.context_dir, "rendered_artifacts")
        if os.path.exists(artifacts_dir) and os.path.isdir(artifacts_dir):
            for root, _, files in os.walk(artifacts_dir):
                for f in files:
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, artifacts_dir)
                    content = self._read_file_raw(full_path)
                    artifacts[rel_path] = content
        return artifacts

    def _get_llm_config(self) -> Dict[str, str]:
        """Resolves LLM endpoints prioritizing self-hosted backends."""
        # Prioritize local endpoints
        local_keys = ["LOCAL_LLM_URL", "LLAMA_API_BASE_URL", "LLM_API_BASE_URL", "OPENAI_API_BASE_URL"]
        for key in local_keys:
            val = os.getenv(key)
            if val:
                logger.info(f"Using local LLM backend from {key}: {val}")
                return {
                    "base_url": val.rstrip("/"),
                    "api_key": os.getenv("LOCAL_LLM_API_KEY", "dummy-local-key"),
                    "model": os.getenv("LOCAL_LLM_MODEL", "llama3")
                }

        # Fallback to OpenRouter
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            logger.info("Using OpenRouter fallback.")
            return {
                "base_url": "https://openrouter.ai/api/v1",
                "api_key": openrouter_key,
                "model": "openrouter/auto"
            }

        # Fallback to OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            logger.info("Using OpenAI fallback.")
            return {
                "base_url": "https://api.openai.com/v1",
                "api_key": openai_key,
                "model": "gpt-4o"
            }

        return {}

    async def _call_llm(self, prompt: str) -> str:
        config = self._get_llm_config()
        if not config:
            msg = "Error: No LLM configuration found (both local and cloud endpoints are undefined)."
            logger.error(msg)
            raise RuntimeError(msg)

        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": config["model"],
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Jules, an expert systems administrator and automation engineer. "
                        "Your job is to analyze Ansible failure logs, identify root causes, "
                        "and patch upstream configurations/variables or Jinja2 templates. "
                        "You must respond in strict JSON format."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{config['base_url']}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=httpx.Timeout(60.0)
                )
                response.raise_for_status()
                res_json = response.json()
                return res_json["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"LLM API call timed out or failed: {e}")
            raise TimeoutError(f"LLM API call failed or timed out: {e}")

    def _build_triage_prompt(self) -> str:
        artifacts_str = "\n".join([f"--- File: {path} ---\n{content}" for path, content in self.rendered_artifacts.items()])
        prompt = f"""
Analyze the following Ansible task deployment failure and propose upstream fixes.

### FAILURE LOG (stderr/output)
{self.failure_log}

### FAILING ANSIBLE TASK (.yml)
{self.failing_task}

### HOST VARIABLES (host_vars.json)
{json.dumps(self.host_vars, indent=2)}

### RENDERED CONFIGURATIONS / TEMPLATES (rendered_artifacts/)
{artifacts_str}

Please diagnose the failure. Identify the root cause (e.g. unquoted key parsing error in Nomad HCL/Jinja template, trailing slash mismatch, syntax issue, variable typo).
Then, map the fix back to the upstream source files in this repository.

You must respond in strict JSON format with the following keys:
1. "root_cause": Detailed explanation of why the deployment failed.
2. "changes": A list of file edits to apply to the repository. Each edit must contain:
   - "filepath": The path of the file to modify relative to the repository root (e.g. "ansible/roles/nginx/templates/app.conf.j2" or "group_vars/all.yaml").
   - "search_content": The original block of code to find in that file.
   - "replace_content": The modified block of code to replace it with.
3. "target_port": The port number of the service to test (integer, or null if none).
4. "health_check_command": A command to run locally inside the sandbox to verify the service is healthy (e.g. "curl -f http://localhost:8080" or "nc -z localhost 6157", or null if none).

Make sure search_content matches exactly what is in the repository. Avoid hardcoded/transient fixes; use robust variables/Jinja syntax where applicable.

Response JSON format:
{{
  "root_cause": "...",
  "changes": [
    {{
      "filepath": "...",
      "search_content": "...",
      "replace_content": "..."
    }}
  ],
  "target_port": 8080,
  "health_check_command": "..."
}}
"""
        return prompt

    def _apply_changes(self, changes: List[Dict[str, str]]) -> List[str]:
        applied = []
        for change in changes:
            filepath = change.get("filepath")
            search_content = change.get("search_content")
            replace_content = change.get("replace_content")

            if not filepath or search_content is None or replace_content is None:
                continue

            full_path = os.path.realpath(os.path.join(self.repo_root, filepath))
            # Security: Path traversal check
            if os.path.commonpath([full_path, self.repo_root]) != self.repo_root:
                logger.warning(f"Blocked path traversal attempt: {filepath}")
                continue

            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if search_content in content:
                    new_content = content.replace(search_content, replace_content)
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    logger.info(f"Successfully applied fix to {filepath}")
                    applied.append(filepath)
                else:
                    # Try a fuzzy search/replace or replace entire file if search_content is empty
                    if not search_content.strip():
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(replace_content)
                        logger.info(f"Overwrote entire file {filepath} (search_content was empty)")
                        applied.append(filepath)
                    else:
                        logger.warning(f"Could not find exact search_content in {filepath}")
            else:
                # File doesn't exist, try creating it with the replace_content
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(replace_content)
                logger.info(f"Created new file {filepath} with proposed fix content")
                applied.append(filepath)

        return applied

    def _run_linters(self, files: List[str]) -> str:
        results = []
        for filepath in files:
            full_path = os.path.join(self.repo_root, filepath)
            if not os.path.exists(full_path):
                continue

            # Run yamllint for YAML files
            if filepath.endswith((".yaml", ".yml")):
                logger.info(f"Running yamllint on {filepath}...")
                proc = subprocess.run(["yamllint", "-c", ".yamllint", filepath], cwd=self.repo_root, capture_output=True, text=True)
                if proc.returncode != 0:
                    results.append(f"yamllint failure on {filepath}:\n{proc.stdout or proc.stderr}")

            # Run ansible-lint if available
            if filepath.endswith((".yaml", ".yml")) and "roles/" in filepath:
                logger.info(f"Running ansible-lint on {filepath}...")
                # Check if ansible-lint is installed
                lint_check = subprocess.run(["which", "ansible-lint"], capture_output=True)
                if lint_check.returncode == 0:
                    proc = subprocess.run(["ansible-lint", filepath], cwd=self.repo_root, capture_output=True, text=True)
                    if proc.returncode != 0:
                        results.append(f"ansible-lint failure on {filepath}:\n{proc.stdout or proc.stderr}")

        return "\n".join(results) if results else "LINTING PASSED"

    def _run_sandbox_checks(self, target_port: Optional[int], health_check_command: Optional[str]) -> str:
        # 1. Run Ansible Playbook --syntax-check
        logger.info("Running Ansible playbook syntax check...")
        proc_syntax = subprocess.run(
            ["ansible-playbook", "-i", "local_inventory.ini", "playbook.yaml", "--syntax-check"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        if proc_syntax.returncode != 0:
            return f"FAILED syntax check:\n{proc_syntax.stdout or proc_syntax.stderr}"

        # 2. Run Ansible Playbook Dry-Run
        logger.info("Running localized Ansible playbook execution (dry-run)...")
        proc_dry = subprocess.run(
            ["ansible-playbook", "-i", "local_inventory.ini", "playbook.yaml", "--check"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        if proc_dry.returncode != 0:
            return f"FAILED playbook dry-run execution:\n{proc_dry.stdout or proc_dry.stderr}"

        # 3. Dynamic service verification/health check
        if health_check_command:
            logger.info(f"Running dynamic health check: {health_check_command}")
            proc_health = subprocess.run(health_check_command, shell=True, capture_output=True, text=True)
            if proc_health.returncode != 0:
                return f"FAILED health check command execution:\n{proc_health.stdout or proc_health.stderr}"

        if target_port:
            logger.info(f"Checking target port responsiveness: {target_port}")
            import socket
            try:
                with socket.create_connection(("localhost", target_port), timeout=5):
                    logger.info(f"Port {target_port} is open and responding.")
            except Exception as e:
                return f"FAILED port check on {target_port}: {e}"

        return "SUCCESS"

    def _resolve_opengist(self) -> Optional[str]:
        """Resolves Opengist dynamically via Consul first, then falls back to localhost."""
        # Try Consul DNS first
        try:
            import socket
            socket.gethostbyname("opengist-http.service.consul")
            logger.info("Discovered Opengist via Consul DNS.")
            return f"http://opengist-http.service.consul:{os.getenv('OPENGIST_PORT', '6157')}"
        except Exception:
            pass

        # Try Consul HTTP Catalog API
        try:
            consul_addr = os.getenv("CONSUL_HTTP_ADDR", "http://10.0.0.1:8500")
            resp = httpx.get(f"{consul_addr}/v1/catalog/service/opengist-http", timeout=2.0)
            if resp.status_code == 200:
                services = resp.json()
                if services:
                    svc = services[0]
                    addr = svc.get("ServiceAddress") or "localhost"
                    port = svc.get("ServicePort", 6157)
                    logger.info(f"Discovered Opengist via Consul catalog API: {addr}:{port}")
                    return f"http://{addr}:{port}"
        except Exception:
            pass

        # Fallback to localhost
        try:
            resp = httpx.get("http://localhost:6157", timeout=1.0)
            if resp.status_code == 200 or resp.status_code == 404: # Opengist might respond with 404 if route doesn't exist but server is up
                logger.info("Opengist is reachable at http://localhost:6157")
                return "http://localhost:6157"
        except Exception:
            pass

        return None

    def _git_operations(self, branch_name: str, pull_request_summary: str) -> Dict[str, Any]:
        """Performs Git branch creation, commit, and Opengist push / local bundle creation."""
        results = {}

        # 1. Create and switch to the branch (use -B to force reset if it already exists)
        subprocess.run(["git", "checkout", "-B", branch_name], cwd=self.repo_root)

        # 2. Stage changes
        subprocess.run(["git", "add", "-A"], cwd=self.repo_root)

        # 3. Commit changes
        subprocess.run(["git", "commit", "-m", f"fix(ansible): automatic triage and patch for task {self.task_id}"], cwd=self.repo_root)

        # 4. Save PR description locally
        pr_summary_path = os.path.join(self.repo_root, "pull_request_summary.md")
        with open(pr_summary_path, "w", encoding="utf-8") as f:
            f.write(pull_request_summary)
        results["pr_summary_path"] = pr_summary_path

        # 5. Try pushing to Opengist
        opengist_url = self._resolve_opengist()
        pushed_to_remote = False
        if opengist_url:
            try:
                # Add Opengist as git remote
                remote_git_url = f"{opengist_url}/git/agent/ansible-fixes.git"
                subprocess.run(["git", "remote", "remove", "opengist"], cwd=self.repo_root, capture_output=True)
                subprocess.run(["git", "remote", "add", "opengist", remote_git_url], cwd=self.repo_root)

                # Push branch
                proc_push = subprocess.run(["git", "push", "opengist", branch_name, "--force"], cwd=self.repo_root, capture_output=True, text=True)
                if proc_push.returncode == 0:
                    logger.info(f"Successfully pushed branch to Opengist: {remote_git_url}")
                    results["pushed_url"] = f"{opengist_url}/agent/ansible-fixes/branch/{branch_name}"
                    pushed_to_remote = True
                else:
                    logger.warning(f"Git push to Opengist failed: {proc_push.stderr}")
            except Exception as e:
                logger.warning(f"Error while pushing to Opengist: {e}")

        # 6. If push failed/skipped, create local bundle
        if not pushed_to_remote:
            bundle_name = f"fix-agent-ansible-{self.task_id}.bundle"
            bundle_path = os.path.join(self.repo_root, bundle_name)
            logger.info(f"Creating local Git bundle as robust offline fallback at: {bundle_path}")
            proc_bundle = subprocess.run(["git", "bundle", "create", bundle_path, branch_name], cwd=self.repo_root, capture_output=True, text=True)
            if proc_bundle.returncode == 0:
                results["bundle_path"] = bundle_path
            else:
                logger.error(f"Failed to create Git bundle: {proc_bundle.stderr}")

        return results

    async def run_triage(self) -> Dict[str, Any]:
        """The main entry point for the Ansible Exception Handler and Git PR loop."""
        logger.info(f"Initializing Triage for Task ID: {self.task_id}")

        # 1. Ask LLM for root cause and upstream patches
        prompt = self._build_triage_prompt()
        llm_response = await self._call_llm(prompt)

        try:
            # Strip markdown json codeblocks if any
            if "```json" in llm_response:
                llm_response = llm_response.split("```json")[1].split("```")[0].strip()
            elif "```" in llm_response:
                llm_response = llm_response.split("```")[1].split("```")[0].strip()

            data = json.loads(llm_response)
        except Exception as e:
            logger.error(f"Failed to parse LLM JSON response: {llm_response}. Error: {e}")
            raise ValueError(f"LLM did not return a valid JSON object. Response: {llm_response}")

        root_cause = data.get("root_cause", "Unknown root cause.")
        changes = data.get("changes", [])
        target_port = data.get("target_port")
        health_check_command = data.get("health_check_command")

        # 2. Reverse-Compilation: Apply the upstream edits
        applied_files = self._apply_changes(changes)

        # 3. Validation & Linting
        lint_log = self._run_linters(applied_files)
        verification_status = self._run_sandbox_checks(target_port, health_check_command)

        # 4. Generate structured markdown PR body
        verification_log = f"""
## ⚙️ Iterative Linting Results
{lint_log}

## 🔍 Local Verification Log
Status: {verification_status}
"""

        pr_markdown = f"""# 🤖 Automated Fix: Ansible Exception Handler for Task {self.task_id}

## 📝 Problem Statement
Ansible playbook execution failed during task execution for task ID: `{self.task_id}`.

## 🔍 Root Cause Analysis
{root_cause}

## 🛠️ Changes Applied
{chr(10).join([f"* Modified `{f}` according to LLM synthesis." for f in applied_files])}

## 🧪 Verification Log
{verification_log}
"""

        # 5. Git Automation (Branch isolation & Opengist/local-bundle upload)
        branch_name = f"fix/agent-ansible-{self.task_id}"
        git_results = self._git_operations(branch_name, pr_markdown)

        return {
            "status": "SUCCESS" if verification_status == "SUCCESS" else "PARTIAL_SUCCESS",
            "root_cause": root_cause,
            "applied_files": applied_files,
            "verification_status": verification_status,
            "pr_markdown": pr_markdown,
            **git_results
        }
