#!/usr/bin/env python3
import os
import re
import ast
import json
import mimetypes
from collections import defaultdict
from pathlib import Path

# --- Configuration ---
ROOT_DIR = "."
OUTPUT_FILE = "FILE_MAP.md"
IGNORE_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".idea", ".vscode", ".Jules", ".jules", "dist", "build",
    ".pytest_cache", "site-packages", "jules-scratch"
}
IGNORE_FILES = {
    ".DS_Store", "FILE_MAP.md", "package-lock.json", "yarn.lock",
    "pnpm-lock.yaml", ".gitkeep"
}

# Known entry points (files that are okay to have no incoming links)
ENTRY_POINTS = {
    "README.md", "TODO.md", "LICENSE", "Makefile", "Dockerfile",
    "docker-compose.yml", "setup.py", "requirements.txt", "package.json",
    "pyproject.toml", ".gitignore", ".env.example", "ansible.cfg",
    "inventory.yaml", "local_inventory.ini", "playbook.yaml",
    "index.html", "bootstrap.sh", "run_tests.sh", "start_services.sh",
    "check_deps.py", "setup.sh", "verify_config_load.py", ".gitattributes",
    "hostfile", ".djlint.toml", "pytest.ini", ".yamllint", ".markdownlint.json",
    "run_download_models.yaml", ".opencode.json", "opencode.json", "send.toml",
    "cluster_status.yaml", "generate_issue_script.py", "test.wav"
}
ENTRY_POINT_EXTENSIONS = {".md", ".txt", ".sh", ".yaml", ".yml", ".json", ".ini", ".cfg", ".toml", ".hcl"}

# --- Data Structures ---
file_metadata = {} # path -> {description, type, status, links_to}
edges = set() # (source, target) tuples
files_by_dir = defaultdict(list)

def get_rel_path(filepath):
    return os.path.relpath(filepath, ROOT_DIR)

def is_ignored(path):
    parts = path.split(os.sep)
    for part in parts:
        if part in IGNORE_DIRS:
            return True
    if parts[-1] in IGNORE_FILES:
        return True
    return False

# --- Parsers ---

def extract_python_info(content, filepath):
    desc = ""
    imports = set()
    try:
        tree = ast.parse(content)
        # Extract Docstring
        desc = ast.get_docstring(tree) or ""

        # Extract Imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0]) # Approximate module
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
                    # Handle relative imports (approximate)
                    # This is tricky without full project context, but we can try mapping back to files
    except Exception:
        pass # Parse error

    # Regex fallback for string references to files
    # Check for references to other known files in the codebase
    return desc, imports

def extract_shell_info(content):
    desc = ""
    lines = content.splitlines()
    if lines and lines[0].startswith("#!"):
        # Check subsequent lines for comments
        comments = []
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("#"):
                comments.append(line.lstrip("#").strip())
            elif not line:
                continue
            else:
                break
        desc = " ".join(comments)
    return desc

def extract_generic_desc(content, filepath):
    # Heuristic: First few lines, look for comments
    lines = content.splitlines()
    for line in lines[:5]:
        line = line.strip()
        if line.startswith(("#", "//", "<!--")):
            return line.lstrip("#/<!- ").rstrip("->").strip()
    return ""

def scan_file_references(content, current_file, all_files):
    """
    Scans content for strings that look like paths to other existing files.
    """
    found = set()

    # Pre-computation for performance
    current_dir = os.path.dirname(current_file)

    # Regex patterns for HTML/Web
    html_src_pattern = re.compile(r'src=["\']([^"\']+)["\']')
    html_href_pattern = re.compile(r'href=["\']([^"\']+)["\']')

    # 1. HTML/JS specific scanning
    if current_file.endswith(('.html', '.js')):
        for match in html_src_pattern.findall(content) + html_href_pattern.findall(content):
            # Normalize path
            # If starts with /, it's relative to root or static root. We try both.
            # If relative, relative to current dir.
            possible_paths = []
            if match.startswith('/'):
                 possible_paths.append(match.lstrip('/'))
                 # Special case for static: /static/... -> pipecatapp/static/...
                 if match.startswith('/static/'):
                     possible_paths.append(os.path.join('pipecatapp', match.lstrip('/')))
            else:
                 possible_paths.append(os.path.normpath(os.path.join(current_dir, match)))

            for p in possible_paths:
                if p in all_files:
                    found.add(p)

    # 2. General Filename Search
    for target_file in all_files:
        if target_file == current_file:
            continue

        filename = os.path.basename(target_file)

        # Python module resolution check
        if current_file.endswith(".py") and target_file.endswith(".py"):
            module_name = os.path.splitext(filename)[0]
            if re.search(r'\b(import|from)\s+(\w+\.)*' + re.escape(module_name) + r'\b', content):
                found.add(target_file)
                continue

        # Ansible/Jinja check
        if current_file.endswith(('.yaml', '.yml', '.j2')):
             # Check for template references (e.g. src="foo.j2")
             if filename in content:
                 found.add(target_file)
                 continue
             # Check for role references (folder name)
             # If target is in a role, check if role name is used
             if 'roles/' in target_file:
                 role_name = target_file.split('roles/')[1].split('/')[0]
                 if f"role: {role_name}" in content or f"- {role_name}" in content:
                     found.add(target_file) # Link to file implies link to role
                     continue

        # Check for full relative path or filename in quotes/string context
        if filename in content:
             found.add(target_file)

    return found

# --- Main Execution ---

def main():
    print("Scanning codebase...")

    # 1. Collect all files
    all_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        # Filter ignores
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            filepath = os.path.join(root, file)
            rel_path = get_rel_path(filepath)

            if is_ignored(rel_path):
                continue

            all_files.append(rel_path)
            files_by_dir[os.path.dirname(rel_path)].append(rel_path)

    # 2. Analyze each file
    print(f"Analyzing {len(all_files)} files...")
    for f in all_files:
        path = Path(f)
        try:
            content = path.read_text(errors='ignore')
        except:
            content = ""

        desc = ""
        # Description Extraction
        if f.endswith(".py"):
            d, _ = extract_python_info(content, f)
            desc = d
        elif f.endswith(".sh"):
            desc = extract_shell_info(content)

        if not desc:
            desc = extract_generic_desc(content, f)

        if not desc:
            desc = f"File: {path.name}"

        # Clean description (first line only, max length)
        desc = desc.split('\n')[0][:100].strip()
        if not desc:
             desc = "No description available."

        file_metadata[f] = {
            "description": desc,
            "links": set()
        }

    # 3. Resolve Dependencies (Pass 2)
    # We do this after collecting all files so we know what valid targets exist
    for f in all_files:
        try:
            content = Path(f).read_text(errors='ignore')
        except:
            continue

        refs = scan_file_references(content, f, all_files)
        for target in refs:
            edges.add((f, target))
            file_metadata[f]["links"].add(target)

    # 4. Determine Status (Orphan vs Entry Point vs Referenced)
    referenced_files = set()
    for src, tgt in edges:
        referenced_files.add(tgt)

    orphans = []

    for f in all_files:
        status = "Referenced"
        if f not in referenced_files:
            # Check entry point
            is_entry = False
            if os.path.basename(f) in ENTRY_POINTS:
                is_entry = True
            elif f.startswith("scripts/") or f.startswith("initial-setup/"):
                 # Scripts are usually entry points
                 is_entry = True
            elif "tests/" in f or "test_" in f:
                # Tests are entry points for the test runner
                is_entry = True
                status = "Test" # Special status
            elif f.endswith(".j2"):
                 # Templates are often referenced by name without extension or constructed paths
                 is_entry = True
                 status = "Template"
            elif "prompt_engineering/" in f or "docs/" in f or "verification/" in f:
                 is_entry = True
                 status = "Documentation/Asset"
            elif f.endswith(".hcl"):
                 is_entry = True
                 status = "Nomad Template"
            elif "pipecat-agent-extension/" in f:
                 is_entry = True
                 status = "Extension"
            elif "workflows/" in f and f.endswith(".yaml"):
                 is_entry = True
                 status = "Workflow Config"
            elif any(f.endswith(ext) for ext in ENTRY_POINT_EXTENSIONS) and (f.count('/') == 0):
                # Root level configs
                is_entry = True
            elif "main" in f: # Heuristic
                is_entry = True

            if is_entry:
                if status not in ["Test", "Template", "Documentation/Asset", "Extension", "Workflow Config"]:
                     status = "Entry Point"
            else:
                status = "Orphan"
                orphans.append(f)

        file_metadata[f]["status"] = status

    # 5. Generate Markdown
    print("Generating report...")

    with open(OUTPUT_FILE, "w") as out:
        out.write("# Codebase File Map\n\n")
        out.write("This document maps every file in the repository, their description, and utilization status.\n\n")

        # Table
        out.write("## File List\n\n")
        out.write("| File Path | Status | Description |\n")
        out.write("| --- | --- | --- |\n")

        # Sort for consistency
        for f in sorted(all_files):
            meta = file_metadata[f]
            status_icon = "🟢"
            if meta["status"] == "Entry Point": status_icon = "🔵"
            elif meta["status"] == "Test": status_icon = "🧪"
            elif meta["status"] == "Orphan": status_icon = "🔴"
            elif meta["status"] in ["Template", "Documentation/Asset", "Extension", "Workflow Config"]: status_icon = "📄"

            # Escape pipes in description
            safe_desc = meta["description"].replace("|", "\\|")
            out.write(f"| `{f}` | {status_icon} {meta['status']} | {safe_desc} |\n")

        out.write("\n## Dependency Diagram\n\n")
        out.write("```mermaid\n")
        out.write("graph LR\n")

        # Define Nodes in Subgraphs
        # We need to create nested subgraphs or at least flat subgraphs for dirs
        # Mermaid doesn't handle deep nesting gracefully in all renderers, sticking to 1 level for now?
        # Let's try to do hierarchy based on directory structure.

        # To make it readable, we assign IDs to nodes
        node_ids = {f: f"node_{i}" for i, f in enumerate(all_files)}

        # Group by directory
        sorted_dirs = sorted(files_by_dir.keys())

        for d in sorted_dirs:
            # Skip root dir in subgraph if we want (or call it "Root")
            dir_label = d if d else "Root"
            # Sanitize label for mermaid id
            safe_dir_id = "dir_" + re.sub(r'[^a-zA-Z0-9]', '_', dir_label)

            out.write(f"    subgraph {safe_dir_id} [{dir_label}]\n")
            out.write(f"        direction TB\n") # Organize files top-down inside folders
            for f in sorted(files_by_dir[d]):
                nid = node_ids[f]
                fname = os.path.basename(f)
                out.write(f"        {nid}[\"{fname}\"]\n")
                # Add click event? No, simple markdown.
            out.write("    end\n")

        # Edges
        out.write("\n")
        for src, tgt in edges:
            out.write(f"    {node_ids[src]} --> {node_ids[tgt]}\n")

        out.write("```\n")

    print(f"Done. Report written to {OUTPUT_FILE}")
    print(f"Found {len(orphans)} potential orphans.")
    for o in orphans:
        print(f"  Orphan: {o}")

if __name__ == "__main__":
    main()
