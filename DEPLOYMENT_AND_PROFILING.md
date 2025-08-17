# Deploying and Profiling AI Services

This guide provides step-by-step instructions for deploying the various AI services on your cluster and for using the built-in benchmarking tools to profile system performance.

## 1. Deploying Core Services

After the Ansible provisioning is complete, your cluster is ready to run the AI services. The following Nomad jobs have been copied to `/home/user/` on your control node.

### Step 1.1: Choose and Deploy ONE Language Model Backend

The heart of the AI pipeline is the Large Language Model (LLM). You have two options for the backend service. You should only run **one** of these at a time.

*   **Option A: `prima.cpp` (Recommended)**
    This is a state-of-the-art inference engine designed for heterogeneous clusters. It can efficiently distribute the workload across multiple nodes.
    ```bash
    nomad job run /home/user/primacpp.nomad
    ```

*   **Option B: `llama.cpp` RPC**
    This is a simpler, more traditional client-server model for the LLM.
    ```bash
    nomad job run /home/user/llamacpp-rpc.nomad
    ```
    **Note:** Before running, you may need to edit the job file to specify the path to the GGUF model you wish to use.

### Step 1.2: Deploy the Main Voice Agent (`pipecat`)

Once your chosen LLM backend is running, deploy the main voice agent application. It will automatically discover and connect to the LLM service using Consul.

```bash
nomad job run /home/user/pipecatapp.nomad
```

### Step 1.3: Verifying Deployment

You can check the status of your newly deployed jobs at any time:
```bash
nomad job status
```
This command will show you if the jobs are running, pending, or have failed. To see detailed logs for a specific job, use:
```bash
nomad job logs <job_name>
# Example:
# nomad job logs pipecatapp
```

---

## 2. Profiling and Benchmarking

This project includes powerful tools to help you measure the performance of your cluster and understand the system load of the AI workloads.

### 2.1: Raw Inference Speed Benchmark (`llama-bench`)

This benchmark measures the pure inference speed of your LLM backend, reported in "tokens per second" (t/s). This is the key metric for raw LLM performance.

**How to Use:**
1.  Ensure you have an LLM backend job (from Step 1.1) running.
2.  The benchmark job file is located at `/home/user/benchmark.nomad`. You can edit this file to customize the test, such as changing the model path (`-m`) or the prompt.
3.  Run the benchmark job:
    ```bash
    nomad job run /home/user/benchmark.nomad
    ```
4.  The job will run, perform the benchmark, and then complete. To see the results, view the logs:
    ```bash
    nomad job logs llama-benchmark
    ```
    The output will contain detailed performance data, including the final tokens/second measurement.

### 2.2: Real-Time Latency Benchmark

This benchmark measures the "end-to-end" conversational latency: the time from when you stop speaking to when the AI starts replying. This is crucial for a natural-feeling interaction.

**How to Use:**
1.  This benchmark is a feature of the main `pipecat` application. To enable it, you must edit the job file.
2.  Open `/home/user/pipecatapp.nomad` for editing.
3.  In the `env` section of the `pipecat-app` task, set the `BENCHMARK_MODE` environment variable to `"true"`.
    ```hcl
    task "pipecat-app" {
      driver = "docker"
      config {
        image = "my-pipecat-image:latest"
      }
      env {
        # ... other environment variables
        BENCHMARK_MODE = "true"
      }
    }
    ```
4.  Deploy (or re-deploy) the application with this change:
    ```bash
    nomad job run /home/user/pipecatapp.nomad
    ```
5.  As you have conversations with the agent, the end-to-end latency for each turn will be printed to the job's logs. You can monitor this in real-time:
    ```bash
    nomad job logs -f pipecatapp
    ```

---

## 3. How to Evaluate System Load

By combining these benchmarks with system monitoring tools, you can get a complete picture of your cluster's performance.

*   **Test Different Models:** Run the `llama-bench` benchmark against various models (e.g., a 3B parameter model vs. a 7B one). This will show you how well your hardware scales to handle more complex models.
*   **Monitor System Resources:** While a benchmark is running, log in to your cluster nodes and use command-line tools like `htop` or `top`. This will give you a real-time view of CPU and memory usage, showing you exactly how much load the AI workload is placing on your machines.
*   **Compare Backends:** Run the same `llama-bench` test against both the `prima.cpp` and `llamacpp-rpc` backends (running them one at a time). This will give you concrete data on which inference engine performs better on your specific hardware setup.

---

## 4. Verifying Cluster Health

After provisioning a new node or restarting the cluster, it's important to verify that all services are running correctly.

### Check Consul Status

This command asks the Consul service for a list of all members in the service mesh.

```bash
consul members
```

You should see a list of all the nodes in your cluster with a status of "alive".

**Example Output:**
```
Node      Address            Status  Type    Build   Protocol  DC   Partition  Segment
AID-E-24  192.168.1.30:8301  alive   server  1.18.1  2         dc1  default    <all>
AID-E-23  192.168.1.188:8301  alive   client  1.18.1  2         dc1  default    <all>
```

### Check Nomad Status

This command asks the Nomad service for the status of the nodes it's managing.

```bash
nomad node status
```

This should show you all the nodes that have successfully joined the Nomad cluster with a status of "ready".

**Example Output:**
```
ID        DC   Name      Class   Drain  Eligibility  Status
1c3af54a  dc1  AID-E-24  <none>  false  eligible     ready
a4f8e6c1  dc1  AID-E-23  <none>  false  eligible     ready
```

If both of these commands show a healthy status for all your nodes, your cluster is up and running correctly.
