# Distributed Conversational AI Pipeline for Legacy CPU Clusters

This project provides a complete solution for deploying a high-performance, low-latency conversational AI pipeline on a cluster of legacy, resource-constrained desktop computers. It uses Ansible for automated provisioning, Nomad for cluster orchestration, and a state-of-the-art AI stack including `prima.cpp` and `pipecat` to create a responsive, streaming, and interruptible voice agent.

## 1. System Requirements

### 1.1. Hardware
- **Cluster Nodes:** 3 to 20 legacy desktop computers.
- **CPU:** Intel Core 2 Duo or similar era (no AVX support required).
- **RAM:** 8GB per node.
- **Storage:** SSD is highly recommended for faster model loading.
- **Control Node:** A separate machine (can be one of the cluster nodes) to run Ansible.

### 1.2. Recommended Linux Distribution
It is highly recommended to use **Debian 12 (Bookworm)** for all cluster nodes. A minimal "net-install" is preferred to avoid unnecessary background services.

## 2. Initial Machine Setup

This section describes how to prepare a new machine to be added to the cluster. This process must be followed for **every node** in the cluster.

### 2.1. Install Debian 12
- Perform a minimal installation of Debian 12.
- During the installation, create a standard user (e.g., `user`).
- When prompted for software selection, deselect "Debian desktop environment" and select only "SSH server" and "standard system utilities".

### 2.2. Run the Initial Setup Script
After installing Debian, log in as the user you created. Then, clone this repository and run the initial setup script. This script will configure the hostname, set up a static IP address, and ensure the SSH server is running.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KittenML/KittenTTS.git
    cd KittenTTS/initial-setup
    ```
2.  **Configure the setup:**
    Edit the `setup.conf` file and set the `HOSTNAME`, `STATIC_IP`, `NETMASK`, `GATEWAY`, and `INTERFACE` variables for the specific machine.
3.  **Run the script:**
    ```bash
    sudo bash setup.sh
    ```
4.  **Reboot:**
    After the script finishes, reboot the machine: `sudo reboot`

## 3. Control Node and Ansible Setup

This section describes how to set up your control node, which will be used to provision the entire cluster.

### 3.1. Install Ansible and Git
On your control node, install Ansible and Git:
```bash
sudo apt update
sudo apt install ansible git -y
```

### 3.2. Clone this Repository
```bash
git clone https://github.com/KittenML/KittenTTS.git
cd KittenTTS
```

### 3.3. Configure SSH Key-Based Authentication
Ansible uses SSH to communicate with the cluster nodes. Passwordless SSH is required.

1.  **Generate an SSH key on the control node:**
    ```bash
    ssh-keygen -t rsa -b 4096
    ```
    Press Enter to accept the default file location and leave the passphrase empty.

2.  **Distribute the public key to each cluster node:**
    For each node in your cluster, run the following command, replacing `user` and `ip_address_of_node` accordingly:
    ```bash
    ssh-copy-id user@ip_address_of_node
    ```
    You will be prompted for the user's password on the remote machine for the last time.

### 3.4. Configure the Ansible Inventory
The `inventory.yaml` file tells Ansible which machines are in your cluster.

1.  **Edit `inventory.yaml`:**
    ```yaml
    all:
      children:
        controller_nodes:
          hosts:
            aide-01:
              ansible_host: 192.168.1.101
            aide-02:
              ansible_host: 192.168.1.102
            aide-03:
              ansible_host: 192.168.1.103
        worker_nodes:
          hosts:
            aide-01:
              ansible_host: 192.168.1.101
            aide-02:
              ansible_host: 192.168.1.102
            aide-03:
              ansible_host: 192.168.1.103
            # Add more worker nodes here
      vars:
        ansible_user: user
    ```
2.  **Important Notes:**
    - The `controller_nodes` group should contain **exactly 3 nodes**. These will be the Nomad servers.
    - All nodes, including the controllers, should be in the `worker_nodes` group.

## 4. Provision the Cluster
Now that your control node is set up and the inventory is configured, you can provision the entire cluster with a single command:

```bash
ansible-playbook playbook.yaml
```
This will run all the necessary Ansible roles to install and configure Nomad, `prima.cpp`, and the `pipecat` application environment on all nodes.

## 5. Deploy the AI Services

Once the Ansible playbook has completed successfully, your cluster is ready. You can now deploy the AI services using Nomad. This project supports two different distributed LLM backends. You should only run **one** of them at a time.

From your control node (or any node in the cluster where you have access to the `nomad` CLI):

### 5.1. Option 1: Deploy with `prima.cpp` (Recommended)
`prima.cpp` is a state-of-the-art implementation designed specifically for heterogeneous, low-resource clusters. It uses advanced techniques like piped-ring parallelism and disk offloading to maximize performance. This is the recommended backend for most use cases.

```bash
nomad job run /home/user/primacpp.nomad
```

### 5.2. Option 2: Deploy with `llama.cpp` RPC
This uses the native RPC functionality built into `llama.cpp`. It's a simpler, more traditional client-server model.

```bash
nomad job run /home/user/llamacpp-rpc.nomad
```

### 5.3. Deploy the `pipecat` Voice Agent
After choosing and deploying one of the LLM backends above, you can deploy the main voice agent application. It will automatically connect to whichever backend is running.

```bash
nomad job run /home/user/pipecatapp.nomad
```

## 6. Testing and Verification

### 6.1. Check Nomad Cluster Status
On one of the controller nodes, run:
```bash
nomad node status
```
All nodes should be listed with a status of `ready`.

### 6.2. Check Job Status
```bash
nomad job status
```
Both the `prima-cluster` and `pipecat-app` jobs should have a status of `running`.

### 6.3. Check Logs
To see the logs for a specific job:
```bash
nomad job logs <job_name>
```

## 7. Performance Tuning
- **Model Selection:** The `prima.cpp` Nomad job is configured to use a placeholder model path. You will need to edit `/home/user/primacpp.noma`d on the master node to point to the GGUF model you want to use. Smaller models (3B, 7B) are recommended.
- **Network:** Wired gigabit ethernet is strongly recommended over Wi-Fi for reduced latency.
- **VAD Tuning:** The `RealtimeSTT` sensitivity can be tuned in `app.py` for better performance in noisy environments.

## 8. Agent Architecture: The TwinService

The core of this application is the `TwinService`, a custom `pipecat` service that acts as the agent's "brain". It sits between the Speech-to-Text (STT) and Text-to-Speech (TTS) services and orchestrates the agent's response. This is where the agent's memory and tool-use capabilities are implemented.

### 8.1. Memory
The agent has both short-term and long-term memory.
- **Short-Term Memory:** The agent remembers the last 10 conversational turns.
- **Long-Term Memory:** The agent uses a FAISS vector store to remember key information from past conversations. When you speak, the agent searches its memory for relevant context to better understand your request.

### 8.2. Tool Use
The agent can use tools to interact with its environment. Currently, the only tool is the vision system.
- The `TwinService` instructs the LLM that it can use a tool called `describe_scene`.
- If you ask "what do you see?", the LLM will decide to use this tool.
- The `TwinService` then gets the latest observation from the `YOLOv8Detector` and feeds it back to the LLM to generate a response.

## 9. Vision Capabilities

The agent's vision is provided by the `YOLOv8Detector` service, which runs in parallel to the main conversation.

### 8.1. How it Works
- The `pipecat` application includes a `YOLOv8Detector` service.
- This service uses `OpenCV` to capture frames from a webcam.
- It runs a YOLOv8 object detection model on each frame.
- When the set of detected objects changes, it generates a text-based observation (e.g., "Observation: I see a person and a cup.") and sends it to the LLM.
- This allows the agent to have a continuous, real-time awareness of its surroundings.

### 8.2. Hardware Requirements
- A USB webcam must be connected to the node where the `pipecat-app` job is running. By default, this will be one of the nodes in the cluster, managed by Nomad.

### 8.3. Verification
To see the vision system in action, you can view the logs of the `pipecat-app` job:
```bash
nomad job logs pipecat-app
```
When objects are detected by the webcam, you will see log messages from the `YOLOv8Detector` service, including the "Observation: ..." text that is being sent to the LLM.

## 9. Benchmarking

This project includes two types of benchmarks to measure performance.

### 9.1. Real-Time Latency Benchmark
This benchmark measures the end-to-end latency of a live conversation. It is useful for understanding the perceived responsiveness of the agent.

To enable this benchmark, you need to set the `BENCHMARK_MODE` environment variable when running the `pipecat-app` job. You can do this by modifying the `pipecatapp.nomad` job file.

1.  **Edit `/home/user/pipecatapp.nomad`** on the master node.
2.  **Add the `env` stanza** to the `task` block:
    ```hcl
    task "pipecat-task" {
      driver = "exec"

      config {
        command = "python3"
        args    = ["/home/user/app.py"]
      }

      env {
        BENCHMARK_MODE = "true"
      }
    }
    ```
3.  **Run the job:** `nomad job run /home/user/pipecatapp.nomad`

### 9.2. Interpreting the Results
When benchmarking is enabled, a performance report will be printed to the job logs after each conversational turn. You can view the logs with `nomad job logs pipecat-app`.

The report will look like this:
```
--- BENCHMARK RESULTS ---
STT Latency: 0.5123s
LLM Time to First Token: 0.2345s
TTS Time to First Audio: 0.4567s
Total Pipeline Latency: 1.2035s
-------------------------
```
- **STT Latency:** Time from the user stopping speaking to the final transcript being generated.
- **LLM Time to First Token (TTFT):** Time from the end of the STT to the first word from the LLM.
- **TTS Time to First Audio (TTFA):** Time from the first word of the LLM to the first chunk of synthesized audio.
- **Total Pipeline Latency:** The full end-to-end time from the user stopping speaking to the agent starting to speak. This is the most important metric for perceived responsiveness.

### 9.3. Standardized Performance Benchmark
This benchmark uses the `llama-bench` tool to measure the raw inference speed of the deployed LLM backend in tokens per second. This is useful for comparing the performance of different models or backends (`prima.cpp` vs. `llama.cpp` RPC) under a consistent load.

1.  **Ensure an LLM backend is running** (see Section 5).
2.  **Edit `/home/user/benchmark.nomad`** on the master node to point to the GGUF model you want to test.
3.  **Run the benchmark job:**
    ```bash
    nomad job run /home/user/benchmark.nomad
    ```
4.  **View the results:**
    The benchmark results will be printed to the job's logs.
    ```bash
    nomad job logs llama-benchmark
    ```
    Look for the "tokens per second" metrics in the `llama-bench` output.
