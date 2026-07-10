# Project Summary: Architecting a Responsive, Distributed Conversational AI Pipeline

Last updated: 2026-06-08

This document summarizes the final architecture and key features of the project.

## Final Architecture

The project has evolved from a single setup script into a sophisticated, multi-layered system for deploying a stateful, embodied AI agent on a cluster of legacy computers.

- **Provisioning Layer:** [Ansible](https://www.ansible.com/) is used for the complete, automated setup of all nodes.
- **Orchestration Layer:** [HashiCorp Nomad](https://www.nomadproject.io/) is used to schedule and manage all application services.
- **Service Discovery Layer:** [HashiCorp Consul](https://www.consul.io/) is integrated with Nomad to provide dynamic service discovery.
- **Application Layer:** The core of the agent is a Python application built on the [pipecat](https://github.com/pipecat-ai/pipecat) real-time streaming framework.

## Key Implemented Features

- **Phase 1-4: Foundational Setup:** Deployed a robust, multi-service architecture using Ansible and Nomad.
- **Phase 5: Vision Integration:** Added a `YOLOv8Detector` service, giving the agent the ability to "see".
- **Phase 6: Agent Embodiment:**
  - Created the `TwinService`, the agent's "brain."
  - Implemented both short-term and long-term memory.
  - Implemented a tool-use framework with `vision`, `ssh`, and `mcp` tools.
- **Phase 7: Self-Healing and Adaptation (SEAL-Inspired):**
  - Implemented a closed-loop, autonomous system (`supervisor.py`) that monitors for job failures.
  - Upon failure, a `reflection` agent (`reflect.py`) performs root cause analysis.
  - Simple issues are healed directly by an Ansible playbook (`heal_job.yaml`).
  - For novel failures, an `adaptation_manager.py` script automatically generates a new test case and uses an evolutionary algorithm (`openevolve`) to adapt the reflection agent's logic, enabling it to handle the failure in the future.
- **Phase 8-9: Advanced MoE Architecture:**
  - Implemented a Mixture of Experts architecture with dynamic routing using Consul and isolation with Nomad Namespaces.
- **Phase 10: Zero-Touch Provisioning:**
  - Created a `pxe_server` Ansible role to fully automate the installation of Debian on new, bare-metal machines.
- **Phase 11: Code Execution:**
  - Implemented a `CodeRunnerTool` that allows the agent to write and execute Python code in a secure, sandboxed Docker container.
- **Phase 12: Web Browsing:**
  - Implemented a `WebBrowserTool` using Playwright that allows the agent to browse the web to answer questions.
- **Phase 13: IPFS & Package Caching:**
  - Implemented an internal package cache system for the swarm using IPFS. This includes an apt package caching proxy and PyPI proxy to optimize distributed service deployments across the cluster.
- **Phase 14: DwarfStar (ds4) Inference Engine:**
  - Integrated the DwarfStar (ds4) native inference engine for DeepSeek V4 models (Flash/PRO), deployed via a dedicated Ansible role and Nomad templates for accelerated distributed CPU/GPU inference.
- **Phase 15: Btrfs Snapshots & OS Recovery:**
  - Standardized on Btrfs filesystem snapshots for pre-deployment OS recovery, managed via the `btrfs_snapshot` Ansible role and the `recover_os.py` recovery tool, protecting critical cluster directories via automatic rsync synchronizations.
- **Phase 16: Ternlight Ternary Embedding Search:**
  - Integrated the ultra-lightweight 7MB ternary embedding model service, accessible via `TernlightTool`, deployed as a Node.js microservice via Nomad, featuring browser-side search in the 'Instant Docs' tab of the Mission Control UI.
- **Phase 17: Ouroboros Webring & Circular Navigation:**
  - Enabled circular navigation between cluster services and friend agents via the Ouroboros webring, persisting member data in Consul KV and running a background discovery task to update the webring periodically.
- **Phase 18: Model Training as Code (MTaC):**
  - Integrated Aleph Alpha's "Model Training as Code" framework, allowing agents to programmatically generate and launch containerized ML training pipelines (Unsloth, Torchtune) as Nomad jobs with telemetry streaming and loss tracking.
- **Phase 19: SkillLibrary & SetOperationalModeTool:**
  - Implemented the `SkillLibrary` database for persistent behavioral skill retention (e.g., 'backpass') along with the `SetOperationalModeTool` to allow agents to dynamically activate procedural guidelines into their system prompts.

---

## References

- **[pipecat-ai](https://github.com/pipecat-ai/pipecat):** The real-time, streaming conversational AI framework.
- **[physiii/twin](https://github.com/physiii/twin):** The agent embodiment framework that inspired the `TwinService`.
- **[codelion/openevolve](https://github.com/codelion/openevolve):** The AlphaEvolve implementation for prompt engineering.
- **[geerlingguy/beowulf-ai-cluster](https://github.com/geerlingguy/beowulf-ai-cluster):** The Ansible benchmarking project.
- **[instavm/coderunner-ui](https://github.com/instavm/coderunner-ui):** The code execution UI that inspired the `CodeRunnerTool`.
- **[HashiCorp Consul](https://www.consul.io/):** The service networking solution.
- **[Nomad Namespaces](https://developer.hashicorp.com/nomad/docs/namespaces):** Documentation for Nomad's multi-tenancy features.
- **[Debian Preseed](https://wiki.debian.org/DebianInstaller/Preseed):** Documentation for automating the Debian installer.
