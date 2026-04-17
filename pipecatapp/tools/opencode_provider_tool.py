import os
import uuid
import time
import requests
import logging
import re
from typing import Dict, Any, Optional

class OpenCodeProviderTool:
    """A tool that wraps the OpenCode CLI as a provider, running it via Nomad raw_exec.

    This implements the Paseo 'provider' orchestration pattern, executing a CLI agent,
    intercepting its stdout/stderr streams, and returning standard Pipecat agent events.
    """

    def __init__(self):
        self.description = (
            "Delegates a coding task to the OpenCode CLI, running it as a Nomad batch job. "
            "It intercepts standard output streams and standardizes them into structured agent events. "
            "Returns a dictionary with 'final_output' containing the execution result."
        )
        self.name = "opencode_provider"
        self.nomad_url = os.environ.get("NOMAD_ADDR", f"http://{os.getenv("CLUSTER_IP", "127.0.0.1")}:4646")
        self.token = os.environ.get("NOMAD_TOKEN")
        self.default_timeout = 600  # 10 minutes default for coding agents
        self.headers = {"X-Nomad-Token": self.token} if self.token else {}

    def _parse_opencode_output(self, logs: str) -> Dict[str, Any]:
        """Parses the raw stdout of the OpenCode CLI into structured events."""
        events = []

        # Simple heuristic parser (similar to Paseo's provider-level standardization)
        for line in logs.splitlines():
            line = line.strip()
            if not line:
                continue

            if "OpenCode AI" in line:
                continue # Skip branding

            if line.startswith("> ") or "Thinking..." in line:
                events.append({"type": "thought", "content": line})
            elif "Executing" in line or "Tool call" in line:
                events.append({"type": "tool_execution", "content": line})
            elif "Error" in line:
                events.append({"type": "error", "content": line})
            else:
                events.append({"type": "text", "content": line})

        return {
            "agent_type": "opencode_cli",
            "events_count": len(events),
            "events": events,
            "raw_output": logs
        }

    def run(self, task: str) -> Dict[str, Any]:
        """Executes the OpenCode CLI with the given task via a Nomad raw_exec batch job."""
        job_id = f"opencode-provider-{uuid.uuid4().hex[:8]}"
        logging.info(f"Dispatching OpenCode Provider Nomad job: {job_id}")

        # Construct Job JSON for a raw_exec task
        job_payload = {
            "Job": {
                "ID": job_id,
                "Name": job_id,
                "Type": "batch",
                "Datacenters": ["dc1"],
                "TaskGroups": [
                    {
                        "Name": "opencode",
                        "Count": 1,
                        "RestartPolicy": {
                            "Attempts": 0,
                            "Mode": "fail"
                        },
                        "Tasks": [
                            {
                                "Name": "execution",
                                "Driver": "raw_exec",
                                "Config": {
                                    # We use raw_exec assuming opencode is installed on the node (via the Ansible role)
                                    "command": "/usr/local/bin/npm",
                                    "args": ["exec", "--", "opencode", task]
                                },
                                "Resources": {
                                    "CPU": 500,
                                    "MemoryMB": 512
                                }
                            }
                        ]
                    }
                ]
            }
        }

        try:
            # 1. Register Job
            reg_resp = requests.post(f"{self.nomad_url}/v1/jobs", json=job_payload, headers=self.headers, timeout=10)
            reg_resp.raise_for_status()

            # 2. Wait for Allocation
            alloc_id = None
            start_time = time.time()
            while time.time() - start_time < self.default_timeout:
                try:
                    allocs_resp = requests.get(f"{self.nomad_url}/v1/job/{job_id}/allocations", headers=self.headers, timeout=10)
                    allocs_resp.raise_for_status()
                    allocs = allocs_resp.json()

                    if allocs:
                        allocs.sort(key=lambda x: x.get('CreateTime', 0), reverse=True)
                        latest_alloc = allocs[0]
                        alloc_id = latest_alloc['ID']
                        client_status = latest_alloc.get('ClientStatus')

                        if client_status in ['complete', 'failed']:
                            break
                except Exception as e:
                    logging.warning(f"Error polling allocations for job {job_id}: {e}")

                time.sleep(2)

            if not alloc_id:
                return {"final_output": f"Error: Nomad job timed out waiting for allocation after {self.default_timeout}s."}

            if time.time() - start_time >= self.default_timeout:
                return {"final_output": f"Error: OpenCode execution timed out after {self.default_timeout}s."}

            # 3. Fetch Logs
            logs = ""
            try:
                for log_type in ['stdout', 'stderr']:
                    log_resp = requests.get(
                        f"{self.nomad_url}/v1/client/fs/logs/{alloc_id}?task=execution&type={log_type}&plain=true",
                        headers=self.headers,
                        timeout=10
                    )
                    if log_resp.status_code == 200:
                        content = log_resp.text
                        if content:
                            logs += content + "\n"
            except Exception as e:
                logs += f"Error fetching logs: {e}\n"

            # 4. Standardize output (Paseo provider pattern)
            parsed_data = self._parse_opencode_output(logs)

            # Workflow outputs should return a dict with 'final_output'
            return {
                "final_output": parsed_data["raw_output"],
                "agent_events": parsed_data["events"]
            }

        except Exception as e:
            return {"final_output": f"Nomad execution error: {e}"}
        finally:
            # 5. Cleanup
            try:
                requests.delete(f"{self.nomad_url}/v1/job/{job_id}?purge=true", headers=self.headers, timeout=10)
            except:
                pass
