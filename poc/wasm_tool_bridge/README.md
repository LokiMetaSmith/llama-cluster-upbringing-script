# WASM Tool Bridge Proof of Concept

This directory contains a Proof of Concept (PoC) demonstrating how Python can execute lightweight WebAssembly (WASM) tools using the `Extism` runtime, as an alternative to running tools in heavy isolated Docker containers.

## Background

Our current cluster orchestrates conversational AI using Nomad and Docker. While Docker is great for the main LLM processes, deploying every simple AI tool or background worker as a separate Docker container exhausts the memory of our legacy hardware (8GB RAM nodes).

This PoC evaluates WASM as a plug-in architecture for our AI pipeline, heavily inspired by the memory efficiency seen in the `Pollen` mesh project.

## Project Structure

*   `text_processor/`: A Rust crate that compiles to WASM. It accepts a JSON payload with text and an action (`uppercase`, `lowercase`, `reverse`) and returns the processed text.
*   `host.py`: A Python script simulating the `TwinService`. It uses the `extism` SDK to load the WASM plugin, invoke it, and track execution stats.
*   `python_tool.py`: A pure-Python equivalent of the text processor for comparison.

## Requirements

*   Rust (`cargo`) with the `wasm32-wasip1` target.
*   Python 3 with the `extism` package installed.

### Setup Environment
```bash
rustup target add wasm32-wasip1
pip install extism
```

### Build the WASM Plugin
```bash
cd text_processor
cargo build --release --target wasm32-wasip1
```

## Running the Evaluation

To evaluate the footprint of the WASM sandbox vs a native python execution:

**1. Run the Python Equivalent:**
```bash
python3 python_tool.py reverse "Hello Extism!"
```
*Outputs:*
```
Result: !msitxE olleH
Execution time: ~0.01 ms
Peak memory usage: ~0.000 MB
```

**2. Run the WASM Sandbox:**
```bash
python3 host.py reverse "Hello Extism!"
```
*Outputs:*
```
Result: !msitxE olleH
Execution time: ~100.00 ms (includes cold-start load of the sandbox)
Peak memory usage: ~0.268 MB
```

## Conclusion & Insights

While a raw python function call is inevitably faster and uses less memory *inside the same process*, the power of WASM comes when comparing it to a **Docker container**.

If this tool were containerized and deployed via Nomad, the baseline memory footprint would be tens to hundreds of megabytes just for the OS and Python runtime. The Extism WASM plugin provides a secure, sandboxed execution environment with a memory footprint of just ~0.25 MB, making it an incredibly viable candidate for replacing Dockerized micro-tools in our legacy cluster.