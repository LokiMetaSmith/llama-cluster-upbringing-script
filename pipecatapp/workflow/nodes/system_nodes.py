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

@registry.register
class SleepNode(Node):
    """A node that sleeps for a configurable amount of time."""
    async def execute(self, context: WorkflowContext):
        import asyncio
        seconds = self.config.get("config", {}).get("seconds", 1)
        try:
            override = self.get_input(context, "override_seconds")
            if override is not None:
                seconds = float(override)
        except ValueError:
            pass

        await asyncio.sleep(seconds)
        self.set_output(context, "status", f"Slept for {seconds} seconds")

@registry.register
class MegafileDecompositionNode(Node):
    """A node that checks the megafile queue and refactors bloated files."""

    async def execute(self, context: WorkflowContext):
        import json
        import os
        from pipecatapp.tools.ast_editor_tool import ASTEditorTool
        from pipecatapp.tools.file_editor_tool import FileEditorTool
        from pipecatapp.llm_clients import get_llm_client
        import fcntl

        # Determine base directory; default to CWD if not specified in context
        base_dir = context.global_inputs.get("root_dir", os.getcwd())
        queue_path = os.path.join(base_dir, ".liminal", "megafiles_queue.json")

        if not os.path.exists(queue_path):
            context.set_output("status", "No megafiles queued")
            return

        # Open with file lock to prevent race conditions during pop
        with open(queue_path, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                queue = json.load(f)
            except json.JSONDecodeError:
                queue = []

            if not queue:
                fcntl.flock(f, fcntl.LOCK_UN)
                context.set_output("status", "No megafiles queued")
                return

            target_file = queue.pop(0)

            # Immediately write the popped queue back to disk while locked
            f.seek(0)
            f.truncate()
            json.dump(queue, f)
            fcntl.flock(f, fcntl.LOCK_UN)

        # Lock the file logic could go here via Keystone Polyphony baton

        file_editor = FileEditorTool()
        ast_editor = ASTEditorTool()

        # 1. Read the file
        content = file_editor.read_file(target_file)
        if "Error" in content:
            context.set_output("status", f"Failed to read megafile: {content}")
            return

        # 2. Use a frontier model to plan the decomposition
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
