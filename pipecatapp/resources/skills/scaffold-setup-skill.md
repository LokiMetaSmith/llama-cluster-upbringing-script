---
name: scaffold-setup-skill
description: Generate a repo-embedded setup skill for a software project. Use when the user says "scaffold setup skill", "create a setup skill", "generate a setup wizard", "bundle a skill with this repo", or wants to create a natural language setup interface for a codebase.
version: 1.0.0
metadata:
  authored_by: scaffold-setup-skill
  authored_on: 2026-05-14
---

# Scaffold Setup Skill

Analyzes a software repo and generates a repo-embedded `.claude/skills/setup/SKILL.md` that acts as a natural language setup wizard — covering config parameters, dependency installation, infrastructure, dev workflow onboarding, and MkDocs documentation Q&A.

## When to use

- "Scaffold a setup skill for this repo"
- "Create a setup wizard for [project]"
- "Bundle a skill with my repo"
- User wants a natural language setup interface for a codebase

## Inputs

`$ARGUMENTS` may be a path to the target repo. If omitted, use the current working directory. Confirm the path with the user before proceeding.

---

## Procedure

### Phase 1 — Discovery

Read `references/discovery-patterns.md` before scanning.

Scan the target repo and produce a categorized file inventory:

| Category | Patterns to find |
|---|---|
| Config params | `.env.example`, `.env.sample`, `config/*.{yaml,yml,toml,json}`, `settings.py`, `*.config.{js,ts}` |
| Dependencies | `package.json`, `requirements.txt`, `pyproject.toml`, `Pipfile`, `go.mod`, `Cargo.toml`, `composer.json` |
| Infrastructure | `docker-compose.yml`, `Dockerfile*`, `terraform/`, `k8s/`, `helm/` |
| Dev workflow | `Makefile`, `justfile`, `scripts/*.sh`, `*.sh` at repo root, `.github/workflows/` |
| Documentation | `mkdocs.yml`, `docs/` tree (nav structure + first paragraph per file, not full content) |
| Setup guides | `README.md`, `CONTRIBUTING.md`, `INSTALL.md`, `docs/getting-started.md` |

Report the inventory to the user. Flag missing categories explicitly — e.g., "No `.env.example` found; will infer params from source code scan."

---

### Phase 2 — Analysis

Read `references/parameter-extraction.md` before this phase.

Extract three outputs from the discovered files:

**A. Parameter schema** — for every configurable value in the project:

```
name:         ENV_VAR or config key name
required:     true | false
type:         string | url | boolean | integer | secret | path | enum
description:  what this controls
default:      value or null
constraints:  format rules, min/max, allowed values
env_variants: [dev, staging, prod] — which environments use this param
depends_on:   [OTHER_PARAM] — params that must be resolved first
is_secret:    true if the value must not be echoed or stored in plaintext
```

**B. Setup steps** — an ordered list of commands/actions across these stages:
1. Dependency install (with exact command)
2. Config generation (write .env / config files)
3. Infrastructure startup (docker, db, etc.)
4. Migrations / seeds
5. Asset compilation
6. Verification

**C. MkDocs index** — if `mkdocs.yml` exists:
- Parse the `nav:` key for section titles and file paths
- For each entry, read the first non-empty paragraph of the target `.md` file
- Output a table: `section title | file path | one-line summary`
- Note the generation date

---

### Phase 3 — Clarification

Surface gaps to the user — keep this to 3–5 targeted questions, batched by topic:

1. **Missing params**: Params found in source code but absent from `.env.example` — confirm required and get descriptions
2. **Ambiguous params**: Params with no description or unclear type — ask for context
3. **Environment coverage**: Which variants (local dev, docker, cloud/prod) should the generated skill handle?
4. **Custom steps**: Any setup steps not captured by standard files (e.g., external service registration, manual credential creation)?
5. **Secret handling**: Confirm which params are secrets that must not be echoed during Q&A

---

### Phase 4 — Generation

Read `references/skill-template.md` before writing.

Fill in the template using the parameter schema, setup steps, and MkDocs index from Phases 2–3. Write the output to:

```
<repo-root>/.claude/skills/setup/SKILL.md
```

Also update `<repo-root>/CLAUDE.md`:
- If no CLAUDE.md exists: create a minimal one that notes the setup skill
- If CLAUDE.md exists: append a `## Skills` section with one line referencing `.claude/skills/setup/SKILL.md`
- Never overwrite existing CLAUDE.md content — only append if the reference isn't already present

---

### Phase 5 — Automated Testing

Run three checks against the generated skill. Report results as a pass/fail table.

**1. Coverage check** — run `scripts/coverage_check.py <repo-root> <generated-skill-path>`:
- Ground truth: all params from `.env.example` and analyzed config files
- Checked: all params documented in the generated skill
- Pass: 100% of required params covered, ≥80% of optional params covered

**2. Flow validation** — inspect the generated question flow:
- Every branch leads to another question or a terminal step (no dead ends)
- No param is asked more than once
- All `depends_on` references resolve to real param names in the schema

**3. Docs index validation** — if MkDocs integration is present:
- Every file path in the index exists in the repo
- No `nav:` entry from `mkdocs.yml` is missing from the index

Report a table: check name | result | details.

---

### Phase 6 — Human Dry Run

Walk through the generated skill section by section as a simulated new user. For each section, show what the skill would do, then ask for approval or edits.

| Section | What to show | Question to ask |
|---|---|---|
| Detection | What the skill would detect in the current repo state | "Does this detection logic look right?" |
| Questions | All questions in order with answer format | "Right order? Anything missing or redundant?" |
| Config output | Example `.env` for a dev setup | "Does this look complete and correct?" |
| Setup steps | Ordered step list | "Steps correct and in the right sequence?" |
| Docs index | Full index table | "Any documentation gaps?" |

Accumulate all requested edits; apply them in one pass after all sections are reviewed.

---

### Phase 7 — Finalize

1. Apply edits from dry run
2. Re-run automated tests to confirm no regressions
3. Report to the user:
   - Output path: `<repo-root>/.claude/skills/setup/SKILL.md`
   - Params documented: N required, M optional
   - Setup stages: K steps
   - Docs index: P entries
   - Test results: pass / warn / fail summary

---

## Anti-patterns

- Don't skip Phase 3 even if analysis looks complete — there are always undocumented params
- Don't embed actual secret values in the generated skill
- Don't mark a param `required: false` just because it has a default — "has default" ≠ "truly optional"
- Don't write a docs index entry for a file that doesn't exist in the repo
- Don't overwrite existing CLAUDE.md content
- Don't skip Phase 6 — automated tests cannot catch UX flow problems

## Compatibility

- Read access to full target repo
- Write access to `<repo-root>/.claude/` and `<repo-root>/CLAUDE.md`
- Python 3.8+ required for `scripts/coverage_check.py`
- MkDocs integration requires `mkdocs.yml`; gracefully skips if absent
- Works with any project type; discovery and extraction adapt to what's present
