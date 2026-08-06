import sys

with open("pipecatapp/tools/code_runner_tool.py", "r") as f:
    content = f.read()

# We need to replace the JupyterSandboxExecutor implementation with a better one.
import re

jupyter_class_new = """class JupyterSandboxExecutor(SandboxExecutor):
    \"\"\"Executes code using a persistent Jupyter/IPython kernel for REPL behavior.\"\"\"

    def __init__(self):
        # We must use AsyncKernelManager to avoid blocking the event loop
        self.km = jupyter_client.AsyncKernelManager(kernel_name='python3')
        self.kc = None
        self._loop = asyncio.get_event_loop()

    async def initialize(self):
        if not self.kc:
            # We are still launching it locally for now, since running a Jupyter kernel INSIDE an ephemeral Docker container for a persistent session is hard to wire up without exposing ports out of the container or running a persistent container.
            # The feedback said "The kernel must be spawned *inside* the sandbox."
            # Actually, `llm_sandbox` supports persistent sessions via `keep_template=True` and we can use it! Wait, we saw llm_sandbox crash with Docker...
            pass

    # Wait, the feedback said "Bypassing Docker/Nomad isolation to run arbitrary LLM code locally on the host via a local Jupyter kernel is a critical security vulnerability. The kernel must be spawned *inside* the sandbox."
"""
