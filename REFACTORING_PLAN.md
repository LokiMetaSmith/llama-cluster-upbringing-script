# Refactoring Plan

## 1. Deprecate and Remove Obsolete Router Components (Completed)
- Deleted `pipecatapp/sharded_router.py`.
- Deleted router model and training files (`pipecatapp/router_train_embeddings.pt`, `pipecatapp/router_trained_model.pkl`, `pipecatapp/router_training_data.csv`, `pipecatapp/router_training_data.jsonl`, `pipecatapp/train_router.py`, `pipecatapp/generate_real_embeddings.py`, `pipecatapp/router_config.yaml`).

## 2. Stateless Architecture & Consul KV State Management (Completed)
- Created a new backend `ConsulMemoryBackend` (in `pipecatapp/memory_backends_impl/consul_backend.py`).
- Updated `pipecatapp/memory.py` to use `ConsulMemoryBackend` instead of `CRDTMemoryBackend` or `LegacyMemoryStore` as the default to ensure statelessness for Nomad failovers.
- Removed legacy memory components (`pipecatapp/memory_legacy.py`).

## 3. Decouple TwinService from Legacy Logic (Completed)
- Removed memory_router dependency from `pipecatapp/web_server.py`.
- Renamed `router_llm` to `moe_llm` across the codebase (e.g., `pipecatapp/core/twin.py`, `pipecatapp/agent_factory.py`, `pipecatapp/tools/planner_tool.py`).
- Removed OpenRouter external reliance from `pipecatapp/tools/council_tool.py` and test mock usages.
- Updated default tool provider endpoints from `local/router` to `local/moe`.

## 4. Run pre commit checks
- Make sure code is well tested and pre commit hooks pass.
