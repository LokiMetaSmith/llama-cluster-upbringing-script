import os
import json
import logging
import asyncio
import subprocess
import tempfile
import shlex
from pipecatapp.utils.command_runner import CommandRunner

class AutoloopTool:
    """
    WARNING: THIS TOOL RUNS CODE LOCALLY WITHOUT A SANDBOX.
    It should only be used in trusted environments or for non-destructive metrics.

    A standalone tool providing direct, lightweight access to the `autoloop-ai` library.
    It allows the agent to run iterative, hill-climbing optimization on any target file
    using a custom metric command.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def run(self,
                  target_file: str,
                  metric_command: str,
                  directives: str,
                  experiments: int = 5,
                  agent: str = "claude") -> str:
        """
        Runs the autoloop-ai optimization loop natively.

        Args:
            target_file (str): The specific file to mutate in each iteration.
            metric_command (str): Shell command to run. Its exit code determines success (0 = pass).
            directives (str): Plain text research goals / instructions.
            experiments (int): Number of hypothesize -> edit -> eval loops to run.
            agent (str): The LLM backend to use (e.g., 'claude', 'openai').

        Returns:
            str: JSON summary of the autoloop run.
        """
        if os.getenv("AUTOLOOP_ALLOW_UNSANDBOXED", "false").lower() != "true":
            return json.dumps({"error": "AutoloopTool is currently restricted due to running unsandboxed. Set AUTOLOOP_ALLOW_UNSANDBOXED=true in your environment to override if you are in a trusted, airgapped environment."})

        try:
            from autoloop import AutoLoop
        except ImportError:
            return json.dumps({"error": "autoloop-ai is not installed. Please run `uv pip install autoloop-ai`."})

        self.logger.warning(f"AutoloopTool running locally on {target_file}. No Docker sandbox active!")

        if not os.path.exists(target_file):
            return json.dumps({"error": f"Target file {target_file} does not exist."})

        # Write program_instructions to a temporary file
        fd, directives_path = tempfile.mkstemp(suffix=".md", text=True)
        with os.fdopen(fd, 'w') as f:
            f.write(directives)

        # Create a synchronous metric that runs the command locally
        def local_metric(current_target_path: str) -> float:
            try:
                cmd_args = shlex.split(metric_command)
                result = CommandRunner.run(
                    cmd_args,
                    shell=False,
                    capture_output=True,
                    timeout=60
                )
                if result.returncode == 0:
                    return 1.0
                return 0.0
            except Exception as e:
                self.logger.error(f"Error running local metric: {e}")
                return 0.0

        results_dir = tempfile.mkdtemp(prefix="autoloop_results_")

        try:
            loop = AutoLoop(
                target=target_file,
                metric=local_metric,
                directives=directives_path,
                budget_seconds=60,
                agent=agent,
                higher_is_better=True,
                results_dir=results_dir,
                verbose=False
            )

            # Run experiments
            await asyncio.to_thread(loop.run, experiments=experiments)

            summary = {
                "target_file": target_file,
                "total_experiments": experiments,
                "best_score": loop.best_score,
                "improvements_found": sum(1 for r in loop.results if r.improved),
                "results_dir": loop.config.results_dir,
                "warning": "Evaluations were run locally without a sandbox."
            }
            return json.dumps(summary, indent=2)

        finally:
            if os.path.exists(directives_path):
                os.remove(directives_path)

if __name__ == "__main__":
    # Test script locally
    async def main():
        tool = AutoloopTool()
        with open("dummy.py", "w") as f:
            f.write("print('Hello')")

        # Test requires an LLM backend configured with ENV vars usually,
        # so this might fail if no API keys are set, but it tests the harness.
        res = await tool.run(
            target_file="dummy.py",
            metric_command="python dummy.py",
            directives="Make it print World",
            experiments=1
        )
        print(res)
        if os.path.exists("dummy.py"):
            os.remove("dummy.py")

    asyncio.run(main())
