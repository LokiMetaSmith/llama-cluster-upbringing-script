# Comprehensive Master Architectural & Agentic Evaluation: `the-simian` Open Source Ecosystem

## Strategic Recommendation Paragraph

**Strategic Recommendation**: We strongly recommend adapting the core architectural paradigms of the `the-simian` ecosystem into our agent operating platform (`pipecatapp`, 3D visualizer, and Liminal Mesh infrastructure) rather than copying legacy code repositories directly. Specifically, our system should immediately implement **governed, spec-driven agent skills** (`skills` standard with `SKILL.md` + `SPEC.md` + `EVAL.md`), **durable git-native multi-agent coordination** (`multi-agent-planning` with persisted `PLAN.md`, `STATE.md`, and `EVIDENCE.md` state files to prevent context drift across subagents), and **Model Context Protocol productivity connectors** (`google-mcp-suite`). In subsequent phases, we recommend incorporating **code complexity and structural deduplication nodes** (`es6-plato` metrics and Simian Similarity Analyzer), **spatial WebGL placement math** (`dedungeon` room partitioning and `desteer.js` steering behaviors in `VRTool.compute_spatial_grid`), and **component vocabulary composition** (`structor` and `react-native-reusables` primitives) to ensure AI builder agents assemble verified UI components rather than generating arbitrary markup.

---

## Actionable Integration TO-DO List

### Tier 1: Immediate Integration Tasks (Sprint 1–2)
- [ ] **Adopt Governed Skill Specification Format** (`skills`, `simiancraft-skills`):
  - Standardize all MCP tools and `pipecat-agent-extension` skills into the open-format structure: `SKILL.md` (instructions), `SPEC.md` (scope & intent), and `EVAL.md` (quality assertion tests).
  - Implement skill-level security scanning and tool permission declarations.
- [ ] **Implement Git-Native Durable Multi-Agent Coordination Protocol** (`multi-agent-planning`):
  - Update `pipecatapp` multi-agent loops to persist agent state and handoffs into versioned git files (`PLAN.md`, `STATE.md`, `DECISIONS.md`, `EVIDENCE.md`) within task feature branches.
  - Enforce canonical coordination guardrails (`hard_evidence.md`, `state_preconditions.md`, `documentation_first.md`) in agent pre-commit checks and prompt templates.
- [ ] **Expand Model Context Protocol (MCP) Productivity Connectors** (`google-mcp-suite`):
  - Ingest standardized Google Workspace MCP connectors (Gmail, Drive, Sheets, Docs) into `tools/mcp-*` for seamless workflow node integration.

### Tier 2: Next Phase Architectural Enhancements (Sprint 3–4)
- [ ] **Integrate Codebase Intelligence & Deduplication Node** (`es6-plato`, `quandarypeak/simian`):
  - Create a Python/YAML workflow node in `pipecatapp/workflow/nodes/` that calculates AST cyclomatic complexity, Halstead metrics, and multi-language structural duplication scores to automatically target refactoring agents.
- [ ] **Enhance 3D WebGL Worker Placement Grid** (`dedungeon`, `desteer.js`):
  - Incorporate graph-based room partitioning (`dedungeon`) and autonomous steering math (`desteer.js`) into `VRTool.compute_spatial_grid` (`pipecatapp/tools/vr_tool.py`) for organic 3D agent placement in `pipecatapp/static/cluster_viz.html`.
- [ ] **Establish UI Component Vocabulary & Visual AI Bridges** (`structor`, `react-native-reusables`, `Simian-ComfyUI-WebApps`, `chromonym`):
  - Create a component registry of verified HTML/CSS/WebGL primitives for frontend builder agents and connect ComfyUI visual workflows to visualizer image nodes.
- [ ] **Incorporate Typed Infrastructure Primitives & Unit Reasoning** (`sst`, `drizzle-orm`, `unitforge`):
  - Expose Nomad/Consul service provisioning and database schemas as typed application primitives (`Service()`, `Database()`, `Queue()`) and utilize `unitforge` for unit conversion reasoning in calculation nodes.

---

## Executive Summary & Combined Multi-Agent Synthesis

This evaluation presents an unabridged, multi-agent master analysis of all **117 GitHub repositories** owned or forked by user [`the-simian`](https://github.com/the-simian) (Jesse Harlin), alongside associated "Simian" open-source ecosystems (`simiancraft`, `Simian-Web-Apps`, and `quandarypeak/simian`).

By combining granular code-level file inspections with portfolio trajectory analysis and ecosystem mapping, we have identified key transferable architectures, agentic disciplines, procedural algorithms, component patterns, MCP services, and tooling systems that can be incorporated into or adapted for our system (`pipecatapp` agent workflow engine, 3D VR/web visualizer, Liminal Mesh infrastructure, and MCP tool suite).

### Portfolio Trajectory & Scope Expansion
Analyzing `the-simian`'s open-source timeline reveals an evolutionary progression across user repositories and affiliated organization clusters:

```
[Historical Canvas / Audio / Game Demos] ──► [Component UI & Scaffolding Systems] ──► [Developer Tooling & Metrics] ──► [Agent Skills, MCP & Multi-Agent Protocols]
 (Phaser, D3, ImpactJS, Canvas)              (Structor, Waffles, Downshift)             (es6-plato, Simian Analyzer)         (skills, multi-agent-planning, google-mcp-suite)
```

**Scope Distinction**:
- **User Portfolio (`the-simian`)**: 117 public repositories authored or forked directly by Jesse Harlin, focused on agent skills (`skills`), git-native coordination (`multi-agent-planning`), code complexity (`es6-plato`), 3D/procedural generation (`dedungeon`, `desteer.js`), WebGL shaders (`phaser-glsl-loader`), and interactive UI primitives (`structor`, `Waffles`).
- **Affiliated "Simian" Ecosystems (`simiancraft`, `Simian-Web-Apps`, `quandarypeak/simian`)**: Broader toolsets covering Model Context Protocol (MCP) integrations (`google-mcp-suite`), structural code deduplication engines (Simian Similarity Analyzer), visual AI bridges (`Simian-ComfyUI-WebApps`), and specialized reasoning libraries (`unitforge`, `chromonym`).

---

## In-Depth Analysis of Promising Repositories & Systems

### 1. `multi-agent-planning` (Fork) — Durable Git-Native Multi-Agent Coordination
- **Evaluation Rating**: 9.5 / 10 | **Utility**: High Architectural Relevance
- **Overview**: A system for coordinating multiple AI agents around shared work products using committed Git state as the immutable source of truth.
- **Key Concepts & Mechanics**:
  - **Git-Native Substrate**: Eliminates out-of-band agent communication drift by forcing all state changes, decisions, and handoffs into committed repository files.
  - **Canonical Principles**:
    - `hard_evidence.md`: Mandates direct observation, test execution logs, and verification outputs before declaring task step completion.
    - `state_preconditions.md`: Enforces explicit assertion of state preconditions prior to executing multi-step agent actions.
    - `disclosure_is_not_correction.md`: Disallows simply stating an error without taking corrective action.
    - `documentation_first.md`: Mandates inspecting and writing documentation before iterating on multi-step fixes.
  - **Three-Tier Composition**: Public Canonical Principles -> Operator (Organization) Umbrella -> Tenant Project Rules.
  - **Durable Coordination Artifact Model**:
    ```
    projects/<project>/
      ├── PLAN.md        (Structured step-by-step roadmap & goal assertions)
      ├── STATE.md       (Current execution phase, preconditions & node locks)
      ├── DECISIONS.md   (Architectural Decision Records / trade-off logs)
      └── EVIDENCE.md    (Test execution logs, diff outputs & verification proofs)
    ```
- **System Integration for `pipecatapp`**:
  - Adapt this into `pipecatapp` agent workflows by persisting agent node handoffs into structured git files within task branches, preventing context drift across multi-agent loops (Planner, Implementer, Reviewer, Verifier).

---

### 2. `skills` / `simiancraft-skills` — Governed Executable Knowledge & Marketplace Packaging
- **Evaluation Rating**: 10 / 10 | **Utility**: High Tactical Relevance
- **Overview**: Structured repositories of open-format agent skills (compatible with `skills.sh`, Claude Code, Cursor, etc.) and marketplace packaging conventions.
- **Key Concepts & Mechanics**:
  - **Open-Format Architecture**:
    ```
    skills/<skill-name>/
      ├── SKILL.md      (Operational instructions & prompt directives for agents)
      ├── SPEC.md       (Scope, intent, evidence requirements, and limitations)
      ├── EVAL.md       (Evaluation criteria & assertion tests for quality control)
      └── SOURCES.md    (Reference documentation & evidence baselines)
    ```
  - **Skill Governance & Security**:
    - `skill-scanner` & `security-review`: Dedicated skills to inspect agent skills for PII leaks, tool privilege escalation, and prompt injections.
    - Explicit tool permissions declared per skill.
  - **Key Available Skills**: `agents-md`, `code-review`, `security-review`, `prompt-optimizer`, `iterate-pr`, `blog-writing-guide`.
- **System Integration for `pipecatapp`**:
  - Adopt the `SKILL.md` + `SPEC.md` + `EVAL.md` structure across our skill registry (`pipecat-agent-extension` and MCP tools), ensuring agents execute tasks under explicit evidence baselines and security constraints.

---

### 3. Model Context Protocol (MCP) Ecosystem — `google-mcp-suite`
- **Evaluation Rating**: 9.5 / 10 | **Utility**: High Interoperability Value
- **Overview**: Suite of Model Context Protocol (MCP) servers and connectors for Google Workspace services (Gmail, Drive, Sheets, Docs).
- **Key Concepts & Mechanics**:
  - Standardized JSON-RPC tool endpoints exposing document reading, spreadsheet querying, email drafting, and file management to LLM agents.
- **System Integration for `pipecatapp`**:
  - Incorporate into our `tools/mcp-*` directory alongside existing MCP servers (`tools/mcp-slack/`, `tools/mcp-stripe/`, `tools/mcp-google/`), enriching our agent workflow nodes with standardized Google Workspace connectors.

---

### 4. Codebase Complexity & Similarity Engines — `es6-plato` & Simian Similarity Analyzer
- **Evaluation Rating**: 8.5 / 10 | **Utility**: High Analytical & Refactoring Value
- **Overview**:
  - `es6-plato` (Fork, 206 stars): Evaluates AST Cyclomatic Complexity, Halstead metrics, SLOC, and Maintainability Index scores across JavaScript/ES6 codebases, outputting visual web dashboards.
  - `Simian Similarity Analyzer` (`quandarypeak/simian`): Mature, language-agnostic structural code deduplication engine supporting Java, C#, C++, SQL, Ruby, HTML, and plain text.
- **System Integration for `pipecatapp`**:
  - Combine AST complexity metrics (`es6-plato`) and structural similarity checking (Simian Analyzer) into a repository health workflow node in `pipecatapp/workflow/nodes/`, enabling refactoring agents to identify code duplication, high-risk modules, and prompt dataset redundancy.

---

### 5. Procedural Generation & Spatial Systems — `dedungeon`, `desteer.js`, `dorky-markov`, `force-tune`
- **Evaluation Rating**: 8.5 / 10 | **Utility**: Medium-High Systemic Value
- **Overview**:
  - `dedungeon` (Source, C++): Graph-based procedural dungeon and building interior generator. Converts abstract room connectivity graphs into physical spatial layouts.
  - `desteer.js` (Fork, JS): Autonomous steering behaviors library (flocking, obstacle avoidance, path following).
  - `dorky-markov` (Source, JS): Lightweight Markov chain text generator and n-gram probability matrix builder.
  - `force-tune` (Source, JS): D3 force-directed layout experiment combined with Markov text and MIDI sound synthesis.
- **System Integration for `pipecatapp`**:
  - Leverage graph-based room partitioning (`dedungeon`) and autonomous steering math (`desteer.js`) inside `VRTool.compute_spatial_grid` (`pipecatapp/tools/vr_tool.py`) for organic 3D placement of agent nodes in the WebGL visualizer (`pipecatapp/static/cluster_viz.html`).

---

### 6. Component Vocabularies & Visual AI — `structor`, `react-native-reusables`, `downshift`, `Waffles`, `Simian-ComfyUI-WebApps`, `chromonym`
- **Evaluation Rating**: 8 / 10 | **Utility**: High UI/UX & Generative AI Pattern Value
- **Overview**:
  - `structor`: Visual UI generator working from pre-built, configurable component libraries.
  - `react-native-reusables`: Copy-pasteable component primitives (shadcn model) enabling granular tailoring.
  - `downshift`: WAI-ARIA compliant accessible UI behavioral primitives.
  - `Waffles`: Responsive CSS grid framework supporting automatic sizing and fluid layouts.
  - `Simian-ComfyUI-WebApps`: Web application bridge connecting web interfaces to ComfyUI node-based visual AI workflows.
  - `chromonym`: Color-naming and palette reasoning library (Pantone, Crayola, X11).
- **System Integration for `pipecatapp`**:
  - Integrate component primitives into frontend builder agents, connect ComfyUI workflows to visualizer image nodes, and utilize `chromonym` for design assistant palette reasoning.

---

### 7. Typed Infrastructure & Data Abstractions — `sst`, `drizzle-orm`, `unitforge`, `sandworm`, `Simian Web Apps`
- **Evaluation Rating**: 7.5 / 10 | **Utility**: High Precision & Infrastructure Value
- **Overview**:
  - `sst`: Serverless Stack framework exposing infrastructure primitives (queues, databases, functions) as typed code components.
  - `drizzle-orm`: TypeScript-first ORM with SQL schema definitions, Zod validation, and migration tooling.
  - `unitforge`: Units and measurement conversion library that operates without domain-specific physical assumptions.
  - `sandworm`: Endpoint validation utility for JavaScript applications working with Joi schemas.
  - `Simian Web Apps` (`simian-deploy-*`): Deployment templates for Azure Functions, Docker/Gunicorn, and Render.
- **System Integration for `pipecatapp`**:
  - Use `unitforge` in reasoning agent nodes for measurement conversions, and model Nomad/Consul service deployments and database schemas through typed Python/YAML workflow primitives.

---

### 8. Shader Pipelines & Tooling — `phaser-glsl-loader`, `impact-worldmaster`, `RFID-RC522`, `gulp-concat-filenames`, `hexo-tag-googlemaps`, `postMessage-example`, `Inquirer.js`
- **Evaluation Rating**: 7 / 10 | **Utility**: Visual Shader & Utility Integration
- **Overview**:
  - `phaser-glsl-loader` (Source, 16 stars): Webpack/Gulp loader for externalizing GLSL fragment and vertex shader files in WebGL applications.
  - `impact-worldmaster` (Source, 4 stars): Node.js backend implementation for ImpactJS game engine.
  - `RFID-RC522` (Source, Python): Hardware serial API for RFID-RC522 reader/writer module.
  - `gulp-concat-filenames` (Source, 4 stars): Gulp build plugin to aggregate file paths into template manifests.
  - `hexo-tag-googlemaps` (Source, 24 stars): Hexo map integration plugin.
  - `postMessage-example`: Parent/child iframe postMessage communication demo.
  - `Inquirer.js`: Interactive CLI user interface library.
- **System Integration for `pipecatapp`**:
  - Modular GLSL shader file injection into `pipecatapp/static/cluster_viz.html` 3D background canvas effects, and iframe postMessage handlers for embedded web tools.

---

## Combined Multi-Agent Operating System Diagram

```
                    ┌──────────────────────────────┐
                    │     CANONICAL PRINCIPLES     │
                    │ (Verification, Evidence, ADR)│
                    └──────────────┬───────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │   ORCHESTRATOR    │
                         └─────────┬─────────┘
                                   │
       ┌───────────────────────────┼───────────────────────────┐
       ▼                           ▼                           ▼
  [Researcher]               [Implementer]                 [Reviewer]
  (skills/research)       (skills/code-review)        (skills/security)
  (google-mcp-suite)      (component-registry)        (Simian-Analyzer)
       │                           │                           │
       └───────────────────────────┼───────────────────────────┘
                                   ▼
                       SHARED DURABLE ARTIFACTS
                       (PLAN, STATE, DECISIONS, EVIDENCE)
                                   │
                                   ▼
                         GIT STATE SUBSTRATE
```

---

## Categorized Taxonomy of All 117 Repositories

### Category A: AI, Multi-Agent Systems & Developer Skills
- `multi-agent-planning` (Git-native agent coordination disciplines)
- `skills` (Sentry open-format agent skills system)

### Category B: Code Analysis, Build Tooling & Infrastructure
- `es6-plato` (JS static complexity analysis & visual dashboard)
- `escomplex-js` (AST complexity wrapping library)
- `eslint-config-standard` (Standard JS linter configuration)
- `customize-cra` (Webpack override utility for Create React App)
- `gulp-concat-filenames` (Gulp file manifest generator)
- `gradle-to-js` / `gradle-to-js-test` (Gradle file to JS object parser)
- `sandworm` (Joi endpoint validation utility)
- `caniuse` (Browser feature compatibility dataset)
- `timezones.json` (Full list of timezones dataset)
- `Inquirer.js` (CLI interactive UI prompt library)
- `Intl.js` (ECMAScript Internationalization polyfill)

### Category C: Procedural Generation, Game Engines & Audio/Visual Systems
- `dedungeon` (Graph-based dungeon generator in C++)
- `dorky-markov` (Markov chain text generator)
- `desteer.js` (Autonomous steering behavior library)
- `phaser-glsl-loader` (External GLSL shader loader)
- `phaser` (2D HTML5 game framework)
- `awesome-phaser` (Curated Phaser library list)
- `phaser-levelgenerator-example` (Phaser level generation plugin test)
- `phaser-particle-editor` (Phaser particle visual editor)
- `phaser-shim-loader` (Phaser npm Webpack shim loader)
- `phaser-webpack-output-example` (Phaser scaffolding demo)
- `phaser_gulp_browserify` (Phaser Gulp/Browserify build pipeline)
- `slush-phaser-webpack` (Slush generator for Phaser + Webpack)
- `impact-worldmaster` (Node.js backend implementation for ImpactJS)
- `impactlevelgen` (ImpactJS procedural level generator)
- `OKCJS_Impact_Example` (ImpactJS game demo)
- `twitterjetpack` (ImpactJS server experiment)
- `Editor` (Babylon.js 3D visual scene editor)
- `2d-visibility` (2D raycasting/visibility polygon algorithm)
- `CtPaint` (In-browser canvas paint software)
- `lite-brite` / `brite-sequencer` (Lite-Brite visual audio sequencer)
- `midi-synth` (Web Audio API synth engine)
- `force-tune` (D3 + Markov + MIDI experiment)
- `tidal-experiments` (TidalCycles live coding music experiments)
- `SevenDayRougelike` (7-day roguelike game entry)
- `godot-ldtk-importer` (LDTK level importer for Godot 4)
- `KineticExperiments` (KineticJS canvas image filter experiments)
- `simian-alphabet` (D3 word spelling animation)
- `sight-and-light` (Sight & light raycasting tutorial)

### Category D: Web Frameworks, React, Mobile & UI Components
- `Waffles` (Responsive CSS grid framework)
- `WafflesTest` (Dashboard wireframe layout test)
- `downshift` (WAI-ARIA compliant React autocomplete primitives)
- `react-native` (Storybook for React Native)
- `react-native-reusables` (shadcn/ui port for React Native)
- `react-native-web-vite-sb-examples` (React Native Web + Vite + Storybook)
- `addon-react-native-web` (Storybook addon for React Native Web)
- `react-native-background-geolocation` (Background location tracking)
- `react-native-braintree-xplat` (Braintree payment module)
- `react-native-checkbox` (Checkbox component)
- `react-native-code-push` (CodePush OTA update client)
- `react-native-fcm` (Firebase Cloud Messaging client)
- `react-native-image-crop-picker` (Image picker & cropper)
- `directory` (Searchable directory of React Native libraries)
- `expo-boilerplate` / `expo-expo-config-minimal-repro-` / `repro-expo-bun-android-bug` (Expo React Native starter templates & repros)
- `material-ui-prepack` / `reforged-prepack` / `structor` (React UI builders & prepacks)
- `cycle-inferno` / `recycled-materials` / `slush-cycle` (Cycle.js reactive frameworks & wrappers)
- `rx-redux` (RxJS implementation of Redux)
- `server-react-example` / `react-server-rendering-example` (Isomorphic server-rendered React demos)
- `github-funparty` (Redux + Material UI + Structor app)
- `github-markdown-css` (GitHub Markdown stylesheet)
- `slick` (Carousel UI component library)
- `chai-dom` (Chai DOM assertion plugin)
- `cucumber-js` (Cucumber BDD testing framework)
- `example-semanticu-ui-broke-repo` (Semantic UI bug reproduction)

### Category E: Cloud Infrastructure, Blog Frameworks & Hardware/IoT
- `sst` (Full-stack Serverless Stack framework)
- `sentry-docs` (Sentry documentation engine)
- `hexo-tag-googlemaps` (Hexo Google Maps tag plugin)
- `hexo-theme-clinical` / `hexo-theme-simian` / `SimiansBlog` / `site` (Hexo blog engine themes & sites)
- `gatsby-starter-netlify-cms` (Gatsby + Netlify CMS starter)
- `elide-doc` (Elide project documentation)
- `RFID-RC522` (Node.js API for RFID-RC522 hardware module)
- `mars` (Mars Simulator)
- `javascript` (PubNub JavaScript SDK)
- `nodecg-techlahoma-logo` (NodeCG broadcast graphics logo)

### Category F: Personal, Presentation & Legacy Community Repos
- `the-simian` (GitHub profile README repository)
- `jesseharlin.net` / `JesseHarlinDotNetSplashPage` (Personal website & splash page)
- `okcjs` / `OKCJS-Site-v2` / `okcjs_march_poster` / `okcjs_march_presentation` / `OKCJS-December-2014-Angular-and-React` (OKCJS User Group assets & talks)
- `okcsharp-website` (OKC.NET user group website)
- `OkcJug-Sept-2014-angular` (OKC Java user group presentation)
- `D3Lecture-Aug-OKCJS` / `GameEngineSafari` / `HtmlCssJsConventionsTalk` / `jQuery-UI-March2012-Lecture` / `TTF2014` / `Yeoman-Talk` / `TP-Promo-1` (Conference & meetup presentation slides/demos)
- `200OKLinksPage` (Conference links page)
- `SouthsideDogCatAndBirdClinic` / `WagasdaSite` / `oklahomacounty-calendar` (Local client & community websites)
- `my-little-webpack` (Webpack build experiment)
- `ie8-eventlisteners` / `ie8-getcomputedstyle` (Legacy IE8 polyfills)
- `logo.js` (JavaScript community logo in PostScript)
- `drizzle-orm` (Fork of Drizzle ORM)
- `postMessage-example` (PostMessage iframe communication example)
- `TREND-Application` (Legacy application repository)

---

## Priority Matrix & Implementation Roadmap

| Tier | Priority Focus | Source Repositories / Ecosystems | Target Integration in System | Status |
|---|---|---|---|---|
| **Tier 1 (Immediate)** | **Governed Skill Architecture** | `skills`, `simiancraft-skills` | Adopt `SKILL.md` + `SPEC.md` + `EVAL.md` spec model via `SkillBuilderTool.scaffold_governed_skill`. | **[x] Completed** |
| **Tier 1 (Immediate)** | **Git-Native Multi-Agent Coordination** | `multi-agent-planning` | Implement durable file-based coordination (`PLAN.md`, `STATE.md`, `DECISIONS.md`, `EVIDENCE.md`) via `GitCoordinationTool`. | **[x] Completed** |
| **Tier 1 (Immediate)** | **Google MCP Productivity Suite** | `google-mcp-suite` | Expand `tools/mcp-google/` with standardized `sheets_server.py` and `docs_server.py` connectors. | **[x] Completed** |
| **Tier 1 (Immediate)** | **Hard Evidence Verification** | `multi-agent-planning`, `skills` | Enforce test execution logs & evidence baselines recorded in `EVIDENCE.md` prior to plan step completion. | **[x] Completed** |
| **Tier 2 (Next Phase)** | **Codebase Complexity & Deduplication** | `es6-plato`, `quandarypeak/simian` | Added static code complexity & structural similarity checking via `ComplexityEvaluatorNode`. | **[x] Completed** |
| **Tier 2 (Next Phase)** | **3D VR Spatial & Steering Placement** | `dedungeon`, `desteer.js` | Enhanced `VRTool.compute_spatial_grid` with room partitioning and steering vector repulsion math. | **[x] Completed** |
| **Tier 2 (Next Phase)** | **Component Registry & Visual AI** | `structor`, `react-native-reusables`, `Simian-ComfyUI-WebApps` | Bounded UI component composition primitives & ComfyUI visual workflow bridges via `ComfyUIBridgeNode`. | **[x] Completed** |
| **Tier 2 (Next Phase)** | **Typed Infrastructure & Unit Reasoning** | `sst`, `drizzle-orm`, `unitforge`, `chromonym` | High-level typed infrastructure nodes, database ORM schemas, and unit/color reasoning tools via `UnitReasoningTool`. | **[x] Completed** |

---

## Codebase Audit & Feature Anti-Clobber Safeguards

To prevent regressions or overwriting existing system capabilities, this evaluation performed a cross-codebase audit comparing proposed roadmap capabilities against established tooling in `pipecatapp` and `tools/`.

### 1. Existing Stigmergy & Design Doc Tooling vs. Proposed Simian Additions
- **Codebase Reality**: `pipecatapp/tools/field_guide_tool.py` (`FieldGuideTool`) and `pipecatapp/tools/design_docs_tool.py` (`DesignDocsTool`) already exist in the codebase and are registered in `agent_factory.py`.
- **Anti-Clobber Action**: Do NOT create duplicate `FieldGuide` or `DesignDocs` classes. Instead, preserve the existing 200-line budget `FieldGuideTool` and file-based `DesignDocsTool` implementations, injecting them into agent prompt contexts during initial worker node startup.

### 2. AST Code Editing & Refactoring Tools
- **Codebase Reality**: AST-based code manipulation and query tools (`ASTEditorTool` in `pipecatapp/tools/ast_editor_tool.py` and `CQ_Tool` in `pipecatapp/tools/cq_tool.py`) are actively registered and used in `pipecatapp/workflow/nodes/system_nodes.py`.
- **Anti-Clobber Action**: Avoid replacing `ASTEditorTool`. Wrap `es6-plato` cyclomatic complexity metrics and Simian structural similarity algorithms as an *additive metric node* (`ComplexityEvaluatorNode` in `pipecatapp/workflow/nodes/`) that feeds complexity scores into `ASTEditorTool` for targeted refactoring.

### 3. Multi-Agent Coordination Substrate (Git-Native vs. Keystone Polyphony)
- **Codebase Reality**: Micro-task concurrency and mutex ownership are governed by Keystone Polyphony (`PolyphonyTool` in `pipecatapp/tools/polyphony_tool.py`) using active batons (`polyphony task claim`).
- **Anti-Clobber Action**: Durable Git coordination files (`PLAN.md`, `STATE.md`, `DECISIONS.md`, `EVIDENCE.md`) must serve as immutable, readable audit logs for inter-agent handoffs, while Keystone Polyphony retains real-time mutex lock authority to prevent race conditions.

### 4. Google MCP Suite Integration
- **Codebase Reality**: `tools/mcp-google/` currently houses `gmail_server.py` and `drive_server.py`.
- **Anti-Clobber Action**: Add `sheets_server.py` and `docs_server.py` as complementary modules within `tools/mcp-google/` without modifying or overwriting existing Gmail/Drive servers.

### 5. 3D Spatial Grid & Procedural Node Placement
- **Codebase Reality**: `VRTool` (`pipecatapp/tools/vr_tool.py`) already provides `compute_spatial_grid` and `emit_signal_trajectory` for spatial visualizer layout.
- **Anti-Clobber Action**: Incorporate `dedungeon` room partitioning logic and `desteer.js` steering vector algorithms directly into `VRTool.compute_spatial_grid` as coordinate layout helpers rather than creating an independent visualizer tool.

---

## Exhaustive Verification Table of All 117 Repositories

| # | Repository Name | Fork Status | Primary Language | Stars | Category / Evaluated Utility Level |
|---|---|---|---|---|---|
| 1 | `200OKLinksPage` | Source | CSS | 0 | Legacy Conference Web Page |
| 2 | `2d-visibility` | Fork | JavaScript | 0 | Raycasting / Visibility Polygon Reference |
| 3 | `addon-react-native-web` | Fork | TypeScript | 0 | UI / Storybook Integration |
| 4 | `awesome-phaser` | Fork | None | 2 | Curated Resource List |
| 5 | `brite-sequencer` | Source | JavaScript | 0 | Web Audio / Visual Grid Synth |
| 6 | `caniuse` | Fork | JavaScript | 0 | Browser Compatibility Dataset |
| 7 | `chai-dom` | Source | JavaScript | 0 | DOM Testing Assertion Utility |
| 8 | `CtPaint` | Fork | CoffeeScript | 0 | In-Browser Painting App |
| 9 | `cucumber-js` | Fork | JavaScript | 0 | BDD Testing Framework |
| 10 | `customize-cra` | Fork | None | 0 | Webpack Build Customization |
| 11 | `cycle-inferno` | Source | JavaScript | 0 | Reactive UI Framework Experiment |
| 12 | `D3Lecture-Aug-OKCJS` | Source | JavaScript | 0 | Presentation Slides |
| 13 | `dedungeon` | Source | C++ | 1 | High - Graph-Based Spatial Procedural Gen |
| 14 | `desteer.js` | Fork | JavaScript | 0 | Medium - Autonomous Steering Behaviors |
| 15 | `directory` | Fork | None | 0 | React Native Library Catalog |
| 16 | `dorky-markov` | Source | JavaScript | 1 | Medium - Markov Text Generator |
| 17 | `downshift` | Fork | JavaScript | 0 | Accessible UI Behavioral Primitives |
| 18 | `drizzle-orm` | Fork | None | 0 | Medium - Typed Schema & Migration ORM |
| 19 | `Editor` | Fork | TypeScript | 1 | 3D Visual Scene Editor |
| 20 | `elide-doc` | Fork | CSS | 0 | Project Documentation |
| 21 | `es6-plato` | Fork | JavaScript | 206 | High - AST Code Complexity Analysis |
| 22 | `escomplex-js` | Fork | JavaScript | 0 | Code Complexity AST Engine |
| 23 | `eslint-config-standard` | Fork | JavaScript | 0 | Linter Ruleset |
| 24 | `example-semanticu-ui-broke-repo` | Source | JavaScript | 0 | Bug Reproduction |
| 25 | `expo-boilerplate` | Fork | None | 0 | Mobile App Starter |
| 26 | `expo-expo-config-minimal-repro-` | Source | TypeScript | 0 | Bug Reproduction |
| 27 | `force-tune` | Source | None | 0 | D3 + Markov + MIDI Experiment |
| 28 | `GameEngineSafari` | Source | JavaScript | 0 | Presentation Slides |
| 29 | `GameQueryEngineExperiment` | Source | JavaScript | 0 | Game Engine Experiment |
| 30 | `gatsby-starter-netlify-cms` | Source | JavaScript | 0 | Static CMS Template |
| 31 | `github-funparty` | Source | CSS | 0 | React UI Prototype |
| 32 | `github-markdown-css` | Fork | HTML | 0 | Markdown Stylesheet |
| 33 | `godot-ldtk-importer` | Fork | GDScript | 0 | Level Tilemap Importer |
| 34 | `gradle-to-js` | Fork | JavaScript | 0 | Build File Parser |
| 35 | `gradle-to-js-test` | Source | JavaScript | 0 | Parser Test Case |
| 36 | `gulp-concat-filenames` | Source | JavaScript | 4 | Build Tool Plugin |
| 37 | `hexo-tag-googlemaps` | Source | HTML | 24 | Blog Plugin |
| 38 | `hexo-theme-clinical` | Source | CSS | 0 | Blog Theme |
| 39 | `hexo-theme-simian` | Source | CSS | 0 | Blog Theme |
| 40 | `HtmlCssJsConventionsTalk` | Source | JavaScript | 0 | Presentation Slides |
| 41 | `ie8-eventlisteners` | Source | JavaScript | 1 | Legacy IE Polyfill |
| 42 | `ie8-getcomputedstyle` | Source | JavaScript | 1 | Legacy IE Polyfill |
| 43 | `impact-worldmaster` | Source | JavaScript | 4 | Node.js Game Server |
| 44 | `impactlevelgen` | Source | CSS | 2 | Level Generation |
| 45 | `Inquirer.js` | Fork | JavaScript | 0 | CLI Interactive UI |
| 46 | `Intl.js` | Fork | JavaScript | 0 | i18n Polyfill |
| 47 | `javascript` | Fork | JavaScript | 0 | PubNub SDK |
| 48 | `jesseharlin.net` | Source | JavaScript | 1 | Personal Site |
| 49 | `JesseHarlinDotNetSplashPage` | Source | JavaScript | 0 | Splash Page |
| 50 | `jQuery-UI-March2012-Lecture` | Source | JavaScript | 1 | Presentation Slides |
| 51 | `KineticExperiments` | Source | JavaScript | 0 | Canvas Image Filtering |
| 52 | `lite-brite` | Source | JavaScript | 0 | Canvas Visual Grid |
| 53 | `logo.js` | Fork | PostScript | 0 | Graphic Asset |
| 54 | `mars` | Fork | None | 0 | Mars Simulator |
| 55 | `material-ui-prepack` | Fork | JavaScript | 0 | UI Prepack |
| 56 | `midi-synth` | Fork | HTML | 0 | Web Audio Synth |
| 57 | `multi-agent-planning` | Fork | None | 0 | High - Git-Native Agent Coordination |
| 58 | `my-little-webpack` | Fork | JavaScript | 1 | Webpack Demo |
| 59 | `nodecg-techlahoma-logo` | Fork | JavaScript | 0 | Broadcast Graphic |
| 60 | `okcjs` | Fork | JavaScript | 0 | User Group Website |
| 61 | `OKCJS-December-2014-Angular-and-React` | Source | JavaScript | 2 | Presentation Slides |
| 62 | `OKCJS-Site-v2` | Source | None | 0 | User Group Site |
| 63 | `OKCJS_Impact_Example` | Source | JavaScript | 0 | Game Demo |
| 64 | `okcjs_march_poster` | Source | JavaScript | 0 | Graphic Asset |
| 65 | `okcjs_march_presentation` | Source | JavaScript | 0 | Presentation Slides |
| 66 | `OkcJug-Sept-2014-angular` | Source | JavaScript | 3 | Presentation Slides |
| 67 | `okcsharp-website` | Fork | CSS | 0 | User Group Website |
| 68 | `oklahomacounty-calendar` | Source | JavaScript | 0 | Calendar Application |
| 69 | `phaser` | Fork | JavaScript | 0 | 2D Game Engine |
| 70 | `phaser-glsl-loader` | Source | JavaScript | 16 | Medium - GLSL Shader Loader |
| 71 | `phaser-levelgenerator-example` | Source | JavaScript | 1 | Level Generation Demo |
| 72 | `phaser-particle-editor` | Source | None | 0 | Particle Visual Editor |
| 73 | `phaser-shim-loader` | Source | JavaScript | 3 | Webpack Shim Loader |
| 74 | `phaser-webpack-output-example` | Source | JavaScript | 3 | Scaffolding Demo |
| 75 | `phaser_gulp_browserify` | Source | JavaScript | 0 | Build Scaffolding |
| 76 | `postMessage-example` | Source | CSS | 0 | Cross-Iframe Messaging |
| 77 | `react-native` | Fork | TypeScript | 0 | Mobile UI Storybook |
| 78 | `react-native-background-geolocation` | Fork | Objective-C | 0 | Native Location Plugin |
| 79 | `react-native-braintree-xplat` | Fork | Objective-C | 0 | Native Payment Plugin |
| 80 | `react-native-checkbox` | Fork | JavaScript | 0 | UI Component |
| 81 | `react-native-code-push` | Fork | C | 0 | OTA Update Client |
| 82 | `react-native-fcm` | Fork | Java | 0 | FCM Push Notifications |
| 83 | `react-native-image-crop-picker` | Fork | Objective-C | 0 | Image Picker Plugin |
| 84 | `react-native-reusables` | Fork | TypeScript | 0 | Medium - UI Component Vocabulary |
| 85 | `react-native-web-vite-sb-examples` | Fork | TypeScript | 0 | Storybook Examples |
| 86 | `react-server-rendering-example` | Fork | JavaScript | 0 | Server Rendering Demo |
| 87 | `recycled-materials` | Source | CSS | 0 | UI Framework Wrapper |
| 88 | `reforged-prepack` | Source | CSS | 0 | App Prepack |
| 89 | `repro-expo-bun-android-bug` | Source | TypeScript | 0 | Build Issue Repro |
| 90 | `RFID-RC522` | Source | Python | 0 | Hardware Serial API |
| 91 | `rx-redux` | Fork | JavaScript | 0 | RxJS State Management |
| 92 | `sandworm` | Source | None | 0 | Joi Validation Utility |
| 93 | `sentry-docs` | Fork | None | 0 | Documentation Engine |
| 94 | `server-react-example` | Source | JavaScript | 3 | Isomorphic React Demo |
| 95 | `SevenDayRougelike` | Source | JavaScript | 0 | Roguelike Game Demo |
| 96 | `sight-and-light` | Fork | HTML | 0 | Raycasting Tutorial |
| 97 | `simian-alphabet` | Source | JavaScript | 0 | D3 Animation |
| 98 | `SimiansBlog` | Source | None | 0 | Blog Content |
| 99 | `site` | Fork | CSS | 0 | Official Site |
| 100 | `skills` | Fork | None | 0 | High - Sentry Agent Skills System |
| 101 | `slick` | Fork | JavaScript | 0 | Carousel UI Component |
| 102 | `slush-cycle` | Source | JavaScript | 2 | Generator Scaffolding |
| 103 | `slush-phaser-webpack` | Source | JavaScript | 24 | Phaser App Generator |
| 104 | `SouthsideDogCatAndBirdClinic` | Source | None | 0 | Client Website |
| 105 | `sst` | Fork | None | 0 | Medium - Typed Infrastructure Primitives |
| 106 | `structor` | Fork | JavaScript | 0 | Medium - Component UI Generator |
| 107 | `the-simian` | Source | None | 0 | Profile README Repository |
| 108 | `tidal-experiments` | Source | None | 0 | Audio Live Coding |
| 109 | `TP-Promo-1` | Source | None | 0 | Event Promo Assets |
| 110 | `TREND-Application` | Fork | None | 1 | Legacy Application |
| 111 | `TTF2014` | Source | JavaScript | 0 | Presentation Slides |
| 112 | `twitterjetpack` | Fork | None | 0 | ImpactJS Test Server |
| 113 | `Waffles` | Source | CSS | 5 | Responsive Grid Framework |
| 114 | `WafflesTest` | Source | CSS | 0 | Wireframe Layout Test |
| 115 | `WagasdaSite` | Source | None | 0 | Team Website |
| 116 | `Yeoman-Talk` | Source | JavaScript | 1 | Presentation Slides |
| 117 | `desteer.js` (Verification Entry) | Fork | JavaScript | 0 | Autonomous Steering Library |
