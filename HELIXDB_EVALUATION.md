# HelixDB Evaluation Report

## 1. Overview

This document evaluates [HelixDB](https://github.com/HelixDB/helix-db) against the current memory and database architecture of our project, specifically addressing the criteria of **distributed capabilities**, **recoverability**, **speed**, and **efficiency**.

HelixDB is a new, Rust-based graph-vector database designed specifically for AI memory, RAG, and knowledge graphs. It unifies graph, vector, key-value, document, and relational data models into a single query engine.

### Current Architecture Summary
Currently, our AI memory and RAG systems rely on a fragmented stack:
- **Vector Storage:** `faiss-cpu` index paired with a SQLite store (`pipecatapp/memory.py`).
- **Relational/Document Storage:** SQLite (`memories`, `consolidations`, `dynamic_skills` tables).
- **Graph Storage:** A separate `memorygraphMCP` service utilizing a `SQLiteFallbackBackend` exposed via `FastMCP` (`pipecatapp/memory_graph_service/server.py`).

---

## 2. Evaluation Criteria

### 2.1. Distributed Capabilities
**Current Setup:** SQLite and FAISS are inherently single-node, embedded systems. While they run well in our current containerized environment (Docker/Nomad), they do not support native horizontal scaling or distributed replication. Running them across a cluster requires complex network file systems (NFS/EFS) or application-level sharding, which introduces latency and consistency issues.
**HelixDB:** HelixDB is designed with distributed systems in mind. While the open-source local CLI (`helix start dev`) runs as a single container instance, its architecture (as seen in HelixDB Cloud) natively supports high availability. It uses an object-storage-backed deployment with a single-writer / auto-scaling reader topology and high-availability gateways. Deployed natively within our Nomad/Consul cluster, a HelixDB container could easily serve as a centralized, queryable AI memory engine accessible by all edge and core nodes without file-locking contention.

### 2.2. Ability to Recover
**Current Setup:** Recovering our current memory state requires restoring SQLite `.db` files and ensuring the FAISS index remains synchronized with the SQLite row IDs. If the node fails during a write, the FAISS index and SQLite store could become out of sync, leading to data corruption or orphaned vectors.
**HelixDB:** HelixDB provides strong ACID transaction guarantees. By writing all modalities (graph and vector) into a single transaction log and storage engine, it prevents the "split-brain" synchronization issues we face with FAISS + SQLite. For local Nomad deployments, passing the `--disk` flag to the Helix container ensures state is persisted to a mounted volume, allowing seamless recovery upon task restart.

### 2.3. Speed
**Current Setup:** FAISS is highly optimized for fast vector similarity search, and SQLite is extremely fast for local read/writes. However, the bottleneck in our system is **application-level joins**. To find memories that are both semantically similar (FAISS) *and* relationally linked (SQLite graph), the application must perform multiple queries and merge the results in Python memory.
**HelixDB:** Built from scratch in Rust, HelixDB is extremely fast. More importantly, it pushes the query execution down to the database layer. A single query can traverse graph relationships and perform vector similarity scoring simultaneously. This eliminates the network and serialization overhead of pulling data into the Python application just to filter it.

### 2.4. Efficiency
**Current Setup:** We are currently managing three separate logical stores. When a new memory is created, we must update the FAISS index, insert metadata into SQLite, and potentially update the graph relationships in the MCP service. This uses more disk space, memory, and CPU cycles due to data duplication and Python application overhead.
**HelixDB:** Helix unifies KV, documents, relational, graph, and vector paradigms. Instead of running a separate `memory_graph_service` and a separate FAISS index, we could consolidate all memory operations into a single HelixDB instance. This reduces the number of running containers, lowers RAM usage (replacing in-memory FAISS and Python overhead with optimized Rust), and vastly simplifies the codebase.

---

## 3. Lessons Learned & Recommendations

Even if we do not immediately replace our stack with HelixDB, there are several key lessons we can apply to our current project:

1. **Unify Modalities Where Possible:** The fragmentation between our FAISS vector index, SQLite metadata store, and `memorygraphMCP` graph store creates technical debt and fragile synchronization. Moving towards a system that handles graph relationships and vector embeddings together is highly desirable.
2. **Push Logic to the Query Engine:** Currently, we pull data from FAISS and SQLite to merge it in Python. HelixDB teaches us that representing AI memory as a graph, where nodes have vector properties, allows the database to execute complex queries (e.g., "Find the top 3 semantically similar memories that are also directly connected to the current user node").
3. **MCP as a First-Class Citizen:** HelixDB natively incorporates MCP (Model Context Protocol). Our current workaround involves wrapping `memorygraph` in a `FastMCP` FastAPI wrapper. Adopting tools that natively speak MCP can reduce our API bridging code.

### Conclusion

**Should we include HelixDB?**
Yes, HelixDB is a strong candidate for replacing our fragmented memory stack. Its Rust-based architecture, unified graph-vector model, and built-in distributed/ACID capabilities directly solve the scaling and synchronization limits of our current SQLite + FAISS implementation.

**Next Steps:**
Based on this evaluation, it is recommended to proceed with a Proof-of-Concept (PoC). The PoC should involve deploying a `helix` container as a Nomad job and rewriting the `pipecatapp/memory.py` module to route standard semantic memory and graph memory creation through the HelixDB REST API.

### Proof-of-Concept (PoC) TODO List

To validate HelixDB in our environment without disrupting the existing system, the following steps outline a localized PoC integration:

- [ ] **1. Containerize HelixDB for Nomad**
  - Create a new Dockerfile or identify the official HelixDB image tag.
  - Write an Ansible task or Nomad job file (`helixdb.nomad`) to deploy a local instance using `helix start dev --disk` to ensure data persistence across container restarts.
  - Expose the default HelixDB port (`6969`) to the cluster network.

- [ ] **2. Develop HelixDB Python Client Adapter**
  - Since HelixDB provides Rust and TypeScript SDKs, build a lightweight Python HTTP client that constructs JSON AST payloads and sends them to the `POST /v1/query` REST endpoint.
  - Implement basic CRUD operations for Graph nodes and Vector embeddings using the client.

- [ ] **3. Implement an Abstract Memory Backend Interface**
  - Refactor `pipecatapp/memory.py` to extract the `FAISS` and `SQLite` logic into a backend interface (e.g., `BaseMemoryBackend`).
  - Create a new `HelixMemoryBackend` that implements the interface using the Python client.

- [ ] **4. Integrate MCP Tooling**
  - Review the existing `pipecatapp/memory_graph_service/server.py` implementation.
  - Write an alternative `HelixMCPService` that registers tools (`store_memory`, `create_relationship`, `search_memories`) but routes execution to HelixDB instead of the `SQLiteFallbackBackend`.

- [ ] **5. Testing and Benchmarking**
  - Write integration tests inside `tests/` to verify semantic search and graph traversal accuracy on the `HelixMemoryBackend`.
  - Use `llama-bench` or custom latency metrics to compare the inference-to-retrieval latency between the legacy FAISS/SQLite setup and the new HelixDB setup.

- [ ] **6. Production Evaluation**
  - Review memory constraints and CPU usage of the Helix container in Nomad versus the python-based FAISS setup.
  - Decide on full migration vs rollback based on the PoC outcomes.
