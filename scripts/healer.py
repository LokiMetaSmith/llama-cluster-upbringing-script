import os
import sys
import json
import time
import argparse
import asyncio
import httpx
import subprocess
import requests
from typing import List, Optional, Dict

# --- Configuration ---
NOMAD_ADDR = os.environ.get("NOMAD_ADDR", "http://localhost:4646")
CONSUL_HTTP_ADDR = os.environ.get("CONSUL_HTTP_ADDR", "http://localhost:8500")
CONSUL_HTTP_TOKEN = os.environ.get("CONSUL_HTTP_TOKEN", "")

class NomadWatcher:
    """Interacts with Nomad to find failed allocations and retrieve logs."""

    def __init__(self, nomad_url: str = NOMAD_ADDR):
        self.nomad_url = nomad_url

    def get_failed_allocs(self) -> List[Dict]:
        """Fetch allocations with status 'failed'."""
        try:
            # We filter client-side for simplicity in this prototype
            resp = requests.get(f"{self.nomad_url}/v1/allocations", timeout=5)
            resp.raise_for_status()
            allocs = resp.json()

            failed = []
            for alloc in allocs:
                if alloc['ClientStatus'] == 'failed':
                    failed.append(alloc)
            return failed
        except Exception as e:
            print(f"[Watcher] Error polling Nomad: {e}")
            return []

    def get_logs(self, alloc_id: str, task_name: str, log_type: str = "stderr") -> str:
        """Fetch logs for a specific task in an allocation."""
        try:
            # /v1/client/fs/logs/:alloc_id?task=:task_name&type=:type
            params = {'task': task_name, 'type': log_type, 'plain': 'true'}
            resp = requests.get(f"{self.nomad_url}/v1/client/fs/logs/{alloc_id}", params=params, timeout=10)
            if resp.status_code == 200:
                return resp.text
            else:
                print(f"[Watcher] Failed to get logs: {resp.status_code} {resp.text}")
                return ""
        except Exception as e:
            print(f"[Watcher] Error fetching logs: {e}")
            return ""

class HealerAgent:
    """Interacts with the internal LLM cluster to fix code."""

    def __init__(self, consul_addr: str = CONSUL_HTTP_ADDR, token: str = CONSUL_HTTP_TOKEN):
        self.consul_addr = consul_addr
        self.token = token.strip() if token else None

    async def _resolve_service(self, service_name: str) -> Optional[str]:
        """Find the base URL for a service via Consul."""
        headers = {"X-Consul-Token": self.token} if self.token else {}
        async with httpx.AsyncClient(headers=headers) as client:
            try:
                resp = await client.get(f"{self.consul_addr}/v1/health/service/{service_name}?passing")
                resp.raise_for_status()
                services = resp.json()
                if services:
                    svc = services[0]['Service']
                    return f"http://{svc['Address']}:{svc['Port']}/v1"
            except Exception as e:
                print(f"[Agent] Discovery failed for {service_name}: {e}")
        return None

    async def chat(self, messages: List[Dict], model_service: str = "rpc-coding", mock: bool = False) -> str:
        """Send a chat completion request."""
        if mock:
            return self._mock_chat(messages)

        base_url = await self._resolve_service(model_service)
        if not base_url:
            # Fallback for dev environment if consul isn't reachable but we have a direct address
            # Or return error
            print(f"[Agent] Could not resolve {model_service}. Using localhost fallback?")
            # return "Error: Service unavailable"
            # Hardcoded fallback for testing if Consul fails in sandbox
            base_url = "http://localhost:8081/v1"

        payload = {
            "model": model_service,
            "messages": messages,
            "temperature": 0.2
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{base_url}/chat/completions", json=payload, timeout=120)
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
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
    # To demonstrate the bug (crash), we call the function directly.
    # We expect this to execute successfully (no crash) if the code is robust.
    # Currently, it triggers ZeroDivisionError, causing the test to FAIL/ERROR.
    val = risky_math(0)
    # If we want to assert specific behavior (like returning 0), we could add:
    # assert val == 0.0
```
"""
        elif "rewrite the Source Code" in last_msg:
            # We must use triple quotes for the multi-line string, but the inner python code also has triple quotes.
            # We need to escape them or use a different quote style for the outer string.
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

# --- Main Logic ---

async def run_local_mode(args):
    agent = HealerAgent()

    # 1. Read Inputs
    with open(args.log, 'r') as f:
        log_content = f.read()

    with open(args.target, 'r') as f:
        source_content = f.read()

    print(f"[*] Analyzing failure in {args.target}...")

    # 2. Generate Reproduction
    print("[*] Phase 1: generating reproduction test...")
    test_code = await agent.generate_reproduction_test(log_content, source_content, mock=args.mock)

    test_filename = f"tests/repro_{int(time.time())}.py"
    with open(test_filename, 'w') as f:
        f.write(test_code)
    print(f"    -> Written to {test_filename}")

    # 3. Verify Failure
    print("[*] Phase 2: Verifying failure...")
    # Make sure we can import the target by adding CWD to PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    result = subprocess.run(["pytest", test_filename], capture_output=True, text=True, env=env)

    # NOTE: In reproduction, we EXPECT failure.
    # However, if the test is "assert X", a crash is also a failure.
    # If the test is "with pytest.raises(Error)", then a PASS means we successfully reproduced the expected crash logic.
    # But usually, a reproduction script is written to CRASH if the bug is present (i.e., return code != 0).
    # OR it asserts the correct behavior and FAILS because the behavior is wrong.

    # My mock generates `risky_math(0)` which crashes. So result.returncode will be != 0.

    if result.returncode == 0:
        print("[!] The generated test PASSED (it failed to reproduce the bug). Aborting.")
        # print(result.stdout)
        return
    else:
        print("    -> Test FAILED as expected. Proceeding to fix.")
        error_output = result.stdout + result.stderr

    # 4. Generate Fix
    print("[*] Phase 3: Generating fix...")
    fixed_code = await agent.fix_code(source_content, test_code, error_output, mock=args.mock)

    # Backup
    backup_path = args.target + ".bak"
    with open(backup_path, 'w') as f:
        f.write(source_content)

    # Apply
    with open(args.target, 'w') as f:
        f.write(fixed_code)
    print("    -> Patch applied.")

    # 5. Verify Fix
    print("[*] Phase 4: Verifying fix...")
    # Now we expect the test to PASS (because we fixed the code to handle the edge case)
    # But wait, if the test is `risky_math(0)` and we changed it to return 0.0,
    # the test script itself might need to update its assertion?
    # The mock test I wrote does `risky_math(0)` naked. If it returns 0.0, it won't crash, so pytest returns 0 (PASS).
    result_fix = subprocess.run(["pytest", test_filename], capture_output=True, text=True, env=env)

    if result_fix.returncode == 0:
        print("[SUCCESS] The fix works! Test passed.")
        # Commit logic could go here
    else:
        print("[FAILURE] The fix did not work. Reverting...")
        with open(args.target, 'w') as f:
            f.write(source_content)
        print("    -> Reverted to original.")
        print(result_fix.stdout)

def main():
    parser = argparse.ArgumentParser(description='Lazarus: Self-Healing Agent')
    parser.add_argument('--watch', action='store_true', help='Watch Nomad for failures')
    parser.add_argument('--local-mode', action='store_true', help='Run in local dev mode')
    parser.add_argument('--log', help='Path to crash log (local mode)')
    parser.add_argument('--target', help='Path to target source file (local mode)')
    parser.add_argument('--mock', action='store_true', help='Use mock LLM responses')

    args = parser.parse_args()

    if args.local_mode:
        if not args.log or not args.target:
            print("Error: --local-mode requires --log and --target")
            sys.exit(1)
        asyncio.run(run_local_mode(args))
    else:
        print("Watch mode not fully implemented yet.")

if __name__ == "__main__":
    main()
