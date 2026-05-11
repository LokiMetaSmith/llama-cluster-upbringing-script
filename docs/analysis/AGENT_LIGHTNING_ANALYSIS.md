# Agent Lightning Analysis

## Overview

Agent Lightning is a library from Microsoft Research designed to provide training and optimization capabilities for AI agents with minimal code changes. It supports various agent frameworks (e.g., LangChain, OpenAI Agent SDK, AutoGen) and even raw API calls.

## Core Capabilities

- **Zero/Minimal Code Change**: Integrates by emitting events (`agl.emit_xxx()`) or using a tracer to collect prompts, tool calls, and rewards.
- **Framework Agnostic**: Can be layered over any existing agent framework or custom abstractions.
- **Selective Optimization**: Allows targeting specific agents in a multi-agent system.
- **Supported Algorithms**: Includes Reinforcement Learning (RL), Automatic Prompt Optimization, Supervised Fine-tuning (SFT), and more.
- **Architecture**:
  - **LightningStore**: Central hub storing tasks, resources, and execution traces.
  - **Algorithm**: Reads spans, learns, and posts updated resources (prompts, weights).
  - **Trainer**: Manages data streaming, resource ferrying, and inference engine updates.

## Integration Potential for TwinService and Custom Abstractions

Our project relies heavily on custom abstractions like `TwinService`, `WorkflowContext`, and various specific nodes (`EmperorAgentNode`, `LLMRouterNode`, etc.) rather than standard frameworks.

**How Agent Lightning could fit in:**
1. **Trace Collection**: We can integrate the Agent Lightning tracer or manual `agl.emit` calls within our node execution logic (e.g., inside `EmperorAgentNode.execute` or `ToolExecutorNode.execute`). This would capture the exact prompts we construct and the tool outputs we receive.
2. **Reward Calculation**: We need to define explicit reward functions for our agent tasks. This could be tied to our existing test suites or the output of our `ExperimentTool` and `CodeRunnerTool`.
3. **Prompt Optimization**: Agent Lightning could automatically tune our `SYSTEM_PROMPT_TEMPLATE` or specific tool descriptions based on execution traces and success rates.
4. **Policy Updates**: If we move towards trainable routing or smaller models, Agent Lightning could orchestrate the RL fine-tuning process.

## Next Steps and Architectural Considerations

If we decide to adopt Agent Lightning, we should proceed with the following phases:

1. **Proof of Concept (PoC)**:
   - Create a dedicated experiment branch.
   - Install `agentlightning`.
   - Instrument a single, well-defined workflow (e.g., a simple code generation or math task) with Agent Lightning tracing.
   - Define a basic reward function (e.g., code compilation success).
   - Run a short Automatic Prompt Optimization loop to see if it can improve the system prompt.
2. **Architecture Integration**:
   - If the PoC is successful, design a clean integration layer. Instead of scattering `agl.emit` calls everywhere, we should hook into our existing `WorkflowContext` or `TwinService` logging mechanisms.
   - Determine how `LightningStore` will interact with our existing `pmm_memory.db` and ChromaDB setup.
3. **Multi-Agent Optimization**:
   - Apply the framework to our `SwarmTool` and `TechnicianAgent` interactions to optimize the delegation and reduce phases.

## Conclusion

Agent Lightning appears highly relevant and potentially very beneficial for our goal of continuous agent improvement. Its framework-agnostic nature makes it a strong candidate for integrating with our custom architecture without requiring a massive rewrite. The primary effort will be in defining robust reward functions and cleanly injecting the tracing instrumentation.
