# Dirac Evaluation: Inclusion vs Inspiration

## 1. Executive Summary
Dirac is an open-source coding agent highly optimized for token efficiency, accuracy, and speed. It recently topped the TerminalBench 2.0 leaderboard by achieving high task completion rates while significantly reducing API costs (by approximately 65% compared to other agents). Given our project's constraints (legacy CPU clusters, split inference on older hardware, 8GB RAM nodes), Dirac's extreme token efficiency makes it a highly attractive solution for handling coding and refactoring tasks.

This document evaluates the key features of Dirac that align with our resource-constrained architecture and presents two paths for adopting these capabilities: **Inclusion** (integrating Dirac as a CLI tool) and **Inspiration** (re-implementing Dirac's core logic in our native tools).

## 2. Key Features Relevant to Our Project

Dirac employs several novel techniques to drastically reduce context window bloat and improve reasoning capabilities:

*   **Hash-Anchored Edits:** Instead of relying on line numbers (which drift and confuse LLMs during multi-step edits) or standard search/replace blocks (which require large amounts of exact context), Dirac uses stable line hashes. This means the LLM needs to output far fewer tokens to specify exactly where an edit should occur.
*   **AST-Native Precision:** Dirac parses the Abstract Syntax Tree (AST) of the target languages (Python, TypeScript, etc.). This allows the agent to issue structural commands (e.g., "extract this function", "rename this class") instead of dealing with raw text manipulation, completely eliminating syntax errors and reducing the token payload.
*   **Multi-File Batching:** By modifying multiple files in a single LLM roundtrip, it drastically reduces the number of tool-call cycles and prompt reiterations required for complex refactors.
*   **High-Bandwidth Context Curation:** It strictly minimizes the context prompt. Rather than dumping entire files into the context window, it only feeds what is necessary, saving compute on our legacy LLaMA nodes.

## 3. Path A: Inclusion (Integration as a CLI Tool)

**Concept:** We wrap the `dirac` CLI in a Python tool (e.g., `pipecatapp/tools/dirac_tool.py`), similar to how we integrated `opencode` or `smol_agent_computer`. Our main agent would delegate complex coding tasks to the Dirac sub-agent.

**Pros:**
*   **Immediate ROI:** We gain access to hash-anchored edits, AST precision, and multi-file batching immediately without having to write the complex parsing logic ourselves.
*   **Proven Efficiency:** We instantly inherit the 65% token reduction and 100% accuracy on refactors.
*   **Maintained Upstream:** We benefit from ongoing improvements to Dirac by the open-source community.

**Cons:**
*   **Node.js Overhead:** Dirac is a Node/TypeScript application. Running it requires a Node runtime and installing npm packages globally on our legacy worker nodes, which may consume valuable memory (RAM) and disk space.
*   **Tool Calling Compatibility:** Dirac strictly requires models with "native tool calling enabled" (no MCP). While it supports standard providers (OpenAI, Anthropic), we must ensure our local LLaMA RPC models (served via `llama-cpp-python` or standard OpenAI-compatible endpoints) strictly adhere to the exact tool-calling schema Dirac expects.
*   **Loss of Fine-Grained Control:** Dirac operates as a "black box" agent loop. Our orchestrator hands off the task, but loses insight into the intermediate steps unless it parses Dirac's stdout.

## 4. Path B: Inspiration (Re-implementing Features)

**Concept:** We analyze Dirac's techniques and natively build them into our existing Python tools (like `file_editor`, `autoresearch`, and `code_runner`).

**Pros:**
*   **Zero Additional Overhead:** We keep our cluster lean by avoiding a Node.js runtime and avoiding another heavy sub-agent process.
*   **Perfect Harmony with Local Models:** We can design the hash-anchoring and AST prompts to perfectly match the quirks and strengths of the specific local models (like `phi-3-mini` or LLaMA-3) we are running on our legacy hardware.
*   **Python-Native:** Our entire ecosystem is Python/Ansible. Building AST manipulation in Python (using libraries like `ast` or `libcst`) integrates beautifully with our existing architecture.

**Cons:**
*   **High Development Cost:** Writing a robust hash-anchored editing system and AST parser from scratch is a significant engineering effort.
*   **Maintenance Burden:** We will have to maintain this complex editing logic and fix edge cases ourselves.
*   **Reinventing the Wheel:** We spend time building infrastructure that Dirac has already solved.

## 5. Decision: The Hybrid Approach

Based on evaluation, the decision is to pursue **both paths simultaneously**.

1.  **Immediate Value (Path A):** We will integrate the Dirac CLI as a new tool (`dirac_tool`) today. This allows the system to immediately take advantage of the massive 65% token savings, highly accurate AST manipulation, and multi-file batching.
2.  **Long-term Resilience (Path B):** While Dirac is running via CLI, we will begin upgrading our native Python tools (like `file_editor` and `autoresearch`) to draw inspiration from Dirac's techniques. Specifically, we will implement our own hash-anchored line edits and Python AST manipulation. Once these native features achieve parity, we can slowly phase out the heavier Node.js dependency on the worker nodes.

See `DIRAC_TODO.md` for the concrete step-by-step integration plan.