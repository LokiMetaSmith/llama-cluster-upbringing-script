# ToDo: Architecting a Responsive, Distributed Conversational AI Pipeline

This document outlines the action plan for refactoring the project to use a modern, distributed architecture based on the technical report. All phases are now complete.

## Phase 1: Cluster Orchestration with Nomad
- [x] **Create a Nomad Ansible Role:**
  - [x] Create a new Ansible role named `nomad`.
- [x] **Update the Main Playbook:**
  - [x] Add the `nomad` role to the main `playbook.yaml`.

## Phase 2: Distributed LLM with prima.cpp
- [x] **Create a `prima.cpp` Ansible Role:**
  - [x] Create a new Ansible role named `primacpp`.
- [x] **Create a Nomad Job for `prima.cpp`:**
  - [x] Create a Nomad job file (`primacpp.nomad`).

## Phase 3: Conversational AI Pipeline with pipecat
- [x] **Create a `pipecat_app` Ansible Role:**
  - [x] Create a new Ansible role named `pipecatapp`.
- [x] **Develop the `pipecat` Application:**
  - [x] Create a Python application (`app.py`).
- [x] **Create a Nomad Job for the `pipecat` Application:**
  - [x] Create a Nomad job file (`pipecatapp.nomad`).

## Phase 4: Integration, Testing, and Documentation
- [x] **Update `README.md`:**
  - [x] Update the `README.md` to document the deployment process.
- [x] **Testing:**
  - [x] Add verification steps for each phase.

## Phase 5: Vision Integration
- [x] **Create a `vision` Ansible Role:**
  - [x] Create a new Ansible role named `vision`.
- [x] **Develop the Vision Service:**
  - [x] Create a custom `pipecat` service (`YOLOv8Detector`).
- [x] **Update Documentation for Vision Capabilities:**
  - [x] Add a section to `README.md`.

## Phase 6: Agent Embodiment with TwinService
- [x] **Create `TwinService`:**
  - [x] Create a new `FrameProcessor` class in `app.py`.
- [x] **Implement Memory:**
  - [x] Create a `MemoryStore` class.
- [x] **Implement Tool Use:**
  - [x] Create a tool-use framework in `TwinService`.
- [x] **Integrate into Pipeline:**
  - [x] Modify the main `pipecat` pipeline.
- [x] **Update Documentation:**
  - [x] Update the `README.md`.

## Phase 7: Self-Reflection and Growth with OpenEvolve
- [x] **Create `prompt_engineering` Directory:**
  - [x] Create a new top-level directory and dependencies.
- [x] **Create Evaluation Suite & Scripts:**
  - [x] Create placeholder scripts and test cases.
- [x] **Update Documentation:**
  - [x] Create a `PROMPT_ENGINEERING.md` file.

## Phase 8: Mixture of Experts (MoE) Architecture
- [x] **Parameterize Nomad Jobs:**
    - [x] Refactor `primacpp.nomad` and `llamacpp-rpc.nomad`.
- [x] **Implement MoE Routing in `TwinService`:**
    - [x] Refactor `TwinService` to act as a router.
- [x] **Update Documentation:**
    - [x] Update `README.md` to explain the MoE architecture.

## Phase 9: Advanced MoE Architecture
- [ ] **Integrate Consul:**
    - [ ] Create a new `consul` Ansible role to install and configure Consul.
    - [ ] Update Nomad jobs to register services with Consul.
- [ ] **Implement Dynamic Service Discovery:**
    - [ ] Refactor `TwinService` to query Consul for expert service locations.
- [ ] **Implement Nomad Namespaces:**
    - [ ] Update the `nomad` Ansible role to enable namespaces.
    - [ ] Update Nomad jobs to use namespaces.
- [ ] **Update Documentation:**
    - [ ] Update `README.md` to document the new Consul and Namespace features.

---

## References
- **[prima.cpp](https://github.com/gitalbenar/prima.cpp):** The distributed LLM inference engine.
- **[pipecat-ai](https://github.com/pipecat-ai/pipecat):** The real-time, streaming conversational AI framework.
- **[physiii/twin](https://github.com/physiii/twin):** The agent embodiment framework that inspired the `TwinService`.
- **[codelion/openevolve](https://github.com/codelion/openevolve):** The AlphaEvolve implementation for prompt engineering.
- **[geerlingguy/beowulf-ai-cluster](https://github.com/geerlingguy/beowulf-ai-cluster):** The Ansible benchmarking project.
- **[HashiCorp Consul](https://www.consul.io/):** The service networking solution.
- **[Nomad Namespaces](https://developer.hashicorp.com/nomad/docs/namespaces):** Documentation for Nomad's multi-tenancy features.
