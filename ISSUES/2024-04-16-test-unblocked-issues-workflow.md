# Test Unblocked Issues Workflow

## Context
A new GitHub Actions workflow has been added in `.github/workflows/unblocked-issues.yml` to automatically invoke an AI agent (Jules) when issues are unblocked (closed). The `auto-merge.yml` workflow requires any pull request to be accompanied by a new issue definition in the `ISSUES/` directory to merge automatically. We also need to ensure that the unblocked-issues workflow correctly functions as intended, triggering off `issues: closed` events and reading the properties properly.

## Acceptance Criteria
- Verify the behavior of `.github/workflows/unblocked-issues.yml` by monitoring a closed issue in a testing environment or via a mock event payload to `on-unblocked@v1`.
- Ensure Jules is correctly invoked with the right prompt variables when an authorized user closes an issue.
- Consider refactoring `.github/workflows/unblocked-issues.yml` to support different target branches or configurable settings (like the trusted user list).
