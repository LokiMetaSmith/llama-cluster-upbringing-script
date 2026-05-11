# LLMRouter Evaluation Report

## 1. Executive Summary

This document evaluates the [LLMRouter](https://github.com/ulab-uiuc/LLMRouter) library for inclusion in the Pipecat-App project. The goal is to determine if `LLMRouter` can improve our current model selection strategy—which currently relies on static, hardcoded "tiers"—by enabling dynamic, semantic, or cost-aware routing to local and external experts.

**Recommendation:** **Adopt with Caution (Pilot Phase).** `LLMRouter` offers significant advantages for dynamic expert selection, which is currently missing. However, it introduces a training workflow (generating routing data) that differs from our current configuration-driven approach. A pilot integration wrapping it in a Workflow Node is recommended.

---

## 2. Current System Analysis

### 2.1 Architecture

The current system uses a **Workflow Engine** (`workflow/runner.py`) where agents are defined as graphs of nodes (e.g., `workflows/default_agent_loop.yaml`).

### 2.2 Routing Mechanism

Routing is currently handled by the `SimpleLLMNode` class in `ansible/roles/pipecatapp/files/workflow/nodes/llm_nodes.py`.

* **Logic:** Static, tiered mapping.
  * `tier="fast"` → `llamacpp-rpc-router` (e.g., Phi-3)
  * `tier="capable"` → `llamacpp-rpc-coding` (e.g., CodeLlama)
  * `tier="balanced"` → `llamacpp-rpc-main` (e.g., Llama-3-8B)
* **Discovery:** Uses `consul-aio` to find services registered as `llamacpp-rpc-<expert_name>`.
* **Limitations:**
  * **Static:** The workflow designer must choose the tier at design time. There is no runtime decision-making based on query complexity.
  * **No "Smart" Routing:** A simple "hello" might go to the "balanced" model if that's what the node is configured for, wasting resources. Conversely, a complex coding question sent to a "balanced" node might fail if "capable" was required but not selected.

---

## 3. LLMRouter Analysis

### 3.1 Overview

`LLMRouter` is an open-source library designed to optimize LLM inference by dynamically selecting the most suitable model for a given query.

### 3.2 Key Features

* **Routing Strategies:** Supports multiple strategies including:
  * **KNN / SVM / MLP:** Supervised learning approaches.
  * **Causal LLM:** Uses a small LM to score candidates.
  * **Matrix Factorization:** Collaborative filtering style.
* **Local Execution:** The routing logic itself runs locally (Python). It does not *require* an external API for the routing decision, though it can route *to* external APIs.
* **Data Pipeline:** Includes tools to generate training data (query -> best model) using benchmark datasets or custom data.

### 3.3 Relevance to Our Project

* **Local Compatibility:** Highly compatible. It installs as a standard Python package (`pip install llmrouter`).
* **Model Selection:** It solves the exact problem of "which expert should I ask?".
* **Latency:** Inference for simple routers (KNN/MLP) is negligible compared to LLM generation time.

---

## 4. Comparative Analysis

| Feature | Current System (`SimpleLLMNode`) | Proposed System (`LLMRouter`) |
| :--- | :--- | :--- |
| **Decision Time** | Design Time (Static) | Runtime (Dynamic) |
| **Logic** | Hardcoded `if/else` based on "tier" | Trained Model / Heuristic |
| **Maintenance** | Low (Config changes) | Medium (Requires training data & retraining) |
| **Integration** | Native Python code | Library dependency + wrapper node |
| **Local Support** | Native (Consul Discovery) | Native (Customizable endpoints) |
| **Cost/Performance** | Fixed per workflow node | Optimized per query |

### 4.1 Pros of Adopting LLMRouter

1. **Efficiency:** Can automatically route simple queries to smaller, faster local models (e.g., `phi-3`) and complex ones to larger models (e.g., `llama-3-70b` or external APIs), optimizing latency and VRAM usage.
2. **Decoupling:** Removes the "tier" logic from the application code. The application just asks for a "response," and the router decides who gives it.
3. **Extensibility:** Easier to add new experts. You train the router to recognize the new expert's domain (e.g., "bio-medical") rather than rewriting workflow YAMLs.

### 4.2 Cons / Challenges

1. **Training Overhead:** To work well, `LLMRouter` needs to be "taught" which of our models is good at what. This requires a dataset of queries labeled with "best model". Generating this for our specific local experts might be time-consuming.
2. **Cold Start:** Out-of-the-box, it might not know that `llamacpp-rpc-coding` is good at Python. We would need to map its generic model concepts to our specific Consul service names.

---

## 5. Integration Plan

To integrate `LLMRouter` without disrupting the current stability, I propose creating a new workflow node type: `LLMRouterNode`.

### 5.1 Step 1: Dependency Management

Add `llmrouter` to `ansible/roles/python_deps/files/requirements.txt`.

### 5.2 Step 2: Create `LLMRouterNode`

Create a new class in `workflow/nodes/llm_nodes.py`:

```python
@registry.register
class LLMRouterNode(Node):
    """
    Routes a query to the best available expert using LLMRouter.
    """
    def __init__(self, ...):
        # Initialize LLMRouter with a config that maps to our local Consul services
        pass

    async def execute(self, context: WorkflowContext):
        query = self.get_input(context, "user_text")

        # 1. Ask LLMRouter for the best model name
        #    e.g., returns "qwen2.5-coder"
        router_response = self.router.route(query)
        selected_model = router_response.model_name

        # 2. Map 'selected_model' to a Consul Service
        #    e.g., "qwen2.5-coder" -> "llamacpp-rpc-coding"
        service_name = self.service_mapper.get(selected_model)

        # 3. Call the service (reusing logic from SimpleLLMNode)
        response = await self.call_service(service_name, query)

        self.set_output(context, "response", response)
```

### 5.3 Step 3: Training / Configuration

* Initially, use a **Rule-Based Router** or **Zero-Shot Router** (if available) to avoid the immediate need for a massive training dataset.
* Or, use the `LLMRouter`'s data generation tools to create a small "calibration" dataset using our active experts.

---

## 6. Conclusion

`LLMRouter` represents a mature approach to the "MoE" (Mixture of Experts) problem we are tackling. While our current static tiers work for simple workflows, they will not scale as we add more specialized experts.

**Decision:** **Proceed with a Proof of Concept.**

1. Implement `LLMRouterNode`.
2. Configure it to route between just two distinct local experts (e.g., "Chat" vs. "Coder").
3. Evaluate if the overhead of maintaining the router config outweighs the benefit of dynamic selection.
