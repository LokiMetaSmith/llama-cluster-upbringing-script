---
name: renovate
description: Systematic cleanup of existing or inherited codebases. Map → cover → clean, module by module. Use when a codebase is messy, vibe-coded, or you're taking it over and want to clean it up without breaking anything.
---

# Renovate

Announce: **"Renovate mode on."**

**Why this exists**: Cleaning code you didn't write is risky. You don't know what's load-bearing, what's deliberately weird, or what has no tests. Renovate enforces a safe sequence: map the structure, establish a regression safety net, then clean. `/backpass` is for code you just wrote. Renovate is for everything else.

---

## Overview

```
PHASE 0: Triage   → assess scope and decide mapping depth
PHASE 1: Map      → build structural understanding
PHASE 2: Audit    → measure test coverage gaps
PHASE 3: Cover    → write characterization tests for uncovered modules
PHASE 4: Clean    → apply /backpass module by module
PHASE 5: Report   → what changed, what didn't, what's still owed
```

No phase can be skipped. Phases 3 and 4 may be short if coverage is already good.

---

## Phase 0: Triage

Assess:

- [ ] Languages, file count, approximate LOC (`find . -name "*.py" | wc -l`, etc.)
- [ ] Git status: is there a clean commit to baseline against? (`git log --oneline -5`)
- [ ] Test framework in use (`pytest`, `jest`, `go test`, `cargo test`, etc.)
- [ ] Existing coverage tooling or reports

**Depth decision** — escalate to deep map if **any** of:

- >50 source files
- Multiple languages
- No existing tests
- Non-obvious business logic (the domain isn't clear from file names alone)

**Standard depth**: `/repo-map` only.
**Deep depth**: `/repo-map` + `/understand` (understand-anything).

Announce the chosen depth before proceeding.

---

## Phase 1: Map

Run `/repo-map`:

```bash
repo-map "$PROJECT_ROOT" --full
# large repos:
repo-map "$PROJECT_ROOT" --budget 8000
# Python-heavy (richer metadata):
repo-map "$PROJECT_ROOT" --full --enrich-python
```

Navigate the map per `/repo-map` skill rules — **never load the full file**. Read only the guide (first ~80 lines), then grep + slice for specific sections.

From the catalog, identify:

- [ ] Entry points (main, CLI handlers, API routes)
- [ ] Core logic modules (highest cleanup value, clean these first)
- [ ] Utility/helper modules
- [ ] Orphan or obviously dead files

Build a **cleanup priority list**: core logic first, utilities last, config last. Announce the list before proceeding.

For deep path: invoke `/understand` after the repo map to fill in cross-module flows and domain narrative.

---

## Phase 2: Coverage Audit

Locate tests:

```bash
find . \( -name "test_*.py" -o -name "*_test.py" -o -name "*.test.ts" -o -name "*.test.js" -o -name "*_test.go" \) \
  | grep -v .venv | grep -v node_modules | grep -v target
```

Measure coverage if tooling exists:

| Language | Command |
|----------|---------|
| Python | `pytest --cov=src --cov-report=term-missing` |
| Go | `go test ./... -coverprofile=coverage.out && go tool cover -func=coverage.out` |
| JS/TS | `npx jest --coverage` |
| Rust | `cargo tarpaulin` |

For each module in the priority list, record: **covered** or **uncovered**.

**Gate**: any core-logic module that is uncovered must have characterization tests written before it can be cleaned. Do not proceed to Phase 4 for a module without coverage.

---

## Phase 3: Characterization Tests

Characterization tests capture **current behavior**, not intended behavior. They are regression guards, not correctness validators. Write them for buggy behavior too — bugs are a separate concern.

Rules:
- Test observable outputs (return values, side effects, emitted events) — not internals
- If you find a bug while writing tests: add a `# BUG: description` comment and move on. Do not fix it.
- All characterization tests must pass (green) before Phase 4 begins

See [REFERENCE.md](REFERENCE.md) for characterization test patterns by language and how to bootstrap a test framework from scratch.

---

## Phase 4: Clean

Apply `/backpass` to each module in the priority list, one module at a time.

After each module:
1. Run the full test suite
2. Tests must be green before moving to the next module
3. If tests break: revert that module's changes, record the failure in the report, continue with the next module

Constraints from `/backpass` apply in full:
- Equivalence-preserving: change form, not behavior
- No new features during this pass
- No bug fixes during this pass (note them for a follow-up forward pass)

---

## Phase 5: Report

```
Renovate complete.

Modules cleaned:  N
Modules skipped:  N
  - [module]: reason (insufficient coverage / test failures / out of scope)

Simplifications:
  - [file:line] description
  - [file:line] description

Bugs found (not fixed — follow-up needed):
  - [file:line] description

Coverage: X% → Y%

Follow-up items: [optional]
```

If nothing was simplified: **"Renovate complete. No simplifications found — codebase was already clean."**

---

## Rules

- **Map before touch.** Never start cleaning without Phase 1 complete.
- **Cover before clean.** Never apply `/backpass` to an uncovered module.
- **One module per test run.** Do not batch modules across a single run.
- **Note bugs, don't fix them.** Renovate changes form. Fixes are a separate forward pass.
- **Tests are the gate.** Failing tests stop the module. Suite must be green before the next.
