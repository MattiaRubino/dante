# DANTE Internal Changelog

This changelog records significant project-state and architecture milestones. It is not a replacement for Git history and is not intended to list every commit.

## 2026-08-23

### Frontend materialization and protected-main integration

- Closed frontend materialization FM-00..FM-07 at their stated direct-evidence scopes.
- Integrated the closed frontend materialization and bounded integration hardening into protected `main` through PR #28.
- Final PR head: `a6607ceabd35f874dc9e5f63fe8f57f71a92bf80`.
- Protected-main merge commit: `f1aacb0724088e0b4b086008a5219c2fba5ce0cf`.
- Verified the merge commit has exactly two parents: prior `main` `fd3bc8dd918cf6aadeff4572221af68612c3cb42` and PR head `a6607ceabd35f874dc9e5f63fe8f57f71a92bf80`.
- Verified the merged tree contains the exact accepted PR tree with no file delta between the PR head and merged `main` tree.
- PR exact-head Dependency Review, Backend CI and Frontend CI completed successfully, including `Backend CI Gate` and `Frontend CI Gate`.
- `Frontend CI Gate` calibration is complete. Its protected-main ruleset promotion remains classified **OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE** because direct ruleset readback is not exposed through the available connector.
- Push-main CI for the merge SHA is not classified PASS because the available connector exposes PR-associated workflow-run lookup only; direct push-run readback remains unavailable through this interface.
- The integration branch was observed absent after merge; no manual branch deletion was performed during the merge operation.
- Frontend integration is now **CLOSED / INTEGRATED**. Future capabilities remain trigger-activated rather than placeholder-installed.

## 2026-08-18

### Product naming

- Established **DANTE** as the current product/app name.
- `LifeOS` remains the previous working/project name in historical evidence, Git history and existing technical/repository identifiers where preserving chronology or compatibility matters.
- The rename is naming-only: Product North Star, Domain Model, Logical Model and Physical Model semantics remain unchanged.

## 2026-08-10

### Project governance and handoff

- Established `main` as the single integrated source of truth.
- Defined DEV/UAT/PROD as deployment environments rather than permanent Git branches.
- Added repository-first handoff rules for humans and AI agents.
- Added global `PROJECT-STATUS`, roadmap and per-workstream operational handoffs.
- Consolidated detailed V1 product-definition documents into the canonical documentation path without deleting historical documentation/history.

### Data, AI and integrations architecture

- Accepted the hybrid personal data model: typed relational core + metadata/JSONB + graph-like personal relationship layer + provenance + audit/version history.
- Confirmed shared-schema/workspace ownership rather than per-user tables/databases.
- Defined progressive formalization for unpredictable life domains.
- Defined Assets, Capabilities and Requirements as reusable planning concepts.
- Defined AI semantic ingestion: AI proposes structured entities/relations/actions; LifeOS validates and persists.
- Confirmed LifeOS owns canonical memory/state while AI remains provider-replaceable.
- Defined Context Builder and provider-neutral Tool API / MCP-compatible direction.
- Defined Integration Hub, provenance, deduplication and raw-versus-derived data principles.

### Active delivery

- Phase 4 Home/Today UX remains in progress on `prototype/phase-4-today-home` / PR #2.
- Backend Foundation and Domain Model v0 are ready to begin in parallel.

## Earlier foundation

Earlier product, architecture and UX decisions remain available in the existing repository documentation and Git history. This file intentionally does not duplicate every prior decision.