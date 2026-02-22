# Obsidian Workflow Design: The "Active Vault" Architecture

## Overview

This document outlines the architectural vision for integrating **Obsidian** (a local Markdown/Canvas knowledge base) with **Pipecat** (our agentic workflow engine). The goal is to transform static notes into "Active Documents"—files that are both human-readable interfaces and executable agent environments.

By treating the Obsidian Vault as a shared filesystem between the user and the AI, we enable a powerful new paradigm: **The Self-Evolving Knowledge Graph**.

## 1. The "Active Document" Concept

An **Active Document** is a file (Markdown or Canvas) that contains:
1.  **Static Content:** User notes, context, research.
2.  **Agent Directives:** Instructions for the AI (e.g., `#todo: summarize this`, `<!-- run: python -->`).
3.  **Live State:** The AI updates the document in place (appending results, checking off tasks, updating graphs).

### The "Gardener" Metaphor
Instead of a chat interface (Ephemeral), we use a "Gardener" agent (Persistent).
*   **The Soil:** Your Obsidian Vault.
*   **The Seeds:** New notes or Canvas nodes created by the user.
*   **The Gardener:** Pipecat, watching the file system. It detects changes (e.g., a new file with `#agent`), "waters" it (executes the workflow), and "prunes" it (summarizes/cleans up).

---

## 2. Feature Comparison: Obsidian Canvas vs. Pipecat Workflow

We aim to bridge the gap between the **visual/organizational** power of Obsidian Canvas and the **execution/logic** power of Pipecat Workflows.

| Feature | Obsidian Canvas (`.canvas`) | Pipecat Workflow (`.yaml`) | **Hybrid Goal** |
| :--- | :--- | :--- | :--- |
| **Format** | JSON | YAML | **Interchangeable** (Converter) |
| **Visuals** | 2D (x, y, w, h, color) | None (Graph only) | **3D Spatial** (x, y, z, w, h, d, color) |
| **Logic** | Implicit (visual connections) | Explicit (Inputs/Outputs) | **Visual Logic** (Edges = Data Flow) |
| **Grouping** | Visual Groups | None (Flat list) | **Semantic Scopes** (Groups = Sub-workflows) |
| **Content** | Rich (MD, Images, Web) | Code/Config only | **Rich Context** (Embeds as input) |
| **Zoom** | UI Scaling | None | **Semantic Zoom** (Z-axis layers) |

### Missing Features in Pipecat Workflow (to be added)
1.  **Visual Properties:** `x`, `y`, `width`, `height`, `color`.
2.  **Spatial Reasoning:** `z` (Depth/Layer), `depth` (3D size).
3.  **Grouping:** The concept of a "Parent" node or container (representing a Group in Canvas).

### Missing Features in Obsidian Canvas (to be inferred)
1.  **Execution Semantics:** Canvas edges have no "port" concept. We will infer ports based on connection side (Left=Input, Right=Output) or node type.
2.  **Strong Typing:** Canvas text is unstructured. We will use simple syntax markers (e.g., `Type: PythonNode`) within the text to define node behavior.

---

## 3. The Hybrid Workflow Schema (3D Extension)

We will extend the Pipecat `Node` schema to support 3D spatial properties. This allows us to represent complex, multi-layered workflows (e.g., "Zoom Out" to see the high-level strategy layer at `z=100`, "Zoom In" to see the code implementation layer at `z=0`).

### Enhanced Node Schema
```yaml
nodes:
  - id: "node_1"
    type: "code_runner"
    # Functional Properties
    inputs:
      - code: "print('Hello')"
    # Visual/Spatial Properties
    position:
      x: 0.0
      y: 0.0
      z: 0.0          # Layer/Abstraction Level
    dimensions:
      width: 400.0
      height: 200.0
      depth: 10.0     # Visual "thickness" or complexity weight
    style:
      color: "#ff0000"
      shape: "box"    # or "sphere", "cylinder" for 3D viz
    parent: "group_1" # Hierarchy
```

### The "Zoom" Metaphor
*   **Z-Axis = Abstraction Level.**
    *   **High Z (e.g., 100):** Executive Summary, High-Level Goals.
    *   **Mid Z (e.g., 0):** The actual Workflow Logic (Nodes/Edges).
    *   **Low Z (e.g., -100):** Logs, Debug Data, Raw Outputs.
*   **Interaction:**
    *   **Zoom Out:** The camera moves back; lower Z layers fade out or collapse into summary nodes.
    *   **Zoom In:** The camera moves forward; summary nodes expand into detailed sub-graphs.

---

## 4. Implementation Strategy

### Phase 1: Schema & Converter (This Task)
1.  Update `pipecatapp/workflow/node.py` to support `position` (x,y,z), `dimensions` (w,h,d), `style`.
2.  Implement `CanvasConverter` to map:
    *   Canvas File -> Workflow Context
    *   Workflow Context -> Canvas File (Visualization)

### Phase 2: The 3D Visualizer (Future)
1.  Update `pipecatapp/static/vr_index.html` (or create `workflow_3d.html`) using **Three.js** or **A-Frame**.
2.  Render the workflow as a 3D node graph.
3.  Implement "Semantic Zoom" controls (filtering visibility by Z-level).

### Phase 3: The Gardener Service (Future)
1.  Implement a file watcher service (`Watchdog` based).
2.  On file change (`.md` or `.canvas`), parse for directives.
3.  Execute corresponding workflow.
4.  Write results back to the file (atomically).
