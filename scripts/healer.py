import os
import sys
import json
import time
import argparse
import asyncio
import re
import subprocess
import requests
from typing import List, Optional, Dict, Any, Tuple

try:
    from sudo_env import load_sudo_env
    load_sudo_env()
except ImportError:
    pass

# Determine repository root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# --- Configuration ---
NOMAD_ADDR = os.environ.get("NOMAD_ADDR", "http://localhost:4646")
CONSUL_HTTP_ADDR = os.environ.get("CONSUL_HTTP_ADDR", "http://localhost:8500")
CONSUL_HTTP_TOKEN = os.environ.get("CONSUL_HTTP_TOKEN", "")


def get_consul_token() -> str:
    """Retrieve Consul authentication token from env or disk."""
    if "CONSUL_HTTP_TOKEN" in os.environ and os.environ["CONSUL_HTTP_TOKEN"].strip():
        return os.environ["CONSUL_HTTP_TOKEN"].strip()
    token_file = "/etc/consul.d/management_token"
    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                return f.read().strip()
        except Exception:
            pass
    return ""


def get_nomad_tls_kwargs(nomad_url: str) -> Dict[str, Any]:
    """Generates TLS arguments for Nomad API requests ensuring strict certificate trust."""
    kwargs: Dict[str, Any] = {}
    if nomad_url.startswith("https"):
        cacert = os.environ.get("NOMAD_CACERT") or "/etc/nomad.d/tls/ca.pem"
        if os.path.exists(cacert):
            kwargs["verify"] = cacert
        else:
            kwargs["verify"] = True  # Strict system CA trust validation, NEVER verify=False

        client_cert = os.environ.get("NOMAD_CLIENT_CERT") or "/etc/nomad.d/tls/cli.cert.pem"
        client_key = os.environ.get("NOMAD_CLIENT_KEY") or "/etc/nomad.d/tls/cli.key.pem"
        if os.path.exists(client_cert) and os.path.exists(client_key):
            kwargs["cert"] = (client_cert, client_key)
    return kwargs


def extract_repo_source_from_traceback(stderr: str, repo_root: str = REPO_ROOT) -> Optional[str]:
    """Extracts target file path from Python traceback if it points to a file within repo_root."""
    if not stderr:
        return None
    matches = re.findall(r'File\s+"([^"]+)"', stderr)
    for match in reversed(matches):
        norm_match = os.path.normpath(match)
        if os.path.isabs(norm_match):
            rel = os.path.relpath(norm_match, repo_root)
            if not rel.startswith("..") and os.path.isfile(os.path.join(repo_root, rel)):
                # Exclude virtual environments and hidden caches
                if not any(part in rel for part in (".venv", "venv", "site-packages", "__pycache__")):
                    return os.path.join(repo_root, rel)
        else:
            cand = os.path.join(repo_root, norm_match)
            if os.path.isfile(cand) and not any(part in cand for part in (".venv", "venv", "site-packages", "__pycache__")):
                return cand
    return None


def record_adaptation_case(job_id: str, alloc_id: str, diagnostic_data: Dict[str, Any], repo_root: str = REPO_ROOT):
    """Bridge runtime failure into prompt_engineering/generated_evaluators."""
    try:
        reflection_dir = os.path.join(repo_root, "reflection")
        if reflection_dir not in sys.path:
            sys.path.insert(0, reflection_dir)
        import adaptation_manager
        test_case_yaml = adaptation_manager.generate_test_case(diagnostic_data)
        out_dir = os.path.join(repo_root, "prompt_engineering", "generated_evaluators")
        os.makedirs(out_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        case_file = os.path.join(out_dir, f"failure_{job_id}_{timestamp}.yaml")
        with open(case_file, "w") as f:
            f.write(test_case_yaml)
        print(f"[Adaptation] Generated evolution test case at {case_file}")
    except Exception as e:
        print(f"[Adaptation] Failed to generate adaptation test case: {e}")


class NomadWatcher:
    """Interacts with Nomad to find failed allocations and retrieve logs."""

    def __init__(self, nomad_url: str = NOMAD_ADDR):
        self.nomad_url = nomad_url
        self.tls_kwargs = get_nomad_tls_kwargs(self.nomad_url)
        self.processed_alloc_ids: set = set()

    def get_failed_allocs(self) -> List[Dict]:
        """Fetch allocations with status 'failed', 'lost', or failed task states."""
        try:
            resp = requests.get(f"{self.nomad_url}/v1/allocations", timeout=10, **self.tls_kwargs)
            resp.raise_for_status()
            allocs = resp.json()

            failed = []
            for alloc in allocs:
                client_status = alloc.get('ClientStatus', '').lower()
                has_failed_task = False
                task_states = alloc.get('TaskStates') or {}
                for tname, tstate in task_states.items():
                    if tstate.get('Failed', False):
                        has_failed_task = True
                        break

                if client_status in ('failed', 'lost') or has_failed_task:
                    failed.append(alloc)
            return failed
        except Exception as e:
            print(f"[Watcher] Error polling Nomad: {e}")
            return []

    def get_logs(self, alloc_id: str, task_name: str, log_type: str = "stderr") -> str:
        """Fetch logs for a specific task in an allocation using API with CLI fallback."""
        try:
            params = {'task': task_name, 'type': log_type, 'plain': 'true'}
            resp = requests.get(
                f"{self.nomad_url}/v1/client/fs/logs/{alloc_id}",
                params=params,
                timeout=10,
                **self.tls_kwargs
            )
            if resp.status_code == 200 and resp.text.strip():
                return resp.text
        except Exception as e:
            print(f"[Watcher] HTTP log fetch failed ({e}), trying CLI fallback...")

        try:
            cmd = ["nomad", "alloc", "logs", f"-{log_type}", "-tail", "-n", "200", alloc_id, task_name]
            env = os.environ.copy()
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15, env=env)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout
        except Exception as e:
            print(f"[Watcher] CLI log fetch failed: {e}")

        return ""

    def restart_job(self, job_id: str) -> bool:
        """Restarts a Nomad job after healing or failure remediation."""
        print(f"[Watcher] Attempting to restart job '{job_id}'...")
        try:
            cmd = ["nomad", "job", "restart", "-yes", job_id]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode == 0:
                print(f"[Watcher] Successfully restarted job '{job_id}'.")
                return True
        except Exception as e:
            print(f"[Watcher] CLI restart failed: {e}")

        try:
            resp = requests.put(
                f"{self.nomad_url}/v1/job/{job_id}/scale",
                json={"Count": 1},
                timeout=10,
                **self.tls_kwargs
            )
            return resp.status_code in (200, 201)
        except Exception as e:
            print(f"[Watcher] API restart failed: {e}")
            return False


class HealerAgent:
    """Interacts with the internal LLM cluster to fix code."""

    def __init__(self, consul_addr: str = CONSUL_HTTP_ADDR, token: Optional[str] = None):
        self.consul_addr = consul_addr
        self.token = token.strip() if token else get_consul_token()

    async def _resolve_service(self, service_name: str) -> Optional[str]:
        """Find the base URL for a service via Consul."""
        headers = {"X-Consul-Token": self.token} if self.token else {}
        def _fetch():
            try:
                resp = requests.get(f"{self.consul_addr}/v1/health/service/{service_name}?passing", headers=headers, timeout=5)
                if resp.status_code == 200:
                    services = resp.json()
                    if services:
                        svc = services[0]['Service']
                        addr = svc.get('Address') or '127.0.0.1'
                        port = svc.get('Port')
                        return f"http://{addr}:{port}/v1"
            except Exception as e:
                print(f"[Agent] Discovery failed for {service_name}: {e}")
            return None
        return await asyncio.to_thread(_fetch)

    async def chat(self, messages: List[Dict], model_service: str = "rpc-coding", mock: bool = False) -> str:
        """Send a chat completion request to the cluster LLM."""
        if mock:
            return self._mock_chat(messages)

        base_url = await self._resolve_service(model_service)
        if not base_url:
            for fallback_name in ["llama-api-main", "vllm", "opencode"]:
                base_url = await self._resolve_service(fallback_name)
                if base_url:
                    break

        if not base_url:
            base_url = os.environ.get("LLAMA_API_URL", "http://127.0.0.1:8081/v1")

        payload = {
            "model": model_service,
            "messages": messages,
            "temperature": 0.2
        }

        def _post():
            resp = requests.post(f"{base_url}/chat/completions", json=payload, timeout=120)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

        try:
            return await asyncio.to_thread(_post)
        except Exception as e:
            return f"Error talking to LLM: {e}"

    def _mock_chat(self, messages: List[Dict]) -> str:
        """Return canned responses for testing."""
        last_msg = messages[-1]['content']
        if "STANDALONE Python test file" in last_msg:
            return """
```python
import pytest
from pipecatapp.chaos_module import risky_math

def test_reproduction():
    val = risky_math(0)
```
"""
        elif "rewrite the Source Code" in last_msg:
            return '''
```python
def risky_math(x):
    """A risky function."""
    if x == 0:
        return 0.0  # Safe fallback
    return 100 / x
```
'''
        return "Error: No mock response found."

    async def generate_reproduction_test(self, log_content: str, target_file_content: str, mock: bool = False) -> str:
        """Ask the LLM to write a reproduction test case."""
        prompt = f"""
You are an expert QA Engineer. I have a crash log and the relevant source code.
Your task is to write a STANDALONE Python test file (using `pytest`) that reproduces this specific crash.

CRASH LOG:
```
{log_content}
```

SOURCE CODE:
```python
{target_file_content}
```

INSTRUCTIONS:
1. The test should import the module/function and call it with arguments that trigger the crash.
2. The test MUST fail if the bug exists.
3. Output ONLY the Python code block for the test file. No markdown formatting outside the code block.
4. Name the test function `test_reproduction`.
"""
        messages = [{"role": "user", "content": prompt}]
        response = await self.chat(messages, mock=mock)
        return self._extract_code(response)

    async def fix_code(self, source_code: str, test_code: str, error_output: str, mock: bool = False) -> str:
        """Ask the LLM to fix the source code."""
        prompt = f"""
You are a Senior Software Engineer. We have a bug in our code.
I will provide the Source Code, the Failing Test, and the Test Output.
Your task is to rewrite the Source Code to fix the bug while preserving functionality.

FAILING TEST:
```python
{test_code}
```

TEST OUTPUT:
```
{error_output}
```

CURRENT SOURCE CODE:
```python
{source_code}
```

INSTRUCTIONS:
1. Analyze why the code failed.
2. Return the COMPLETE, corrected Source Code.
3. Output ONLY the Python code block.
"""
        messages = [{"role": "user", "content": prompt}]
        response = await self.chat(messages, mock=mock)
        return self._extract_code(response)

    def _extract_code(self, response: str) -> str:
        """Clean up markdown code blocks."""
        if "```python" in response:
            return response.split("```python")[1].split("```")[0].strip()
        elif "```" in response:
            return response.split("```")[1].split("```")[0].strip()
        return response.strip()


# --- Remediation & Watch Loops ---

async def heal_allocation(alloc: Dict[str, Any], watcher: NomadWatcher, agent: HealerAgent,
                          repo_root: str = REPO_ROOT, mock: bool = False, auto_restart: bool = True) -> bool:
    """Investigate and remediate a single failed allocation."""
    alloc_id = alloc.get("ID", "unknown")
    job_id = alloc.get("JobID", "unknown")
    task_states = alloc.get("TaskStates") or {}

    print(f"\n[Healer] [*] Investigating failed allocation {alloc_id[:8]} for job '{job_id}'...")

    for task_name, task_state in task_states.items():
        is_failed = task_state.get("Failed", False) or alloc.get("ClientStatus") == "failed"
        if not is_failed:
            continue

        stderr_log = watcher.get_logs(alloc_id, task_name, log_type="stderr")
        diagnostic_data = {
            "job_id": job_id,
            "alloc_id": alloc_id,
            "task_name": task_name,
            "client_status": alloc.get("ClientStatus"),
            "events": task_state.get("Events", []),
            "logs": {"stderr": stderr_log}
        }

        # Save diagnostic artifact
        log_dir = os.path.join(repo_root, "logs", "healer")
        os.makedirs(log_dir, exist_ok=True)
        dump_path = os.path.join(log_dir, f"failure_{job_id}_{alloc_id[:8]}.json")
        with open(dump_path, "w") as f:
            json.dump(diagnostic_data, f, indent=2)
        print(f"[Healer] Saved failure diagnostics to {dump_path}")

        # Record test case for prompt engineering / evolution archive
        record_adaptation_case(job_id, alloc_id, diagnostic_data, repo_root=repo_root)

        # Check if traceback points to an internal repository source file
        target_file = extract_repo_source_from_traceback(stderr_log, repo_root=repo_root)
        if target_file and os.path.exists(target_file):
            print(f"[Healer] [+] Located offending source file: {target_file}")
            with open(target_file, "r") as f:
                source_content = f.read()

            print("[Healer] Phase 1: Generating reproduction test...")
            test_code = await agent.generate_reproduction_test(stderr_log, source_content, mock=mock)
            test_filename = os.path.join(repo_root, "tests", f"repro_{int(time.time())}.py")
            with open(test_filename, "w") as f:
                f.write(test_code)
            print(f"[Healer] Written repro test to {test_filename}")

            env = os.environ.copy()
            env["PYTHONPATH"] = repo_root
            repro_res = subprocess.run(["pytest", test_filename], capture_output=True, text=True, env=env)

            if repro_res.returncode != 0:
                print("[Healer] Phase 2: Bug confirmed reproducible in pytest. Synthesizing fix...")
                error_output = repro_res.stdout + repro_res.stderr
                fixed_code = await agent.fix_code(source_content, test_code, error_output, mock=mock)

                backup_path = target_file + ".bak"
                with open(backup_path, "w") as f:
                    f.write(source_content)
                with open(target_file, "w") as f:
                    f.write(fixed_code)

                verify_res = subprocess.run(["pytest", test_filename], capture_output=True, text=True, env=env)
                if verify_res.returncode == 0:
                    print(f"[Healer] [SUCCESS] Autonomous patch verified! Code repaired: {target_file}")
                    if auto_restart:
                        watcher.restart_job(job_id)
                    return True
                else:
                    print("[Healer] [FAILURE] Proposed patch failed verification. Reverting...")
                    with open(target_file, "w") as f:
                        f.write(source_content)
            else:
                print("[Healer] Reproduction test did not reproduce failure. Moving to cluster recovery.")

        # Infrastructure / Service recovery
        if auto_restart:
            watcher.restart_job(job_id)

    return True


async def watch_allocations(watcher: NomadWatcher, agent: HealerAgent, repo_root: str = REPO_ROOT,
                            interval: int = 15, run_once: bool = False, mock: bool = False,
                            auto_restart: bool = True):
    """Continuously poll Nomad allocations and heal failures in real time."""
    print(f"\n[Lazarus Healer] [*] Starting Nomad Failure Watcher (Poll Interval: {interval}s)...")
    print(f"  Nomad URL:  {watcher.nomad_url}")
    print(f"  Consul URL: {agent.consul_addr}")
    print(f"  Repo Root:  {repo_root}")

    while True:
        failed_allocs = watcher.get_failed_allocs()
        new_failures = [a for a in failed_allocs if a.get("ID") not in watcher.processed_alloc_ids]

        if new_failures:
            print(f"[Lazarus Healer] Detected {len(new_failures)} new failed allocation(s).")
            for alloc in new_failures:
                alloc_id = alloc.get("ID")
                watcher.processed_alloc_ids.add(alloc_id)
                await heal_allocation(
                    alloc=alloc,
                    watcher=watcher,
                    agent=agent,
                    repo_root=repo_root,
                    mock=mock,
                    auto_restart=auto_restart
                )
        else:
            print(f"[Lazarus Healer] Cluster allocations healthy ({len(watcher.processed_alloc_ids)} historical failures tracked).")

        if run_once:
            break

        await asyncio.sleep(interval)


async def run_local_mode(args):
    """Run interactive local reproduction and repair on a single file."""
    agent = HealerAgent()
    with open(args.log, 'r') as f:
        log_content = f.read()

    with open(args.target, 'r') as f:
        source_content = f.read()

    print(f"[*] Analyzing failure in {args.target}...")
    test_code = await agent.generate_reproduction_test(log_content, source_content, mock=args.mock)
    test_filename = f"tests/repro_{int(time.time())}.py"
    with open(test_filename, 'w') as f:
        f.write(test_code)
    print(f"    -> Written to {test_filename}")

    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    result = subprocess.run(["pytest", test_filename], capture_output=True, text=True, env=env)

    if result.returncode == 0:
        print("[!] The generated test PASSED (it failed to reproduce the bug). Aborting.")
        return

    print("    -> Test FAILED as expected. Proceeding to fix.")
    error_output = result.stdout + result.stderr
    fixed_code = await agent.fix_code(source_content, test_code, error_output, mock=args.mock)

    backup_path = args.target + ".bak"
    with open(backup_path, 'w') as f:
        f.write(source_content)

    with open(args.target, 'w') as f:
        f.write(fixed_code)
    print("    -> Patch applied.")

    result_fix = subprocess.run(["pytest", test_filename], capture_output=True, text=True, env=env)
    if result_fix.returncode == 0:
        print("[SUCCESS] The fix works! Test passed.")
    else:
        print("[FAILURE] The fix did not work. Reverting...")
        with open(args.target, 'w') as f:
            f.write(source_content)
        print("    -> Reverted to original.")


def main():
    parser = argparse.ArgumentParser(description='Lazarus: Autonomous Cluster Self-Healing Agent')
    parser.add_argument('--watch', action='store_true', help='Watch Nomad for allocation failures')
    parser.add_argument('--once', action='store_true', help='Run a single audit pass across allocations and exit')
    parser.add_argument('--interval', type=int, default=15, help='Polling interval in seconds (default: 15)')
    parser.add_argument('--no-restart', action='store_true', help='Disable automatic Nomad job restart')
    parser.add_argument('--local-mode', action='store_true', help='Run in local dev mode')
    parser.add_argument('--log', help='Path to crash log (local mode)')
    parser.add_argument('--target', help='Path to target source file (local mode)')
    parser.add_argument('--mock', action='store_true', help='Use mock LLM responses for dry-run/testing')

    args = parser.parse_args()

    if args.local_mode:
        if not args.log or not args.target:
            print("Error: --local-mode requires --log and --target")
            sys.exit(1)
        asyncio.run(run_local_mode(args))
    elif args.watch or args.once:
        watcher = NomadWatcher()
        agent = HealerAgent()
        asyncio.run(watch_allocations(
            watcher=watcher,
            agent=agent,
            repo_root=REPO_ROOT,
            interval=args.interval,
            run_once=args.once,
            mock=args.mock,
            auto_restart=not args.no_restart
        ))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
