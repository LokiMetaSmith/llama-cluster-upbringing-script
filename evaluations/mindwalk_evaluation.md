# Evaluation of cosmtrek/mindwalk for Feature Ingestion

## 1. Executive Summary & Recommendation

This report evaluates **cosmtrek/mindwalk**, a local 3D visualization tool that replays coding-agent sessions over a map of a repository. It analyzes the feasibility of full integration versus feature ingestion into the Pipecat-App ecosystem, focusing on compatibility, footprint, and active data pipelines.

**Recommendation: High-Priority Feature Ingestion (No Full Inclusion).**
* **Why No Full Inclusion?** Full inclusion of `mindwalk` would introduce dual Go and Node.js compilation runtimes, run a background local daemon, and require a heavy, local WebGL/Three.js-heavy frontend stack. This is redundant for our containerized, resource-constrained Nomad cluster nodes.
* **Why Feature Ingestion?** The core architectural insight of `mindwalk` is extremely powerful: **representing agent execution visually as a glowing timeline path of "heat" or "light" over a codebase structure**.
* **Ingestion Strategy:** We will adopt the lightweight data schemas of `mindwalk` (under `schema/`) to build a **Telemetry Trace Adapter** inside `pipecatapp`. This adapter will parse our agent session logs (such as workflow contexts, execution histories, and tool results) and format them into standardized, local-first trace logs. These traces can then be directly replayed, or used to drive custom retro-futuristic visualization widgets inside **CommandDeck** or **OpenGravity** without the overhead of a standalone Go app.

---

## 2. Technical Profile of Mindwalk

### A. Core Concepts
`mindwalk` separates the replay system into two highly decoupled components:
1. **The Citymap (`citymap.schema.json`):** A deterministic layout of the codebase where files are arranged into a tree or a flat terrain using rectangles (`x, z, w, d`). The same repository structure always generates the exact same visual coordinate map.
2. **The Trace (`trace.schema.json`):** A normalized, linear stream of "file-touch" event sequences indicating exactly when and how the agent interacted with files (observation vs mutation).

### B. Language & Tech Stack
* **Backend:** Written in **Go**, which parses Claude Code/Codex JSONL logs, generates the deterministic layout, maps the repository structure, merges the trace data, and serves the static build.
* **Frontend:** Built with **React** and **Three.js** (via React Three Fiber/Drei). It draws the codebase as a "night map" and plays the session back as moving streams of light.

### C. Runtime & Memory Footprint
* The Go backend is highly lightweight (~15MB RAM) and serves local requests.
* The frontend relies heavily on GPU-accelerated WebGL. On low-power hardware (such as our core 2 Duo mesh nodes), rendering full 3D interactive citymaps in real-time can create significant graphics pipeline bottlenecks. This reinforces our choice to focus on feature ingestion—selectively using lightweight frontend dashboards and timeline HUD elements rather than full 3D graphics rendering.

---

## 3. Core Architectural Insights (Timeline & Visual Replay)

`mindwalk` introduces several UX-altering features that we can selectively ingest:

```
  Seen (Moss Green)   ──>   Read (Moon White)   ──>   Edited (Warm Amber)
     (observation)             (observation)               (mutation)
```

1. **Persistent Deepest Touch States:**
   * Files keep their highest level of interaction: **Seen/Hit (Moss Green)**, **Read (Moon White)**, and **Edited (Warm Amber)**.
   * This provides an instant visual heuristic of the agent's "understanding boundary" vs. its "action boundary."
2. **Cool vs. Warm Playback Timeline:**
   * **Observation phases** (searching, reading files, reading terminal output) are colored **cool** (blues/teals).
   * **Mutation/Verification phases** (writing files, running tests/verify commands) are colored **warm** (yellows/orange/amber).
   * This lets developers visually spot where the agent spent its time wandering/thinking vs. where it actually executed changes.
3. **Timeline Marks & Navigation:**
   * Key orchestration moments like context compactions, subagent launches, and user feedback loops are represented as interactive nodes on the playback rail. Developers can click on a mark to jump the playhead to that exact moment.

---

## 4. Schema Evaluation & Telemetry Mapping

The underlying telemetry schemas are exceptionally lightweight and map cleanly onto our existing pipelines.

### A. Trace Schema Suitability
The `trace.schema.json` is simple and fully local-first. It aggregates session metadata, statistical metrics, events, and timeline marks. This maps directly to our workflow execution logs.

### B. Action/Tool Mapping
We can map our existing `pipecatapp` tool invocations to the standardized `mindwalk` trace action types:

| Our Tool | Mindwalk Action Type | Description / Heuristic |
| :--- | :--- | :--- |
| `search`, `lightweight_project_mapper`, `schema_mapper` | **`search`** | Scans directories, maps structure, or queries DB schemas. |
| `archivist`, `document_tool`, `rag` | **`read`** | Reads file content or fetches documentation chunks. |
| `file_editor`, `ast_editor` | **`edit`** | Modifies codebase files. |
| `shell`, `code_runner`, `ssh`, `web_browser` | **`exec`** | Executes terminal commands or custom script pipelines. |
| `ansible`, `dependency_scanner`, `submit_solution` | **`verify`** | Performs validations, checks syntax, or submits task solutions. |
| `ouroboros`, `atproto`, `scheduler` | **`other`** | General API interactions, sync routines, or orchestration loops. |

### C. Stats Extraction
The telemetry format embeds high-value analytical stats that we can compute on-the-fly:
* **Churn rate:** Unique files that were edited in 3 or more separate step sequences.
* **Edits after last verify:** Helps catch whether the agent made edits without verifying syntax/compilation at the end.
* **Error Rate:** Ratio of failed step/tool executions to successful ones.

---

## 5. Feature Ingestion Roadmap for CommandDeck & OpenGravity

Instead of running a separate visualizer, we can implement these mechanics natively:

### A. Ingestion into CommandDeck
* **Visual Playback Rail:** Add a linear canvas playback bar to the bottom of the execution monitor. Color-code the execution blocks along the cool/warm spectrum according to the tool type being run.
* **Step Navigator:** Render timeline marks (user turns, subagents spawned, error occurrences) on the progress bar, allowing users to scrub or hover to see the context of that specific execution step.
* **Retro HUD Metrics:** Render the calculated session stats (error rate, file churn, edits-after-last-verify) directly on CommandDeck's Evangelion-themed sidebar.

### B. Ingestion into OpenGravity
* **Interactive Code Map Workspace:** Use the deterministically computed lightweight tree schema to draw a clean radial code explorer.
* **Live Glowing File Tree:** As the proactive agent executes code or reads files via the WebContainer environment, make the corresponding file-tree nodes glow in moss green (searched/hit), moon white (read), or warm amber (modified) in real-time.

---

## 6. Active Prototyping: Telemetry Exporter (`MindwalkTraceExporter`)

To facilitate feature ingestion, we will scaffold a Python-based **`MindwalkTraceExporter`** inside `pipecatapp/utils/mindwalk_exporter.py`.

This exporter will:
1. Accept our agent step sequences or workflow execution state outputs.
2. Maintain counters and calculate the exact mathematical metrics required by the mindwalk schema (such as `churnFiles`, `editsAfterLastVerify`, `regressionRate`, and `maxEditsPerFile`).
3. Export a strict JSON trace conforming entirely to `trace.schema.json` version 1, ready for immediate ingestion or visual playback rendering.
