# Evaluation of FreeLLMAPI for Swarm Failover & Request Routing Integration

## 1. Executive Summary & Recommendation

This report evaluates the core routing and failover patterns from **FreeLLMAPI** (an advanced OpenAI-compatible proxy aggregating and orchestrating multiple LLM free tiers) to guide architectural upgrades for our internal, resource-constrained **Mixture of Experts (MoE) LLM Swarm**.

Our cluster operates in a highly constrained environment: **Intel Core 2 Duo nodes (8GB RAM)**, interconnected over a private Tailscale mesh (`tailscale0`), orchestrated via **Nomad** and **Consul**, and using **Keystone Polyphony** for decentralized multi-agent collaboration.

### The Masterclass of FreeLLMAPI
FreeLLMAPI represents a production-grade masterclass in client-side, local-first API resilience. It moves beyond naïve round-robin and hardcoded try-catch fallback blocks to implement a mathematically rigorous, feedback-driven routing substrate.

### Core Architectural Recommendations for Our MoE Swarm
1. **Adopt Convex Bandit Scoring with Thompson Sampling**: Replace static priority fallback chains in our API gateway (`moe_gateway`) with a dynamic Multi-Armed Bandit using **Beta-Binomial Conjugacy** and **Marsaglia-Tsang Gamma draws**. This guarantees continuous, low-overhead exploration of healthy experts while avoiding the stale week-long average bottlenecks of flat window metrics.
2. **Implement Dual-Level Failure Isolation (Key-level vs. Model-level)**: Decouple transient key-level failures (individual account rate-limiting, credit exhaustion) from global model-level capabilities. Only penalize a model's aggregate routing priority if *all* of its registered keys/providers are exhausted.
3. **Deploy Output Token Reserve Capping**: Clamp the reserved output token estimation used during context window and TPM pre-checks to a hard threshold (`OUTPUT_RESERVE_CAP = 2000`). This completely eliminates the "bogus exhaustion" bug where a client requesting a large `max_tokens` falsely starves the entire routing layer on healthy, small-context endpoints.
4. **Ingest Context Handoff and Sticky Session Pinning**: Keep multi-turn conversations anchored to the same model instance (sticky sessions via request hashing) for a 30-minute window to stabilize reasoning. If a hard failover to another expert is required, automatically inject a **Context Handoff System Prompt** summarizing the ongoing state to prevent reasoning degradation.
5. **Coordinate Failovers with Nomad/Swarm scaling**: Wire the gateway's failover signals back to the `TaskSupervisor` and `SwarmTool`. When the gateway detects that an expert model is in hard cooldown and has no alternative healthy providers, it must trigger an on-demand Nomad job spawn to spin up a new worker instance rather than failing the client's request.

---

## 2. Deconstructing the Smart Routing Engine: Multi-Armed Bandits

Naïve routers rank models by hardcoded priorities or flat historical success rates. This creates a critical "exploration vs. exploitation" deadlock: a model that starts with a few successes is exploited exclusively, while other potentially faster or more capable models are permanently starved of trials.

FreeLLMAPI resolves this elegantly using **Thompson Sampling** modeled over decay-weighted historical observations.

### 2.1 The Mathematical Formulation
For each expert model, reliability is modeled as a **Beta distribution** $Beta(\alpha, \beta)$ where:
* $\alpha$ (Alpha) represents success credit.
* $\beta$ (Beta) represents failure credit.

$$
\alpha = successes_{weighted} + PRIOR\_SUCCESS
$$
$$
\beta = failures_{weighted} + PRIOR\_FAILURE
$$

With $PRIOR\_SUCCESS = 1$ and $PRIOR\_FAILURE = 1$, the prior is a uniform distribution (complete uncertainty).

#### The Sampler
To route a request, the engine draws a random sample from each model's Beta distribution:
$$
R_i \sim Beta(\alpha_i, \beta_i)
$$
The model with the highest drawn sample $R_i$ wins the trial. This mathematically guarantees that:
1. Highly reliable models are exploited frequently (since their distributions peak near 1.0).
2. Unexplored models are naturally explored (since their uniform-like wide distributions can occasionally yield high random samples).
3. Degraded models are benched automatically, but naturally recover as their success probabilities are updated.

### 2.2 Implementing High-Performance Beta Sampling on Legacy CPUs
On legacy CPUs (such as the Core 2 Duo), standard trigonometric or inverse-transform Beta generators are too slow or numerically unstable. FreeLLMAPI implements an extremely fast **Marsaglia and Tsang method** using two **Gamma distribution** draws:

If $X \sim Gamma(\alpha, 1)$ and $Y \sim Gamma(\beta, 1)$, then:
$$
Z = \frac{X}{X + Y} \sim Beta(\alpha, \beta)
$$

The Marsaglia and Tsang method draws Gamma samples efficiently via a squeeze-acceptance-rejection method over a normal distribution, avoiding expensive transcendental calculations in the hot loop.

### 2.3 Decay-Weighted Sliding Windows
A model that degraded 3 days ago should not carry the same penalty today. FreeLLMAPI aggregates successes and failures in daily buckets, applying an exponential decay based on a **half-life of 2 days**:

$$
Weight(t) = 0.5^{\frac{Age(t)}{T_{half\_life}}}
$$

This ensures recent performance dominates the scorer, allowing temporary node network hiccups to be forgotten within 48 hours without polluting long-term averages.

### 2.4 Multi-Objective Score Integration (The Convex Combination)
The routing engine blends three independent normalized axes:
1. **Reliability** ($\in [0, 1]$): Drawn from the Thompson Beta sampler.
2. **Speed** ($\in [0, 1]$): Blends throughput (via a saturating $1 - e^{-\frac{tokens/s}{\sigma}}$ curve) and Time-To-First-Token (TTFB) (via a linear ramp between 300ms and 5000ms).
3. **Intelligence** ($\in [0, 1]$): Normalized intelligence composite (based on size labels and capability ranks).

These are combined as a **convex combination** using user-configurable weights:
$$
Base = w_{rel} \cdot Reliability + w_{speed} \cdot Speed + w_{intel} \cdot Intelligence
$$
Where:
$$
w_{rel} + w_{speed} + w_{intel} = 1.0
$$

#### The Guardrails (Multiplicative Multipliers)
Rather than adding arbitrary penalty constants (which are easily overwhelmed or cause out-of-bounds scores), the system applies always-on **multiplicative guardrails**:

$$
Score_{effective} = Base \times HeadroomFactor \times RateLimitFactor
$$

* **HeadroomFactor**: Monitored via monthly token usage compared to provider caps. It stays at 1.0 until usage exceeds 80%, then linearly ramps down to a floor of 0.1 to gracefully deflect traffic before a complete lockout occurs.
* **RateLimitFactor**: Sinks the score dynamically on active rate-limit hits (down to a floor of 0.4), decaying back to 1.0 over time as penalties lapse.

---

## 3. Robust Fallback, Key Isolation & Cooldown Mechanics

### 3.1 Separating Key-Level vs. Model-Level Cooldowns
One of the most profound lessons of FreeLLMAPI is **Dual-Level Failure Isolation**:
* **Key-level isolation**: If an API key on a provider (e.g., a specific Groq account) returns a `429 Too Many Requests` or `413 Request Too Large`, *only that specific key* is placed on a short cooldown.
* **Model-level penalty**: A global model-level priority penalty is **only** applied if *all* registered keys/providers serving that model are currently exhausted.

$$\text{Apply Model-Level Penalty} \iff \text{No other usable key exists for model}$$

#### The Consequence
Without this isolation, a single transient rate-limit hit on one account would demote the entire model (e.g., Llama 3.3 70B) in the global router, forcing users onto weaker models even when multiple alternate healthy sibling keys are completely idle.

### 3.2 Actionable Exhaustion Diagnostics
When all routes are exhausted, typical proxies return an opaque `429 All models exhausted`. FreeLLMAPI collects precise reason codes across the routing loop to summarize *why* routing failed, category-by-category:

```
All models exhausted: 12 routes checked (4 rate-limited or on cooldown, 2 no usable key configured, 6 prompt too large). Soonest reset ~45s.
```

This is highly actionable: the client can immediately identify if the failure is due to configuration (missing keys), prompt engineering (prompt too large), or transient network limits (rate-limiting).

---

## 4. The Routing Token Reserve Cap Solution

A major bug in custom API gateways is the "bogus exhaustion" issue:
1. A client initiates a request with a very large `max_tokens` (e.g., 32,000) to ensure a complete response.
2. The routing engine's pre-checks attempt to reserve both the prompt size AND the requested `max_tokens` against model context windows and Token-Per-Minute (TPM) limits.
3. This calculation exceeds the TPM limit of every free-tier model (which typically ranges from 6,000 to 30,000 TPM), immediately throwing a 429 "All models exhausted" error without ever attempting an upstream call.

### The Solution: Output Token Reserve Capping
FreeLLMAPI implements a hard clamp on the reserved output size during routing checks, while still passing the client's original requested limit to the selected provider:

```typescript
export const OUTPUT_RESERVE_CAP = 2000;

export function routingReserveTokens(requestedMaxTokens: number | null | undefined): number {
  const requested = requestedMaxTokens != null && requestedMaxTokens > 0 ? requestedMaxTokens : 1000;
  return Math.min(requested, OUTPUT_RESERVE_CAP);
}
```

#### Why It Works
By clamping the pre-check reservation to a reasonable threshold (like 2,000 tokens), the router avoids falsely starving small-context or low-TPM models. If the model actually emits more than the reservation, standard runtime 429/413 handlers are triggered downstream—but the request is at least allowed to start, solving the starvation problem.

---

## 5. Session Continuity & Context Handoff

In a distributed swarm, failover can happen mid-conversation due to dynamic node scaling, sleep cycles, or rate-limits. This introduces a major challenge: when a session switches from Node A (running `Llama-3`) to Node B (running `Gemini-Flash`), Node B has no idea it is picking up someone else's work, leading to setup question repetition or hallucinatory state resets.

FreeLLMAPI addresses this with two key mechanisms:

### 5.1 Sticky Sessions
To maintain context and reduce state shifts, requests carry a hash of the first user message or a session header (`X-Session-Id`). The router pins subsequent conversation turns to the same model/provider for a 30-minute sliding window, overriding the bandit's random draws as long as the pinned model remains healthy and under its rate-limits.

### 5.2 Context Handoff System Prompt
When a session is forced to switch models mid-conversation, the proxy dynamically injects a compact, highly descriptive system message at the beginning of the message history:

```
FreeLLMAPI context handoff:
You are taking over an ongoing conversation from another model (groq:llama-3 -> google:gemini-flash).
Continue the user's task using the conversation context already provided in this request.
Do not restart the task, re-ask already answered setup questions, or discard prior tool results.
Respect the user's latest message as the highest-priority instruction.
```

This aligns the new model's attention mechanism with the existing state, smoothing the transition and preserving high task success rates despite backend infrastructure switches.

---

## 6. Swarm Ingestion Roadmap for Our MoE Gateway

We can directly map these lessons onto our existing `pipecatapp/moe_gateway/` and `app.py` architectures to build a bulletproof local-first routing gateway.

### 6.1 Phase 1: Upgrading the Gateway with Thompson-Sampling Scoring
* **Action**: Refactor `moe_gateway`'s routing logic to implement the Beta-binomial posterior sampler.
* **Storage**: Maintain decay-weighted success/failure pseudo-counts inside our local SQLite database (`freeapi.db` equivalent), updating counts on-the-fly when processing `app.py` request outcomes.
* **Math Optimization**: Implement the Marsaglia-Tsang Gamma generator in Python/NumPy to calculate Beta draws instantly without CPU bottlenecks on our Core 2 Duo nodes.

### 6.2 Phase 2: Implementing Output Token Reserve Capping
* **Action**: Modify the context-window and Token-Per-Minute pre-flight checks inside `pipecatapp/llm_clients.py` and `expert_tracker.py`.
* **Logic**: Introduce `OUTPUT_RESERVE_CAP = 2000` to clamp the estimated reservation size. This allows larger coding models on low-TPM local servers (like GGUF backends) to receive and process requests, preventing false-positive router rejections.

### 6.3 Phase 3: Integrating Failover with Swarm Auto-Scaling
Our cluster has a massive advantage over standard free-tier proxies: **we control the underlying physical/containerized infrastructure**.
We can tie FreeLLMAPI's failure signals directly into our **Nomad Task Supervisor**:

```
                  +--------------------------------+
                  |         User Request           |
                  +--------------------------------+
                                  |
                                  v
                        +------------------+
                        |   moe_gateway    |
                        +------------------+
                                  |
               +------------------+------------------+
               | (Routes successfully)               | (All keys on Cooldown / 429)
               v                                     v
+-----------------------------+         +-------------------------------+
| Process Request on Active   |         |   Trigger Failover Event      |
| Expert Node                 |         +-------------------------------+
+-----------------------------+                      |
                                                     v
                                        +-------------------------------+
                                        | TaskSupervisor Intercepts     |
                                        | (Extracts modelDbId / name)   |
                                        +-------------------------------+
                                                     |
                                                     v
                                        +-------------------------------+
                                        | Calls SwarmTool.spawn_workers  |
                                        | (Dynamically provisions new   |
                                        | GGUF/vLLM instances on Nomad) |
                                        +-------------------------------+
                                                     |
                                                     v
                                        +-------------------------------+
                                        | Pre-warms instance and        |
                                        | updates Consul catalog        |
                                        +-------------------------------+
```

1. **Failure Interception**: When `moe_gateway` throws an exhaustion exception carrying the precise reason codes, `TaskSupervisor` (which already polls memory and worker events) intercepts the event.
2. **On-Demand Scaling**: If the exhaustion is due to lack of healthy local providers (e.g., GGUF server crashed or OOM'd), `TaskSupervisor` immediately invokes `SwarmTool.spawn_workers(model_name)` to spin up a fresh instance on an idle worker node.
3. **Queue & Retry**: The client's request is held in a lightweight, non-blocking queue for up to 30s while the new container boots, pre-warms its GGUF weights, registers with Consul, and is discovered by the gateway, delivering seamless auto-healing.

### 6.4 Phase 4: Context Handoff for Keystone Polyphony
* **Action**: Inject the context handoff system message inside the `ExternalLLMClient.process_text` flow when a multi-agent routing switch is triggered.
* **Collaboration**: Write the handoff transition state directly to Keystone Polyphony's shared scratchpad via `PolyphonyTool.share()`, allowing sibling agents to audit and guide the newly selected expert to prevent context drift.

---

## 7. Anti-Rationalization & Verification Matrix

To ensure these workflows are strictly adhered to by developers and agents alike, we establish this mandatory verification checklist:

| Excuse for bypassing | Corrective Action / Workflow Requirement | Verification Evidence |
| :--- | :--- | :--- |
| *"Our local swarm is too small to need bandit routing; simple priority is fine."* | Bandit routing is critical to prevent CPU hot-spots on Core 2 Duo nodes. Exploitation must be distributed dynamically based on live load, speed, and latency. | Verify that a simulation of 10 concurrent requests distributes load across different healthy expert endpoints. |
| *"Clamping the output token reservation is unsafe; we might OOM the GGUF backend."* | The clamp is strictly a routing pre-check heuristic. The physical GGUF backend still receives the true limit and handles OOM boundaries natively. | Run `pytest pipecatapp/tests/test_llm_clients.py` and confirm that all custom token pre-flight bounds tests pass cleanly. |
| *"Context Handoff adds unnecessary token overhead."* | Handoff is only injected on a forced *model-level switch* mid-session, occupying less than 150 tokens, but completely preserving execution fidelity. | Confirm that session-history unit tests demonstrate correct injection when switching model parameters. |

---

## 8. Conclusion

FreeLLMAPI demonstrates that resilient, intelligent routing is a software-solvable problem. By combining **Thompson-sampling bandits**, **dual-level cooldown isolation**, **token reserve clamping**, and **context-aware session handoffs**, it achieves near-perfect uptime and high user satisfaction over fragile, unstable free-tier providers.

Integrating these architectural patterns into our **Mixture of Experts Swarm** and coupling them with **Nomad's container orchestration** will elevate our legacy cluster into a highly resilient, self-healing, and high-fidelity autonomous agent execution substrate.
