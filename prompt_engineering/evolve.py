from openevolve import OpenEvolve
import os
import argparse
import asyncio
import json
import random
import glob

def select_parent_from_archive():
    """Selects a parent agent from the archive using weighted random sampling.

    This function scans the agent archive for metadata files, extracts their
    fitness scores, and uses these scores to perform a weighted random

    selection. Agents with higher fitness have a higher chance of being
    selected. This encourages "survival of the fittest" while still allowing
    for exploration from less optimal agents.

    If the archive is empty, it returns the path to the original `app.py`
    script as the seed for the first generation.

    Returns:
        tuple: A tuple containing the path to the selected parent's code
               and the parent's ID (or None for the initial seed).
    """
    archive_dir = os.path.join(os.path.dirname(__file__), "archive")
    meta_files = glob.glob(os.path.join(archive_dir, "*.json"))

    if not meta_files:
        print("--- Archive is empty. Seeding evolution with initial app.py ---")
        initial_program_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "ansible", "roles", "pipecatapp", "files", "app.py")
        )
        return initial_program_path, None

    agents = []
    weights = []
    for meta_file in meta_files:
        with open(meta_file, 'r') as f:
            meta = json.load(f)
            # We add a small epsilon to fitness to allow agents with 0.0 fitness to be selected
            fitness = meta.get("fitness", 0.0) + 1e-6
            agent_id = os.path.basename(meta_file).replace(".json", "")
            agents.append(agent_id)
            weights.append(fitness)

    selected_agent_id = random.choices(agents, weights=weights, k=1)[0]
    parent_program_path = os.path.join(archive_dir, f"{selected_agent_id}.py")
    print(f"--- Selected parent agent {selected_agent_id} with fitness {weights[agents.index(selected_agent_id)]-1e-6:.4f} ---")
    return parent_program_path, selected_agent_id


async def run_evolution(test_case_path=None):
    """Initializes and runs the OpenEvolve algorithm with a DGM-style archive.

    This function implements the core loop of the Darwin Gödel Machine. It:
    1. Selects a parent agent from the archive based on fitness.
    2. Passes the parent's ID to the evaluator via an environment variable
       to establish lineage.
    3. Uses OpenEvolve to mutate the selected parent.
    4. The evaluator saves the new agent and its metadata (including the
       parent's ID) back to the archive.
    5. The process repeats, creating a branching tree of agent evolution.
    """
    # Ensure API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Please set OPENAI_API_KEY environment variable")

    parent_id = None
    try:
        # Set dynamic test case if provided
        if test_case_path:
            os.environ["DYNAMIC_TEST_CASE_PATH"] = os.path.abspath(test_case_path)

        # 1. Select parent from archive
        initial_program_path, parent_id = select_parent_from_archive()
        if not os.path.exists(initial_program_path):
            raise FileNotFoundError(f"Parent program file not found at {initial_program_path}")

        # 2. Pass parent ID to evaluator to track lineage
        if parent_id:
            os.environ["PARENT_AGENT_ID"] = parent_id

        # 3. Initialize and run the mutation
        evolve = OpenEvolve(
            initial_program_path=initial_program_path,
            evaluation_file="prompt_engineering/evaluator.py",
            prompt="""
You are an expert Python programmer tasked with improving a file to pass a series of tests.
The user will provide you with a file and the results of a test run.
Your task is to modify the file to fix the failing tests.
The provided file is a Python script that is part of a larger application.
The tests are run using pytest.

Your goal is to make the tests pass. A fitness score of 1.0 means all tests passed.

You must provide your response as a single JSON object containing two keys:
1. "rationale": A single sentence explaining the change you made.
2. "code": The full, complete, modified Python code.

Do not add any extra explanations, notes, or markdown formatting outside of the JSON object.
Example response:
```json
{
  "rationale": "Added a null check to prevent a crash when the input is empty.",
  "code": "import os\\n\\ndef my_function(data):\\n    if data is None:\\n        return\\n    # ... rest of the code"
}
```
""",
        )

        # The openevolve `run` function returns the best program it found in the
        # single iteration. Since our evaluator saves every agent, we don't
        # need the return value here, but we can still print it for logging.
        new_program = await evolve.run(iterations=1) # Only 1 iteration per parent
        print("\n--- Mutation complete. New agent saved to archive by evaluator. ---")
        if new_program and new_program.metrics:
            print("New program metrics:")
            for name, value in new_program.metrics.items():
                print(f"  {name}: {value:.4f}")


    finally:
        # Clean up environment variables
        if "DYNAMIC_TEST_CASE_PATH" in os.environ:
            del os.environ["DYNAMIC_TEST_CASE_PATH"]
        if "PARENT_AGENT_ID" in os.environ:
            del os.environ["PARENT_AGENT_ID"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evolve a prompt using OpenEvolve.")
    parser.add_argument(
        "--test-case",
        type=str,
        help="Path to a specific YAML test case file to use for evaluation."
    )
    args = parser.parse_args()

    asyncio.run(run_evolution(test_case_path=args.test_case))
