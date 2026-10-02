# Evaluation of Tangle for Inclusion vs. Feature Extraction

## Executive Summary

This document evaluates the [TangleML/tangle](https://github.com/TangleML/tangle) orchestration project to determine the feasibility of either including it fully as a backend service or extracting specific features (such as its visual DAG UI and component format) to augment our existing architecture.
Given the recent stabilization of the `pipecatapp` Workflow Engine to run statelessly across our clustered hardware and our strict 8GB per-node memory limitations, deploying a heavy, standalone Tangle backend (which uses its own orchestration layer, database, and launcher system) is not feasible.
Therefore, the recommendation is to pursue **Feature Extraction**, specifically targeting Tangle's visual drag-and-drop DAG frontend and its standardized component specification format.

## Architecture Fit (Augmenting `pipecatapp`)

Our current system manages jobs via Nomad and uses the `pipecatapp` Workflow Engine, relying on Consul KV for state management to avoid memory bloat.
Tangle's backend (`cloud_pipelines_backend`) acts as a full-fledged orchestrator. It uses an SQL database (via SQLAlchemy) to maintain state and implements its own `Launcher` interfaces (e.g., Docker, Kubernetes, SkyPilot) to schedule containerized jobs. Introducing this backend would duplicate our existing Nomad scheduling and Consul state management logic, while significantly exceeding our 8GB memory cap due to the heavy FastAPI + SQLAlchemy stack running alongside our existing services.
However, Tangle’s **Component Specification** format is highly standardized and heavily inspired by Kubeflow Pipelines (KFP). It defines tasks via a `ComponentSpec` (YAML/JSON) detailing inputs, outputs, implementation, and container specifications. This format can be easily parsed by our existing Python applications without needing the entire Tangle orchestration backend.

## Feature Extraction Analysis

### 1. Component Specification Format

The `ComponentSpec` (found in `cloud_pipelines_backend/component_structures.py`) defines a clean `dataclass` structure for components:

* `InputSpec` / `OutputSpec`
* `ContainerSpec` (image, command, args, env)
* `GraphSpec` (for DAGs and tasks)
**Actionable Insight:** We can easily extract the KFP-like `ComponentSpec` logic. By adopting this schema, we can standardize how we define tools and workflows in our `pipecatapp` Workflow Engine. The definitions can be stored as YAML/JSON and loaded dynamically without requiring Tangle's database.

### 2. Visual Drag-and-Drop DAG UI

Tangle's UI is completely decoupled from its backend. The Tangle repository instructs users to clone a separate repository (`TangleML/tangle-ui`) to get the frontend build artifacts, which the backend then serves as static files using FastAPI's `StaticFiles`.
**Actionable Insight:** Because the frontend is a static Single Page Application (SPA), we can extract the UI layer entirely.

* We can serve the frontend as a lightweight static asset (e.g., via NGINX or directly embedded in our existing UI).
* We would need to implement an API translation layer within our existing `pipecatapp` application that mimics Tangle's REST API endpoints (e.g., `/api/components`, `/api/pipeline_runs`) but routes the execution and state retrieval through our existing Nomad/Consul architecture.

## Decoupling Feasibility (Frontend vs Backend Separation)

Tangle achieves decoupling by relying strictly on REST API communication between the UI and backend.

* **Backend:** Defines API routes in `api_router.py` for managing components, pipelines, runs, and secrets.
* **Frontend:** A standalone SPA that makes standard HTTP requests.

This makes it extremely feasible to discard the Tangle backend entirely. We can write a lightweight adapter in our `pipecatapp` that exposes the necessary endpoints for the Tangle UI to render the visual DAG, while translating run requests into native Nomad job submissions.

## Resource Implications (Addressing the 8GB Node Limit)

* **Full Inclusion (Rejected):** Running Tangle’s FastAPI backend + SQLAlchemy database + background poller loop would consume significant RAM and CPU, violating the strict 8GB memory limits on our legacy compute nodes.
* **Feature Extraction (Recommended):** By extracting the YAML Component Specification parser and utilizing the pre-built static SPA frontend, the memory footprint added to our system is negligible. The static files can be served with minimal overhead, and the component parser runs as lightweight native Python within our existing, strictly bound container tasks.

## Recommendation

**Proceed with Feature Extraction.**

1. **Do not deploy the Tangle backend.**
2. Adopt the KFP-style `ComponentSpec` format for defining our internal `pipecatapp` workflow components.
3. Investigate adapting the `tangle-ui` SPA to communicate with a lightweight translation layer inside `pipecatapp`, allowing us to use its drag-and-drop DAG builder to visualize and construct Nomad workflows.
