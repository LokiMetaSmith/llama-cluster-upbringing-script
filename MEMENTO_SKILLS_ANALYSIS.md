# Memento-Skills Architecture Analysis

## 1. Overview
[Memento-Skills](https://github.com/Memento-Teams/Memento-Skills) is an open-source framework that enables LLM agents to rewrite and evolve their own skills without retraining the underlying model. The framework achieves this through a "Read-Write Reflective Learning" loop where an agent accesses a library of reusable skills, attempts a task, reflects on its performance, and dynamically generates or refines skills in an external library.

The core contribution is a closed-loop system for generating, executing, and refining task-specific agents using externalized memory (skills as files).

## 2. Core Concepts Extracted

### 2.1 Skills as Markdown (with Code)
Skills are treated as structured file bundles rather than simple string prompts.
- A skill is serialized into a `SKILL.md` file that contains:
  - YAML frontmatter defining metadata (name, description, required dependencies/keys).
  - Instructions and behavior.
- "Playbook" skills have an explicit `ExecutionMode.PLAYBOOK` which means they wrap runnable code (like Python scripts) alongside the markdown. "Knowledge" skills (`ExecutionMode.KNOWLEDGE`) are purely text-based instructions.
- Skills are versioned and can be embedded/vectorized for retrieval.

### 2.2 ReAct Execution Loop & Tool Bridge
When executing a skill, the framework spins up an execution loop (`SkillExecutor`) using a controlled ReAct (Reason-Act) style prompt.
- It uses a `ToolBridge` which safely exposes tools to the LLM.
- Every execution runs in an isolated context (like a sandbox), forcing the LLM to write self-contained operations rather than depending on persistent state variables across turns.

### 2.3 Reflective Learning (Self-Evolution)
When a skill fails or encounters an issue (e.g., an execution loop is detected by `loop_detector.py`, or errors are parsed by `error_recovery.py`), the agent reflects on the failure and proposes modifications to the `SKILL.md` or its associated scripts. This forms the "Write" part of the Read-Write loop.

## 3. Integration Plan for Pipecat

Our Pipecat cluster currently relies on the `MemoryStore` (SQLite) and static tools defined in Python under `pipecatapp/tools/`. We can adopt the Memento-Skills philosophy to allow the EmperorAgent to dynamically create and refine its own tools on the fly.

### 3.1 Extended MemoryStore (`MemoryStore.skills`)
We will extend `pipecatapp/memory.py` to store these skills.
- Table: `dynamic_skills`
- Schema: `id`, `name`, `description`, `content` (the markdown definition/code), `version`, `created_at`, `updated_at`.
- Like Memento, we'll store the logic as text/markdown which the LLM can rewrite.

### 3.2 Dynamic Tool Registration (`DynamicSkillTool`)
We need a way for the Langchain/Emperor Agent framework to invoke these stored skills as tools.
- We will write a wrapper class `DynamicSkillTool` (in `pipecatapp/tools/`) that is instantiated based on records from the `MemoryStore`.
- This tool will act as a sub-agent or code runner that evaluates the prompt embedded in the dynamic skill.

### 3.3 SkillBuilderTool
To close the loop, we provide the EmperorAgent with a `SkillBuilderTool`.
- This tool allows the agent to:
  - `create_skill(name, description, content)`
  - `update_skill(name, new_content)`
  - `read_skill(name)`
  - `list_skills()`
- When the agent realizes it lacks a capability, it can synthesize a solution, test it (via the existing `CodeRunnerTool` or `OpenCodeProviderTool`), and when successful, persist it via the `SkillBuilderTool`. Future agent interactions will load this dynamically.

## 4. Summary
By extracting the "Skills-as-Files" external memory concept from Memento-Skills and implementing a dynamic tool registration and building layer, we achieve the same "continual learning without retraining" goal natively within Pipecat's architecture.
