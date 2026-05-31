# LiteGraph vs ReactFlow Analysis

This document compares the current workflow visualization library (`LiteGraph.js`) against the user-requested `ReactFlow` library, identifying critical features that we might be missing and whether migrating or supplementing is necessary.

## Current Setup: LiteGraph.js

We are currently using `LiteGraph.js` for our visual workflow editor (`pipecatapp/static/js/editor.js`) and 3D VR environment (`cluster_viz.html`, `vr_index.html`).

### LiteGraph Strengths

- **Canvas2D/WebGL Native:** Renders entirely on a Canvas element. This makes it highly performant for thousands of nodes and perfectly suited for our VR/3D visualization using A-Frame (`aframe-htmlembed-component`).
- **No Dependencies:** It's a single JS file without a heavy build step or React dependency, making it easy to drop into vanilla HTML pages.
- **Built-in Execution Engine:** It's not just UI; it has an execution engine built-in, though we mainly use our Python backend.

### LiteGraph Weaknesses

- **Styling:** Because it draws directly to a Canvas, it cannot be styled with modern CSS/Tailwind. Customizing the UI requires writing low-level Canvas API drawing code.
- **Accessibility:** Canvas text and elements are not readable by screen readers.
- **Ecosystem:** Smaller community, fewer plugins, less documentation compared to ReactFlow.

## Alternative: ReactFlow

ReactFlow is a highly popular React-based library for node-based editors, mentioned in our `FLOWISE_ANALYSIS.md`.

### ReactFlow Strengths

- **DOM-Based Nodes:** Every node is a regular React component. This means you can put any HTML inside them (forms, dropdowns, rich text, video players) and style them using standard CSS/Tailwind.
- **Accessibility:** Since nodes are DOM elements, they are much more accessible.
- **Rich Interaction:** Features like minimaps, background grids, auto-layout algorithms (Dagre/Elk), and rich interactive handles are standard.
- **State Management:** Integrates perfectly with modern state management (Zustand, Redux) and React contexts.

### ReactFlow Weaknesses

- **Performance at Scale:** Because every node is a DOM element, rendering thousands of nodes can be slower than Canvas.
- **React Dependency:** Requires a React build toolchain. It cannot be easily dropped into our current vanilla JS setup.
- **VR/3D Compatibility:** Crucially, because it relies on standard HTML/DOM positioning, integrating it into our WebVR/A-Frame 3D space would be exceptionally difficult or impossible compared to a flattened Canvas texture.

## Critical Missing Features in LiteGraph (Compared to ReactFlow)

Based on the ReactFlow feature set, here are the things we are missing in LiteGraph:

1. **Rich Node Content:** ReactFlow allows embedding complex UI components (like a Monaco code editor, complex forms, or dynamic lists) directly inside the node. In LiteGraph, we are limited to basic widgets (sliders, toggles, text boxes) that we have to manually draw on the canvas.
2. **Auto-Layout:** ReactFlow has extensive examples of integrating with `dagre` or `elkjs` to automatically arrange messy graphs. LiteGraph requires manual positioning or custom algorithms.
3. **Sub-Flows & Grouping:** While LiteGraph has "Subgraphs", ReactFlow's handling of visually grouping nodes (Parent/Child relationships where moving the parent moves the children) is much more robust and visually clear. This directly impacts our "Active Vault" Obsidian goal of mapping "Canvas Groups" to Workflow Scopes.
4. **Custom Edge Routing:** ReactFlow provides smooth step paths, custom edge components (e.g., edges with buttons on them to delete the connection), and smart routing to avoid overlapping nodes.
5. **Accessibility (a11y):** ReactFlow nodes are readable by screen readers and can be navigated via keyboard more naturally than a unified Canvas element.

## Conclusion & Recommendation

While ReactFlow offers a superior developer experience for building rich, accessible 2D web UIs, **we should NOT migrate away from LiteGraph.js at this time.**

**Why?**
The primary reason is our core architectural goal: **3D Workflow Visualization and VR Integration** (as outlined in `OBSIDIAN_TODO.md` and `OBSIDIAN_WORKFLOW_DESIGN.md`).

LiteGraph renders to a `<canvas>`, which makes it trivial to map as a texture onto a 3D plane in A-Frame/Three.js. ReactFlow relies on absolute positioning of `<div>` elements, which cannot be easily projected into a true 3D WebGL space.

### Action Items to Bridge the Gap

Instead of migrating, we should focus on adding ReactFlow's best concepts to our LiteGraph implementation:

1. **Implement Auto-Layout:** Integrate a library like `dagre.js` to calculate node positions, then apply those `x,y` coordinates to our LiteGraph nodes.
2. **Enhance Node Metadata:** As noted in `FLOWISE_ANALYSIS.md`, we should build a strong separation between the visual card and the backend execution logic, allowing dynamic UI generation based on Python schema definitions.
3. **Group Support:** We need to explicitly build "Group" visual boundaries in LiteGraph to support the Obsidian Canvas grouping feature.
