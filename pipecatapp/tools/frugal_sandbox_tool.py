import os
import sys
import time
import math
import logging
import subprocess
import re
from typing import Optional, Dict, Any

try:
    import resource
except ImportError:
    resource = None

class FrugalSandboxTool:
    """A metadata-driven frugal sandboxing tool for low-cost code execution and escalation analysis.

    This tool sits as a meta-layer above execution environments. It executes Python code
    in a resource-restricted sandbox, measures physical compute resource consumption (duration, RAM),
    grades the output value/contribution to the original query, and decides whether the low-weight
    solution should be retained or escalated to a high-capacity frontier model.
    """

    def __init__(self):
        self.name = "frugal_sandbox"
        self.description = (
            "Runs lightweight code in a secure resource-constrained sandbox, tracks physical CPU/memory "
            "consumption, grades the contribution value of the output, and calculates a Value Density Ratio "
            "to recommend whether to accept the lightweight output or escalate to a high-capacity frontier expert."
        )
        self.input_schema = {
            "type": "object",
            "properties": {
                "task_query": {
                    "type": "string",
                    "description": "The original user task, goal, or problem description."
                },
                "proposed_code": {
                    "type": "string",
                    "description": "The Python code proposed by a low-weight model or system component to be tested."
                },
                "max_memory_mb": {
                    "type": "integer",
                    "description": "Memory limit in MB for the sandbox process (default: 64).",
                    "default": 64
                },
                "timeout_seconds": {
                    "type": "integer",
                    "description": "Maximum execution duration in seconds (default: 10).",
                    "default": 10
                },
                "expected_output_pattern": {
                    "type": "string",
                    "description": "Optional regex pattern to look for in stdout to verify code output success."
                }
            },
            "required": ["task_query", "proposed_code"]
        }

    def _set_resource_limits(self, max_memory_mb: int):
        """Sets resource limits inside the spawned subprocess using preexec_fn."""
        if resource is None:
            return

        try:
            # Set virtual memory limit (RLIMIT_AS) to a safer virtual space limit (minimum 256MB)
            max_virtual_bytes = max(256, max_memory_mb) * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (max_virtual_bytes, max_virtual_bytes))
        except Exception as e:
            logging.warning(f"Failed to set RLIMIT_AS limit in subprocess: {e}")

        try:
            # Set data segment/heap limit (RLIMIT_DATA) to max_memory_mb
            # On macOS, setting RLIMIT_DATA is sometimes restricted/unsupported, so we wrap it
            max_data_bytes = max_memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_DATA, (max_data_bytes, max_data_bytes))
        except Exception as e:
            logging.warning(f"Failed to set RLIMIT_DATA limit in subprocess: {e}")

    async def run(
        self,
        task_query: str,
        proposed_code: str,
        max_memory_mb: int = 64,
        timeout_seconds: int = 10,
        expected_output_pattern: Optional[str] = None
    ) -> Dict[str, Any]:
        """Executes the proposed Python code inside a secure resource-limited subprocess,

        measures the duration and peak RSS memory, grades the contribution value, and computes
        the Value Density Ratio (VDR) to make an escalation recommendation.

        Args:
            task_query (str): The original task or goal description.
            proposed_code (str): The Python script to run.
            max_memory_mb (int, optional): Strict memory limit in MB. Defaults to 64.
            timeout_seconds (int, optional): Execution timeout in seconds. Defaults to 10.
            expected_output_pattern (str, optional): Regex pattern to match in output. Defaults to None.

        Returns:
            Dict[str, Any]: Structured execution report with scores, metrics, and escalation decision.
        """
        # Ensure values are within logical bounds
        max_memory_mb = max(16, min(512, max_memory_mb))
        timeout_seconds = max(1, min(60, timeout_seconds))

        logging.info(f"FrugalSandbox: Starting run. Memory limit: {max_memory_mb}MB, Timeout: {timeout_seconds}s")

        # 1. Track resource usage baseline before child execution
        initial_child_rss_bytes = 0
        if resource:
            try:
                initial_child_rss_bytes = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                # On macOS ru_maxrss is in bytes, on Linux it is in kilobytes
                if sys.platform != 'darwin':
                    initial_child_rss_bytes *= 1024
            except Exception:
                pass

        # Prepare execution args
        args = [sys.executable, "-"]

        # Define the preexec function to enforce memory limits (Unix only)
        preexec_fn = None
        if sys.platform != 'win32' and resource is not None:
            preexec_fn = lambda: self._set_resource_limits(max_memory_mb)

        start_time = time.perf_counter()
        stdout, stderr, exit_code, timed_out = "", "", -1, False

        try:
            # Run the process securely with stdin code delivery and strict limits
            proc = subprocess.run(
                args,
                input=proposed_code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=preexec_fn,
                timeout=timeout_seconds
            )
            stdout = proc.stdout.decode('utf-8', errors='replace')
            stderr = proc.stderr.decode('utf-8', errors='replace')
            exit_code = proc.returncode
        except subprocess.TimeoutExpired as e:
            timed_out = True
            exit_code = 124
            stdout = e.stdout.decode('utf-8', errors='replace') if e.stdout else ""
            stderr = f"Execution timed out after {timeout_seconds} seconds.\n" + (e.stderr.decode('utf-8', errors='replace') if e.stderr else "")
        except Exception as e:
            exit_code = -1
            stderr = f"Unexpected execution error: {e}"

        duration_ms = int((time.perf_counter() - start_time) * 1000)

        # 2. Measure child process memory consumption differential
        peak_rss_bytes = 0
        if resource:
            try:
                post_child_rss_bytes = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                if sys.platform != 'darwin':
                    post_child_rss_bytes *= 1024
                # Differential estimation
                peak_rss_bytes = max(0, post_child_rss_bytes - initial_child_rss_bytes)
            except Exception:
                pass

        # If differential is zero or unavailable, fallback to standard subprocess memory measurement
        if peak_rss_bytes <= 0:
            # We estimate a default minimum footprint for running the python interpreter
            peak_rss_bytes = 15 * 1024 * 1024  # ~15MB base python overhead

        peak_rss_mb = round(peak_rss_bytes / (1024 * 1024), 2)

        # 3. Compute Resource Cost Score (C_exec)
        # Duration in seconds multiplied by (Memory in MB + 1.0)
        cost_score = round((duration_ms * 0.001) * (peak_rss_mb + 1.0), 4)

        # 4. Grade Value Contribution (V_contrib)
        value_contrib = 0.0
        if timed_out:
            value_contrib = 0.0
        elif exit_code != 0:
            value_contrib = 0.0
        elif not stdout.strip():
            value_contrib = 1.0
        else:
            # Base score for successful execution returning output
            base_score = 2.0

            # Richness score based on log size of stdout
            richness_score = min(3.0, math.log10(len(stdout) + 1))

            # Query relevance: Check density of task query terms in stdout
            stopwords = {"the", "and", "a", "of", "to", "in", "is", "that", "it", "for", "on", "with", "as", "at", "by", "an", "be", "this", "are", "from", "how", "what", "why", "run", "code", "write", "print"}
            words = [w.strip("?,.:;!\"'()[]").lower() for w in task_query.split()]
            query_keywords = {w for w in words if w and w not in stopwords and len(w) > 2}

            query_relevance_score = 0.0
            if query_keywords:
                matched_keywords = {kw for kw in query_keywords if kw in stdout.lower()}
                match_ratio = len(matched_keywords) / len(query_keywords)
                query_relevance_score = match_ratio * 3.0

            # Pattern match score
            pattern_score = 0.0
            if expected_output_pattern:
                try:
                    if re.search(expected_output_pattern, stdout):
                        pattern_score = 2.0
                except Exception as e:
                    logging.error(f"FrugalSandbox regex pattern compile error: {e}")

            value_contrib = min(10.0, base_score + richness_score + query_relevance_score + pattern_score)

        value_contrib = round(value_contrib, 2)

        # 5. Compute Value Density Ratio (VDR)
        value_density_ratio = round(value_contrib / (cost_score + 1.0), 4)

        # 6. Evaluate Escalation Recommendation
        # If execution succeeds with high utility and low cost, retain the low-weight result.
        # Otherwise, recommend escalating to a heavyweight frontier model.
        escalation_recommended = True
        recommendation_msg = ""

        if timed_out:
            recommendation_msg = "Escalate to frontier model: code execution timed out."
        elif exit_code != 0:
            recommendation_msg = "Escalate to frontier model: code execution failed with exit code."
        elif value_contrib < 4.0:
            recommendation_msg = "Escalate to frontier model: insufficient output value/contribution returned."
        elif value_density_ratio < 0.5:
            recommendation_msg = "Escalate to frontier model: resource cost too high relative to value contribution."
        else:
            escalation_recommended = False
            recommendation_msg = "Low-cost success: retain low-weight model output (high Value Density Ratio)."

        report = {
            "execution_metrics": {
                "exit_code": exit_code,
                "duration_ms": duration_ms,
                "peak_rss_mb": peak_rss_mb,
                "timed_out": timed_out
            },
            "stdout": stdout,
            "stderr": stderr,
            "evaluation_scores": {
                "execution_cost_score": cost_score,
                "value_contribution_score": value_contrib,
                "value_density_ratio": value_density_ratio
            },
            "escalation_decision": {
                "escalation_recommended": escalation_recommended,
                "recommendation": recommendation_msg
            }
        }

        logging.info(f"FrugalSandbox: Finished. Escalation Recommended: {escalation_recommended}. VDR: {value_density_ratio}")
        return report
