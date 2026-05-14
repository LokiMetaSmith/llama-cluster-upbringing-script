import httpx
import os
from .registry import registry
from ..node import Node
from ..context import WorkflowContext

@registry.register
class ConsulServiceDiscoveryNode(Node):
    """A node that discovers available services from a Consul agent."""
    async def execute(self, context: WorkflowContext):
        consul_http_addr = context.global_inputs.get("consul_http_addr")
        if not consul_http_addr:
            raise ValueError("Consul HTTP address not provided in global inputs.")

        service_names = set()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{consul_http_addr}/v1/catalog/services")
                response.raise_for_status()
                services = response.json()

            for name, service_info in services.items():
                # This logic can be expanded to be more sophisticated
                if name.startswith("rpc-"):
                    service_names.add(name.replace("rpc-", ""))

                tags = service_info.get("Tags", [])
                if "expert" in tags:
                    for tag in tags:
                        if tag not in ["expert", "llm"]:
                            service_names.add(tag)
                            break

        except httpx.RequestError as e:
            # It's better to log an error and continue with an empty list
            # than to crash the whole workflow.
            print(f"Could not connect to Consul for expert discovery: {e}")

        self.set_output(context, "available_services", sorted(list(service_names)))

@registry.register
class FileReadNode(Node):
    """A node that safely reads a text file from the context sandbox.
    Input: 'file_path' (relative to sandbox)
    Output: 'file_content'
    """
    async def execute(self, context: WorkflowContext):
        file_path = self.get_input(context, "file_path")

        # Define the sandbox directory
        sandbox_dir = os.path.realpath("/tmp/pipecat_context")
        os.makedirs(sandbox_dir, exist_ok=True)

        if not file_path:
             self.set_output(context, "file_content", "Error: No file path provided.")
             return

        # Sanitize and resolve the full path
        try:
            # Join with sandbox and resolve absolute path
            full_path = os.path.realpath(os.path.join(sandbox_dir, file_path.strip()))

            # Security Check: Ensure the resolved path is within the sandbox directory
            # Using commonpath handles sibling directory attacks (e.g., sandbox vs sandbox_hack)
            # This is safer than startswith(sandbox_dir)
            if os.path.commonpath([sandbox_dir, full_path]) != sandbox_dir:
                self.set_output(context, "file_content", f"Error: Access denied. File path '{file_path}' attempts to escape the sandbox directory.")
                return

            if not os.path.exists(full_path):
                 self.set_output(context, "file_content", f"Error: File not found in sandbox: {file_path}")
                 return

            if not os.path.isfile(full_path):
                 self.set_output(context, "file_content", f"Error: Path is not a file: {file_path}")
                 return

            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.set_output(context, "file_content", content)

        except Exception as e:
            self.set_output(context, "file_content", f"Error reading file: {e}")

@registry.register
class DreamNode(Node):
    """A node that fetches recent memories/history via the Archivist service to enable model dreaming."""
    async def execute(self, context: WorkflowContext):
        query = self.get_input(context, "query") or "recent important events and conversations"
        archivist_url = self.get_input(context, "archivist_url") or f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8008"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{archivist_url}/research",
                    json={"query": query, "max_steps": 5},
                    timeout=120
                )
                if response.status_code == 200:
                    data = response.json()
                    content = data.get("content", "No content returned.")
                    self.set_output(context, "history", content)
                else:
                    self.set_output(context, "history", f"Error querying Archivist: {response.status_code} - {response.text}")
        except Exception as e:
            self.set_output(context, "history", f"Failed to connect to Archivist service: {e}")

@registry.register
class FileWriteNode(Node):
    """A node that safely writes text to a file in the context sandbox.
    Input: 'file_path' (relative to sandbox), 'file_content'
    Output: 'write_status'
    """
    async def execute(self, context: WorkflowContext):
        # file_path might come from config or input
        file_path = self.get_input(context, "file_path") or self.config.get("config", {}).get("file_path")
        file_content = self.get_input(context, "file_content")

        sandbox_dir = os.path.realpath("/tmp/pipecat_context")
        os.makedirs(sandbox_dir, exist_ok=True)

        if not file_path:
             self.set_output(context, "write_status", "Error: No file path provided.")
             return

        try:
            full_path = os.path.realpath(os.path.join(sandbox_dir, file_path.strip()))

            if os.path.commonpath([sandbox_dir, full_path]) != sandbox_dir:
                self.set_output(context, "write_status", f"Error: Access denied. File path '{file_path}' attempts to escape the sandbox directory.")
                return

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(file_content or "")
            self.set_output(context, "write_status", f"Successfully wrote to {full_path}")

        except Exception as e:
            self.set_output(context, "write_status", f"Error writing file: {e}")

@registry.register
class HumanApprovalNode(Node):
    """A node that pauses execution to request human approval for high-risk actions.
    Input: 'prompt', 'action_details'
    Output: 'approval_status', 'human_feedback'
    """
    async def execute(self, context: WorkflowContext):
        try:
            prompt = self.get_input(context, "prompt")
        except ValueError:
            prompt = "Human approval required for action."

        try:
            action_details = self.get_input(context, "action_details")
        except ValueError:
            action_details = "No details provided."

        # Check if auto-approved via global inputs (for testing/automation)
        if context.global_inputs.get("human_approval_granted") is True:
            self.set_output(context, "approval_status", "approved")
            self.set_output(context, "human_feedback", "Auto-approved via global input.")
            return

        if context.global_inputs.get("human_approval_granted") is False:
            self.set_output(context, "approval_status", "rejected")
            self.set_output(context, "human_feedback", "Auto-rejected via global input.")
            raise ValueError(f"Workflow execution halted: Human approval rejected. Action: {action_details}")

        # Fallback to CLI interaction
        import asyncio
        import os

        print(f"\n=== HUMAN APPROVAL REQUIRED ===")
        print(f"Prompt: {prompt}")
        print(f"Action Details: {action_details}")
        print(f"===============================\n")

        loop = asyncio.get_event_loop()
        try:
            # We use run_in_executor to avoid blocking the async event loop with input()
            user_input = await loop.run_in_executor(None, input, "Approve this action? (yes/no): ")
        except EOFError:
            user_input = "no"

        user_input = user_input.strip().lower()
        if user_input in ['y', 'yes']:
            self.set_output(context, "approval_status", "approved")
            self.set_output(context, "human_feedback", "Approved by human via CLI.")
        else:
            self.set_output(context, "approval_status", "rejected")
            self.set_output(context, "human_feedback", "Rejected by human via CLI.")
            raise ValueError(f"Workflow execution halted: Human approval rejected. Action: {action_details}")
