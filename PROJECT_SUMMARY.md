# ToDo: Architecting a Responsive, Distributed Conversational AI Pipeline

This document outlines the action plan for refactoring the project to use a modern, distributed architecture based on the technical report. All phases are now complete.

## Phase 1: Cluster Orchestration with Nomad
- [x] **Create a Nomad Ansible Role:**
- [x] **Update the Main Playbook:**

## Phase 2: Distributed LLM with prima.cpp
- [x] **Create a `prima.cpp` Ansible Role:**
- [x] **Create a Nomad Job for `prima.cpp`:**

## Phase 3: Conversational AI Pipeline with pipecat
- [x] **Create a `pipecat_app` Ansible Role:**
- [x] **Develop the `pipecat` Application:**
- [x] **Create a Nomad Job for the `pipecat` Application:**

## Phase 4: Integration, Testing, and Documentation
- [x] **Update `README.md`:**
- [x] **Testing:**

## Phase 5: Vision Integration
- [x] **Create a `vision` Ansible Role:**
- [x] **Develop the Vision Service:**
- [x] **Update Documentation for Vision Capabilities:**

## Phase 6: Agent Embodiment with TwinService
- [x] **Create `TwinService`:**
- [x] **Implement Memory:**
- [x] **Implement Tool Use:**
- [x] **Integrate into Pipeline:**
- [x] **Update Documentation:**

## Phase 7: Self-Reflection and Growth with OpenEvolve
- [x] **Create `prompt_engineering` Directory:**
- [x] **Create Evaluation Suite & Scripts:**
- [x] **Update Documentation:**

## Phase 8: Mixture of Experts (MoE) Architecture
- [x] **Parameterize Nomad Jobs:**
- [x] **Implement MoE Routing in `TwinService`:**
- [x] **Update Documentation:**

## Phase 9: Advanced MoE Architecture
- [x] **Integrate Consul:**
- [x] **Implement Dynamic Service Discovery:**
- [x] **Implement Nomad Namespaces:**
- [x] **Update Documentation:**

## Phase 10: Zero-Touch Provisioning with PXE
- [x] **Create `pxe_server` Ansible Role:**
- [x] **Create Preseed and DHCP Configuration:**
- [x] **Update Documentation:**

---

## References
- **[prima.cpp](https://github.com/gitalbenar/prima.cpp):** The distributed LLM inference engine.
- **[pipecat-ai](https://github.com/pipecat-ai/pipecat):** The real-time, streaming conversational AI framework.
- **[physiii/twin](https://github.com/physiii/twin):** The agent embodiment framework that inspired the `TwinService`.
- **[codelion/openevolve](https://github.com/codelion/openevolve):** The AlphaEvolve implementation for prompt engineering.
- **[geerlingguy/beowulf-ai-cluster](https://github.com/geerlingguy/beowulf-ai-cluster):** The Ansible benchmarking project.
- **[HashiCorp Consul](https://www.consul.io/):** The service networking solution.
- **[Nomad Namespaces](https://developer.hashicorp.com/nomad/docs/namespaces):** Documentation for Nomad's multi-tenancy features.
- **[Debian Preseed](https://wiki.debian.org/DebianInstaller/Preseed):** Documentation for automating the Debian installer.
