# Evaluation of Prompt Compass: Ultra-Lightweight Content-Aware Routing

## 1. Executive Summary

This evaluation analyzes the claims and architectural viability of integrating a "Prompt Compass" style router into our Keystone Polyphony Mixture of Experts (MoE) Gateway. The Prompt Compass model introduces a pre-flight, content-aware routing layer designed to direct user prompts to appropriate model tiers (local vs. cloud) while simultaneously acting as a PII and jailbreak firewall.

### The Claims:
*   **0.57 MB Router Size:** Achieves categorization without heavy embedding models (~88MB+) or Vector DB dependencies.
*   **~5ms CPU Latency:** Exceedingly fast execution on standard CPU hardware, bypassing the need for GPU acceleration.
*   **Cost Savings (Up to 96%):** Deflects trivial prompts to smaller, local/free models (e.g., 3B parameter models) while reserving frontier models for complex queries.
*   **4-in-1 Functionality:** Handles routing, PII detection, language detection, and jailbreak/injection screening simultaneously.
*   **~82% Accuracy:** Provides a "good enough" classification heuristic for routing, with extremely low false positives (<5%) for blocking genuine prompts.

### Strategic Fit for Our Swarm:
Our cluster operates in a highly constrained environment: **Intel Core 2 Duo nodes (8GB RAM)**. We currently employ a **health/reliability-based Multi-Armed Bandit (Thompson Sampling)** in `moe_gateway`. The Prompt Compass approach offers a missing, highly complementary dimension: **content-based triage**.

We strongly recommend building a native Python reimplementation of this concept as a pre-flight step in `gateway.py`.

---

## 2. Comparison to Existing System

### Current Approach: Thompson Sampling (Health/Reliability)
Currently, `ansible/roles/moe_gateway/files/gateway.py` relies on a feedback-driven Multi-Armed Bandit using Beta-Binomial Conjugacy.
*   **Strengths:** Excellent at routing around network degradation, API rate limits, and model outages. It inherently "discovers" the most reliable model over time.
*   **Weaknesses:** It is **content-blind**. A simple "Hello" or translation task is just as likely to be routed to an expensive frontier model (`gpt-4-turbo`) as a complex reasoning task, provided the frontier model has a high reliability score. This leads to inefficient resource utilization.

### Prompt Compass Approach: Pre-Flight Content Triage
The Prompt Compass model acts *before* reliability routing.
*   **Mechanism:** Inspects the raw string of the prompt to classify its intent/complexity, presence of PII, and likelihood of being a jailbreak.
*   **Benefit:** Enables tier-based routing. Trivial tasks can be forced to lightweight local/free models, preserving frontier capacity for tasks that genuinely require it.

### Synergy: A Two-Stage Routing Pipeline
1.  **Stage 1 (Content Triage - Prompt Compass):** Determine the *tier* of model required (e.g., `local_trivial`, `frontier_reasoning`) and block malicious/PII requests.
2.  **Stage 2 (Reliability Selection - Thompson Sampling):** Within the selected tier, use the existing Multi-Armed Bandit to pick the healthiest, most reliable specific expert.

---

## 3. Architectural Mapping

Integrating this into our MoE Gateway requires placing the classifier directly in the request pipeline of `ansible/roles/moe_gateway/files/gateway.py`.

### Gateway Pipeline Modification
When a request hits the `/chat/completions` endpoint:

1.  **Intercept Payload:** Extract the `messages` array from the incoming JSON payload.
2.  **Concatenate Prompt:** Extract the latest user message string.
3.  **Run Fast Classifier (In-Process):** Pass the string through the lightweight Python classifier.
    *   *If Jailbreak/PII Detected:* Return a 400 Bad Request or intercept and scrub the prompt immediately.
    *   *Else:* Determine the required model tier (e.g., `Tier 1: Trivial`, `Tier 2: Complex`).
4.  **Filter Candidates:** Filter the `EXTERNAL_EXPERTS` dictionary to only include models matching the requested tier.
5.  **Thompson Sampling:** Pass the filtered list to the existing `select_best_expert()` function to choose the most reliable model from that specific tier.

---

## 4. Feasibility of Python Reimplementation

To maintain the 0.57 MB size and ~5ms latency on an Intel Core 2 Duo, we cannot use standard HuggingFace transformers, PyTorch, or vector databases.

### Recommended Implementation Strategy

To achieve this in native Python within our constraints, we should use a **quantized linear model or classical NLP pipeline** serialized efficiently.

**Option A: Scikit-Learn Pipeline (TF-IDF + Linear SVM/Logistic Regression)**
*   **Mechanism:** Train a lightweight pipeline using `TfidfVectorizer` (with limited vocab size, e.g., max 10,000 features, character n-grams for robustness against typos) and a `LinearSVC` or `LogisticRegression` classifier.
*   **Size:** Can easily be compressed under 1MB using `joblib` or `pickle` by aggressively pruning feature weights.
*   **Latency:** Inference involves a simple sparse matrix multiplication. Well under 5ms, even on a Core 2 Duo.
*   **Pros:** Native Python, no massive binary dependencies, highly transparent.

**Option B: ONNX Runtime with a Distilled Micro-Model**
*   **Mechanism:** Distill a tiny language model (e.g., an ultra-small fastText variant or a tiny CNN) and export it to ONNX.
*   **Size:** An 8-bit quantized ONNX model can easily fit within the <1MB constraint.
*   **Latency:** `onnxruntime` is highly optimized for CPU inference and operates entirely in-memory without starting child processes.
*   **Pros:** Potentially higher accuracy on complex jailbreaks than simple TF-IDF.

**Recommendation:** For the first iteration, **Option A** (or a highly optimized pure Python implementation using pre-computed term frequency hashes and weight dictionaries) is the most viable path to guarantee zero dependency bloat while maintaining extreme speed.

### Adapting to the Swarm
Because our cluster uses local node isolation, the 0.57MB artifact must be statically included in the repository (e.g., in `ansible/roles/moe_gateway/files/static/compass_weights.json` or `.pkl`) and loaded into memory *once* during the FastAPI `lifespan` event to avoid disk I/O on every request.

---

## 5. Integration Roadmap

1.  **Phase 1: Model Artifact Generation (Offline)**
    *   Train a lightweight, highly compressed classifier (e.g., Logistic Regression over character n-grams) on a public dataset of standard prompts, jailbreaks, and PII.
    *   Export the weights to a tiny, static JSON or `.pkl` file (target < 1MB).
2.  **Phase 2: Gateway Pipeline Integration**
    *   Add a `PromptCompassRouter` class to `gateway.py`.
    *   Load the static weights in the FastAPI `lifespan` context manager.
    *   Inject the pre-flight check into the `chat_completions` route.
3.  **Phase 3: Tier Tagging**
    *   Update the `EXTERNAL_EXPERTS` dictionary in `gateway.py` to include a `tier` metadata tag (e.g., `openai_gpt4` = `complex`, `together_1bit_bonsai_27b` = `trivial`).
    *   Modify `select_best_expert()` to accept a tier filter.
4.  **Phase 4: Telemetry & Monitoring**
    *   Log classification results and latency in the SQLite database (`gateway_metrics.db`) to monitor the false positive rate and performance overhead.