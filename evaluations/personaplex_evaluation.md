# Evaluation of NVIDIA/personaplex for Feature Ingestion

## 1. Executive Summary & Recommendation

This report evaluates **NVIDIA/personaplex**, a real-time, full-duplex speech-to-speech conversational model based on the Moshi architecture. PersonaPlex enables persona control through text-based role prompts and audio-based voice conditioning.

**Recommendation: High-Priority Consideration for Specialized Nodes.**
PersonaPlex represents a paradigm shift for **CommandDeck**, particularly for real-time tabletop simulations. The ability to field a persona-controlled agent that acts as a fluid, live NPC or a voice-activated assistant managing automated combat scenarios with imperceptible lag is highly desirable. However, its 7B parameter footprint means it cannot run effectively on low-power mesh nodes. It should be targeted strictly at high-tier, GPU-accelerated nodes within the cluster.

---

## 2. Technical Profile

* **Architecture:** Based on the [Moshi architecture](https://arxiv.org/abs/2410.00037) and Helium LLM backbone. It utilizes a hybrid system prompt consisting of both text and audio elements.
* **Input/Output:** Full-duplex speech-to-speech. Processes the user's microphone audio and an agent text prompt to generate agent audio and text in real-time.
* **Model Size:** 7B parameters.
* **Control Mechanisms:**
  * *Text-based role prompts* (e.g., "You are an astronaut on a Mars mission...")
  * *Audio-based voice conditioning* (e.g., predefined voice embeddings like NATF2 or VARM1).
* **Dependencies:** Requires the Opus audio codec library and PyTorch. Accelerated inference is strongly recommended.

---

## 3. Hardware & Feasibility Analysis

The most significant hurdle for integrating PersonaPlex is its computational weight.

* **GPU Requirements:** A 7B model requires significant VRAM (approximately 14-16GB for reasonable batching and context, or 4-8GB if heavily quantized, though real-time audio generation is extremely latency-sensitive).
* **Cluster Strategy (Centralized GPU Orchestrators):** Currently, PersonaPlex must be restricted to GPU-heavy orchestrator nodes (e.g., those with RTX 3090s/4090s or equivalent datacenter GPUs). Lower-tier nodes interacting with PersonaPlex will need to stream audio over the network to the centralized service rather than running inference locally.
* **Low-Power Mesh Nodes (Core 2 Duo / 4-8GB RAM):** Deploying the native 7B dense model on our mesh nodes is **unfeasible**. The memory bandwidth and compute required completely breaks the low-latency guarantees.
* **Advanced Feasibility Strategy (SSD Streaming on Edge Nodes):** Given the limitations of the mesh nodes, a hybrid architecture leveraging **Colibri's SSD streaming techniques** (`io_uring` sparse MoE loading) could make local execution possible.
    * By converting the dense Transformer backbone into a sparse MoE structure (or using dynamic MoE-LoRAs) and leveraging asynchronous NVMe read pipelines in C/Rust, we could stream only the activated experts directly from disk to pinned memory.
    * Using audio-lookahead (running the router head slightly ahead on incoming audio frames), we can hide the disk latency. See the supplementary document [`colibri_moshi_ssd_streaming.md`](./colibri_moshi_ssd_streaming.md) for the complete Rust architectural blueprint outlining this path.

---

## 4. Comparisons to Existing Pipelines

### A. PersonaPlex vs. Cascading Pipelines (Whisper + LLM + TTS)
Our traditional approach involves a pipeline: User Audio -> STT (Whisper) -> Text -> LLM (Llama/Mistral) -> Text -> TTS (Coqui/Piper) -> Agent Audio.
* **Latency:** The cascading pipeline suffers from compounding latency at each step, making interruptions or rapid back-and-forth impossible. PersonaPlex is end-to-end and full-duplex, allowing for true "turn-taking", pausing, and backchanneling.
* **Expressiveness:** Cascading TTS often lacks the nuanced emotional context of the LLM's intent. PersonaPlex generates audio natively, allowing the persona's tone to match the generated response perfectly.

### B. PersonaPlex vs. Standard Moshi
* **Control:** Standard Moshi is highly capable but can be difficult to steer into specific, persistent personas. PersonaPlex is explicitly fine-tuned on synthetic and real conversations to maintain a consistent persona based on an injected text prompt and voice embedding.
* **Use Case Fit:** For CommandDeck NPCs, the ability to instantly swap out a text prompt ("You are a grumpy innkeeper") and get a consistent performance is far superior to standard Moshi's generalized interactions.

---

## 5. Structured Data & Prompt Integration

A core requirement for our tabletop simulations is the ingestion of structured data. Our pipelines frequently parse complex XML/JSON state data to feed into simulators.

**How PersonaPlex Handles This:**
PersonaPlex's text prompts are not just static strings; they can act as dynamic state injectors.
* **Example Prompt:** `You work for CitySan Services... Information: Verify customer name Omar Torres. Upcoming pickup: April 12th.`
* **Pipeline Integration:** Our existing `schema_mapper` and data extraction tools can dynamically parse tabletop XML (e.g., NPC stats, current health, location, recent events) and compile it into a dense, natural language prompt string injected directly into the PersonaPlex hybrid prompt.
* **Real-time Shifts:** Because PersonaPlex processes the prompt continuously, changing the injected JSON state (e.g., an NPC takes damage) can immediately alter the text prompt provided to the model in the next turn, dynamically shifting the voice conditioning and conversational tone (e.g., from confident to panicked) without restarting the audio stream.

---

## 6. Pros and Cons for Inclusion

### Pros:
* **True Full-Duplex:** Unmatched low latency and support for user interruptions, crucial for live tabletop simulations.
* **Dynamic Persona Steering:** Excellent ability to consume structured context and roleplay specific NPCs.
* **Generalization:** Built on Helium LLM, allowing it to handle out-of-distribution prompts gracefully.

### Cons:
* **Resource Heavy:** 7B parameters means it cannot be distributed to edge/mesh nodes.
* **Network Latency:** If centralized on heavy GPU nodes, mesh nodes will introduce network latency when streaming audio, potentially eating into the model's low-latency benefits.
* **Immature Ecosystem:** Compared to standard Llama/GGUF ecosystems, the Moshi/PersonaPlex server architecture might require custom wrapping for robust Nomad cluster deployment.

---

## 7. Next Steps / TODOs

1. **Proof of Concept (PoC) Deployment:**
   - Create a standalone Docker container for `moshi.server` with PersonaPlex weights.
   - Deploy as a Nomad job strictly constrained to GPU-equipped nodes.
2. **Network Streaming Audio Client:**
   - Develop a lightweight Python client (using websockets and Opus) that can run on CommandDeck/mesh nodes to stream microphone input to the central PersonaPlex server and play back the response.
3. **Structured Data Adapter:**
   - Build a middleware layer in `pipecatapp` that translates live XML/JSON simulator state into PersonaPlex-formatted text prompts on-the-fly.
4. **Latency Benchmarking:**
   - Measure the end-to-end latency from a remote mesh node capturing audio to receiving the first audio frame back from the GPU node.
5. **SSD Streaming Prototype (Colibri + Moshi):**
   - Review the [Colibri/Moshi SSD Streaming Blueprint](./colibri_moshi_ssd_streaming.md) for a long-term strategy to offload inference back onto local NVMe-equipped edge nodes. Begin prototyping the Rust `io_uring` module.
