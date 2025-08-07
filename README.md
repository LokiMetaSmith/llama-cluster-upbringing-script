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

Once the Ansible playbook has completed successfully, your cluster is ready. The final step is to deploy the AI services using Nomad.

From your control node (or any node in the cluster where you have access to the `nomad` CLI):

### 5.1. Deploy the `prima.cpp` LLM Cluster
```bash
nomad job run /home/user/primacpp.nomad
```

### 5.2. Deploy the `pipecat` Voice Agent
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
- **Model Selection:** The `prima.cpp` Nomad job is configured to use a placeholder model path. You will need to edit `/home/user/primacpp.nomad` on the master node to point to the GGUF model you want to use. Smaller models (3B, 7B) are recommended.
- **Network:** Wired gigabit ethernet is strongly recommended over Wi-Fi for reduced latency.
- **VAD Tuning:** The `RealtimeSTT` sensitivity can be tuned in `app.py` for better performance in noisy environments.
