from openevolve import OpenEvolve
import os
import argparse
import asyncio

# This is a placeholder for the real evolution logic.
# A real implementation would need to load the initial prompt from app.py,
# configure the OpenEvolve object, and run the evolution.

async def run_evolution(test_case_path=None):
    """Initializes and runs the OpenEvolve algorithm.

    This function sets up the OpenEvolve environment, pointing it to the
    initial program (`app.py`) and the custom evaluator script. It then
    runs the evolutionary process for a set number of iterations to improve
    the program based on the evaluation results.

    Args:
        test_case_path (str, optional): The path to a specific YAML test case
            file to be used for the evaluation. If provided, this path is
            passed to the evaluator via an environment variable. Defaults to None.

    Raises:
        ValueError: If the OPENAI_API_KEY environment variable is not set.
        FileNotFoundError: If the initial program file cannot be found.
    """
    # Ensure API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Please set OPENAI_API_KEY environment variable")

    # If a dynamic test case is provided, set it as an environment variable
    # so the evaluator script can find it.
    if test_case_path:
        print(f"--- Using dynamic test case: {test_case_path} ---")
        os.environ["DYNAMIC_TEST_CASE_PATH"] = os.path.abspath(test_case_path)
    elif "DYNAMIC_TEST_CASE_PATH" in os.environ:
        # Clear any stale env var if not used in this run
        del os.environ["DYNAMIC_TEST_CASE_PATH"]


    # The initial program is the main application script
    initial_program_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "ansible", "roles", "pipecatapp", "files", "app.py")
    )

    if not os.path.exists(initial_program_path):
        raise FileNotFoundError(
            f"Initial program file not found at {initial_program_path}. "
            "Please ensure the file exists and the path is correct."
        )

    # Initialize the system
    evolve = OpenEvolve(
        initial_program_path=initial_program_path,
        evaluation_file="prompt_engineering/evaluator.py",
        # We can add a prompt to guide the evolution of the code
        prompt="""
You are an expert Python programmer tasked with improving a file to pass a series of tests.
The user will provide you with a file and the results of a test run.
Your task is to modify the file to fix the failing tests.
The provided file is a Python script that is part of a larger application.
The tests are run using pytest.
You should only output the full, complete, modified Python code. Do not add any extra explanations, notes, or markdown formatting.
Your goal is to make the tests pass. A fitness score of 1.0 means all tests passed.
""",
        # config_path="path/to/config.yaml" # Optional config
    )

    # Run the evolution
    best_program = await evolve.run(iterations=10)
    print("Best program metrics:")
    for name, value in best_program.metrics.items():
        print(f"  {name}: {value:.4f}")

    print("\nBest program code:")
    print(best_program.code)

    # Clean up the environment variable
    if "DYNAMIC_TEST_CASE_PATH" in os.environ:
        del os.environ["DYNAMIC_TEST_CASE_PATH"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evolve a prompt using OpenEvolve.")
    parser.add_argument(
        "--test-case",
        type=str,
        help="Path to a specific YAML test case file to use for evaluation."
    )
    args = parser.parse_args()

    asyncio.run(run_evolution(test_case_path=args.test_case))
