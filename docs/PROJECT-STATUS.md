# Project Status

- Last updated: 2026-08-10
- Canonical branch after integration: `main`
- Current product stage: V1 product definition complete; Phase 4 UX prototyping in progress; backend/domain foundation ready to start in parallel
- Production application code: not started yet

## Read this first

Any human or AI agent continuing LifeOS should read, in this order:

1. [`README.md`](../README.md)
2. this file
3. the relevant file under [`docs/workstreams/`](workstreams/)
4. the architecture/product documents linked by that workstream
5. accepted ADRs under [`docs/decisions/`](decisions/)

Conversation history is useful context but is not the canonical project state when repository documentation exists.

## Completed / accepted foundations

- Product vision and V1 scope are defined.
- Core V1 concepts and user flows are documented, including Goal, Program, Project, Routine, Activity/Event, reminders, planned-versus-actual execution, confirmations, provenance, onboarding, learning, health/wellness boundaries and work/meeting lifecycle.
- Web direction: Next.js + React + TypeScript.
- Mobile direction: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic + SQLAlchemy + Alembic.
- PostgreSQL is the primary source of truth.
- Personal data architecture is accepted: typed relational core + flexible metadata/JSONB + graph-like personal relationship layer + provenance + audit/version history.
- AI is isolated behind a replaceable gateway and must use structured proposals validated by LifeOS domain services.
- External integrations are normalized through an Integration Hub/provider layer.
- V1 remains personal-first; collaboration/social capabilities are deferred.

## Active workstreams

### Phase 4 — Home / Today UX

- Status: **IN PROGRESS**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2
- Handoff: [`docs/workstreams/today-home.md`](workstreams/today-home.md)
- The detailed Phase 4 prototype documentation remains on its active branch until accepted and merged.

### Backend Foundation

- Status: **READY TO START**
- Intended branch: `feature/backend-foundation`
- Handoff: [`docs/workstreams/backend-foundation.md`](workstreams/backend-foundation.md)

### Core Domain Model

- Status: **READY TO START / may progress with backend foundation**
- Intended branch: `feature/domain-model` or a bounded slice inside `feature/backend-foundation`
- Handoff: [`docs/workstreams/domain-model.md`](workstreams/domain-model.md)

## Immediate next work

1. Continue Phase 4 UX independently on its prototype branch.
2. Consolidate accepted documentation and project-governance rules into `main`.
3. Start the backend foundation without waiting for final visual design.
4. Define Domain Model v0 and invariants before committing to the complete SQL schema.
5. Implement the first vertical slice only after the core domain model is coherent: Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation.
6. Add registers, assets, skills, requirements/capabilities and semantic relations incrementally rather than designing every specialist module upfront.
7. Replace Phase 4 mock data progressively with versioned backend APIs when both sides are ready.

## Important constraints — do not reopen casually

- `main` is the integrated source of truth; feature/fix/docs/prototype branches feed it through PRs.
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

## Historical branches

- `docs/project-foundation`: historical foundation branch; no unique work currently missing from `main`.
- `docs/v1-scope-and-flows`: contains the detailed V1 product-definition documents being consolidated into the canonical documentation baseline.
- `prototype/phase-4-today-home`: active Phase 4 exploratory implementation and documentation; remains separate until its work is accepted.

Historical branches and Git history are retained. Consolidation does not require deleting prior documentation or history.
