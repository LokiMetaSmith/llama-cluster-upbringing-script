# Project Summary: Architecting a Responsive, Distributed Conversational AI Pipeline

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
- **Phase 7: Self-Reflection and Growth:**
    - Created an offline workflow using `openevolve` to automatically improve the agent's core prompt.
- **Phase 8-9: Advanced MoE Architecture:**
    - Implemented a Mixture of Experts architecture with dynamic routing using Consul and isolation with Nomad Namespaces.
- **Phase 10: Zero-Touch Provisioning:**
    - Created a `pxe_server` Ansible role to fully automate the installation of Debian on new, bare-metal machines.
- **Phase 11: Code Execution:**
    - Implemented a `CodeRunnerTool` that allows the agent to write and execute Python code in a secure, sandboxed Docker container.
- **Phase 12: Web Browsing:**
    - Implemented a `WebBrowserTool` using Playwright that allows the agent to browse the web to answer questions.

---

## References
- **[prima.cpp](https://github.com/gitalbenar/prima.cpp):** The distributed LLM inference engine.
- **[pipecat-ai](https://github.com/pipecat-ai/pipecat):** The real-time, streaming conversational AI framework.
- **[physiii/twin](https://github.com/physiii/twin):** The agent embodiment framework that inspired the `TwinService`.
- **[codelion/openevolve](https://github.com/codelion/openevolve):** The AlphaEvolve implementation for prompt engineering.
- **[geerlingguy/beowulf-ai-cluster](https://github.com/geerlingguy/beowulf-ai-cluster):** The Ansible benchmarking project.
- **[instavm/coderunner-ui](https://github.com/instavm/coderunner-ui):** The code execution UI that inspired the `CodeRunnerTool`.
- **[HashiCorp Consul](https://www.consul.io/):** The service networking solution.
- **[Nomad Namespaces](https://developer.hashicorp.com/nomad/docs/namespaces):** Documentation for Nomad's multi-tenancy features.
- **[Debian Preseed](https://wiki.debian.org/DebianInstaller/Preseed):** Documentation for automating the Debian installer.
