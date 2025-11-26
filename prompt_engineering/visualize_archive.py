import os
import json
import glob
import sys
from graphviz import Digraph

def visualize_archive():
    """
    Scans the agent archive, builds an evolutionary tree, and saves it as a PNG image.
    """
    print("--- Generating evolutionary tree visualization ---")
    archive_dir = os.path.join(os.path.dirname(__file__), "archive")
    output_path = os.path.join(archive_dir, "evolution_tree") # .png will be added by graphviz

    if not os.path.isdir(archive_dir):
        print(f"Error: Archive directory not found at {archive_dir}", file=sys.stderr)
        sys.exit(1)

    meta_files = glob.glob(os.path.join(archive_dir, "*.json"))
    if not meta_files:
        print("Archive is empty. Nothing to visualize.")
        return

    dot = Digraph(comment='Agent Evolutionary Tree', graph_attr={'rankdir': 'TB', 'splines': 'ortho'})

    # First pass: Add all agents as nodes
    all_agents = {}
    for meta_file in meta_files:
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
                agent_id = os.path.basename(meta_file).replace(".json", "")
                all_agents[agent_id] = meta

                # Add node with color based on fitness
                fitness = meta.get("fitness", 0.0)
                color = get_color_for_fitness(fitness)
                label = f"ID: {agent_id}\nFitness: {fitness:.4f}"
                dot.node(agent_id, label=label, style='filled', fillcolor=color)

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read or parse metadata file {meta_file}: {e}", file=sys.stderr)

    # Second pass: Add edges
    for agent_id, meta in all_agents.items():
        parent_id = meta.get("parent")
        if parent_id and parent_id in all_agents:
            dot.edge(parent_id, agent_id)
        elif parent_id is None:
            # Add a root node for the initial seed
            dot.node('root', 'Initial Seed', shape='box', style='filled', fillcolor='gray')
            dot.edge('root', agent_id)

    # The logic to save the graph will be in the next step.
    _save_graph(dot, output_path)


def get_color_for_fitness(fitness: float) -> str:
    """
    Returns a color for a node based on its fitness score.
    Uses a green-to-red scale.
    """
    if fitness >= 0.9:
        return "#a1d99b"  # Light Green
    elif fitness >= 0.5:
        return "#fee08b"  # Light Yellow
    else:
        return "#fc8d59"  # Light Red

def _save_graph(dot, output_path):
    """
    Renders and saves the graph to a file, handling potential errors.

    Args:
        dot (Digraph): The graph object to save.
        output_path (str): The base path for the output file (without extension).
    """
    try:
        dot.render(output_path, format='png', cleanup=True)
        print(f"--- Evolutionary tree saved to {output_path}.png ---")
    except FileNotFoundError:
        print("\n--- ERROR: 'graphviz' command not found. ---", file=sys.stderr)
        print("Please install the Graphviz command-line tools.", file=sys.stderr)
        print("See: https://graphviz.org/download/", file=sys.stderr)
        # We don't exit here, as the campaign might still be considered a success.
    except Exception as e:
        print(f"\n--- ERROR: An unexpected error occurred during graph rendering: {e} ---", file=sys.stderr)


if __name__ == "__main__":
    visualize_archive()
