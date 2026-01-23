# Scaling Long-Running Autonomous Coding - Implementation Scope

This document tracks the progress of integrating the "Browser from Scratch" autonomous coding architecture into `pipecatapp`.

## Phase 1: Foundation (The Shared Brain)
- [x] **Implement Event Bus API** (`event_api.py` / `server.py`)
    - [x] Create FastAPI service with `POST /events` and `GET /events`.
    - [x] Implement SQLite backend (`events.db`) for task state tracking.
    - [x] Add `GET /tasks/{task_id}` for direct status checks.
- [x] **Service Discovery & Deployment**
    - [x] Update `pipecatapp` build/startup scripts to include `event_api`.
    - [x] Register service in Consul (e.g., `event-bus` or extend `memory-service`).

## Phase 2: Agent Integration
- [ ] **Update Worker Agent** (`worker_agent.py`)
    - [ ] Ensure it discovers the Event Bus correctly.
    - [ ] Verify payload format matches `POST /events` expectation.
- [ ] **Update Technician Agent** (`technician_agent.py`)
    - [ ] Ensure it reports detailed progress (plan, execution steps) to Event Bus.
- [ ] **Update Manager Agent** (`manager_agent.py`)
    - [ ] Replace mock polling with real `GET /events` polling.
    - [ ] Implement "Reduce" phase logic using real worker outputs.

## Phase 3: The Judge & Quality Assurance
- [ ] **Implement Judge Agent** (or distinct Judge loop in Manager)
    - [ ] Create `JudgeAgent` or `VerificationTool`.
    - [ ] Define criteria for "success" (e.g., lint pass, test pass, functionality check).
- [ ] **Workflow Upgrade**
    - [ ] Update Manager to dispatch "Verify" tasks after "Execute" tasks.
    - [ ] Implement retry/feedback loop: if Judge fails, Manager creates new fix task.

## Phase 4: Smart Context (Git Submodules/Docs)
- [ ] **Create SpecLoader Tool**
    - [ ] Tool to clone/pull external git repositories (e.g., library docs).
    - [ ] Ingest text/markdown from these repos into RAG/Memory.
- [ ] **Context Injection**
    - [ ] Allow Manager to specify "External Specs" to load for a mission.

## Phase 5: Scaling & Swarm
- [ ] **Infrastructure Tuning**
    - [ ] Verify Nomad job templates allow dynamic scaling.
    - [ ] Test with >10 concurrent agents.
- [ ] **SwarmTool Upgrade**
    - [ ] Ensure `SwarmTool` can handle batch dispatch efficiently.
