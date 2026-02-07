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
        sandbox_dir = os.path.abspath("/tmp/pipecat_context")
        os.makedirs(sandbox_dir, exist_ok=True)

        if not file_path:
             self.set_output(context, "file_content", "Error: No file path provided.")
             return

        # Sanitize and resolve the full path
        try:
            # Join with sandbox and resolve absolute path
            full_path = os.path.abspath(os.path.join(sandbox_dir, file_path.strip()))

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
