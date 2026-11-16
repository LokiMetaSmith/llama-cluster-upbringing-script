"""Persistent npcsh/npcrs Unix-socket daemon and .jinx execution engine."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import signal
import socket
import subprocess
import sys
import threading
from typing import Any, Optional

import yaml
from jinja2.sandbox import SandboxedEnvironment

logger = logging.getLogger("npcsh_daemon")

_PARAM_KEY_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_PARAM_VAL_RE = re.compile(r"^[a-zA-Z0-9._:/-]*$")
_SANDBOX_ENV = SandboxedEnvironment(autoescape=False)

DEFAULT_SOCKET_PATH = "/run/npcsh/daemon.sock"
USER_SOCKET_PATH = os.path.expanduser("~/.npcsh/daemon.sock")


def _parse_jinx_inputs(raw_inputs: Any) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    if isinstance(raw_inputs, dict):
        merged.update(raw_inputs)
    elif isinstance(raw_inputs, list):
        for entry in raw_inputs:
            if isinstance(entry, dict):
                merged.update(entry)
            elif isinstance(entry, str):
                merged.setdefault(entry, "")
    return merged


def _validate_param(key: str, value: Any) -> str:
    if not _PARAM_KEY_RE.match(key):
        raise ValueError(f"Invalid jinx parameter key: {key!r}")
    str_val = str(value)
    if not _PARAM_VAL_RE.match(str_val):
        raise ValueError(f"Invalid characters in jinx parameter {key!r}: {str_val!r}")
    return str_val


def render_jinx_step(code_template: str, context: dict[str, Any]) -> str:
    """Render a .jinx step script using Jinja2 SandboxedEnvironment."""
    template = _SANDBOX_ENV.from_string(code_template)
    return template.render(**context)


def execute_jinx_file(
    jinx_path: str,
    params: Optional[dict[str, Any]] = None,
    timeout: float = 30.0,
    dry_run: bool = False,
    allowed_root: Optional[str] = None,
) -> dict[str, Any]:
    """Load, render, and execute a declarative .jinx workflow file over Unix pipes."""
    real_path = os.path.realpath(jinx_path)
    if allowed_root is not None:
        real_root = os.path.realpath(allowed_root)
        if os.path.commonpath([real_root, real_path]) != real_root:
            raise ValueError(f"Path traversal blocked for jinx file: {jinx_path!r}")

    if not os.path.isfile(real_path) or not real_path.endswith(".jinx"):
        raise FileNotFoundError(f"Jinx template not found: {jinx_path!r}")

    with open(real_path, "r", encoding="utf-8") as handle:
        doc = yaml.safe_load(handle) or {}

    jinx_name = str(doc.get("jinx_name") or os.path.basename(real_path))
    context = _parse_jinx_inputs(doc.get("inputs"))
    if params:
        for k, v in params.items():
            context[k] = _validate_param(k, v)

    sanitized_context = {k: _validate_param(k, v) for k, v in context.items()}
    steps = doc.get("steps") or []

    exec_env = os.environ.copy()
    if dry_run:
        exec_env["NPCSH_DRY_RUN"] = "1"

    stdout_parts: list[str] = []
    stderr_parts: list[str] = []
    step_results: list[dict[str, Any]] = []
    last_returncode = 0

    for step in steps:
        if not isinstance(step, dict):
            continue
        step_name = str(step.get("name") or "step")
        engine = str(step.get("engine") or "bash").lower()
        code_template = str(step.get("code") or "")
        rendered_code = render_jinx_step(code_template, sanitized_context)

        if engine in ("bash", "sh"):
            shell_bin = "/bin/bash" if engine == "bash" else "/bin/sh"
            proc = subprocess.run(
                [shell_bin, "-c", rendered_code],
                env=exec_env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            stdout_parts.append(proc.stdout)
            stderr_parts.append(proc.stderr)
            last_returncode = proc.returncode
            step_results.append(
                {
                    "name": step_name,
                    "returncode": proc.returncode,
                    "stdout": proc.stdout.strip(),
                    "stderr": proc.stderr.strip(),
                }
            )
            if proc.returncode != 0:
                break
        else:
            raise ValueError(f"Unsupported jinx step engine: {engine!r}")

    return {
        "status": "ok" if last_returncode == 0 else "error",
        "jinx_name": jinx_name,
        "returncode": last_returncode,
        "stdout": "\n".join(part.strip() for part in stdout_parts if part.strip()),
        "stderr": "\n".join(part.strip() for part in stderr_parts if part.strip()),
        "steps": step_results,
    }


class NPCSHDaemon:
    """Persistent Unix-domain-socket daemon avoiding cold-start Python per CLI call."""

    def __init__(
        self,
        socket_path: Optional[str] = None,
        allowed_root: Optional[str] = None,
    ) -> None:
        raw_socket = socket_path or os.getenv("NPCSH_SOCKET_PATH") or DEFAULT_SOCKET_PATH
        self.socket_path = os.path.expanduser(raw_socket)
        self.allowed_root = allowed_root
        self._server_sock: Optional[socket.socket] = None
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _handle_request(self, raw_bytes: bytes) -> dict[str, Any]:
        try:
            payload = json.loads(raw_bytes.decode("utf-8"))
        except Exception as exc:
            return {"status": "error", "error": f"Invalid JSON request: {exc}", "returncode": 1}

        command = payload.get("command")
        if command == "ping":
            return {"status": "ok", "pong": True, "pid": os.getpid()}

        if command == "run_jinx":
            jinx_path = payload.get("jinx_path")
            if not isinstance(jinx_path, str) or not jinx_path:
                return {"status": "error", "error": "Missing 'jinx_path'", "returncode": 1}
            params = payload.get("params") or {}
            if not isinstance(params, dict):
                return {"status": "error", "error": "'params' must be an object", "returncode": 1}
            dry_run = bool(payload.get("dry_run", False))
            timeout = float(payload.get("timeout", 30.0))
            try:
                return execute_jinx_file(
                    jinx_path=jinx_path,
                    params=params,
                    timeout=timeout,
                    dry_run=dry_run,
                    allowed_root=self.allowed_root,
                )
            except Exception as exc:
                return {"status": "error", "error": str(exc), "returncode": 1}

        return {"status": "error", "error": f"Unknown command: {command!r}", "returncode": 1}

    def _serve_client(self, conn: socket.socket) -> None:
        try:
            chunks: list[bytes] = []
            while True:
                data = conn.recv(65536)
                if not data:
                    break
                chunks.append(data)
            response = self._handle_request(b"".join(chunks))
            conn.sendall((json.dumps(response) + "\n").encode("utf-8"))
        except Exception as exc:
            logger.error(f"Error handling daemon client: {exc}")
        finally:
            conn.close()

    def start(self, background: bool = False) -> None:
        """Bind the Unix domain socket and start serving requests."""
        sock_dir = os.path.dirname(os.path.abspath(self.socket_path))
        if sock_dir:
            os.makedirs(sock_dir, exist_ok=True)
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)

        self._stop_event.clear()
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.socket_path)
        os.chmod(self.socket_path, 0o660)
        sock.listen(32)
        sock.settimeout(0.25)
        self._server_sock = sock

        if background:
            self._thread = threading.Thread(target=self._accept_loop, daemon=True)
            self._thread.start()
        else:
            self._accept_loop()

    def _accept_loop(self) -> None:
        assert self._server_sock is not None
        while not self._stop_event.is_set():
            try:
                conn, _ = self._server_sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            worker = threading.Thread(target=self._serve_client, args=(conn,), daemon=True)
            worker.start()

    def stop(self) -> None:
        """Stop the Unix socket daemon and clean up socket file."""
        self._stop_event.set()
        if self._server_sock is not None:
            try:
                self._server_sock.close()
            except OSError:
                pass
            self._server_sock = None
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        if os.path.exists(self.socket_path):
            try:
                os.unlink(self.socket_path)
            except OSError:
                pass


def send_daemon_request(
    socket_path: str,
    payload: dict[str, Any],
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Send a JSON request to a running NPCSHDaemon over its Unix socket."""
    resolved_socket = os.path.expanduser(socket_path)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(timeout)
        client.connect(resolved_socket)
        client.sendall(json.dumps(payload).encode("utf-8"))
        client.shutdown(socket.SHUT_WR)
        chunks: list[bytes] = []
        while True:
            data = client.recv(65536)
            if not data:
                break
            chunks.append(data)
    return json.loads(b"".join(chunks).decode("utf-8"))


def _resolve_active_socket(explicit_socket: Optional[str] = None) -> Optional[str]:
    candidates = [
        explicit_socket,
        os.getenv("NPCSH_SOCKET_PATH"),
        USER_SOCKET_PATH,
        DEFAULT_SOCKET_PATH,
    ]
    for candidate in candidates:
        if candidate:
            expanded = os.path.expanduser(candidate)
            if os.path.exists(expanded):
                return expanded
    return None


def _parse_kv_args(kv_items: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in kv_items:
        if "=" not in item:
            raise ValueError(f"Expected key=value argument, got: {item!r}")
        key, value = item.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entrypoint for both npcsh-daemon and npc client dispatch."""
    parser = argparse.ArgumentParser(description="npcsh / npcrs daemon and .jinx CLI")
    parser.add_argument("--daemon", action="store_true", help="Run persistent Unix socket daemon")
    parser.add_argument("--socket", default=None, help="Unix domain socket path")
    parser.add_argument("--dry-run", action="store_true", help="Run jinx step in dry-run mode")
    parser.add_argument("target", nargs="?", help="Path to .jinx file to execute")
    parser.add_argument("params", nargs="*", help="key=value parameters for the .jinx template")

    args = parser.parse_args(argv)
    is_daemon = args.daemon or os.path.basename(sys.argv[0]) == "npcsh-daemon"

    if is_daemon:
        daemon = NPCSHDaemon(socket_path=args.socket or DEFAULT_SOCKET_PATH)

        def _handle_sig(_signum: int, _frame: Any) -> None:
            daemon.stop()

        signal.signal(signal.SIGTERM, _handle_sig)
        signal.signal(signal.SIGINT, _handle_sig)
        daemon.start(background=False)
        return 0

    if not args.target:
        parser.print_help()
        return 1

    kv_params = _parse_kv_args(args.params)
    active_socket = _resolve_active_socket(args.socket)
    if active_socket:
        response = send_daemon_request(
            active_socket,
            {
                "command": "run_jinx",
                "jinx_path": os.path.abspath(args.target),
                "params": kv_params,
                "dry_run": args.dry_run,
            },
        )
    else:
        response = execute_jinx_file(
            jinx_path=args.target,
            params=kv_params,
            dry_run=args.dry_run,
        )

    if response.get("stdout"):
        print(response["stdout"])
    if response.get("stderr"):
        print(response["stderr"], file=sys.stderr)
    return int(response.get("returncode", 1))


if __name__ == "__main__":
    sys.exit(main())
