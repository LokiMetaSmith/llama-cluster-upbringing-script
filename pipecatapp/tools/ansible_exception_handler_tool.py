import os
import logging
from pipecatapp.utils.ansible_triage import AnsibleTriageHandler

class AnsibleExceptionHandlerTool:
    """A tool that automates troubleshooting and patching of failing Ansible deployments in a sandbox.

    Given a context directory containing failure logs and rendered configurations,
    this tool reproduces the failure, uses LLM synthesis to determine root cause and upstream patches,
    reverse-compiles those patches, validates syntax/linting iteratively, and runs sandbox checks.
    It then isolates the fix on a new git branch, attempts to push to Opengist, and falls back to
    creating a local git bundle and detailed PR summary markdown locally if Opengist is offline.
    """
    def __init__(self):
        self.name = "ansible_exception_handler"
        self.description = (
            "Isolate, troubleshoot, reverse-compile, and generate verified Pull Requests or "
            "Git patches/bundles for failing Ansible tasks using LLM exception triage."
        )
        self.input_schema = {
            "type": "object",
            "properties": {
                "context_dir": {
                    "type": "string",
                    "description": "Absolute path to the temporary context directory containing failure logs and configs."
                },
                "task_id": {
                    "type": "string",
                    "description": "The unique Ansible task ID or name that failed (used to name branch and bundle)."
                }
            },
            "required": ["context_dir", "task_id"]
        }

    async def run(self, context_dir: str, task_id: str) -> str:
        """Runs the Ansible Exception Handler and Git PR loop asynchronously.

        Args:
            context_dir (str): The path to the failure context files.
            task_id (str): The unique ID of the failed task.

        Returns:
            str: A formatted string summary of the triage results, files updated, and Git delivery status.
        """
        logger = logging.getLogger("AnsibleExceptionHandlerTool")
        logger.info(f"Invoking Ansible Exception Handler Tool for task ID: {task_id}")

        if not os.path.exists(context_dir):
            return f"Error: Specified context directory '{context_dir}' does not exist."

        try:
            handler = AnsibleTriageHandler(context_dir=context_dir, task_id=task_id)
            result = await handler.run_triage()

            summary = []
            summary.append(f"Triage status: {result.get('status')}")
            summary.append(f"Root Cause Analysis:\n{result.get('root_cause')}")
            summary.append(f"Applied Upstream Fixes: {', '.join(result.get('applied_files', []))}")
            summary.append(f"Verification Check: {result.get('verification_status')}")

            if "pushed_url" in result:
                summary.append(f"Pushed to Opengist Git Remote: {result.get('pushed_url')}")
            elif "bundle_path" in result:
                summary.append(f"Git Bundle Created (Local Fallback): {result.get('bundle_path')}")

            if "pr_summary_path" in result:
                summary.append(f"Pull Request Markdown Summary Created: {result.get('pr_summary_path')}")

            return "\n\n".join(summary)

        except Exception as e:
            logger.exception(f"Exception during tool execution: {e}")
            return f"Error: Ansible Exception Handler execution failed: {e}"
