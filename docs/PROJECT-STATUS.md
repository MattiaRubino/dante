# Project Status

- Last updated: 2026-08-11
- Canonical branch: `main`
- Current product stage: V1 product definition complete; Phase 4 UX prototyping in progress; backend/domain foundation ready to start in parallel; multi-actor discovery/research evidence integrated into `main`
- Production application code: not started yet
- Documentation/governance consolidation: **COMPLETE on `main`**

## Read this first

Any human or AI agent continuing LifeOS should read, in this order:

1. [`README.md`](../README.md)
2. this file
3. [`docs/development/operating-rules.md`](development/operating-rules.md)
4. the relevant file under [`docs/workstreams/`](workstreams/)
5. the architecture/product documents linked by that workstream
6. accepted ADRs under [`docs/decisions/`](decisions/)
7. relevant current code/tests before editing implementation

Conversation history is useful context but is not the canonical project state when repository documentation exists.

## Completed / accepted foundations

- Product vision and V1 scope are defined.
- Detailed V1 product-definition documents are integrated into `main`.
- Core V1 concepts and user flows are documented, including Goal, Program, Project, Routine, Activity/Event, reminders, planned-versus-actual execution, confirmations, provenance, onboarding, learning, health/wellness boundaries and work/meeting lifecycle.
- Web direction: Next.js + React + TypeScript.
- Mobile direction: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic + SQLAlchemy + Alembic.
- PostgreSQL is the primary source of truth.
- Personal data architecture is accepted: typed relational core + flexible metadata/JSONB + graph-like personal relationship layer + provenance + audit/version history.
- AI is isolated behind a replaceable gateway and must use structured proposals validated by LifeOS domain services.
- External integrations are normalized through an Integration Hub/provider layer.
- `main` is the single integrated project source of truth.
- DEV, UAT and PROD are deployment environments rather than permanent Git branches.
- Repository-first human/AI handoff, source-precedence and parallel-work rules are established.
- V1 remains personal-first; collaboration/social capabilities are deferred.
- Multi-actor/collaboration discovery evidence is integrated into `main`: a dedicated simulation plus one consolidated external Deep Research document with semantic and bibliographic QC. This evidence does not itself change V1 scope, the domain model or architecture.

## Active workstreams

### Phase 4 — Home / Today UX

- Status: **IN PROGRESS**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2
- Handoff: [`docs/workstreams/today-home.md`](workstreams/today-home.md)
- Detailed Phase 4 prototype documentation remains on its active branch until accepted and merged.
- Branch-local `docs/phase-4/frontend-master.md` is the exact operational source for the latest Phase 4 iteration.

### Backend Foundation

- Status: **READY TO START**
- Intended branch: `feature/backend-foundation`
- Handoff: [`docs/workstreams/backend-foundation.md`](workstreams/backend-foundation.md)

### Core Domain Model

- Status: **READY TO START / may progress with backend foundation**
- Preferred initial execution: bounded slice inside `feature/backend-foundation` if both tracks would otherwise edit the same core files
- Handoff: [`docs/workstreams/domain-model.md`](workstreams/domain-model.md)

## Completed evidence workstreams

### Multi-Actor / Collaboration Discovery

- Status: **COMPLETE — integrated into `main` via PR #6**
- Historical work branch: `docs/multi-actor-discovery`
- Pull request: #6 — merged
- Handoff: [`docs/workstreams/multi-actor-discovery.md`](workstreams/multi-actor-discovery.md)
- Simulation: [`docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`](product/multi-actor-collaboration-discovery-simulation-2026-08.md)
- Consolidated research: [`docs/product/multi-actor-collaboration-research-2026-08.md`](product/multi-actor-collaboration-research-2026-08.md)
- Generic evidence acquisition is closed. Any later evidence synthesis or Multi-Actor Readiness pass must be started deliberately as a separate workstream.

## Immediate next work

1. Continue Phase 4 UX independently on its prototype branch.
2. Start the backend foundation from current `main` without waiting for final visual design.
3. Define Domain Model v0 and invariants before committing to the complete SQL schema.
4. Implement the first vertical slice only after the core domain model is coherent: Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation.
5. Add registers, assets, skills, requirements/capabilities and semantic relations incrementally rather than designing every specialist module upfront.
6. Replace Phase 4 mock data progressively with versioned backend APIs when both sides are ready.
7. Treat the integrated multi-actor simulation/research as evidence only. If the project intentionally chooses to act on it, start a separate evidence-synthesis / Multi-Actor Readiness workstream rather than continuing generic research or promoting research vocabulary directly into binding domain decisions.

## Repository coherence baseline

A repository/branch coherence audit was performed on 2026-08-10 after documentation consolidation.

At that point:

- `docs/project-foundation` had no commits ahead of `main` and was historical;
- `docs/v1-scope-and-flows` had no commits ahead of `main`; its accepted V1 documents were already integrated;
- the completed project-governance helper branches had no unique commits ahead of `main`;
- `prototype/phase-4-today-home` was synchronized with the accepted `main` baseline and intentionally ahead only for Phase 4 UX/prototype/test work;
- the Phase 4 diff did not contain older competing copies of the accepted DB/AI architecture.

This is a dated baseline, not a permanent assumption. Before future merges or handoffs, re-check Git using the coherence gate in [`development/operating-rules.md`](development/operating-rules.md).

## Important constraints — do not reopen casually

- `main` is the integrated source of truth; feature/fix/docs/prototype branches feed it through PRs.
- Current accepted `main` takes precedence over historical branches and conversation memory.
- A branch is authoritative only for its scoped unmerged work; it does not override unrelated accepted decisions.
- DEV, UAT and PROD are environments, not permanent Git branches.
- Do not create per-user database tables or databases.
- Do not turn the entire product into arbitrary JSON or one universal graph table.
- AI never writes SQL directly, changes physical schema, or bypasses backend validation.
- Time passing does not mean completion.
- Planned state and actual outcome remain distinct.
- The past is not silently rewritten; important future changes are versioned/auditable.
- Do not introduce specialized databases, caches or orchestration systems before measured need.

## Documentation rule

A work item is not considered complete when only code or design is updated. The relevant workstream handoff and durable documentation must also be updated in the same PR. Significant architectural decisions require an ADR.

Incremental progress normally updates the workstream handoff, not this global status file. Update `PROJECT-STATUS.md` when global project truth changes.

## Historical / active branches

- `docs/project-foundation`: historical foundation branch; no unique accepted work missing from `main` at the last coherence audit.
- `docs/v1-scope-and-flows`: historical source branch whose detailed V1 product-definition documents are integrated into `main`.
- completed `docs/project-governance*` helper branches: historical/obsolete after consolidation; no unique accepted work ahead of `main` at the last audit.
- `prototype/phase-4-today-home`: active Phase 4 exploratory implementation and documentation; remains separate until its work is accepted.
- `docs/multi-actor-discovery`: historical evidence branch after PR #6 merge; its accepted evidence is now integrated into `main` and `main` is authoritative.

Historical branches and Git history are retained. Consolidation did not delete prior documentation or history.
