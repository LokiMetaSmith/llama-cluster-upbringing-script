# Scheduled Task

## Task description (edit only this section)

Run through all of our tests (unit and end to end), do a dry run of the bootstrap application, run the linter, and identify anything else that can help improve and catch code quality issues.

For tests, you can use:

- `pytest tests/unit/`
- `pytest tests/e2e/` (if present)

For linters and static checks:

- `./scripts/lint.sh`
- `vulture`
- `mypy pipecatapp scripts`

For the bootstrap dry-run:

- `./bootstrap.sh --dry-run` or similar check.

## Scheduled Jules task → GitHub Issue (template)

## Goal

Run the scheduled task described above and create (or update) a single GitHub issue with the best actionable finding. Do not create a PR.

## Strong suggestion: consult docs via context7

When your recommendation depends on how a library/tool/framework is supposed to behave, strongly prefer verifying it using context7 (official docs, API references, and authoritative library documentation). Use that information to:

- confirm the expected behavior
- avoid incorrect assumptions
- justify the proposal and validation steps

## What to do each run

1. Perform the task described in “Task description”.
2. Choose one best finding: highest value with the lowest complexity.
3. Create a GitHub issue for it using the `gh` CLI, unless a matching issue already exists.

## Avoid duplicate issues

Before creating a new issue, search existing issues (open and closed) for a close match.

- Search by a short, specific phrase from your intended issue title and 1–2 unique keywords from your intended issue body.
- If you find an open issue that already covers the same finding, do not create a new issue. Add a comment to the existing issue with:
  - what you found today (new evidence, scope clarification, new affected files/areas)
  - any updated recommendation
- If you only find closed issues covering the same finding, do not create a new issue.

## Issue standard (Jules decides the actual title + wording)

- Title: concise, specific, action-oriented (start with an area prefix like “Docs:”, “CI:”, “Build:”, “Refactor:”, etc.)
- Body must be markdown and must not include code examples.
- Body structure:
  - Summary (1–3 sentences)
  - What I found (facts/evidence)
  - Proposed change (smallest reasonable scope)
  - Why (value: correctness, maintainability, lower complexity, reduced risk)
  - Scope / non-goals (explicit boundaries)
  - Validation plan (how to confirm it’s correct)
  - Risks / rollback notes

## Labels

Apply labels when creating the issue with `gh issue create --label ...`.

- Use existing repo labels where possible.
- Always apply a general maintenance label (e.g. “maintenance” or “tech-debt”).
- Also apply one task-specific label inferred from the task (e.g. “documentation”, “ci”, “cleanup”, “refactor”, “quality”).
- Do not apply a “jules” label unless you explicitly want the issue to trigger Jules again.

### Fetch available labels (gh CLI)

Use this to see which labels already exist in the repo:

- `gh label list`

(Optional: show more / filter)

- `gh label list --limit 200`
- `gh label list --search "doc"`

## Hard rules

- Do not create branches, commits, PRs, or modify files.
- Create at most one new issue per run.
- If a duplicate exists, comment and stop.
