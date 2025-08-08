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
- [x] **Create a `prima.cpp` Ansible Role:**
  - [x] Create a new Ansible role named `primacpp`.
  - [x] This role will install the necessary dependencies for `prima.cpp` (`fio`, `libzmq3-dev`, `HiGHS`).
  - [x] It will clone the `prima.cpp` repository from GitHub.
  - [x] It will compile `prima.cpp`, with a conditional flag to compile the master node with `USE_HIGHS=1`.
  - **Verification:**
    - `ansible-playbook playbook.yaml --limit worker_nodes`
    - SSH into target machine.
    - `ls /home/user/prima.cpp/` should show the compiled binaries.
- [x] **Create a Nomad Job for `prima.cpp`:**
  - [x] Create a Nomad job file (e.g., `primacpp.nomad`) that defines how to run the `prima.cpp` cluster.
  - [x] This job will use a `raw_exec` driver to run the `llama-cli` binary.
  - [x] It will use Nomad's service discovery to pass the IP addresses of the master and next nodes to the `llama-cli` command.
  - [x] It will also configure the `llama-server` to expose the OpenAI-compatible API.
  - **Verification:**
    - `nomad job run primacpp.nomad`
    - `nomad job status primacpp` should show the job as 'running'.
    - The OpenAI-compatible API should be accessible at the specified port.

## Phase 3: Conversational AI Pipeline with pipecat
- [x] **Create a `pipecat_app` Ansible Role:**
  - [x] Create a new Ansible role named `pipecatapp`.
  - [x] This role will install the necessary python dependencies for the `pipecat` application, including `pipecat-ai`, `RealtimeSTT`, `faster-whisper`, `MeloTTS`, etc. This will be managed via a `requirements.txt` file.
  - **Verification:**
    - `ansible-playbook playbook.yaml --limit worker_nodes`
    - SSH into target machine.
    - `pip3 list` should show the installed packages.
- [x] **Develop the `pipecat` Application:**
  - [x] Create a Python application (`app.py`) that uses the `pipecat` framework.
  - [x] This application will define the conversational pipeline:
    - [x] `RealtimeSTT` for speech-to-text.
    - [x] `OpenAILLMService` configured to point to the `prima.cpp` Nomad service.
    - [x] `MeloTTS` for text-to-speech.
  - [x] It will implement the interruptible logic as described in the report.
  - **Verification:**
    - `python3 /home/user/app.py` should run without errors.
- [x] **Create a Nomad Job for the `pipecat` Application:**
  - [x] Create a Nomad job file (e.g., `pipecatapp.nomad`) to run the `pipecat` application.
  - [x] This job will use the `exec` driver to run the python application.
  - **Verification:**
    - `nomad job run pipecatapp.nomad`
    - `nomad job status pipecatapp` should show the job as 'running'.

## Phase 4: Integration, Testing, and Documentation
- [x] **Update `README.md`:**
  - [x] Update the `README.md` to document the new, Nomad-based deployment process.
  - [x] Explain how to configure the `inventory.yaml` for the Nomad cluster.
  - [x] Explain how to run the Ansible playbook to provision the cluster.
  - [x] Explain how to deploy the `prima.cpp` and `pipecat` Nomad jobs.
- [x] **Testing:**
  - [x] Thoroughly test the end-to-end pipeline on the cluster.
  - [x] Benchmark the performance (tokens/sec, time-to-first-token).
  - [x] Tune the parameters as described in the report.

## Phase 5: Vision Integration
- [x] **Create a `vision` Ansible Role:**
  - [x] Create a new Ansible role named `vision`.
  - [x] This role will install the necessary system dependencies for video processing.
  - [x] It will update the `requirements.txt` to include `ultralytics` and `opencv-python-headless`.
  - **Verification:**
    - `ansible-playbook playbook.yaml --limit worker_nodes`
    - SSH into target machine.
    - `pip3 list | grep ultralytics` should show the package.
- [x] **Develop the Vision Service:**
  - [x] Create a custom `pipecat` service (`YOLOv8Detector`) in `app.py`.
  - [x] This service will capture video, run YOLOv8, and inject text observations into the pipeline.
  - [x] Integrate the service into the main pipeline to run in parallel.
  - **Verification:**
    - Run the `pipecat` application.
    - The logs should show "Observation: I see..." messages when objects are detected by the webcam.
- [x] **Update Documentation for Vision Capabilities:**
  - [x] Add a section to `README.md` explaining the new vision feature.
  - [x] Document any new configuration options or dependencies.
  - **Verification:**
    - The `README.md` contains a new section on Vision Capabilities.

## Phase 6: Agent Embodiment with TwinService
- [x] **Create `TwinService`:**
  - [x] Create a new `FrameProcessor` class in `app.py` called `TwinService`.
  - [x] This service will act as the "brain" of the agent, sitting between the STT and LLM services.
- [x] **Implement Memory:**
  - [x] Create a simple file-based vector store for long-term memory.
  - [x] The `TwinService` will perform a semantic search on this memory to retrieve context for the LLM prompt.
  - [x] The `TwinService` will update the memory with a summary of each interaction.
- [x] **Implement Tool Use:**
  - [x] The `TwinService` will parse the user's request to see if it's a command for a tool.
  - [x] It will integrate the existing `YOLOv8Detector` as a tool that can be queried for a description of the current scene.
- [x] **Integrate into Pipeline:**
  - [x] Modify the main `pipecat` pipeline to be `STT -> TwinService -> TTS`.
- [ ] **Update Documentation:**
  - [ ] Update the `README.md` to explain the new agentic capabilities.
