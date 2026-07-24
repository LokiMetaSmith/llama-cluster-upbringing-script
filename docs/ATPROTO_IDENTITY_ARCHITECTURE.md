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

## Implementation Plan (Proposed)

1. **Identity Mapping**: Create a configuration (e.g., YAML or Consul KV) that maps each internal agent personality/role to a specific ATProto handle and app password.
2. **Sync Buffer Module**: Develop a `PdsSyncBuffer` module to intercept calls from the `ATProtoTool`. If the PDS is reachable, it forwards the request; if not, it queues it locally.
3. **Background Sync Worker**: Deploy a lightweight background task (e.g., via Nomad or a threading loop) that periodically checks the sync buffer and pushes pending records to the PDS when online.
4. **Tool and Prompt Updates**: Update the `ATProtoTool` to use the sync buffer and update agent system prompts to inject their assigned ATProto handles, emphasizing the strict separation of public broadcast vs. private internal thoughts.
