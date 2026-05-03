# CRDT Agent Memory PoC

This directory contains a Proof of Concept (PoC) demonstrating how to use Conflict-free Replicated Data Types (CRDTs) to manage the memory and state of our conversational AI agents, inspired by the decentralized orchestration of the Pollen mesh.

## Background
Currently, the `TwinService` orchestrator tracks agent conversation history in simple Python lists (`pipecatapp/memory.py`). If a Nomad node hosting an agent crashes or loses network connectivity mid-thought, the entire short-term memory of that agent is lost, and the conversation breaks.

If we migrate this state to a CRDT, the state becomes a living, distributed document. The agent's memory can be synchronized across multiple nodes seamlessly. If Node A crashes, Node B can pick up the exact conversation state and continue without dropping a beat.

## Implementation Details
*   **Library:** This PoC uses `y-py`, the Python port of the popular `Yjs` CRDT framework. *(Note: We evaluated `automerge-py`, but its Python bindings are currently unstable/incompatible with modern Python syntax compared to the highly active Yjs ecosystem).*
*   **File:** `run_poc.py` simulates a central memory document that is split across two "disconnected" nodes.

## Running the Evaluation
To see the CRDT conflict resolution in action, run the script:

```bash
pip install y-py
python3 run_poc.py
```

### What Happens?
1.  **Base State:** We initialize an agent document with a base `conversation` array and a `metadata` map indicating the active node.
2.  **Split:** The network splits. Node A and Node B now have independent copies of the document.
3.  **Concurrent Mutation:**
    *   Node A (the agent processing LLM tokens) appends a new message to the `conversation` array.
    *   Node B (a background orchestration task) simultaneously updates the `metadata` to reflect that a tool execution finished.
4.  **Merge:** The nodes reconnect and exchange binary state updates.
5.  **Result:** In a traditional JSON overwrite, one of these updates would crush the other (data loss). Because this is a CRDT, the document merges deterministically. Both the new message and the updated metadata survive.

## Next Steps for the Main Application
To implement this in `pipecatapp`:
1.  Replace the `list` in `pipecatapp/memory.py` with a `Y.YDoc`.
2.  Implement a WebRTC or WebSocket sync provider that broadcasts `Y.encode_state_as_update()` delta payloads between the Nomad nodes running the `TwinService`.