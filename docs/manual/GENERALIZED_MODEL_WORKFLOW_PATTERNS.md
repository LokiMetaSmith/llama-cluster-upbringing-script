# Generalized Model Configuration & Workflow Architectural Patterns

This guide extracts and generalizes core model configuration principles, adaptive reasoning controls, fallback mechanisms, context window management strategies, and enterprise governance patterns into reusable architectural principles. These patterns apply across LLM providers (Anthropic, OpenAI, local llama.cpp / vLLM clusters, Bedrock, Google Cloud, Azure Foundry) and serve as a blueprint for building resilient agent workflows.

---

## 1. Dynamic Model Aliasing & Hybrid Routing Architectures

### 1.1 Semantic Model Aliases

Hardcoding exact model version IDs (e.g., `claude-3-5-sonnet-20241022` or `gpt-4o-2024-08-06`) into application code creates maintenance overhead whenever model providers release updates or retire endpoints.

* **Pattern:** Introduce abstraction layers through semantic aliases.
  * **`best` / `fable`:** Points to the highest-capability autonomous reasoning model for long-running, multi-step investigation and verification tasks.
  * **`opus` / `reasoning`:** Points to deep-reasoning tier models suited for complex architecture, root-cause debugging, and synthesis.
  * **`sonnet` / `standard`:** Points to balanced, high-throughput models for day-to-day coding, tool usage, and transformation.
  * **`haiku` / `fast`:** Points to low-latency, lightweight models for classification, routing, filtering, and summary passes.
  * **`default`:** Resolves dynamically to the system, role, or account default.

### 1.2 Planner-Executor Hybrid Mode (`opusplan` / Asymmetric Task Dispatch)

Complex tasks benefit from asymmetric model capabilities: heavy reasoning is required to decompose a goal into a plan, but execution of individual subtasks is faster and cheaper on a mid-tier model.

* **Pattern:** Implement a single hybrid pipeline alias (e.g., `opusplan` or Asymmetric Dual-Model Execution).
  * **Planning Phase:** Uses a frontier reasoning model (`opus` / high effort) to formulate the task DAG, identify edge cases, and establish verification criteria.
  * **Execution Phase:** Seamlessly switches the agent context to a high-speed execution model (`sonnet` / medium effort) to run code, call tools, and handle deterministic operations.
  * **Context Synchronization:** Both phases share the same context state and auto-compaction bounds, preventing context drops during phase switches.

---

## 2. Adaptive Effort Levels & Dynamic Reasoning Budgets

### 2.1 Multi-Tier Effort Calibration

Modern reasoning models dynamically allocate thinking tokens based on effort level parameters rather than fixed, static token counts.

| Effort Level | Intended Use Case | Behavior & Trade-off |
| :--- | :--- | :--- |
| `low` | Rapid feedback, renames, simple formatting, small edits | Fast response, minimal/no extended thinking tokens. |
| `medium` | Standard engineering tasks, straightforward features | Balanced reasoning; default for modern balanced tiers. |
| `high` | Multi-file bug fixes, edge case detection, verification | Deep investigation and proactive testing before responding. |
| `xhigh` / `max` | Security audits, formal verification, autonomous problem solving | Unconstrained reasoning budget; evaluates multiple solution paths. |
| `ultracode` | Orchestrated dynamic multi-agent workflows | Combines `xhigh` reasoning with autonomous subagent orchestration. |

### 2.2 Per-Turn Effort Overrides & Keywords (`ultrathink`)

In multi-turn agent interactions, forcing high effort on every turn wastes compute on simple acknowledgments or single-line code fixes.

* **Pattern:** Allow session effort settings to be overridden at runtime on a per-turn basis via prompt keywords (e.g., `ultrathink`) or skill frontmatter metadata without modifying global session configuration.

---

## 3. Resilient Fallback Model Chains & Safety/Domain Failovers

### 3.1 Multi-Tier Availability Fallbacks

When a primary model endpoint experiences rate limits (429), capacity overload (529), or transient transport errors, requests fail over down a pre-configured priority chain.

```text
[Primary: Opus 5.5] ---> (Overload / 529) ---> [Fallback 1: Sonnet 5.5] ---> (Overload) ---> [Fallback 2: Haiku 5.5]
```

* **Guardrails:**
  * **Context Window Non-Degradation:** Fallback targets must have a context window equal to or larger than the primary model to prevent conversation truncation during auto-compaction.
  * **Turn-Scoped Failover:** Fallback switches apply to the active request turn only; subsequent turns re-attempt the primary model first.

### 3.2 Content & Domain Refusal Rerouting

Safety classifiers and specialized domain guards (e.g., cybersecurity, biology, proprietary code checks) may reject requests on high-capability models.

* **Pattern:** Implement deterministic content failover routes:
  * Detect refusal error codes or classifier flags.
  * Automatically re-run the request on a approved fallback model designated for that domain category (or prompt the user/supervisor if interactive mode is active).
  * Maintain conversation history and workspace context during the fallback transition.

---

## 4. Context Window Management & Proactive Auto-Compaction

### 4.1 Token Window Boundaries & Compaction Thresholds

As multi-turn conversations expand towards context limits (e.g., 200K or 1M tokens), proactive auto-compaction prevents context-overflow hard errors.

* **Threshold Strategy:** Compact the conversation history when usage reaches ~90-95% of the model's native context limit (e.g., auto-compact at ~967K tokens on a 1M window model, or ~190K on a 200K model).
* **Compaction Survival Rules:**
  * **Preserved:** System instructions, core mission prompt, latest user message, active tool definitions, and structured state keys.
  * **Summarized:** Intermediate turn logs, historical execution outputs, and old tool call payloads.

### 4.2 Gateway & Unknown Model Window Mapping

When routing through LLM gateways or custom proxy endpoints (e.g., Bedrock ARNs, vLLM, Ollama), model IDs may not be recognized out-of-the-box.

* **Pattern:** Provide model overrides and explicit context window hints (`CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `modelOverrides`, or suffix tags like `[1m]`) so the agent framework correctly enforces auto-compaction boundaries without making inaccurate assumptions.

---

## 5. Enterprise Governance & Allowlist Enforcement

### 5.1 Multi-Tier Policy Hierarchies

Organizations require fine-grained control over model usage across developers and automated agents.

1. **`availableModels` (Allowlist):** Restricts selectable models to a approved set (supports wildcards, version prefixes, or exact model IDs).
2. **`deniedModels` (Deny-list):** Explicitly blocks specific models/versions even if an allowlist wildcard permits them.
3. **`availableModelsMatch: "exact"`:** Disables automatic wildcard matching so newer unvetted model versions are held back until explicitly allowed.
4. **`enforceAvailableModels`:** Extends allowlist checks to the `Default` model selection, preventing fallbacks to non-compliant defaults.

---

## 6. Prompt Caching & Cost-Performance Optimization

* **Prefix Caching:** Structure prompts so static assets (system prompts, tool definitions, background context) appear at the prefix of the message array, maximizing provider prompt cache hit rates.
* **Tiered Cache TTLs:** Apply longer cache Time-To-Live (TTL) values to main orchestrator sessions and shorter TTLs to transient subagent calls.
* **Granular Disabling:** Provide toggles (`DISABLE_PROMPT_CACHING_<TIER>`) to turn off caching selectively on model tiers where cache read overhead exceeds savings.

---

## 7. Summary Architectural Checklist for Workflow Designers

* [ ] Use semantic aliases (`planner`, `executor`, `fast`) rather than hardcoded endpoints.
* [ ] Implement dual-model hybrid execution (`opusplan`) for heavy multi-step workflows.
* [ ] Calibrate reasoning effort levels (`low` through `max`) to match task complexity.
* [ ] Configure non-degrading fallback model chains for high availability.
* [ ] Define proactive auto-compaction boundaries at ~90-95% context capacity.
* [ ] Enforce model allowlists/deny-lists for enterprise security and cost control.
* [ ] Optimize system prompt prefixes to maximize prompt cache hits.
