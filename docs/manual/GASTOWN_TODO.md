# Gas Town Integration Todo

This roadmap tracks the adaptation of Gas Town concepts (Work Ledger, Attribution, Agent CVs) into the Pipecat App ecosystem.

## Phase 1: Foundation - The Work Ledger & Attribution

- [x] **Backend Schema Update:** Modify `pmm_memory.py` to support a `work_items` table (Beads).
  - [x] Add `create_work_item`, `update_work_item`, `get_work_item` methods.
  - [x] Schema: `id`, `title`, `status`, `assignee_id`, `created_by`, `created_at`, `validation_status`, `meta`.
- [x] **API Exposure:** Update `memory-service` (`app.py`) to expose REST endpoints for Work Items.
- [x] **Client Library:** Update `pmm_memory_client.py` with methods to interact with the new endpoints.
- [x] **Testing:** Create integration tests to verify the Work Ledger works as expected.

## Phase 2: Agent Integration

- [x] **Technician Agent:** Update `TechnicianAgent` to:
  - [x] Create a "Plan" as a set of `work_items` in the ledger.
  - [x] Update item status to `in_progress` and `completed` as it executes.
- [x] **Worker Agent:** Update `WorkerAgent` to report status updates to specific work items if assigned a `work_item_id`.

## Phase 3: Agent CVs & Analytics

- [x] **Stats Aggregation:** Add SQL queries to `pmm_memory.py` to calculate success rates by agent and tag.
- [x] **API Endpoint:** Add `GET /agents/{id}/stats` to expose this data.
- [x] **Manager Agent:** Update `ManagerAgent` to query these stats when selecting agents for tasks.

## Phase 4: Validation & Quality Gates

- [x] **Validation Schema:** Add `validation` column (JSON) to `work_items`.
- [x] **Judge Agent:** Create/Update `JudgeAgent` (or equivalent) to perform checks (lint, test) and update the `validation` field.

## Phase 5: Federation (Future)

- [ ] **Remote Ledgers:** Investigate syncing work items across multiple Memory Service instances.
