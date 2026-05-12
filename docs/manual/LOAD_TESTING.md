# Cluster Load Testing and Network Validation

As the cluster scales to a multi-node Swarm architecture (combining core controllers and edge worker nodes), ensuring that requests are properly load-balanced and network overlays are functioning correctly becomes critical.

This repository includes a suite of tools to test Traditional Container Load Balancing (managed by Nomad and routed by Traefik) and internal Service Mesh connectivity (managed by Consul).

## 1. Network Validation Playbook

Before attempting to deploy distributed workloads, you must verify that the underlying Tailscale mesh, Consul DNS, and Nomad APIs are communicating properly across all nodes.

We use a dedicated Ansible playbook to perform these checks.

### Running the Checks

Run the following command from your controller node:

```bash
ansible-playbook -i inventory.yaml tests/playbooks/verify_cluster_network.yaml --ask-become-pass
```

### What It Tests

1.  **Tailscale Mesh Pings**: It finds the `tailscale0` IP of every node in the cluster and ensures every node can ping every other node over the VPN overlay.
2.  **Consul DNS Resolution**: It queries the local Consul DNS resolver (port 8600) on each node to ensure it can successfully look up standard Consul `.service.consul` domains.
3.  **Nomad API (mTLS)**: It performs an authenticated `GET` request to the Nomad Controller API from every worker node using the local client certificates (`cli.cert.pem`), verifying that mTLS is functioning and certificates are valid.
4.  **Traefik Health**: It queries the Consul health endpoint to ensure Traefik is running and registered as a passing service.

---

## 2. Testing Traefik L7 Load Balancing

To verify that HTTP traffic is being evenly distributed across multiple worker nodes, you can deploy a dummy service and run the included asynchronous stress test script.

### Step 2.1: Deploy the Dummy Service

We have provided a lightweight Python web server job that simply echoes its Nomad Node ID and Allocation ID.

1.  Deploy the job to the cluster:
    ```bash
    nomad job run ansible/jobs/dummy_web_service.nomad
    ```
2.  Wait a few seconds, then verify it is running (it is configured to launch 3 instances by default):
    ```bash
    nomad job status dummy-web-service
    ```

### Step 2.2: Run the Stress Test

The stress testing script will blast concurrent HTTP requests to the Traefik load balancer and aggregate the responses to prove that traffic is hitting different nodes.

Run the script from your development machine or the controller node:

> **Note:** The script requires the `aiohttp` library. You can install it using `pip install aiohttp`.

```bash
python3 tests/scripts/stress_test_cluster.py --url "http://<controller_ip>" --host "dummy.local.mesh" --requests 1000 --concurrency 50
```

*   **`--url`**: The IP address of the node running Traefik (usually your primary controller).
*   **`--host`**: The Traefik Host routing rule defined in the dummy job (`dummy.local.mesh`).
*   **`--requests`**: Total number of requests to execute.
*   **`--concurrency`**: Number of simultaneous workers.

### Step 2.3: Analyze the Results

The script will output a table showing the request rate and how the traffic was distributed. A successful test will show an roughly even split of traffic across multiple `Node` IDs and `Alloc` IDs:

```text
========================================
STRESS TEST RESULTS
========================================
Total Requests:      1000
Concurrency:         50
Duration:            1.45 seconds
Requests/sec:        689.65
Successful Requests: 1000
Failed Requests:     0

Load Distribution by Node:
-------------------------
node-worker-1          345 ( 34.5%)
node-worker-2          330 ( 33.0%)
node-controller-1      325 ( 32.5%)

Load Distribution by Allocation (Container):
----------------------------------------
alloc-id-1234...                       345 ( 34.5%)
alloc-id-5678...                       330 ( 33.0%)
alloc-id-9012...                       325 ( 32.5%)
```

If 100% of the traffic hits a single node, or if there is a high failure rate, it indicates a misconfiguration in Traefik routing or Consul service registration.
