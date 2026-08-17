# Project Status

- Last updated: 2026-08-17
- Canonical branch: `main`
- Current product stage: accepted LifeOS Product Identity / North Star established; Core Domain Model closed and integrated into `main`; Logical Model closed on its completed integration branch; Physical Model not started; Phase 4 UX structural rebaseline remains a separate product/design workstream
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

- [`docs/product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) is the **Accepted current living definition of LifeOS product identity and North Star**. It defines what LifeOS is, its whole-life orchestration direction, capability boundaries and non-negotiable product principles without freezing final UX, autonomy, pricing, providers or release scope.
- Product vision and V1 scope are defined; older high-level vision wording remains useful context where it does not conflict with the accepted North Star.
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
- Core Domain Model / Domain Atlas is **CLOSED** and was integrated into `main` via PR #10. The final Whole-Domain state is `PASS WITH HARDENING / POST-WRITE QA PASS / CLOSED`, with the previously stage-bound WD-03 and WD-05 obligations discharged by the completed Logical Model validation.
- Logical Model is **CLOSED** on `feature/logical-model`. Whole-Logical is `PASS WITH HARDENING / REMOTE QA PASS`; WD-03 is `PASS`; WD-05 is `PASS`. The closure checkpoint is [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md). This branch-local closure becomes canonical repository truth when the completed Logical Model branch is integrated into `main` through the normal PR/coherence workflow.
- Physical Model is **NOT STARTED and NOT AUTHORIZED by Logical Model closure alone**. No SQL schema, migrations, API/backend implementation, AuthN/AuthZ runtime model, provider adapter implementation or concrete database adoption is implied by Logical Model closure.

## Active workstreams

### Phase 4 — Home / Today UX

- Status: **IN PROGRESS — structural frontend rebaseline is the next design step**
- Branch: `prototype/phase-4-today-home`
- Pull request: #2
- Handoff: [`docs/workstreams/today-home.md`](workstreams/today-home.md)
- The approved Home + Today visual/mechanical baseline remains preserved while the product structure is reassessed against the accepted Product Identity / North Star.
- The next question is no longer merely how to refine Calendar/Today, but what graphical/product structure correctly represents LifeOS as a whole-life operating system.

### Backend Foundation

- Status: **READY TO START, BUT NOT STARTED**
- Intended branch: `feature/backend-foundation`
- Handoff: [`docs/workstreams/backend-foundation.md`](workstreams/backend-foundation.md)
- No backend implementation is authorized merely by Domain or Logical Model closure; sequencing must remain consistent with the next explicitly approved architecture/model phase and the repository cleanup/audit described below.

### Logical Model integration

- Status: **MODEL CLOSED — repository integration is the remaining step**
- Branch: `feature/logical-model`
- Whole-Logical closure: [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md)
- Final workstream continuation: [`docs/workstreams/logical-model-part-9.md`](workstreams/logical-model-part-9.md)
- Integration scope is documentation/model integration only. It must not be used to start the Physical Model, SQL, migrations, API/backend, AuthN/AuthZ runtime, provider adapters or frontend implementation.

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

1. Integrate the completed and remotely QA-verified Logical Model from `feature/logical-model` into `main` through the normal PR and coherence gate, without semantic refactoring or starting a later architecture phase.
2. On the resulting integrated `main`, perform a deliberate general repository/project cleanup and coherence audit before advancing the backend/model architecture. This cleanup may assess stale global documentation, branch/workstream status, duplicated or historical material, sequencing, repository hygiene and any other explicitly approved maintenance, but must preserve accepted semantic history and canonical split-document rules.
3. Only after that cleanup/audit, decide whether to authorize and start a separate **Physical Model** workstream with its own branch, PRE-SCOPE, write gate, validation criteria and technology benchmark/selection boundary. Logical Model closure does not itself authorize Physical Model implementation.
4. Continue the accepted Product Identity / North Star based **structural frontend rebaseline** independently, preserving the approved Home + Today prototype baseline and avoiding redesign by accumulation of badges, controls or isolated modules.
5. Do not start SQL schema/migrations, API/backend implementation, AuthN/AuthZ runtime design, provider adapters or concrete Physical Model implementation as an implicit continuation of the closed Logical Model.
6. Treat product simulations and multi-actor research as evidence rather than automatic implementation commitments.

## Repository coherence baseline

A repository/branch coherence audit was performed on 2026-08-10 after documentation consolidation.

At that point:

- `docs/project-foundation` had no commits ahead of `main` and was historical;
- `docs/v1-scope-and-flows` had no commits ahead of `main`; its accepted V1 documents were already integrated;
- the completed project-governance helper branches had no unique commits ahead of `main`;
- `prototype/phase-4-today-home` was synchronized with the accepted `main` baseline and intentionally ahead only for Phase 4 UX/prototype/test work;
- the Phase 4 diff did not contain older competing copies of the accepted DB/AI architecture.

This is a dated baseline, not a permanent assumption. The completed Core Domain Model was later integrated into `main` via PR #10, and the Logical Model was subsequently completed on `feature/logical-model`. Before the Logical Model merge and again during the planned post-merge cleanup, re-check Git using the coherence gate in [`development/operating-rules.md`](development/operating-rules.md).

## Important constraints — do not reopen casually

- `main` is the integrated source of truth; feature/fix/docs/prototype branches feed it through PRs.
- Current accepted `main` takes precedence over historical branches and conversation memory.
- A branch is authoritative only for its scoped unmerged work; it does not override unrelated accepted decisions.
- The accepted Product Identity / North Star is a **living definition**: it guides current product work but may be deliberately revised, documented and versioned when stronger evidence or product understanding justifies change.
- DEV, UAT and PROD are environments, not permanent Git branches.
- Do not create per-user database tables or databases.
- Do not turn the entire product into arbitrary JSON or one universal graph table.
- AI never writes SQL directly, changes physical schema, or bypasses backend validation.
- Time passing does not mean completion.
- Planned state and actual outcome remain distinct.
- The past is not silently rewritten; important future changes are versioned/auditable.
- Do not introduce specialized databases, caches or orchestration systems before measured need.
- Logical Model closure does not authorize the Physical Model or any implementation layer automatically.
- Physical Model work, if approved later, is a separate phase and must receive a separate explicit gate.

## Documentation rule

A work item is not considered complete when only code or design is updated. The relevant workstream handoff and durable documentation must also be updated in the same PR. Significant architectural decisions require an ADR.

Incremental progress normally updates the workstream handoff, not this global status file. Update `PROJECT-STATUS.md` when global project truth changes.

## Historical / active branches

- `docs/project-foundation`: historical foundation branch; no unique accepted work missing from `main` at the last coherence audit.
- `docs/v1-scope-and-flows`: historical source branch whose detailed V1 product-definition documents are integrated into `main`.
- completed `docs/project-governance*` helper branches: historical/obsolete after consolidation; no unique accepted work ahead of `main` at the last audit.
- `prototype/phase-4-today-home`: active Phase 4 exploratory implementation and documentation; remains separate until its work is accepted.
- `feature/domain-model`: completed historical integration branch; its accepted Core Domain Model / Domain Atlas was integrated into `main` via PR #10 and `main` is authoritative for that integrated state.
- `feature/logical-model`: completed Logical Model branch awaiting normal integration into `main`; its closed branch-local Logical Model is authoritative for that scoped unmerged work until integration.
- `docs/multi-actor-discovery`: historical evidence branch after PR #6 merge; its accepted evidence is now integrated into `main` and `main` is authoritative.

Historical branches and Git history are retained. Consolidation does not require deleting prior documentation or history.
