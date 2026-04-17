import subprocess
from typing import List, Union, Optional, Dict

class CommandRunner:
    """
    Unified execution abstraction for running shell commands and subprocesses.
    This enables easier mocking in unit tests and provides a central point
    for future sandboxing and security audits.
    """

    @staticmethod
    def run(
        cmd: Union[str, List[str]],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        capture_output: bool = True,
        text: bool = True,
        check: bool = False,
        shell: bool = False
    ) -> subprocess.CompletedProcess:
        """
        Executes a command using subprocess.run.
        """
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
