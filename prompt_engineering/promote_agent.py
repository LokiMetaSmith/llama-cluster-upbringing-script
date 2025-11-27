import argparse
import os
import sys
import glob
import json
import shutil

def find_best_agent():
    """Scans the archive and returns the ID of the agent with the highest fitness."""
    archive_dir = os.path.join(os.path.dirname(__file__), "archive")
    meta_files = glob.glob(os.path.join(archive_dir, "*.json"))

    if not meta_files:
        raise FileNotFoundError("The archive is empty. No agents to promote.")

    best_agent = None
    max_fitness = -1.0

    for meta_file in meta_files:
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
                fitness = meta.get("fitness", 0.0)
                if fitness > max_fitness:
                    max_fitness = fitness
                    best_agent = os.path.basename(meta_file).replace(".json", "")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read or parse metadata file {meta_file}: {e}", file=sys.stderr)

    if best_agent is None:
        raise ValueError("Could not find a valid agent to promote in the archive.")

    return best_agent, max_fitness


def promote_agent(agent_id: str, is_best: bool):
    """
    Selects the agent to promote and initiates the promotion process.
    """
    final_agent_id = None
    if is_best:
        print("--- Finding the best agent in the archive... ---")
        final_agent_id, fitness = find_best_agent()
        print(f"--- Found best agent: {final_agent_id} (Fitness: {fitness:.4f}) ---")
    else:
        final_agent_id = agent_id
        print(f"--- Preparing to promote agent: {final_agent_id} ---")

    # Placeholder for the promotion logic
    _perform_promotion(final_agent_id)


def _perform_promotion(agent_id: str):
    """
    Handles the file operations for backing up and promoting the agent.
    """
    if not agent_id:
        raise ValueError("Agent ID cannot be None.")

    base_dir = os.path.dirname(__file__)
    archive_dir = os.path.join(base_dir, "archive")

    source_agent_path = os.path.join(archive_dir, f"{agent_id}.py")
    if not os.path.exists(source_agent_path):
        raise FileNotFoundError(f"Agent code file not found in archive: {source_agent_path}")

    target_app_path = os.path.abspath(os.path.join(base_dir, "..", "ansible", "roles", "pipecatapp", "files", "app.py"))
    if not os.path.exists(target_app_path):
        raise FileNotFoundError(f"Target application file not found at: {target_app_path}")

    backup_path = f"{target_app_path}.bak"

    try:
        # 1. Back up the current app.py
        print(f"--- Backing up current app.py to {backup_path} ---")
        shutil.copy2(target_app_path, backup_path)

        # 2. Promote the new agent
        print(f"--- Promoting agent {agent_id} to {target_app_path} ---")
        shutil.copy2(source_agent_path, target_app_path)

        print("\n✅ Promotion successful!")
        print(f"   - Agent '{agent_id}' is now the active app.py.")
        print(f"   - The previous version is backed up at: {backup_path}")

    except Exception as e:
        print(f"\n--- ERROR: An error occurred during the promotion file operations: {e} ---", file=sys.stderr)
        # Attempt to restore from backup if the promotion failed mid-way
        if os.path.exists(backup_path):
            print("--- Attempting to restore from backup... ---", file=sys.stderr)
            try:
                shutil.copy2(backup_path, target_app_path)
                print("--- Restore successful. ---", file=sys.stderr)
            except Exception as restore_e:
                print(f"--- CRITICAL ERROR: Failed to restore from backup: {restore_e} ---", file=sys.stderr)
                print("--- The main app.py may be in a corrupted state. Please restore manually. ---", file=sys.stderr)
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Promote a successful agent from the archive to become the main application code."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "agent_id",
        nargs='?',
        default=None,
        help="The ID of the agent to promote (e.g., 'a1b2c3d4')."
    )
    group.add_argument(
        "--best",
        action="store_true",
        help="Automatically find and promote the agent with the highest fitness score in the archive."
    )
    args = parser.parse_args()

    try:
        promote_agent(args.agent_id, args.best)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
