import sys
import os

# Add pipecatapp to path to import the tool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pipecatapp')))

try:
    from tools.smol_agent_tool import SmolAgentTool
except ImportError as e:
    print(f"Error importing SmolAgentTool: {e}")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_smol_recovery.py <prompt>")
        sys.exit(1)

    prompt = sys.argv[1]
    print(f"Running smol_agent recovery with prompt: {prompt}")

    agent = SmolAgentTool()
    try:
        result = agent.run(prompt)
        print("Agent result:", result)
    except Exception as e:
        print(f"Agent failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
