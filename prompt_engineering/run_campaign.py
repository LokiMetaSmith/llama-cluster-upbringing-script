import argparse
import subprocess
import os
import json
import glob
import sys

def run_campaign(generations: int):
    """
    Runs an evolutionary campaign for a specified number of generations.

    This function calls the `evolve.py` script in a loop to generate new
    agents and populate the archive.

    Args:
        generations (int): The number of evolutionary steps to run.
    """
    print(f"--- Starting evolutionary campaign for {generations} generations ---")
    evolve_script_path = os.path.join(os.path.dirname(__file__), "evolve.py")

    if not os.path.exists(evolve_script_path):
        print(f"Error: The 'evolve.py' script was not found at {evolve_script_path}", file=sys.stderr)
        sys.exit(1)

    for i in range(generations):
        print(f"\n--- Running Generation {i+1}/{generations} ---")
        try:
            # We use sys.executable to ensure we're using the same Python interpreter
            # that's running this script.
            process = subprocess.Popen(
                [sys.executable, evolve_script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8'
            )

            # Stream the output from the subprocess in real-time
            for line in process.stdout:
                print(line, end='')

            process.wait()
            if process.returncode != 0:
                print(f"\n--- WARNING: Generation {i+1} failed with exit code {process.returncode} ---", file=sys.stderr)

        except Exception as e:
            print(f"\n--- ERROR: An error occurred during generation {i+1}: {e} ---", file=sys.stderr)
            # Decide if we should stop or continue. For now, we'll continue.
            pass


def analyze_archive():
    """
    Analyzes the agent archive, identifies the top 5 performing agents,
    and prints a summary report.
    """
    print("\n--- Campaign finished. Analyzing results... ---")
    archive_dir = os.path.join(os.path.dirname(__file__), "archive")
    meta_files = glob.glob(os.path.join(archive_dir, "*.json"))

    if not meta_files:
        print("Archive is empty. No results to analyze.")
        return

    all_agents = []
    for meta_file in meta_files:
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
                agent_id = os.path.basename(meta_file).replace(".json", "")
                all_agents.append({
                    "id": agent_id,
                    "fitness": meta.get("fitness", 0.0),
                    "parent": meta.get("parent"),
                    "passed": meta.get("passed", False),
                    "rationale": meta.get("rationale")
                })
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read or parse metadata file {meta_file}: {e}", file=sys.stderr)

    # Sort agents by fitness, descending
    sorted_agents = sorted(all_agents, key=lambda x: x["fitness"], reverse=True)

    # The implementation for generating the report will be added in the next step
    top_agents = sorted_agents[:5]
    _generate_report(top_agents)


def _generate_report(top_agents: list):
    """
    Prints a formatted report of the top agents to the console.

    Args:
        top_agents (list): A list of agent dictionaries, sorted by fitness.
    """
    if not top_agents:
        print("No agents to report on.")
        return

    print("\n--- Top 5 Performing Agents ---")
    # Dynamically adjust column width for rationale
    max_rationale_len = max(len(agent.get('rationale', '')) for agent in top_agents) if top_agents else 20
    header_rationale = "Rationale".ljust(max_rationale_len)

    table_width = 80 + max_rationale_len
    print("-" * table_width)
    header = f"{'Rank':<5} | {'Agent ID':<10} | {'Fitness':<10} | {'Passed':<7} | {'Parent ID':<10} | {header_rationale}"
    print(header)
    print("-" * table_width)

    for i, agent in enumerate(top_agents):
        rank = i + 1
        agent_id = agent['id']
        fitness = f"{agent['fitness']:.4f}"
        passed = str(agent['passed'])
        parent_id = agent.get('parent') or 'N/A'
        rationale = agent.get('rationale', 'N/A').ljust(max_rationale_len)
        row = f"{rank:<5} | {agent_id:<10} | {fitness:<10} | {passed:<7} | {parent_id:<10} | {rationale}"
        print(row)

    print("-" * table_width)
    best_agent = top_agents[0]
    best_agent_id = best_agent['id']
    print(f"\n🏆 Best agent found: {best_agent_id}")
    print(f"   - Fitness: {best_agent['fitness']:.4f}")
    print(f"   - Rationale: {best_agent.get('rationale', 'N/A')}")
    best_agent_path = os.path.join(os.path.dirname(__file__), "archive", f"{best_agent_id}.py")
    print(f"   - To review, see file: {best_agent_path}")
    print("-" * table_width)

    # Automatically run the visualization script
    visualize_script_path = os.path.join(os.path.dirname(__file__), "visualize_archive.py")
    if os.path.exists(visualize_script_path):
        print("\n--- Attempting to generate visualization ---")
        try:
            subprocess.run([sys.executable, visualize_script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"--- WARNING: Visualization script failed with exit code {e.returncode} ---", file=sys.stderr)
        except Exception as e:
            print(f"--- ERROR: An unexpected error occurred while running the visualization script: {e} ---", file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a DGM evolutionary campaign to populate the agent archive."
    )
    parser.add_argument(
        "-g", "--generations",
        type=int,
        default=10,
        help="The number of generations (evolutionary steps) to run."
    )
    args = parser.parse_args()

    try:
        run_campaign(args.generations)
        analyze_archive()
    except KeyboardInterrupt:
        print("\nCampaign interrupted by user. Analyzing partial results...", file=sys.stderr)
        analyze_archive()
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        # Still try to analyze whatever results we have
        analyze_archive()
