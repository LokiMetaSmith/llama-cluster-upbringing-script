from .registry import registry
from ..node import Node
from ..context import WorkflowContext
import os
import httpx
import logging
from typing import Dict, Any

@registry.register
class RalphLoopNode(Node):
    """
    Implements a worker-verifier loop (Worker -> Verifier -> Feedback) specifically
    for complex coding tasks, allowing automatic trial-and-error iterations.
    """
    async def execute(self, context: WorkflowContext):
        task = self.get_input(context, "task")
        if not task:
            self.set_output(context, "final_response", "Error: No task provided.")
            return

        # Configurations
        node_config = self.config.get("config", {})
        max_iterations = node_config.get("max_iterations", 3)
        target_service = node_config.get("model_service", "rpc-main")

        consul_http_addr = context.global_inputs.get("consul_http_addr") or os.getenv("CONSUL_HTTP_ADDR")
        base_url = "http://127.0.0.1:8081/v1" # Fallback

        if consul_http_addr:
            try:
                token = os.getenv("CONSUL_HTTP_TOKEN", "")
                headers = {"X-Consul-Token": token.strip()} if token else {}
                async with httpx.AsyncClient(headers=headers) as client:
                    response = await client.get(f"{consul_http_addr}/v1/health/service/{target_service}?passing")
                    if response.status_code == 200:
                        services = response.json()
                        if services:
                            svc = services[0]['Service']
                            base_url = f"http://{svc['Address']}:{svc['Port']}/v1"
            except Exception as e:
                logging.warning(f"Could not discover {target_service}: {e}")

        chat_url = f"{base_url}/chat/completions"

        from pipecatapp.tools.code_runner_tool import CodeRunnerTool
        runner = CodeRunnerTool()

        conversation = [
            {"role": "system", "content": "You are an expert Python programmer. Write code to solve the given task. Output only the raw Python code, without any markdown formatting or explanation."},
            {"role": "user", "content": task}
        ]

        async with httpx.AsyncClient() as client:
            for i in range(max_iterations):
                logging.info(f"RalphLoopNode Iteration {i+1}/{max_iterations}")

                # Worker: Write code
                try:
                    resp = await client.post(
                        chat_url,
                        json={
                            "model": target_service,
                            "messages": conversation,
                            "temperature": 0.2
                        },
                        timeout=120
                    )
                    resp.raise_for_status()
                    generated_code = resp.json()["choices"][0]["message"]["content"]

                    # Clean up the output if the model added markdown
                    if generated_code.startswith("```python"):
                        generated_code = generated_code[len("```python"):].strip()
                    elif generated_code.startswith("```"):
                        generated_code = generated_code[len("```"):].strip()
                    if generated_code.endswith("```"):
                        generated_code = generated_code[:-3].strip()

                except Exception as e:
                    self.set_output(context, "final_response", f"LLM Error during code generation: {e}")
                    return

                # Verifier: Run the code
                logging.info("RalphLoopNode: Verifying code...")
                exec_result = runner.run_code_in_sandbox(generated_code, language="python")

                if isinstance(exec_result, str):
                     if exec_result.startswith("Error") or "Traceback" in exec_result:
                          feedback = f"The code execution failed with the following output/error:\n{exec_result}\n\nPlease fix the error and rewrite the code."
                          conversation.append({"role": "assistant", "content": generated_code})
                          conversation.append({"role": "user", "content": feedback})
                     else:
                          # Success!
                          self.set_output(context, "final_response", f"Success! Output:\n{exec_result}\n\nCode:\n{generated_code}")
                          return
                else:
                     # For more complex execution results depending on what runner returns
                     self.set_output(context, "final_response", f"Execution returned unexpected format: {exec_result}")
                     return

            self.set_output(context, "final_response", f"Failed to generate working code after {max_iterations} iterations. Last error:\n{exec_result}\n\nLast code:\n{generated_code}")
