import httpx
import logging
import json
import os
from .registry import registry
from ..node import Node
from ..context import WorkflowContext

@registry.register
class TaskyAuditNode(Node):
    """
    Evaluates an execution result against a task checklist defined in Markdown.
    Updates the markdown with completed items, outputs an audit report, and a boolean indicating if all are complete.
    """
    def __init__(self, config):
        super().__init__(config)
        self.expected_inputs = {"task_markdown", "execution_result"}
        self.expected_outputs = {"updated_markdown", "all_completed", "audit_report"}

    async def execute(self, context: WorkflowContext):
        task_markdown = self.get_input(context, "task_markdown")
        execution_result = self.get_input(context, "execution_result")

        if not task_markdown:
            self.set_output(context, "updated_markdown", "")
            self.set_output(context, "all_completed", False)
            self.set_output(context, "audit_report", "Error: No task_markdown provided.")
            return

        if not execution_result:
            self.set_output(context, "updated_markdown", task_markdown)
            self.set_output(context, "all_completed", False)
            self.set_output(context, "audit_report", "Error: No execution_result provided.")
            return

        node_config = self.config.get("config", {})
        target_service = node_config.get("model_service", self.config.get("model_service", "rpc-main"))

        consul_http_addr = context.global_inputs.get("consul_http_addr") or os.getenv("CONSUL_HTTP_ADDR")

        updated_markdown = task_markdown
        all_completed = False
        audit_report = "Error: Could not reach LLM service."

        if consul_http_addr:
            try:
                # Attempt to get the token, handle imports properly
                token = ""
                try:
                    from pipecatapp.utils import secret_manager
                    token = secret_manager.get_secret("CONSUL_HTTP_TOKEN") or ""
                except ImportError:
                    token = os.getenv("CONSUL_HTTP_TOKEN", "")

                headers = {"X-Consul-Token": token} if token else {}

                async with httpx.AsyncClient(headers=headers) as client:
                    response = await client.get(f"{consul_http_addr}/v1/health/service/{target_service}?passing")
                    response.raise_for_status()
                    services = response.json()

                    if not services:
                        audit_report = f"Error: Service {target_service} not found."
                    else:
                        address = services[0]['Service']['Address']
                        port = services[0]['Service']['Port']
                        base_url = f"http://{address}:{port}/v1"
                        chat_url = f"{base_url}/chat/completions"

                        system_prompt = (
                            "You are a meticulous Tasky PM agent. Your job is to audit execution results against a markdown task specification.\n"
                            "You must output a JSON object with three keys:\n"
                            "1. 'updated_markdown': The original markdown but with checklist items `[ ]` updated to `[x]` if and only if the execution result explicitly demonstrates they are completed.\n"
                            "2. 'all_completed': A boolean true if all checklist criteria in the markdown are now marked `[x]`, otherwise false.\n"
                            "3. 'audit_report': A short explanation of what was verified, and what is still missing or incomplete.\n"
                            "IMPORTANT: Output ONLY valid JSON, nothing else."
                        )

                        user_prompt = f"TASK MARKDOWN:\n```markdown\n{task_markdown}\n```\n\nEXECUTION RESULT:\n```\n{execution_result}\n```\n\nPlease audit."

                        messages = [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]

                        payload = {
                            "model": target_service,
                            "messages": messages,
                            "temperature": 0.1,
                            "response_format": {"type": "json_object"}
                        }

                        res = await client.post(chat_url, json=payload, timeout=60)
                        res.raise_for_status()

                        response_content = res.json()["choices"][0]["message"]["content"].strip()

                        try:
                            # Strip backticks if any
                            if response_content.startswith("```json"):
                                response_content = response_content[7:]
                            if response_content.endswith("```"):
                                response_content = response_content[:-3]

                            parsed_json = json.loads(response_content.strip())
                            updated_markdown = parsed_json.get("updated_markdown", task_markdown)
                            all_completed = parsed_json.get("all_completed", False)
                            audit_report = parsed_json.get("audit_report", "Could not extract audit report.")
                        except json.JSONDecodeError:
                            audit_report = f"Failed to parse LLM JSON output. Raw output:\n{response_content}"

            except Exception as e:
                logging.error(f"Error in TaskyAuditNode: {e}")
                audit_report = f"Error during audit execution: {e}"

        self.set_output(context, "updated_markdown", updated_markdown)
        self.set_output(context, "all_completed", all_completed)
        self.set_output(context, "audit_report", audit_report)
