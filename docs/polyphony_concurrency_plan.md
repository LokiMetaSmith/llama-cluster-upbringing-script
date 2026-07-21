# Keystone Polyphony - Concurrency Roadmap

This document outlines the file-level concurrency roadmap designed to achieve parity with the Cursor Agent Swarm merge conflict resolution model, using Keystone Polyphony's native RTOS-inspired baton/mutex architecture.

This plan should be implemented in the `keystone-polyphony` repository by the dedicated agent.

## Implementation Steps

### 1. Granular Batons (File-Level Locks)

- **Objective:** Extend the current baton/mutex system (`polyphony task claim`) to support granular file-level or module-level locks.
- **Action:** Implement a `polyphony baton acquire <filepath>` and `polyphony baton release <filepath>` command in the CLI.

### 2. Agent Tool Integration

- **Objective:** Ensure all agents respect the new file locks natively.
- **Action:** Modify the core Pipecat agent tools (e.g., `FileEditorTool` and `ASTEditorTool`) to automatically query Keystone Polyphony for file locks before executing a file write or AST patch. If a file is locked by another agent, the tool should pause, queue the edit, or cleanly fail with an informative context message.

### 3. Conflict Backpressure

- **Objective:** Prevent deadlocks when multiple agents need to modify the same file.
- **Action:** Implement a fallback mechanism. If a file is locked, the agent should:
  - Branch the work.
  - Submit a virtual patch (diff) to the agent currently holding the baton.
  - Broadcast a `share` thought indicating contention so higher-level planner agents can intervene.

### 4. Megafile Flagging and Decomposition

- **Objective:** Handle heavily contested or bloated files before they bottleneck the swarm.
- **Action:** Allow worker agents to use Polyphony to flag a file as a "Megafile". This action should trigger an automatic refactor baton/task for a dedicated decomposition agent (e.g., triggering a pipeline workflow to break the file into smaller modules).
