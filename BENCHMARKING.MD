# A Guide to Benchmarking Your AI Cluster

Benchmarking is the process of testing the performance of your hardware and software to establish a baseline, identify bottlenecks, and measure the impact of changes. This guide covers several key areas:

---

## 1. CPU Performance

Install [sysbench](https://github.com/akopytov/sysbench):

```sh
sudo apt-get install sysbench -y
```

Run the CPU benchmark:

```sh
sysbench cpu --cpu-max-prime=20000 --threads=8 run
```

**What to look for:**  
Pay attention to the `events per second`. A higher number is better and indicates a more powerful CPU.

---

## 2. GPU Performance

For AI and machine learning, the GPU is often the most critical resource. Use [llama.cpp](https://github.com/ggerganov/llama.cpp) for benchmarking LLMs:

```sh
/home/user/llama.cpp/build/bin/bench -m /models/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf -p 512 -n 512
```

**What to look for:**  
The `pp/s` (prompt processing speed) and `tg/s` (token generation speed) are the key metrics. Higher numbers are better.

---

## 3. Disk I/O Performance

Fast disk I/O is important for loading large models and datasets.

Install [fio](https://github.com/axboe/fio):

```sh
sudo apt-get install fio -y
```

Test random read/write performance:

```sh
fio --name=random-rw --ioengine=libaio --rw=randrw --bs=4k --size=1G --numjobs=1 --iodepth=64 --runtime=60 --time_based --end_fsync=1
```

Test sequential read performance:

```sh
fio --name=sequential-read --ioengine=libaio --rw=read --bs=1M --size=1G --numjobs=1 --iodepth=64 --runtime=60 --time_based
```

**What to look for:**  
- **IOPS** (Input/Output Operations Per Second) for random workloads
- **Bandwidth** (MB/s) for sequential workloads

---

## 4. Network Performance

In a distributed cluster, the network can easily become a bottleneck.

Install [iperf3](https://iperf.fr):

```sh
sudo apt-get install iperf3 -y
```

On one node (e.g., controller), start the server:

```sh
iperf3 -s
```

On another node (e.g., worker), connect to the server:

```sh
iperf3 -c <ip_of_server_node>
```

**What to look for:**  
The **Bitrate** in Gbits/sec. This should be close to the theoretical maximum of your network hardware (e.g., 1 Gbit/s, 10 Gbit/s).

---

## 5. Application-Specific Benchmarking

While individual hardware benchmarks are useful, the most meaningful metrics come from real workloads, such as:

- Training time per epoch
- Inference latency
- Throughput (samples/sec)

Use representative models and datasets to measure your cluster's performance for your actual use cases.

---

## Summary Table

| Component | Tool | Command Example | Key Metric |
|-----------|------|----------------|-----------|
| CPU       | sysbench | `sysbench cpu ...` | Events/sec |
| GPU       | llama.cpp | `bench ...` | pp/s, tg/s |
| Disk I/O  | fio      | `fio ...` | IOPS, MB/s |
| Network   | iperf3   | `iperf3 ...` | Gbit/sec |
| App       | (varies) | (varies) | Time, Latency, Throughput |

---

## Tips

- Always run benchmarks under typical workloads.
- Document your baseline results for future comparison.
- Monitor system temperatures and power usage where possible.

---

*Happy benchmarking!*
