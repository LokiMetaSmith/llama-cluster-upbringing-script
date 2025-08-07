# ToDo: Architecting a Responsive, Distributed Conversational AI Pipeline

This document outlines the action plan for refactoring the project to use a modern, distributed architecture based on the technical report.

## Phase 1: Cluster Orchestration with Nomad
- [x] **Create a Nomad Ansible Role:**
  - [x] Create a new Ansible role named `nomad`.
  - [x] This role will download and install the Nomad binary on all nodes in the cluster.
  - [x] It will configure a systemd service for Nomad.
  - [x] It will have separate tasks for server and client configurations.
  - **Verification:**
    - `ansible-playbook playbook.yaml --limit controller_nodes`
    - `ansible-playbook playbook.yaml --limit worker_nodes`
    - SSH into target machine.
    - `nomad --version` should return the installed version.
    - `ls /etc/nomad.d/` should show `nomad.hcl`, `client.hcl` or `server.hcl`.
    - `systemctl status nomad` should show the service as active and running.
- [x] **Update the Main Playbook:**
  - [x] Add the `nomad` role to the main `playbook.yaml`.
  - [x] The `nomad` role will be applied to all hosts, with conditional logic to configure servers and clients based on the `inventory.yaml`.
  - **Verification:**
    - `nomad node status` on a server node should show all client nodes as 'ready'.

## Phase 2: Distributed LLM with prima.cpp
- [ ] **Create a `prima.cpp` Ansible Role:**
  - [ ] Create a new Ansible role named `primacpp`.
  - [ ] This role will install the necessary dependencies for `prima.cpp` (`fio`, `libzmq3-dev`, `HiGHS`).
  - [ ] It will clone the `prima.cpp` repository from GitHub.
  - [ ] It will compile `prima.cpp`, with a conditional flag to compile the master node with `USE_HIGHS=1`.
  - **Verification:**
    - `ansible-playbook playbook.yaml --limit worker_nodes`
    - SSH into target machine.
    - `ls /home/user/prima.cpp/` should show the compiled binaries.
- [ ] **Create a Nomad Job for `prima.cpp`:**
  - [ ] Create a Nomad job file (e.g., `primacpp.nomad`) that defines how to run the `prima.cpp` cluster.
  - [ ] This job will use a `raw_exec` driver to run the `llama-cli` binary.
  - [ ] It will use Nomad's service discovery to pass the IP addresses of the master and next nodes to the `llama-cli` command.
  - [ ] It will also configure the `llama-server` to expose the OpenAI-compatible API.
  - **Verification:**
    - `nomad job run primacpp.nomad`
    - `nomad job status primacpp` should show the job as 'running'.
    - The OpenAI-compatible API should be accessible at the specified port.

## Phase 3: Conversational AI Pipeline with pipecat
- [ ] **Create a `pipecat_app` Ansible Role:**
  - [ ] Create a new Ansible role named `pipecatapp`.
  - [ ] This role will install the necessary python dependencies for the `pipecat` application, including `pipecat-ai`, `RealtimeSTT`, `faster-whisper`, `MeloTTS`, etc. This will be managed via a `requirements.txt` file.
- [ ] **Develop the `pipecat` Application:**
  - [ ] Create a Python application (`app.py`) that uses the `pipecat` framework.
  - [ ] This application will define the conversational pipeline:
    - [ ] `RealtimeSTT` for speech-to-text.
    - [ ] `OpenAILLMService` configured to point to the `prima.cpp` Nomad service.
    - [ ] `MeloTTS` for text-to-speech.
  - [ ] It will implement the interruptible logic as described in the report.
- [ ] **Create a Nomad Job for the `pipecat` Application:**
  - [ ] Create a Nomad job file (e.g., `pipecatapp.nomad`) to run the `pipecat` application.
  - [ ] This job will use the `exec` driver to run the python application.

## Phase 4: Integration, Testing, and Documentation
- [ ] **Update `README.md`:**
  - [ ] Update the `README.md` to document the new, Nomad-based deployment process.
  - [ ] Explain how to configure the `inventory.yaml` for the Nomad cluster.
  - [ ] Explain how to run the Ansible playbook to provision the cluster.
  - [ ] Explain how to deploy the `prima.cpp` and `pipecat` Nomad jobs.
- [ ] **Testing:**
  - [ ] Thoroughly test the end-to-end pipeline on the cluster.
  - [ ] Benchmark the performance (tokens/sec, time-to-first-token).
  - [ ] Tune the parameters as described in the report.
