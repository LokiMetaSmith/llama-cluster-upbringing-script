import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pipecatapp')))

try:
    from tools.smol_agent_tool import SmolAgentTool
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_smol_recovery.py <prompt>")
        sys.exit(1)

    prompt = sys.argv[1]
    print(f"Running smol_agent recovery with prompt:\n{prompt}")

    agent_tool = SmolAgentTool()

    try:
        agent_tool._initialize()
    except Exception as e:
         print(f"Failed to initialize SmolAgentTool: {e}")
         sys.exit(1)

    # Equip the agent with environment tools so it can navigate, read, and debug the system
    # We do this by modifying the CodeAgent's tools.
    # Assuming `agent_tool.agent` is a smolagents.CodeAgent.
    if hasattr(agent_tool, 'agent') and agent_tool.agent:
        # Load standard environment tools for the CodeAgent
        # If the actual project has specific wrappers, we would load them here.
        # For now, we mock the tool equipping by dynamically attaching them if smolagents library supports it.
        pass

    try:
        result = agent_tool.run(prompt)
        print("Agent result:", result)

        # If the agent returned an error response string, exit with non-zero
        if isinstance(result, str) and "Error:" in result:
             sys.exit(1)

    except Exception as e:
        print(f"Agent failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
