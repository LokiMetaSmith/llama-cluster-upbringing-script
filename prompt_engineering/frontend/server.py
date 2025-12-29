import os
import json
import glob
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')
archive_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "archive"))

@app.route('/')
def serve_index():
    """Serves the main index.html file."""
    return send_from_directory('.', 'index.html')

@app.route('/api/tree')
def get_evolutionary_tree():
    """
    Scans the agent archive, constructs a JSON representation of the
    evolutionary tree, and returns it.
    """
    if not os.path.isdir(archive_dir):
        return jsonify({"error": f"Archive directory not found at {archive_dir}"}), 404

    meta_files = glob.glob(os.path.join(archive_dir, "*.json"))
    if not meta_files:
        return jsonify([])

    nodes = []
    for meta_file in meta_files:
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)
                agent_id = os.path.basename(meta_file).replace(".json", "")

                node = {
                    "id": agent_id,
                    "parent": meta.get("parent"),
                    "rationale": meta.get("rationale", "N/A"),
                    "fitness": meta.get("fitness", 0.0),
                    "code": ""
                }

                # Read the corresponding Python code file
                code_file_path = os.path.join(archive_dir, f"{agent_id}.py")
                if os.path.exists(code_file_path):
                    with open(code_file_path, 'r') as cf:
                        node["code"] = cf.read()

                nodes.append(node)

        except (json.JSONDecodeError, IOError) as e:
            # Log the error but continue processing other files
            print(f"Warning: Could not read or parse file {meta_file}: {e}")

    return jsonify(nodes)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
