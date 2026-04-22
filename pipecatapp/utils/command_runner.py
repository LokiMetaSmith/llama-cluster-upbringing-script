import subprocess
from typing import List, Union, Optional, Dict

import os
import logging

logger = logging.getLogger(__name__)


class CommandRunner:
    """
    Unified execution abstraction for running shell commands and subprocesses.
    This enables easier mocking in unit tests and provides a central point
    for future sandboxing and security audits.

    Supports two modes:
    - local: Uses subprocess.run (default)
    - nomad: Uses Nomad API for cluster-native execution
    """

    # Execution modes
    MODE_LOCAL = "local"
    MODE_NOMAD = "nomad"

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, mode: str = None):
        self.mode = mode or os.getenv("COMMAND_RUNNER_MODE", self.MODE_LOCAL)
        self._nomad_client = None
        if self.mode == self.MODE_NOMAD:
            self._init_nomad_client()

    def _init_nomad_client(self):
        """Initialize Nomad API client."""
        try:
            import nomad
            host = os.getenv("NOMAD_HOST", "127.0.0.1")
            port = os.getenv("NOMAD_PORT", "4646")
            cert = os.getenv("NOMAD_CERT")
            self._nomad_client = nomad.Nomad(
                host=host,
                port=port,
                cert=cert
            )
            logger.info(f"CommandRunner initialized in Nomad mode: {host}:{port}")
        except ImportError:
            logger.warning("nomad module not found, falling back to local mode")
            self.mode = self.MODE_LOCAL

    @staticmethod
    def run_local(
        cmd: Union[str, List[str]],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        capture_output: bool = True,
        text: bool = True,
        check: bool = False,
        shell: bool = False
    ) -> subprocess.CompletedProcess:
        """Executes a command using subprocess.run (local mode)."""
        return subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            timeout=timeout,
            capture_output=capture_output,
            text=text,
            check=check,
            shell=shell
        )

    @classmethod
    def run(
        cls,
        cmd: Union[str, List[str]],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        capture_output: bool = True,
        text: bool = True,
        check: bool = False,
        shell: bool = False,
        job_name: str = None,
        namespace: str = "default"
    ) -> subprocess.CompletedProcess:
        """
        Executes a command either locally or via Nomad API.

        If mode is NOMAD and job_name is provided, submits as Nomad job.
        Otherwise, runs locally via subprocess.
        """
        instance = cls.get_instance()
        if instance.mode == cls.MODE_NOMAD and instance._nomad_client and job_name:
            return instance._run_nomad(cmd, job_name, namespace)
        else:
            return cls.run_local(
                cmd, cwd, env, timeout, capture_output,
                text, check, shell
            )

    def _run_nomad(self, cmd: str, job_name: str, namespace: str) -> subprocess.CompletedProcess:
        """Execute command via Nomad API (stub - requires job specification)."""
        # This is a placeholder for full Nomad integration
        # Full implementation would need:
        # - Job template rendering
        # - Job submission
        # - Result polling
        logger.warning(f"Nomad execution not fully implemented, running locally")
        return self.run_local(cmd, check=False)
