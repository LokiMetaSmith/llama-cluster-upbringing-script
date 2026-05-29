# Architecture Decision Record (ADR) Template

This template is used to document significant architectural decisions, infrastructure changes, or new technological adoptions across the cluster.

## 1. Title

**ADR NNN: [Short Noun Phrase Describing the Decision, e.g., Migrate Database to PostgreSQL]**

* **Status:** [Proposed / Accepted / Rejected / Deprecated / Superseded]
* **Date:** [YYYY-MM-DD]
* **Author(s):** [Names or Handles]

## 2. Context

Describe the problem space, the current state of the architecture, and the forces (technical, organizational, or business) that are prompting a change. What is the motivation for this decision?

* *Example:* "Currently, we use SQLite for our agent memory store. However, as we scale to a distributed Nomad cluster, SQLite's lack of concurrent write support is causing lock contention and crashes."

## 3. Decision

State the decision clearly and concisely. What is the chosen solution?

* *Example:* "We will migrate the primary agent memory store from SQLite to a highly available PostgreSQL cluster deployed via Nomad."

## 4. Consequences

What are the implications of this decision? Consider both the positive (benefits) and negative (trade-offs, new technical debt) consequences.

### Positive Consequences

* [e.g., Improved concurrent write performance.]
* [e.g., Support for advanced JSONB querying for complex memory structures.]

### Negative Consequences / Trade-offs

* [e.g., Increased operational complexity to manage a PostgreSQL cluster.]
* [e.g., Requires updating all backend database adapters and writing migration scripts.]

## 5. Alternatives Considered

List the other options that were evaluated and briefly explain why they were rejected.

* **Alternative 1 (e.g., Redis):** Rejected because it doesn't offer the robust persistence guarantees required for long-term agent memory.
* **Alternative 2 (e.g., MongoDB):** Rejected because our existing data access layer is already heavily coupled to SQL paradigms, making the migration cost too high.

## 6. Implementation Notes / References

Provide links to relevant PRs, documentation, or technical spikes that relate to this decision.

* [Link to PR #123: Add PostgreSQL Ansible Role]
* [Link to `evaluation_scenario_template.md` benchmarking SQLite vs Postgres]
