from openevolve import OpenEvolve
import os

# This is a placeholder for the real evolution logic.
# A real implementation would need to load the initial prompt from app.py,
# configure the OpenEvolve object, and run the evolution.

async def run_evolution():
    # Ensure API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Please set OPENAI_API_KEY environment variable")

    # The initial prompt is the router prompt from the main application
    initial_prompt_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "prompts", "router.txt")
    )

    if not os.path.exists(initial_prompt_path):
        raise FileNotFoundError(
            f"Initial prompt file not found at {initial_prompt_path}. "
            "Please ensure the file exists and the path is correct."
        )

    # Initialize the system
    evolve = OpenEvolve(
        initial_program_path=initial_prompt_path,
        evaluation_file="prompt_engineering/evaluator.py",
        # config_path="path/to/config.yaml" # Optional config
    )

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
