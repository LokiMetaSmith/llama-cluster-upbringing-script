A Guide to Benchmarking Your AI ClusterBenchmarking is the process of testing the performance of your hardware and software to establish a baseline, identify bottlenecks, and measure the impact of changes. For an AI cluster, this typically involves testing the CPU, GPU, disk, and network, as well as the end-to-end performance of your AI applications.1. CPU PerformanceTesting the CPU is crucial for tasks like data preprocessing, application logic, and certain types of model inference.Tool: sysbench is a versatile, scriptable benchmarking tool.Strategy: The most common CPU benchmark is to calculate a large number of prime numbers. This tests the raw integer processing power of the CPU cores.Example Command:This command will test the CPU performance using 8 threads.# First, install sysbench
sudo apt-get install sysbench -y

# Run the CPU benchmark
sysbench cpu --cpu-max-prime=20000 --threads=8 run
What to look for: Pay attention to the "events per second". A higher number is better and indicates a more powerful CPU.2. GPU PerformanceFor AI and machine learning, the GPU is often the most critical component. Its performance directly impacts model training and inference speed.Tools:nvidia-smi: For real-time monitoring of GPU usage, temperature, and memory.nvtop: A more detailed, htop-like monitoring tool for NVIDIA GPUs.llama.cpp/bench: The benchmarking tool included with llama.cpp is excellent for testing real-world LLM performance.Strategy: The best way to benchmark your GPU is to use the actual workload it will be running. The bench tool in llama.cpp measures the tokens per second your GPU can generate for a given model, which is the most relevant metric for an LLM.Example Command:This command runs the llama.cpp benchmark on your model.# Run from the build directory inside the llama.cpp folder
/home/user/llama.cpp/build/bin/bench -m /models/Meta-Llama-3-8B-Instruct.Q4_K_M.gguf -p 512 -n 512
What to look for: The pp/s (prompt processing speed) and tg/s (token generation speed) are the key metrics. Higher numbers are better.3. Disk I/O PerformanceFast disk I/O is important for loading large models into memory and handling datasets.Tool: fio (Flexible I/O Tester) is the industry standard for disk benchmarking.Strategy: Test both random read/write speeds (important for databases and small files) and sequential read/write speeds (important for large files like model weights).Example Commands:# Install fio
sudo apt-get install fio -y

# Test random read/write performance
fio --name=random-rw --ioengine=libaio --rw=randrw --bs=4k --size=1G --numjobs=1 --iodepth=64 --runtime=60 --time_based --end_fsync=1

# Test sequential read performance
fio --name=sequential-read --ioengine=libaio --rw=read --bs=1M --size=1G --numjobs=1 --iodepth=64 --runtime=60 --time_based
What to look for: The IOPS (Input/Output Operations Per Second) for random workloads and the bandwidth (MB/s) for sequential workloads.4. Network PerformanceIn a distributed cluster, the network can easily become a bottleneck, especially for tasks that require frequent communication between nodes.Tool: iperf3 is a simple and effective tool for measuring network bandwidth and latency.Strategy: Run iperf3 in server mode on one node and in client mode on another. This will measure the maximum throughput between the two machines.Example Commands:# Install iperf3 on all nodes
sudo apt-get install iperf3 -y

# On one node (e.g., a controller), start the server:
iperf3 -s

# On another node (e.g., a worker), connect to the server:
iperf3 -c <ip_of_server_node>
What to look for: The "Bitrate" in Gbits/sec. This should be close to the theoretical maximum of your network hardware (e.g., 1 Gbit/s, 10 Gbit/s).5. Application-Specific BenchmarkingWhile individual component tests are useful, the most important benchmark is the end-to-end performance of your actual application.Your pipecat app: Your app.py script already has a BenchmarkCollector class that can be enabled with the BENCHMARK_MODE environment variable. This is the best way to measure your system's real-world conversational latency.Your llama.cpp Nomad job: The benchmark.nomad job file is designed to run the llama.cpp/bench tool, giving you a repeatable way to test model performance in the same environment your service runs in.
