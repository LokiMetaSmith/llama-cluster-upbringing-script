import os
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipecatapp.workflow.context import WorkflowContext
from pipecatapp.workflow.nodes.emperor_nodes import EmperorAgentNode

async def test_emperor_node():
    # Setup dummy context
    context = WorkflowContext(workflow_definition={"nodes": []})

    # We set inputs for the node
    # The node expects 'task' or 'user_text' in inputs

    # Since we can't easily mock the live LLM service here without
    # more complex mocking, we will test that the node initializes
    # and we can invoke the tools directly (unit test style)
    # and then try to run execute (integration style, might fail if no LLM).

    # 1. Test Tools
    from pipecatapp.workflow.nodes.emperor_nodes import TOOL_REGISTRY, resolve_abs_path

    print("Testing Tools...")

    # Test file creation
    test_file = "test_hello.txt"
    edit_tool = TOOL_REGISTRY["edit_file"]
    res = edit_tool(test_file, "", "Hello World")
    print(f"Create Result: {res}")

    assert res["action"] == "created_file"
    assert os.path.exists(test_file)

    # Test read
    read_tool = TOOL_REGISTRY["read_file"]
    res = read_tool(test_file)
    print(f"Read Result: {res}")
    assert res["content"] == "Hello World"

    # Test edit/replace
    res = edit_tool(test_file, "World", "Emperor")
    print(f"Edit Result: {res}")
    assert res["action"] == "edited"

    res = read_tool(test_file)
    assert res["content"] == "Hello Emperor"

    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    print("Tools Verification Passed.")

    # 2. Test Node Execution Structure
    # We will try to run it but expect it might fail on LLM connection if not running,
    # or just log error. This verifies the import and class structure works.

    print("\nTesting Node Execution (Dry Run)...")
    node = EmperorAgentNode(config={"id": "test_node"})

    # Inject input (mocking it directly in context outputs for test,
    # since Node.set_input doesn't exist and get_input logic is complex)
    # The clean way is to ensure node config has the input mapping.
    # But for a unit test, we can patch get_input or just test the logic that matters.

    # We'll just define the inputs in the node config so get_input finds them
    node.config["inputs"] = [{"name": "task", "value": "Say hello"}]

    try:
        # We set a very short timeout to not block if LLM is missing
        # Actually the node uses internal httpx.AsyncClient
        # We can't easily mock that without patching.
        # So we just instantiate it to ensure no syntax errors.
        pass
    except Exception as e:
        print(f"Node Init Error: {e}")

    print("Node instantiated successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(test_emperor_node())
        print("\nSUCCESS: Emperor Node Basic Tests Passed")
    except Exception as e:
        print(f"\nFAILURE: {e}")
        sys.exit(1)
