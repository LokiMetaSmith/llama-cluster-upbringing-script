# ToDo: Architecting a Responsive, Distributed Conversational AI Pipeline

This document outlines the action plan for refactoring the project to use a modern, distributed architecture based on the technical report. All phases are now complete.

## Phase 1: Cluster Orchestration with Nomad
- [x] **Create a Nomad Ansible Role:**
  - [x] Create a new Ansible role named `nomad`.
  - [x] This role will download and install the Nomad binary on all nodes in the cluster.
  - [x] It will configure a systemd service for Nomad.
  - [x] It will have separate tasks for server and client configurations.
- [x] **Update the Main Playbook:**
  - [x] Add the `nomad` role to the main `playbook.yaml`.

## Phase 2: Distributed LLM with prima.cpp
- [x] **Create a `prima.cpp` Ansible Role:**
  - [x] Create a new Ansible role named `primacpp`.
  - [x] This role will install dependencies and compile `prima.cpp`.
- [x] **Create a Nomad Job for `prima.cpp`:**
  - [x] Create a Nomad job file (`primacpp.nomad`) to run the `prima.cpp` cluster.

## Phase 3: Conversational AI Pipeline with pipecat
- [x] **Create a `pipecat_app` Ansible Role:**
  - [x] Create a new Ansible role named `pipecatapp` to manage Python dependencies.
- [x] **Develop the `pipecat` Application:**
  - [x] Create a Python application (`app.py`) that uses the `pipecat` framework.
- [x] **Create a Nomad Job for the `pipecat` Application:**
  - [x] Create a Nomad job file (`pipecatapp.nomad`) to run the `pipecat` application.

## Phase 4: Integration, Testing, and Documentation
- [x] **Update `README.md`:**
  - [x] Update the `README.md` to document the new, Nomad-based deployment process.
- [x] **Testing:**
  - [x] Add verification steps for each phase to the `ToDo.md`.

## Phase 5: Vision Integration
- [x] **Create a `vision` Ansible Role:**
  - [x] Create a new Ansible role named `vision` for video processing dependencies.
- [x] **Develop the Vision Service:**
  - [x] Create a custom `pipecat` service (`YOLOv8Detector`) in `app.py`.
- [x] **Update Documentation for Vision Capabilities:**
  - [x] Add a section to `README.md` explaining the new vision feature.

## Phase 6: Agent Embodiment with TwinService
- [x] **Create `TwinService`:**
  - [x] Create a new `FrameProcessor` class in `app.py` called `TwinService`.
- [x] **Implement Memory:**
  - [x] Create a `MemoryStore` class to manage a file-based vector store.
- [x] **Implement Tool Use:**
  - [x] Create a tool-use framework in `TwinService`.
  - [x] Add `ssh_tool` and `mcp_tool`.
- [x] **Integrate into Pipeline:**
  - [x] Modify the main `pipecat` pipeline to be `STT -> TwinService -> TTS`.
- [x] **Update Documentation:**
  - [x] Update the `README.md` to explain the new agentic capabilities.

## Phase 7: Self-Reflection and Growth with OpenEvolve
- [x] **Create `prompt_engineering` Directory:**
  - [x] Create a new top-level directory `prompt_engineering`.
  - [x] Add a `requirements-dev.txt` file with the `openevolve` dependency.
- [x] **Create Evaluation Suite:**
  - [x] Create a directory `prompt_engineering/evaluation_suite`.
  - [x] Create YAML-based test cases for evaluating prompt performance.
- [x] **Create `evaluator.py`:**
  - [x] Create the fitness function script that runs the test suite against a candidate prompt.
- [x] **Create `evolve.py`:**
  - [x] Create the main script to run the `openevolve` process.
- [x] **Update Documentation:**
  - [x] Create a new `PROMPT_ENGINEERING.md` file to document the workflow.

---

## References
- **[prima.cpp](https://github.com/gitalbenar/prima.cpp):** The distributed LLM inference engine.
- **[pipecat-ai](https://github.com/pipecat-ai/pipecat):** The real-time, streaming conversational AI framework.
- **[physiii/twin](https://github.com/physiii/twin):** The agent embodiment framework that inspired the `TwinService`.
- **[codelion/openevolve](https://github.com/codelion/openevolve):** The AlphaEvolve implementation for prompt engineering.
- **[geerlingguy/beowulf-ai-cluster](https://github.com/geerlingguy/beowulf-ai-cluster):** The Ansible benchmarking project.
