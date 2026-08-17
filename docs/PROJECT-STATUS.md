# Project Status

- Last updated: 2026-08-17
- Canonical integrated branch: `main`
- Current accepted main baseline for this workstream: `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Current backend/architecture preparation workstream: **Pre-Physical Repository & Architecture Coherence** on `chore/pre-physical-coherence`
- Current product stage: accepted LifeOS Product Identity / North Star established; Core Domain Model and Logical Model are closed and integrated into `main`; Pre-Physical coherence is in progress; Physical Model is not started; Phase 4 UX remains a separate product/design workstream
- Production application code: **NOT STARTED**

## Read this first

Any human or AI agent continuing LifeOS should read, in this order:

1. [`README.md`](../README.md)
2. [`docs/README.md`](README.md)
3. this file
4. [`docs/development/agent-operating-manual.md`](development/agent-operating-manual.md)
5. [`docs/development/operating-rules.md`](development/operating-rules.md)
6. [`docs/development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
7. [`docs/development/branching-and-environments.md`](development/branching-and-environments.md)
8. the relevant file under [`docs/workstreams/`](workstreams/)
9. linked accepted product/domain/logical/architecture documents and ADRs
10. relevant current code/tests before editing implementation

Conversation history is useful context but is not the canonical project state when repository documentation exists. An active workstream branch can contain newer unmerged truth only inside that bounded workstream.

## Completed / accepted foundations

- [`docs/product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) is the **Accepted current living definition of LifeOS product identity and North Star**.
- Product vision and detailed V1 product-definition documents are integrated into `main`; older terminology remains evidence where it does not conflict with later accepted Domain semantics.
- Web direction: Next.js + React + TypeScript.
- Mobile direction: Expo + React Native + TypeScript.
- Backend toolchain direction: Python + FastAPI + Pydantic; SQLAlchemy + Alembic remain conditional on the accepted Physical persistence design.
- Modular monolith remains the default architecture direction. Specialized infrastructure requires demonstrated benefit from measured workload or a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.
- AI remains isolated behind replaceable/provider-neutral boundaries and must use structured proposals / governed effects rather than becoming canonical truth directly.
- External integrations remain provider-bounded and must preserve provenance plus the distinction between provider state and canonical LifeOS state.
- `main` is the single integrated project source of truth.
- DEV, UAT and PROD are deployment environments rather than permanent Git branches.
- Repository-first human/AI handoff, source-precedence, preservation and exact write-gate rules are established.
- Repository visibility is **public**.
- V1 remains personal-first; collaboration/social capabilities are deferred while multi-actor semantics have been pressure-tested in the Domain/Logical work.
- Core Domain Model / Domain Atlas is **CLOSED** and integrated into `main` via PR #10. Final Whole-Domain state: `PASS WITH HARDENING / POST-WRITE QA PASS / CLOSED`.
- Logical Model is **CLOSED** and integrated into `main` via PR #11. Whole-Logical is `PASS WITH HARDENING / REMOTE QA PASS`; WD-03 is `PASS`; WD-05 is `PASS`.
- The canonical Logical closure checkpoint is [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md).
- The closed Logical Model preserves the accepted Domain owner set and activates `WL-H01..WL-H12` without selecting physical persistence/API/runtime mechanisms.
- Current Physical technology posture is **benchmark posture, not selection**: PostgreSQL hybrid is the current preferred baseline; TypeDB is a mandatory challenger; graph/event/document mechanisms remain bounded secondary candidates; generic EAV/generic-edge/universal meta-model design remains rejected for the canonical kernel.
- Physical Model is **NOT STARTED and NOT AUTHORIZED by Logical Model closure alone**.

## Active workstreams

### Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 0 + Phase 1**
- Branch: `chore/pre-physical-coherence`
- Base / approved Phase-1 PRE-SCOPE: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Handoff: [`docs/workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md)
- Purpose: align repository current truth, clarify supersession, define pre-Physical technical requirements/benchmark inputs and close with clean-room coherence QA before any Physical Model authorization.
- Domain and Logical semantics remain closed unless a separate explicit material reopen is justified.
- No Physical, SQL/schema/migration/API/backend/Auth-provider/provider-adapter implementation is authorized by this workstream implicitly.

### Phase 4 — Home / Today UX

- Status: **IN PROGRESS — separate product/design workstream**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2
- Handoff: [`docs/workstreams/today-home.md`](workstreams/today-home.md)
- The approved Home + Today visual/mechanical baseline remains preserved while product structure is reassessed against the accepted Product Identity / North Star.
- This workstream does not override backend/domain/logical architecture.

## Deferred production workstreams

### Backend Foundation

- Status: **NOT STARTED — DEFERRED pending Pre-Physical coherence and later accepted Physical/runtime prerequisites**
- Historical/intended branch name: `feature/backend-foundation`
- Existing handoff: [`docs/workstreams/backend-foundation.md`](workstreams/backend-foundation.md)
- The existing handoff is known to contain pre-Domain/Logical assumptions and is scheduled for cleanup in a later bounded Pre-Physical phase. Do not execute its old Domain/persistence instructions as current truth.
- Backend Foundation must eventually consume the closed Domain + Logical Models, a separately accepted Physical Model and current runtime/security/integration contracts.

### Physical Model

- Status: **NOT STARTED / NOT AUTHORIZED**
- It may only begin after Pre-Physical Coherence closes and the user explicitly approves a separate branch/PRE-SCOPE/write gate/benchmark and validation boundary.

## Completed evidence/model workstreams

### Core Domain Model / Domain Atlas

- Status: **CLOSED — integrated through PR #10**
- Historical branch: `feature/domain-model`
- `main` is authoritative for the accepted integrated state.

### Logical Model

- Status: **CLOSED — integrated through PR #11**
- Historical branch: `feature/logical-model`
- `main` is authoritative for the accepted integrated state.

### Multi-Actor / Collaboration Discovery

- Status: **COMPLETE — integrated into `main` via PR #6**
- Historical work branch: `docs/multi-actor-discovery`
- Handoff: [`docs/workstreams/multi-actor-discovery.md`](workstreams/multi-actor-discovery.md)
- Simulation: [`docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`](product/multi-actor-collaboration-discovery-simulation-2026-08.md)
- Consolidated research: [`docs/product/multi-actor-collaboration-research-2026-08.md`](product/multi-actor-collaboration-research-2026-08.md)
- Evidence does not automatically change current Domain/Logical architecture.

## Immediate next work

1. Complete and remotely QA **Phase 0 + Phase 1** of [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md).
2. Then perform a **read-only Phase 2 architecture supersession inventory** before proposing any new write gate for old architecture/ADR material.
3. Continue the unified Pre-Physical roadmap in bounded gates: architecture supersession → Backend Foundation handoff cleanup → current Pre-Physical Architecture Baseline → requirements/benchmark preparation → full clean-room QA.
4. Do not start a Physical Model merely because the cleanup is progressing; Physical authorization remains a separate final user gate.
5. Continue Phase 4 UX independently without allowing prototype decisions to redefine accepted backend/domain/logical truth.

## Pre-Physical sequence summary

The detailed sequence is maintained in the active handoff. Broadly:

```text
current-truth documentation
→ architecture supersession cleanup
→ Backend Foundation handoff cleanup
→ current Pre-Physical Architecture Baseline
→ AuthN/AuthZ + security/privacy + consistency + non-functional requirements
→ AI/runtime/integration boundaries
→ durable async + governed API + search/observability/calendar/solver pressure
→ Physical benchmark specification
→ repository engineering safety
→ clean-room coherence QA
→ separate Physical Model authorization decision
```

## Repository coherence baseline

The previous broad repository/branch coherence audit was performed on 2026-08-10 and is now historical evidence rather than a permanent assumption.

Since that audit:

- Core Domain Model was completed and integrated into `main` via PR #10;
- Logical Model was completed and integrated into `main` via PR #11;
- `docs/PROJECT-STATUS.md` was aligned after integration via PR #12;
- current `main` baseline entering Pre-Physical Coherence is `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`;
- the Pre-Physical workstream must establish a fresh coherence baseline before any Physical/backend architecture advancement.

## Important constraints — do not reopen casually

- `main` is the integrated source of truth; bounded feature/fix/docs/chore/prototype branches feed it through PRs.
- Current accepted `main` takes precedence over historical branches and conversation memory.
- A branch is authoritative only for its scoped unmerged work.
- The accepted Product Identity / North Star is a living product definition, not permission to silently rewrite Domain semantics.
- Domain Model and Logical Model remain **CLOSED** unless material new evidence triggers a separately documented reopen.
- DEV, UAT and PROD are environments, not permanent Git branches.
- Do not create per-user database tables or databases.
- Do not turn the product into arbitrary JSON, generic EAV or one universal graph/relationship table.
- Technical registry/edge convenience does not create a universal semantic Entity/Relationship owner.
- AI never writes SQL directly, changes physical schema, bypasses governed validation or becomes accepted canonical truth by output alone.
- Time passing does not mean completion.
- Planned state and actual outcome remain distinct.
- The past is not silently rewritten; corrections/version/history remain auditable.
- Provider state is not automatically canonical LifeOS truth.
- Derived/read/search state is not automatically canonical truth and consequential use must respect freshness/disclosure requirements.
- Specialized infrastructure requires demonstrated benefit; production measurements are one valid form of evidence but not the only one.
- Logical Model closure does not authorize Physical Model, SQL/migrations, APIs, Auth runtime, provider adapters or backend implementation.

## Documentation rule

A work item is not complete when only code or design is updated. Relevant workstream handoff and durable documentation must also be updated in the same PR. Significant architectural decisions require ADR/current-baseline treatment as appropriate.

Incremental progress normally updates the workstream handoff, not this global status file. Update `PROJECT-STATUS.md` only when global project truth changes.

## Historical / active branches

- `chore/pre-physical-coherence`: active bounded Pre-Physical coherence workstream; unmerged branch truth applies only to this scope.
- `prototype/phase-4-today-home`: active separate Phase 4 exploratory workstream.
- `feature/domain-model`: completed historical integration branch; accepted Domain Atlas is integrated into `main` via PR #10.
- `feature/logical-model`: completed historical integration branch; accepted Logical Model is integrated into `main` via PR #11.
- `docs/multi-actor-discovery`: historical evidence branch after PR #6 merge.
- `docs/project-foundation`, `docs/v1-scope-and-flows` and completed project-governance helper branches: historical sources after their accepted work was integrated.

Historical branches and Git history are retained. Cleanup does not mean deleting prior reasoning or pretending later decisions existed earlier.