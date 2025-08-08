# Distributed Conversational AI Pipeline for Legacy CPU Clusters

This project provides a complete solution for deploying a high-performance, low-latency conversational AI pipeline on a cluster of legacy, resource-constrained desktop computers. It uses Ansible for automated provisioning, Nomad for cluster orchestration, and a state-of-the-art AI stack to create a responsive, streaming, and embodied voice agent.

## 1. System Requirements
- **Cluster Nodes:** 3 to 20 legacy desktop computers (Intel Core 2 Duo or similar, 8GB RAM, SSD recommended).
- **Control Node:** A machine to run Ansible for provisioning.
- **Recommended OS:** Debian 12 (Bookworm), minimal install with SSH server.

## 2. Initial Machine Setup
This must be done for **every node** in the cluster.
1.  **Install Debian 12.**
2.  **Clone this repository** and enter the `initial-setup` directory.
3.  **Configure `setup.conf`** with the machine's desired `HOSTNAME` and static IP address details.
4.  **Run the script:** `sudo bash setup.sh`
5.  **Reboot.**

## 3. Control Node & Ansible Provisioning
1.  **On your control node, install Ansible and Git:** `sudo apt install ansible git -y`
2.  **Clone this repository.**
3.  **Configure SSH:** Generate an SSH key (`ssh-keygen`) and distribute it to all cluster nodes (`ssh-copy-id user@<node_ip>`).
4.  **Configure Ansible Inventory:** Edit `inventory.yaml` to list your nodes.
    - The `controller_nodes` group must contain **exactly 3 nodes** to act as Nomad servers.
    - All nodes (including controllers) must be in the `worker_nodes` group.
5.  **Provision the Cluster:** Run `ansible-playbook playbook.yaml`. This will install and configure all required software on all nodes.

## 4. Deploying the AI Services with Nomad
After provisioning, deploy the services from your control node.

### 4.1. Choose and Deploy an LLM Backend (Run ONE only)
- **Option A: `prima.cpp` (Recommended):** State-of-the-art for heterogeneous clusters.
  ```bash
  nomad job run /home/user/primacpp.nomad
  ```
- **Option B: `llama.cpp` RPC:** Simpler, traditional client-server model.
  ```bash
  nomad job run /home/user/llamacpp-rpc.nomad
  ```

### 4.2. Deploy the Voice Agent
This deploys the main `pipecat` application, which will automatically connect to your chosen LLM backend.
```bash
nomad job run /home/user/pipecatapp.nomad
```

## 5. Agent Architecture: The `TwinService`
The core of this application is the `TwinService`, a custom service that acts as the agent's "brain." It orchestrates the agent's responses, memory, and tool use.

### 5.1. Memory
- **Short-Term:** Remembers the last 10 conversational turns.
- **Long-Term:** Uses a FAISS vector store (`long_term_memory.faiss`) to remember key facts. It performs a semantic search over this memory to retrieve relevant context for new conversations.

### 5.2. Tool Use
The agent can use tools to perform actions and gather information. The `TwinService` dynamically provides the list of available tools to the LLM in its prompt, enabling the LLM to decide which tool to use based on the user's query.

#### Available Tools:
- **Vision (`vision.get_observation`)**
  - **Description:** Gets a real-time description of what is visible in the webcam.
  - **Requires:** A USB webcam connected to the node running the `pipecat-app` job.
  - **Example:** "What do you see?"
- **Master Control Program (`mcp.get_status`, `mcp.get_memory_summary`, etc.)**
  - **Description:** A tool for introspection and self-control.
  - **Examples:** "MCP, what is your status?", "Summarize your memory."
- **SSH (`ssh.run_command`)**
  - **Description:** Executes a command on a remote machine via SSH.
  - **Security Warning:** This is a very powerful tool. The credentials are not stored in the code but must be provided by the LLM. For this to work, the user running the agent must have an SSH key configured that allows passwordless access to the target machine. Exercise caution when enabling the LLM to use this tool.
  - **Example:** "Use ssh to run 'ls -l' on host 192.168.1.102 with user 'admin'."

## 6. Testing and Verification
- **Check Cluster Status:** `nomad node status`
- **Check Job Status:** `nomad job status`
- **View Logs:** `nomad job logs <job_name>` (e.g., `pipecat-app`, `prima-cluster`)

## 7. Benchmarking
This project includes two types of benchmarks.

### 7.1. Real-Time Latency Benchmark
Measures the end-to-end latency of a live conversation. Enable it by setting `BENCHMARK_MODE = "true"` in the `env` section of the `pipecatapp.nomad` job file. Results are printed to the job logs.

### 7.2. Standardized Performance Benchmark
Uses `llama-bench` to measure the raw inference speed (tokens/sec) of the deployed LLM backend.
1. Ensure an LLM backend is running.
2. Edit `/home/user/benchmark.nomad` to point to the GGUF model you want to test.
3. Run the job: `nomad job run /home/user/benchmark.nomad`
4. View results in the job logs: `nomad job logs llama-benchmark`

## 8. Advanced Development: Prompt Evolution
For advanced users, this project includes a workflow for automatically improving the agent's core prompt using evolutionary algorithms. See `prompt_engineering/PROMPT_ENGINEERING.md` for details.
