# Obsidian & 3D Workflow Integration Todo List

This document tracks the progress and remaining tasks for integrating Obsidian Canvas and 3D spatial reasoning into the Pipecat workflow engine.

## Phase 1: Core Schema & Converter (In Progress)
- [x] **Create Design Document**: `docs/OBSIDIAN_WORKFLOW_DESIGN.md`
- [x] **Update Workflow Schema**: Added `position` (x,y,z), `dimensions` (w,h,d), `style` to `Node` class in `pipecatapp/workflow/node.py`.
- [x] **Implement Canvas Converter**: Created `pipecatapp/workflow/canvas_converter.py` for bidirectional conversion.
- [ ] **Verify Conversion**: Write tests to ensure data integrity during round-trip conversion.

## Phase 2: 3D Visualization (Next Steps)
- [ ] **Select 3D Library**: Decide between Three.js (standard web) or A-Frame (VR-first). *Recommendation: Three.js for broad compatibility, wrapped in A-Frame for VR.*
- [ ] **Create 3D Viewer**: Implement `pipecatapp/static/workflow_3d.html`.
    - [ ] Render nodes as 3D objects (boxes/spheres) at correct (x,y,z).
    - [ ] Draw connections as 3D lines/curves.
    - [ ] Implement camera controls (Orbit, Pan, Zoom).
- [ ] **Implement "Semantic Zoom"**:
    - [ ] Define Z-axis layers (e.g., Z=0 Logic, Z=100 Summary).
    - [ ] Add UI slider or scroll interaction to fade layers in/out based on camera depth.

## Phase 3: The "Gardener" Agent (Automation)
- [ ] **File Watcher Service**: Create a background service that monitors the Obsidian Vault path.
- [ ] **Active Document Logic**:
    - [ ] Detect "seeds" (new files/nodes with specific tags).
    - [ ] Parse directives (e.g., `<!-- run: python -->`).
    - [ ] Trigger Workflow execution.
    - [ ] Write results back to the file (Markdown append or Canvas node update).

## Phase 4: Advanced Canvas Features
- [ ] **Scope/Group Support**: Map Canvas "Groups" to Workflow "Scopes" or "Sub-workflows".
- [ ] **Rich Content Embedding**: Allow Workflow nodes to reference local assets (images, PDFs) from the Vault.
- [ ] **Bi-directional Sync**: Real-time updates (using WebSocket) to the open Canvas file in Obsidian (if possible via plugin) or just file polling.
