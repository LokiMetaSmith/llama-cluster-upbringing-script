import subprocess
import logging
import shutil
import os
import time
from typing import Any, Optional

logger = logging.getLogger(__name__)

class ProcessInvestigatorTool:
    def __init__(self):
        self.name = "process_investigator"
        self.description = (
            "Captures process snapshots, inspects Python call stacks via py-spy/GDB, "
            "and profiles process I/O and C-extensions via strace and perf."
        )

    def get_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": getattr(self, "name", "process_investigator"),
                "description": getattr(self, "description", "Process Investigator Tool"),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": (
                                "Action to perform: 'list_processes' (snapshot top CPU/MEM tasks), "
                                "'py_spy' (py-spy dump/top/record), 'gdb_py_bt' (GDB Python backtrace), "
                                "'strace' (strace syscall trace), 'perf' (perf stat/top sampling)."
                            ),
                            "enum": ["list_processes", "py_spy", "gdb_py_bt", "strace", "perf"]
                        },
                        "kwargs": {
                            "type": "object",
                            "description": "Additional keyword arguments specific to the action."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def _run_cmd(self, cmd: list[str], timeout: int = 30, use_sudo: bool = True) -> dict[str, Any]:
        """Utility to run a subprocess command cleanly, trying sudo if requested/needed."""
        if use_sudo and os.geteuid() != 0 and shutil.which("sudo"):
            cmd = ["sudo", "-n"] + cmd

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return {
                "success": res.returncode == 0,
                "exit_code": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr
            }
        except subprocess.TimeoutExpired as e:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": e.stdout or "",
                "stderr": f"Command timed out after {timeout} seconds."
            }
        except FileNotFoundError:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Executable not found for command: {' '.join(cmd)}"
            }
        except Exception as e:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Execution error: {str(e)}"
            }

    def list_processes(self, sort_by: str = "cpu", limit: int = 20) -> str:
        """
        Runs 'ps' to capture process information.
        Args:
            sort_by: 'cpu' or 'mem'
            limit: number of top processes to return
        """
        logger.info(f"ProcessInvestigatorTool list_processes invoked, sort_by={sort_by}")

        sort_flag = "-pcpu" if sort_by == "cpu" else "-pmem"
        cmd = ["ps", "eo", "user,pid,pcpu,pmem,args", "--sort", sort_flag]

        res = self._run_cmd(cmd, use_sudo=False)
        if not res["success"]:
            return f"Failed to capture process snapshot: {res['stderr']}"

        lines = res["stdout"].strip().split("\n")
        header = lines[0] if lines else ""
        body = lines[1:limit + 1] if len(lines) > 1 else []

        # Truncate command lines for readability
        formatted_body = []
        for line in body:
            if len(line) > 120:
                formatted_body.append(line[:117] + "...")
            else:
                formatted_body.append(line)

        summary = f"Top processes sorted by {sort_by} (limit {limit}):\n" + header + "\n" + "\n".join(formatted_body)
        return summary

    def py_spy(self, pid: int | str, subaction: str = "dump", duration: int = 5, output_file: Optional[str] = None) -> str:
        """
        Runs py-spy against a Python process PID.
        Args:
            pid: Process ID of Python app
            subaction: 'dump' (print stacks once), 'top' (live top snapshot), 'record' (generate flamegraph SVG)
            duration: Duration in seconds for top/record
            output_file: Target file path for record flamegraph
        """
        if not shutil.which("py-spy") and not os.path.exists("/usr/local/bin/py-spy"):
            return (
                "Error: 'py-spy' binary is not installed on this host.\n"
                "Install via: pip install py-spy or sudo apt install py-spy."
            )

        pid_str = str(pid)
        if subaction == "dump":
            cmd = ["py-spy", "dump", "--pid", pid_str]
            res = self._run_cmd(cmd, timeout=30)
        elif subaction == "top":
            # For non-interactive top snapshot, py-spy top --pid <PID> --duration <Sec>
            cmd = ["py-spy", "top", "--pid", pid_str, "--duration", str(duration)]
            res = self._run_cmd(cmd, timeout=duration + 10)
        elif subaction == "record":
            if not output_file:
                timestamp = int(time.time())
                output_file = f"/tmp/py_spy_profile_{pid_str}_{timestamp}.svg"
            cmd = ["py-spy", "record", "-o", output_file, "--pid", pid_str, "--duration", str(duration)]
            res = self._run_cmd(cmd, timeout=duration + 10)
            if res["success"]:
                return f"Successfully generated py-spy flamegraph at: {output_file}\n{res['stdout']}"
        else:
            return f"Unknown py-spy subaction: '{subaction}'. Choose from 'dump', 'top', 'record'."

        if res["success"]:
            return res["stdout"] or "py-spy command completed with empty output."
        return f"py-spy error (exit code {res['exit_code']}):\n{res['stderr']}\n{res['stdout']}"

    def gdb_py_bt(self, pid: int | str) -> str:
        """
        Attaches GDB to a PID and prints the Python stack using 'py-bt'.
        Args:
            pid: Process ID
        """
        if not shutil.which("gdb"):
            return "Error: 'gdb' is not installed. Install via: sudo apt install gdb python3-dbg."

        pid_str = str(pid)
        cmd = ["gdb", "-p", pid_str, "-batch", "-ex", "py-bt"]
        res = self._run_cmd(cmd, timeout=30)

        if res["success"]:
            return res["stdout"] or "GDB py-bt command completed with empty output."
        return f"GDB py-bt error (exit code {res['exit_code']}):\n{res['stderr']}\n{res['stdout']}"

    def strace(self, pid: int | str, duration: int = 5, summary_only: bool = True) -> str:
        """
        Attaches strace to PID to inspect system calls.
        Args:
            pid: Process ID
            duration: Sampling duration in seconds
            summary_only: If True, uses -c for syscall summary statistics
        """
        if not shutil.which("strace"):
            return "Error: 'strace' is not installed. Install via: sudo apt install strace."

        pid_str = str(pid)
        cmd = ["timeout", str(duration), "strace", "-p", pid_str]
        if summary_only:
            cmd.append("-c")

        res = self._run_cmd(cmd, timeout=duration + 10)
        # Timeout returncode 124 is normal when capturing for 'duration' seconds
        output = (res["stderr"] + "\n" + res["stdout"]).strip()
        if res["exit_code"] in [0, 124]:
            return f"strace output for PID {pid_str} ({duration}s):\n{output}"
        return f"strace error (exit code {res['exit_code']}):\n{output}"

    def perf(self, pid: int | str, duration: int = 5, mode: str = "stat") -> str:
        """
        Profiles CPU/native execution using perf.
        Args:
            pid: Process ID
            duration: Sampling duration in seconds
            mode: 'stat' (counter stats) or 'top' (symbol profile)
        """
        if not shutil.which("perf"):
            return "Error: 'perf' is not installed. Install via: sudo apt install linux-tools-common linux-tools-generic."

        pid_str = str(pid)
        if mode == "stat":
            cmd = ["perf", "stat", "-p", pid_str, "--", "sleep", str(duration)]
        elif mode == "top":
            cmd = ["timeout", str(duration), "perf", "top", "-p", pid_str, "--stdio"]
        else:
            return f"Unknown perf mode: '{mode}'. Choose from 'stat', 'top'."

        res = self._run_cmd(cmd, timeout=duration + 10)
        output = (res["stderr"] + "\n" + res["stdout"]).strip()
        if res["exit_code"] in [0, 124]:
            return f"perf {mode} report for PID {pid_str} ({duration}s):\n{output}"
        return f"perf error (exit code {res['exit_code']}):\n{output}"

    def execute(self, action: str = "list_processes", **kwargs) -> Any:
        # Handle kwargs if wrapped under 'kwargs' dict or directly passed
        if "kwargs" in kwargs and isinstance(kwargs["kwargs"], dict):
            kwargs = kwargs["kwargs"]

        if action in ["list_processes", "ps", "run"]:
            return self.list_processes(
                sort_by=kwargs.get("sort_by", "cpu"),
                limit=kwargs.get("limit", 20)
            )
        elif action == "py_spy":
            pid = kwargs.get("pid")
            if not pid:
                return "Error: 'pid' argument is required for py_spy action."
            return self.py_spy(
                pid=pid,
                subaction=kwargs.get("subaction", kwargs.get("mode", "dump")),
                duration=kwargs.get("duration", 5),
                output_file=kwargs.get("output_file")
            )
        elif action == "gdb_py_bt":
            pid = kwargs.get("pid")
            if not pid:
                return "Error: 'pid' argument is required for gdb_py_bt action."
            return self.gdb_py_bt(pid=pid)
        elif action == "strace":
            pid = kwargs.get("pid")
            if not pid:
                return "Error: 'pid' argument is required for strace action."
            return self.strace(
                pid=pid,
                duration=kwargs.get("duration", 5),
                summary_only=kwargs.get("summary_only", True)
            )
        elif action == "perf":
            pid = kwargs.get("pid")
            if not pid:
                return "Error: 'pid' argument is required for perf action."
            return self.perf(
                pid=pid,
                duration=kwargs.get("duration", 5),
                mode=kwargs.get("mode", "stat")
            )
        else:
            return f"Unknown action: '{action}'. Available: list_processes, py_spy, gdb_py_bt, strace, perf."

    def run(self, sort_by: str = "cpu") -> str:
        """Legacy helper method compatibility."""
        return self.list_processes(sort_by=sort_by)
