# Peer-to-Peer `.gguf` Model Sync PoC

This directory contains a Proof of Concept (PoC) demonstrating how to distribute heavy `.gguf` language models across our legacy CPU cluster using a decentralized Peer-to-Peer (P2P) mechanism.

## Background
Currently, distributing massive LLM weights (e.g., `llama-3-8b.gguf`) to multiple 8GB legacy nodes relies on centralized downloading from a master node or the internet. This creates a massive bandwidth bottleneck.

By using **Syncthing**, nodes treat the `/models` directory as a shared, peer-accelerated folder. If Node A downloads a model, Node B can pull it locally over the high-speed LAN via P2P chunking instead of hitting the control plane.

## Project Structure
* `syncthing_manager.py`: A Python wrapper that automates the downloading, configuration, and API interactions with the local Syncthing daemon.
* `run_poc.py`: The main test script. It spins up two local nodes (`A_Seeder` and `B_Leecher`), pairs them, creates a dummy 5MB `.gguf` file on Node A, and watches Node B automatically leech it.

## Running the Evaluation
To see the P2P synchronization in action, simply run the Python script.

```bash
python3 run_poc.py
```

*Note: The script automatically spins up the `syncthing` daemon, you do not need to install it globally.*

---

## Keystone Polyphony Integration Strategy

While this PoC handles the raw P2P file transport, the true power of this architecture is realized when integrated with the **Keystone Polyphony** state layer and the **Pollen** compute mesh.

### 1. Model Location Awareness (Polyphony)
Keystone will be extended to monitor the local Syncthing REST APIs across the cluster. It will maintain a CRDT state map of "Which nodes currently hold which `.gguf` models in their local storage".

### 2. Intelligent Workload Placement (Pollen)
When a new conversational workload requires a specific model (e.g., a "Math Expert" requiring `phi-3`), Keystone will query its map.
Instead of forcing a random node to download the model, Keystone will issue a `pln grant` to instruct the **Pollen** WASM mesh to schedule the inference workload *directly on the node that already has the model seeded via Syncthing*.

### 3. Distributed Split Inference
If the model is too large for a single legacy node, Keystone will identify a group of peers that have all finished syncing the model, and coordinate them to load split shards into memory, maximizing cache locality.
