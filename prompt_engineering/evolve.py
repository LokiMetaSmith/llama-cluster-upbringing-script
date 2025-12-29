from openevolve import OpenEvolve
import os
import argparse
import asyncio
import json
import random
import glob
import difflib
try:
    from . import promote_agent
except ImportError:
    import promote_agent

def load_archive_metadata():
    """Loads metadata for all agents in the archive.

    Returns:
        list: A list of dictionaries, where each dictionary contains the metadata
              for an agent, including its 'id' and 'path'.
    """
    archive_dir = os.path.join(os.path.dirname(__file__), "archive")
    meta_files = glob.glob(os.path.join(archive_dir, "*.json"))
    archive = []

    for meta_file in meta_files:
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
                agent_id = os.path.basename(meta_file).replace(".json", "")
                meta['id'] = agent_id
                meta['path'] = os.path.join(archive_dir, f"{agent_id}.py")
                archive.append(meta)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse metadata file {meta_file}. Skipping.")
        except Exception as e:
            print(f"Warning: Error loading metadata file {meta_file}: {e}. Skipping.")

    return archive

def select_parent(archive, selection_method="weighted", tournament_size=3, novelty_k=10):
    """
    Selects a parent from the archive based on the chosen strategy.

    Args:
        archive (list): List of agent metadata dicts.
        selection_method (str): 'weighted', 'tournament', or 'random'.
        tournament_size (int): 'k' parameter for tournament selection.

    Returns:
        dict: The selected parent metadata.
    """
    if not archive:
        raise ValueError("Archive is empty. Cannot select a parent.")

    # 1. Random Selection (Pure Exploration)
    if selection_method == "random":
        return random.choice(archive)

    # Helper: Normalize fitness to a number if it is boolean or missing
    def get_fitness_score(agent):
        f = agent.get("fitness", 0)
        if isinstance(f, bool):
            return 1.0 if f else 0.0
        return float(f)

    # 2. Tournament Selection
    if selection_method == "tournament":
        # Ensure k is not larger than the population
        k = min(tournament_size, len(archive))

        # Pick k random candidates
        candidates = random.sample(archive, k)

        # Return the one with the highest fitness
        # specific sort ensures stability if fitness is equal
        best_candidate = max(candidates, key=get_fitness_score)
        return best_candidate

    # 3. Weighted Random (Roulette Wheel) - Existing Logic
    elif selection_method == "weighted":
        # Filter for candidates with positive fitness to avoid zero-division or useless selection
        scored_archive = [(agent, get_fitness_score(agent)) for agent in archive]

        # If all fitnesses are zero, fallback to random
        total_fitness = sum(score for _, score in scored_archive)
        if total_fitness == 0:
            return random.choice(archive)

        pick = random.uniform(0, total_fitness)
        current = 0
        for agent, score in scored_archive:
            current += score
            if current > pick:
                return agent
        return archive[-1] # Fallback

    # 4. Power Law Selection (ShinkaEvolve Strategy)
    elif selection_method == "power_law":
        # Sort archive by fitness descending
        sorted_archive = sorted(archive, key=get_fitness_score, reverse=True)
        N = len(sorted_archive)
        alpha = 1.0  # Power law exponent, Shinka defaults to 1.0 (Zipf's law like)

        # Calculate weights: (rank + 1) ^ -alpha
        weights = [(i + 1) ** -alpha for i in range(N)]
        total_weight = sum(weights)

        pick = random.uniform(0, total_weight)
        current = 0
        for i, weight in enumerate(weights):
            current += weight
            if current > pick:
                return sorted_archive[i]
        return sorted_archive[-1]

    # 5. Novelty Search
    elif selection_method == "novelty":
        if len(archive) <= 1:
            return random.choice(archive)

        # Memoize file reads to avoid redundant I/O
        memoized_code = {}
        def get_agent_code(agent):
            path = agent.get('path')
            if not path or path not in memoized_code:
                try:
                    with open(path, 'r') as f:
                        memoized_code[path] = f.read()
                except (FileNotFoundError, TypeError):
                    memoized_code[path] = "" # Agent might not have a path yet
            return memoized_code[path]

        novelty_scores = []
        for i, agent_i in enumerate(archive):
            code_i = get_agent_code(agent_i)
            distances = []
            for j, agent_j in enumerate(archive):
                if i == j:
                    continue
                code_j = get_agent_code(agent_j)

                # Behavioral distance is 1 minus the similarity ratio from difflib
                distance = 1.0 - difflib.SequenceMatcher(a=code_i, b=code_j).ratio()
                distances.append(distance)

            # Sort distances to find the nearest neighbors
            distances.sort()

            # The number of neighbors to consider (k) cannot be larger than the number of other agents
            k = min(novelty_k, len(distances))

            # Novelty is the average distance to the k-nearest neighbors
            if k > 0:
                novelty_score = sum(distances[:k]) / k
            else:
                novelty_score = 0.0 # Should not happen if len(archive) > 1

            novelty_scores.append((agent_i, novelty_score))

        # Select the agent with the highest novelty score
        if not novelty_scores:
            return random.choice(archive) # Fallback

        best_agent = max(novelty_scores, key=lambda item: item[1])[0]
        return best_agent

    # Default fallback
    return random.choice(archive)


def select_parent_from_archive(selection_method="weighted", tournament_size=3, novelty_k=10):
    """Wrapper function to maintain backward compatibility and orchestrate selection."""
    archive = load_archive_metadata()

    if not archive:
        print("--- Archive is empty. Seeding evolution with initial app.py ---")
        initial_program_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "ansible", "roles", "pipecatapp", "files", "app.py")
        )
        return initial_program_path, None

    selected_agent = select_parent(
        archive, selection_method, tournament_size, novelty_k
    )

    # Calculate fitness for logging
    fitness = selected_agent.get("fitness", 0.0)
    if isinstance(fitness, bool):
        fitness = 1.0 if fitness else 0.0

    print(f"--- Selected parent agent {selected_agent['id']} with fitness {fitness:.4f} using {selection_method} ---")
    return selected_agent['path'], selected_agent['id']


async def run_evolution(test_case_path=None, auto_promote=False, selection_method="weighted", tournament_size=3, novelty_k=10):
    """Initializes and runs the OpenEvolve algorithm with a DGM-style archive."""
    # Ensure API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Please set OPENAI_API_KEY environment variable")

    parent_id = None
    try:
        # Set dynamic test case if provided
        if test_case_path:
            os.environ["DYNAMIC_TEST_CASE_PATH"] = os.path.abspath(test_case_path)

        # 1. Select parent from archive
        initial_program_path, parent_id = select_parent_from_archive(
            selection_method, tournament_size, novelty_k
        )

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
Partial credit is given for passing some tests, so try to fix as many as possible even if you cannot fix all of them.

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

        new_program = await evolve.run(iterations=1) # Only 1 iteration per parent
        print("\n--- Mutation complete. New agent saved to archive by evaluator. ---")
        if new_program and new_program.metrics:
            print("New program metrics:")
            for name, value in new_program.metrics.items():
                if isinstance(value, (int, float)):
                    print(f"  {name}: {value:.4f}")
                else:
                    print(f"  {name}: {value}")

            # Check for auto-promotion
            if auto_promote and new_program.metrics.get("fitness") == 1.0:
                agent_id = new_program.metrics.get("agent_id")
                if agent_id:
                    print(f"\n--- Auto-promoting successful agent {agent_id} ---")
                    try:
                        promote_agent.promote_agent(agent_id, is_best=False)
                    except Exception as e:
                        print(f"Error during auto-promotion: {e}")
                else:
                    print("Warning: High fitness agent found but no agent_id returned by evaluator.")


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
    parser.add_argument(
        "--auto-promote",
        action="store_true",
        help="Automatically promote the new agent if it passes all tests (fitness 1.0)."
    )
    parser.add_argument(
        "--selection-method",
        choices=["weighted", "tournament", "random", "power_law", "novelty"],
        default="weighted",
        help="Strategy for selecting the parent from the archive."
    )
    parser.add_argument(
        "--tournament-size",
        type=int,
        default=3,
        help="Number of candidates to compare in tournament selection (k). Larger k = higher selection pressure."
    )
    parser.add_argument(
        "--novelty-k",
        type=int,
        default=10,
        help="Number of nearest neighbors to compare against for novelty search."
    )
    args = parser.parse_args()

    asyncio.run(run_evolution(
        test_case_path=args.test_case,
        auto_promote=args.auto_promote,
        selection_method=args.selection_method,
        tournament_size=args.tournament_size,
        novelty_k=args.novelty_k,
    ))
