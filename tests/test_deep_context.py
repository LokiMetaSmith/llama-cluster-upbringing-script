import asyncio
import os
import sys
import shutil
import re
from unittest.mock import MagicMock, AsyncMock

# Mock necessary modules before importing app
sys.modules["ultralytics"] = MagicMock()
sys.modules["pipecat.services.openai.llm"] = MagicMock()
sys.modules["pipecat.pipeline.runner"] = MagicMock()
sys.modules["pipecat.frames.frames"] = MagicMock()
sys.modules["consul.aio"] = MagicMock()

# Now import the class to test
from pipecatapp.workflow.runner import WorkflowRunner
from pipecatapp.workflow.nodes.base_nodes import InputNode, OutputNode
from pipecatapp.workflow.nodes.system_nodes import FileReadNode
from pipecatapp.workflow.nodes.llm_nodes import SimpleLLMNode
from pipecatapp.tools.context_upload_tool import ContextUploadTool

# Mock the LLM logic, but verify it receives the correct inputs
class MockSimpleLLMNode(SimpleLLMNode):
    async def execute(self, context):
        # We call the REAL logic to build the prompt, but we mock the network call
        # Since 'SimpleLLMNode.execute' is monolithic, we can't easily spy on just the network call
        # without refactoring.
        # So we will replicate the "Prompt Building" logic check here.

        node_id = self.config.get("id")

        if node_id == "PathExtractor":
            inputs = self.get_input(context, "user_text") or ""
            if "rules.txt" in inputs:
                self.set_output(context, "response", "rules.txt")
            else:
                self.set_output(context, "response", "NO_FILE")

        elif node_id == "ComprehensionStep":
            # Verification: Check if file_content was passed correctly
            file_content = self.get_input(context, "file_content")

            if not file_content:
                self.set_output(context, "response", "ERROR: No file content received.")
                return

            # Simulate LLM summarization
            self.set_output(context, "response", f"SUMMARY: {file_content[:20]}...")

        elif node_id == "ReasoningStep":
            # Verification: Check if summary AND full context were passed
            context_summary = self.get_input(context, "context_summary")
            file_content = self.get_input(context, "full_context") # Named 'full_context' in workflow yaml

            if not context_summary or not file_content:
                 self.set_output(context, "response", "ERROR: Missing context inputs.")
                 return

            self.set_output(context, "response", f"Final Answer based on {context_summary}")

# Patch the registry
from pipecatapp.workflow.nodes.registry import registry
registry._registry["SimpleLLMNode"] = MockSimpleLLMNode

async def test_deep_context_workflow():
    print("Testing Deep Context Workflow with Sandbox Security...")

    # 1. Setup Sandbox
    sandbox_dir = "/tmp/pipecat_context"
    if os.path.exists(sandbox_dir):
        shutil.rmtree(sandbox_dir)
    os.makedirs(sandbox_dir, exist_ok=True)

    # 2. Use the Tool to Upload a File
    upload_tool = ContextUploadTool()
    await upload_tool.execute(content="DEEP CONTEXT PROTOCOL: RHYME_MODE", filename="rules.txt")

    # Verify file exists
    expected_path = os.path.join(sandbox_dir, "rules.txt")
    if not os.path.exists(expected_path):
        print("FAILURE: Tool did not save file to sandbox.")
        return

    # 3. Run Workflow (Valid Access)
    runner = WorkflowRunner("pipecatapp/workflows/deep_context.yaml", runner_id="test_run_valid")
    global_inputs = {
        "user_text": "Please solve this using /deep rules.txt",
    }

    result = await runner.run(global_inputs)

    if result and "Final Answer based on SUMMARY: DEEP CONTEXT PROTOCO" in result:
        print("SUCCESS: Workflow correctly accessed the sandboxed file and passed it through the nodes.")
    else:
        print(f"FAILURE: Workflow failed. Result: {result}")

    # 4. Security Test: Try to read outside sandbox using FileReadNode directly
    print("\nTesting Directory Traversal Attack...")

    from pipecatapp.workflow.context import WorkflowContext

    ctx = WorkflowContext({"nodes": []})

    # We create a malicious node config
    node_config = {"id": "MaliciousReader", "type": "FileReadNode"}
    reader_node = FileReadNode(node_config)

    # We need to trick get_input. Since we can't easily mock context.global_inputs for a specific node input
    # without a full workflow setup, we will subclass for the test again.
    class MaliciousTestNode(FileReadNode):
        def get_input(self, context, name):
            return "../../../etc/passwd"

    malicious_node = MaliciousTestNode(node_config)
    await malicious_node.execute(ctx)

    output = ctx.node_outputs.get("MaliciousReader", {}).get("file_content")

    if "Error: Access denied" in output:
         print("SUCCESS: Security check blocked directory traversal.")
    else:
         print(f"FAILURE: Security check failed! Output: {output}")

    # 5. Security Test: Sibling Attack
    print("\nTesting Sibling Directory Attack...")

    class SiblingAttackNode(FileReadNode):
        def get_input(self, context, name):
            # Attempt to access a sibling folder that shares the prefix
            return "../pipecat_context_hack/secret.txt"

    sibling_node = SiblingAttackNode(node_config)
    await sibling_node.execute(ctx)
    output = ctx.node_outputs.get("MaliciousReader", {}).get("file_content")

    # It should either be Access Denied OR File Not Found (if it resolves safely but doesn't exist)
    # The key is that it shouldn't be read if it DID exist.
    # Since we can't easily create a sibling folder in /tmp in this environment reliably without side effects,
    # we rely on the Access Denied message or the fact that commonpath works.

    # If commonpath works, ../pipecat_context_hack resolves to /tmp/pipecat_context_hack
    # commonpath(/tmp/pipecat_context, /tmp/pipecat_context_hack) is /tmp
    # which != /tmp/pipecat_context. So it should deny access.

    if "Error: Access denied" in output:
         print("SUCCESS: Security check blocked sibling attack.")
    else:
         # Depending on implementation, it might say File Not Found if we allow it to look there?
         # But our implementation checks commonpath BEFORE existence.
         print(f"FAILURE: Sibling attack check failed! Output: {output}")


if __name__ == "__main__":
    asyncio.run(test_deep_context_workflow())
