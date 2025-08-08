from openevolve import OpenEvolve
import os

# This is a placeholder for the real evolution logic.
# A real implementation would need to load the initial prompt from app.py,
# configure the OpenEvolve object, and run the evolution.

def get_initial_prompt():
    """
    This function would ideally read the initial prompt from app.py.
    For now, it returns a dummy prompt.
    """
    return "You are a helpful AI assistant."

async def run_evolution():
    # Ensure API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Please set OPENAI_API_KEY environment variable")

    # Initialize the system
    evolve = OpenEvolve(
        initial_program_path="initial_prompt.txt", # We'll create this file
        evaluation_file="prompt_engineering/evaluator.py",
        # config_path="path/to/config.yaml" # Optional config
    )

    # Create the initial prompt file
    with open("initial_prompt.txt", "w") as f:
        f.write(get_initial_prompt())

    # Run the evolution
    best_program = await evolve.run(iterations=10)
    print(f"Best program metrics:")
    for name, value in best_program.metrics.items():
        print(f"  {name}: {value:.4f}")

    print("\nBest prompt:")
    print(best_program.code)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_evolution())
