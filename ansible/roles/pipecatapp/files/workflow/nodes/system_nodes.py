import httpx
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
                if name.startswith("llamacpp-rpc-"):
                    service_names.add(name.replace("llamacpp-rpc-", ""))

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
