# AT Protocol Identity Architecture for Pipecatapp Agents

This document outlines the architecture for integrating the AT Protocol (Bluesky/Colibri) into the Pipecatapp agent swarm, specifically focusing on giving our agent personalities an AT Protocol identity.

The integration is designed around three core insights regarding the current state of ATProto:

## 1. Exploit the Identity Layer, Isolate the Rest

ATProto's strongest feature is its decentralized identity and authentication system (DIDs and handles). The architecture relies entirely on ATProto's lexicons for establishing agent identities, managing their cryptographic keys, and handling their follower/following social graph.

- **No Custom Identity Systems**: We will not build a custom identity or authentication system for external agent representation.
- **DIDs as Primary Keys**: Decentralized Identifiers (DIDs) provided by ATProto will serve as the unique, global identifiers for our agents in public contexts.
- **Handles for Discovery**: Agent personalities (e.g., `coding_expert`, `creative_expert`) will be mapped to human-readable ATProto handles (e.g., `@coding.pipecat.local`).

## 2. Account for the Public vs. Private Data Split

ATProto currently assumes that all data published to the network is public broadcast data. It treats permissioned or private data as a separate architectural subsystem.

Our local cluster agents generate a mix of public outputs (e.g., finalized answers, public posts) and private/internal data (e.g., internal thought logs, sensitive memory consolidation, local state).

- **Clear Data Boundary**: We maintain a strict boundary between what the agent publishes to its ATProto feed and what it keeps in local cluster storage.
- **Local Storage for Thoughts**: The agent's internal reasoning, scratchpad data, and sensitive state will remain entirely within the local cluster's memory backends (e.g., SQLite, FAISS) and will **never** be pushed to ATProto.
- **Explicit Publishing**: Only explicitly designated "public" actions or responses will be broadcast to the ATProto network via the `ATProtoTool`.

## 3. Build a Local Cache for the PDS (Personal Data Server)

ATProto is not a "local-first" protocol like Git. The Personal Data Server (PDS) is a remote server that must be communicated with via the protocol. Agents cannot simply hold a local clone of the data and expect it to automatically sync.

Because our agents run on a local cluster that may operate offline or experience mesh connectivity drops, we must implement a local storage and sync buffer.

- **Offline Publishing**: If an agent attempts to publish a state, review, or post while the cluster is offline or disconnected from the remote PDS, the system must not crash or lose the data.
- **Sync Buffer Mechanism**: We will implement a local, persistent queue (e.g., a SQLite-backed buffer or a durable Nomad task) that caches intended ATProto actions.
- **Eventual Consistency**: Once network connectivity to the PDS is restored, a background synchronization process will flush the queued posts to the remote server, ensuring eventual consistency without blocking the agent's real-time execution loop.

## Implementation Status

1. **Identity Mapping (Completed)**: Core mapping is configured dynamically in `pipecatapp/agent_factory.py`. It utilizes an `agent_name` parameter to fetch specific identities from the agent configuration, falling back to a global default.
2. **Sync Buffer Module (Completed)**: The `PdsSyncBuffer` module is implemented in `pipecatapp/tools/atproto_sync/sync_buffer.py`. It uses a SQLite backend (dynamically named per agent identity to avoid cross-talk) to queue ATProto intents locally.
3. **Background Sync Worker (Completed)**: The `SyncWorker` is implemented in `pipecatapp/tools/atproto_sync/sync_worker.py` as an asyncio background loop that periodically flushes the queue to the remote PDS.
4. **Tool and Prompt Updates (Completed)**: `ATProtoTool` has been updated to use the sync buffer natively. The `router.txt` prompt has been updated with explicit boundary rules preventing internal state from leaking to public broadcasts.
