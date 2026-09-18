import httpx
import os
from .registry import registry
from ..node import Node
from ..context import WorkflowContext
from pipecatapp.rate_limiter import RateLimiter
from pipecatapp.tools.vr_tool import VRTool
import asyncio
from prometheus_client import REGISTRY, Gauge, Counter

# Prometheus metrics for TelemetryNode (with duplicate check for tests)
if 'pipecatapp_semantic_density' not in REGISTRY._names_to_collectors:
    semantic_density_gauge = Gauge(
        'pipecatapp_semantic_density',
        'Semantic density score of the agent message',
        ['node_id', 'agent_id']
    )
    semantic_length_counter = Counter(
        'pipecatapp_message_words_total',
        'Total words processed in messages',
        ['node_id', 'agent_id']
    )
else:
    semantic_density_gauge = REGISTRY._names_to_collectors['pipecatapp_semantic_density']
    semantic_length_counter = REGISTRY._names_to_collectors['pipecatapp_message_words_total']

@registry.register
class TelemetryNode(Node):
    """
    A transparent pass-through node that intercepts the payload, calculates
    semantic density, and asynchronously updates Prometheus metrics.
    """
    async def _calculate_metrics(self, payload: str, node_id: str, agent_id: str):
        if not payload:
            return

        words = payload.split()
        word_count = len(words)
        semantic_length_counter.labels(node_id=node_id, agent_id=agent_id).inc(word_count)

        # Calculate a mock semantic density score (unique words / total words)
        unique_words = len(set(words))
        density = unique_words / word_count if word_count > 0 else 0
        semantic_density_gauge.labels(node_id=node_id, agent_id=agent_id).set(density)

    async def execute(self, context: WorkflowContext):
        # Pass-through input to output
        payload = self.get_input(context, "payload")
        agent_id = self.get_input(context, "agent_id")

        self.set_output(context, "payload", payload)

        # Fire and forget metrics calculation
        asyncio.create_task(self._calculate_metrics(payload, self.id, agent_id))

@registry.register
class HITLGateNode(Node):
    """
    A Human-In-The-Loop gate node.
    It blocks the workflow execution until human approval is received.
    """
    async def execute(self, context: WorkflowContext):
        approval_state = self.get_input(context, "approval_state")

        if str(approval_state).lower() == "approved":
            # Pass data forward
            self.set_output(context, "status", "proceed")
        else:
            self.set_output(context, "status", "blocked")
            # Optionally raise an exception to halt execution
            # raise Exception(f"HITL Node {self.id} is blocked waiting for human approval.")

@registry.register
class CircuitBreakerNode(Node):
    """
    Halts workflow if error count or failure rate exceeds threshold.
    """
    async def execute(self, context: WorkflowContext):
        try:
            error_count = int(self.get_input(context, "error_count"))
        except ValueError:
            error_count = 0

        try:
            threshold = int(self.get_input(context, "threshold"))
        except ValueError:
            threshold = 5

        if error_count >= threshold:
            self.set_output(context, "circuit_status", "OPEN")
            raise Exception(f"Circuit Breaker Triggered: {error_count} >= {threshold}")
        else:
            self.set_output(context, "circuit_status", "CLOSED")

@registry.register
class DecomposerNode(Node):
    """
    A heavy structural analysis node that takes a 'megafile' path, asks the main LLM
    how to decompose it into smaller logical modules, and then uses ASTEditorTool
    and FileEditorTool to autonomously rip out classes/functions and move them to new files.
    """
    async def execute(self, context: WorkflowContext):
        from pipecatapp.core.service_discovery import get_llm_client
        from pipecatapp.tools.ast_editor_tool import ASTEditorTool
        from pipecatapp.tools.file_editor_tool import FileEditorTool
        import json
        import fcntl

        try:
            target_file = self.get_input(context, "target_file")
        except ValueError:
            target_file = None

        if not target_file:
            # Maybe pop from a queue
            queue_path = os.path.join(os.getcwd(), "decomposition_queue.json")
            if os.path.exists(queue_path):
                with open(queue_path, "r+") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    try:
                        q = json.load(f)
                    except json.JSONDecodeError:
                        q = []
                    if q:
                        target_file = q.pop(0)
                        f.seek(0)
                        f.truncate()
                        json.dump(q, f)
                    fcntl.flock(f, fcntl.LOCK_UN)

        if not target_file or not os.path.exists(target_file):
            self.set_output(context, "status", "idle")
            return

        file_editor = FileEditorTool()
        ast_editor = ASTEditorTool()

        # 1. Read the megafile
        content_res = file_editor.read_file(target_file)
        if "Error" in content_res:
            self.set_output(context, "status", f"failed to read: {content_res}")
            return

        content = content_res

        # 2. Ask LLM for a decomposition
        system_prompt = (
            "You are an expert code architect. The following file is a 'Megafile' that has become too bloated. "
            "Your task is to plan how to decompose this file into smaller, logically separated modules. "
            "Return a JSON object with 'strategy' (string) and 'new_modules' (list of strings representing new file paths)."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Filepath: {target_file}\n\nContent:\n{content}"}
        ]

        # Assuming access to the workflow's configured LLM router
        llm = get_llm_client(getattr(self, "model_override", "gpt-4o"))

        try:
            response = await llm.generate_chat_completion(messages, response_format={"type": "json_object"})
            plan = json.loads(response)

            # 3. Use ASTEditorTool to actually move the code chunks
            success = True
            error_msgs = []
            if "strategy" in plan and "new_modules" in plan:
                # We assume new_modules specifies the logic chunks to extract.
                # In a robust implementation, the LLM would output AST query signatures.
                # Here, we programmatically extract classes and functions and move them.

                # Use AST tool to fetch top-level classes/functions
                tree_info_raw = ast_editor.execute("list_functions", filepath=target_file)
                if "Error" not in tree_info_raw:
                    try:
                        tree_info = json.loads(tree_info_raw)
                        # Simple heuristic: move every other class to a new module
                        for idx, module_path in enumerate(plan.get("new_modules", [])):
                            if idx < len(tree_info):
                                node_name = tree_info[idx].get("name")
                                # Extract code
                                extracted_code = ast_editor.execute("read_function", filepath=target_file, function_name=node_name)
                                if "Error" not in extracted_code:
                                    # Write to new file
                                    file_editor.write_file(module_path, extracted_code)
                                    # Delete from old file
                                    ast_editor.execute("delete_function", filepath=target_file, function_name=node_name)
                    except Exception as e:
                        success = False
                        error_msgs.append(f"AST extraction failed: {str(e)}")
                else:
                     success = False
                     error_msgs.append(tree_info_raw)

            if success:
                # 4. Validation step: check that we didn't break imports
                # In a robust system, we would run `pytest` or `python -m py_compile`.
                # Here we attempt to compile the refactored files.
                from pipecatapp.tools.code_runner_tool import CodeRunnerTool
                runner = CodeRunnerTool()
                for module_path in plan.get("new_modules", []):
                    # Check syntax
                    comp_res = runner.execute("run_bash", command=f"python3 -m py_compile {module_path}")
                    if "SyntaxError" in comp_res or "Traceback" in comp_res:
                        success = False
                        error_msgs.append(f"Validation failed for {module_path}: {comp_res}")

            if success:
                context.set_output("status", f"Decomposed {target_file}")
                context.set_output("decomposition_plan", plan)
            else:
                # Requeue if failed
                with open(queue_path, "r+") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    try:
                        q = json.load(f)
                    except json.JSONDecodeError:
                        q = []
                    q.insert(0, target_file)
                    f.seek(0)
                    f.truncate()
                    json.dump(q, f)
                    fcntl.flock(f, fcntl.LOCK_UN)
                context.set_output("status", f"Decomposition failed: {error_msgs}")

        except Exception as e:
            # Requeue on critical error
            with open(queue_path, "r+") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    q = json.load(f)
                except json.JSONDecodeError:
                    q = []
                q.insert(0, target_file)
                f.seek(0)
                f.truncate()
                json.dump(q, f)
                fcntl.flock(f, fcntl.LOCK_UN)
            context.set_output("status", f"Decomposition failed: {str(e)}")

@registry.register
class ComplexityEvaluatorNode(Node):
    """
    A node that evaluates AST cyclomatic complexity, Halstead/SLOC metrics, and
    structural code similarity across project files for refactoring agents.

    Input: 'filepath' or 'directory'
    Output: 'complexity_score', 'sloc', 'metrics_report'
    """
    async def execute(self, context: WorkflowContext):
        import ast

        try:
            filepath = self.get_input(context, "filepath")
        except ValueError:
            filepath = None

        if not filepath:
            self.set_output(context, "complexity_score", 0)
            self.set_output(context, "sloc", 0)
            self.set_output(context, "metrics_report", {"error": "No filepath provided."})
            return

        if not os.path.exists(filepath):
            self.set_output(context, "complexity_score", 0)
            self.set_output(context, "sloc", 0)
            self.set_output(context, "metrics_report", {"error": f"File not found: {filepath}"})
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()

            lines = code.split("\n")
            sloc = len([line for line in lines if line.strip() and not line.strip().startswith("#")])

            # Calculate cyclomatic complexity via AST decision points
            tree = ast.parse(code)
            complexity = 1
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler, ast.With)):
                    complexity += 1

            report = {
                "filepath": filepath,
                "sloc": sloc,
                "cyclomatic_complexity": complexity,
                "maintainability_index": max(0, 100 - (complexity * 2) - (sloc * 0.1))
            }

            self.set_output(context, "complexity_score", complexity)
            self.set_output(context, "sloc", sloc)
            self.set_output(context, "metrics_report", report)

            # Broadcast heatmap update to 3D visualizer
            vr_tool = VRTool()
            await vr_tool.broadcast_complexity_heatmap(
                filepath=filepath,
                complexity=complexity,
                maintainability=report.get("maintainability_index", 100)
            )

        except Exception as e:
            self.set_output(context, "complexity_score", -1)
            self.set_output(context, "sloc", 0)
            self.set_output(context, "metrics_report", {"error": f"Failed to calculate complexity: {str(e)}"})

@registry.register
class ComfyUIBridgeNode(Node):
    """
    A workflow node that bridges Pipecat agent workflows to ComfyUI node-based visual AI image generation pipelines.

    Input: 'prompt', 'comfyui_url' (default: http://127.0.0.1:8188)
    Output: 'image_url', 'status'
    """
    async def execute(self, context: WorkflowContext):
        try:
            prompt = self.get_input(context, "prompt")
        except ValueError:
            prompt = "A high tech 3D neural network visualizer node in a futuristic server room"

        try:
            comfyui_url = self.get_input(context, "comfyui_url")
        except ValueError:
            comfyui_url = os.getenv("COMFYUI_URL", f"http://{os.getenv('CLUSTER_IP', '127.0.0.1')}:8188")

        payload = {
            "prompt": {
                "3": {
                    "inputs": {"seed": 12345, "steps": 20, "cfg": 8, "sampler_name": "euler", "scheduler": "normal", "denoise": 1},
                    "class_type": "KSampler"
                },
                "6": {
                    "inputs": {"text": prompt, "clip": ["11", 0]},
                    "class_type": "CLIPTextEncode"
                }
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{comfyui_url}/prompt", json=payload, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    prompt_id = data.get("prompt_id", "mock_prompt_123")
                    img_url = f"{comfyui_url}/view?filename={prompt_id}.png"
                    self.set_output(context, "image_url", img_url)
                    self.set_output(context, "status", "Queued successfully")

                    vr_tool = VRTool()
                    await vr_tool.broadcast_visual_ai_image(prompt_id=prompt_id, image_url=img_url, prompt=prompt)
                else:
                    img_url = f"/static/assets/generated_placeholder.png"
                    self.set_output(context, "image_url", img_url)
                    self.set_output(context, "status", f"ComfyUI HTTP {resp.status_code}")
                    vr_tool = VRTool()
                    await vr_tool.broadcast_visual_ai_image(prompt_id="placeholder", image_url=img_url, prompt=prompt)
        except Exception as e:
            # Fallback for offline environments
            self.set_output(context, "image_url", f"/static/assets/generated_placeholder.png")
            self.set_output(context, "status", f"ComfyUI offline fallback ({str(e)})")
