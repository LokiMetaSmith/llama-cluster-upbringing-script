# Follow-up: Local Implementation of Lazy-Hydrating Git Clones

## Context
During the evaluation of Cloudflare Artifacts (`docs/CLOUDFLARE_ARTIFACTS_EVALUATION.md`), it was determined that while the managed service is not suitable for our offline-first architecture, the concept of **ArtifactFS** (lazy-hydrating, blobless Git clones) is highly valuable for reducing agent sandbox startup times.

## Task Description
Investigate the feasibility of implementing a local, self-hosted equivalent to ArtifactFS for the Pipecat cluster.

### Objectives
1. Research existing open-source tools for lazy Git hydration (e.g., `git-vfs`, `Scalar`, or custom FUSE filesystems).
2. Evaluate integration with the existing self-hosted Forgejo instance.
3. Prototype a lightweight daemon that can perform blobless clones and hydrate file contents on-demand when accessed by an agent inside a Nomad sandbox.

### Acceptance Criteria
- A technical design document outlining how to achieve fast, lazy Git clones locally.
- A proof-of-concept script or service demonstrating the functionality against a local Forgejo repository.
