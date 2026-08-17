# LifeOS

LifeOS is an adaptive personal operating system for connecting intentions, plans, real time, actual reality, people/resources, evidence, history and adaptive future planning across web, Android and iOS.

## Project status

The product foundation, Core Domain Model / Domain Atlas and Logical Model are closed at their current stages. The repository is now in a deliberate **Pre-Physical Repository & Architecture Coherence** workstream before any Physical Model or production backend implementation is authorized.

Current tracks:

- **Phase 4 Home/Today UX prototype:** in progress on `prototype/phase-4-today-home`; this remains a separate product/design workstream.
- **Pre-Physical Repository & Architecture Coherence:** in progress on `chore/pre-physical-coherence`; this is the current backend/architecture preparation workstream.
- **Core Domain Model / Domain Atlas:** **CLOSED**, integrated into `main` via PR #10.
- **Logical Model:** **CLOSED**, integrated into `main` via PR #11; Whole-Logical is `PASS WITH HARDENING / REMOTE QA PASS`, with WD-03 and WD-05 discharged.
- **Physical Model:** **NOT STARTED / NOT AUTHORIZED** by Logical closure alone.
- **Backend production implementation:** **NOT STARTED**.

No production application code has been committed yet.

For the exact current state, always read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md) and the active [`docs/workstreams/pre-physical-coherence.md`](docs/workstreams/pre-physical-coherence.md) handoff.

## How to resume work

Any human or AI agent continuing the project should read, in order:

1. this README;
2. [`docs/README.md`](docs/README.md);
3. [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md);
4. [`docs/development/agent-operating-manual.md`](docs/development/agent-operating-manual.md);
5. [`docs/development/operating-rules.md`](docs/development/operating-rules.md);
6. [`docs/development/documentation-and-handoff.md`](docs/development/documentation-and-handoff.md);
7. [`docs/development/branching-and-environments.md`](docs/development/branching-and-environments.md);
8. the relevant [`docs/workstreams/`](docs/workstreams/) handoff;
9. the product/domain/logical/architecture/ADR sources linked by that handoff;
10. relevant current code/tests before changing implementation.

Repository documentation on current `main` is the canonical integrated project memory when chat history or old branches are incomplete, stale or contradictory. An active workstream branch may contain newer unmerged work only inside that workstream's bounded scope.

## Product direction

LifeOS is personal-first in V1 and is designed around whole-life orchestration rather than a collection of isolated feature silos. Product/UI concepts may include goals, plans/programs/projects, activities, events, routines, reminders, measurements, people, resources, work, health, learning, travel and other specialist contexts, but current kernel terminology and semantic ownership are defined by the accepted Domain Atlas rather than by older product labels.

The product direction includes:

- a central adaptive Home/Today/time experience;
- intention → planning → execution/reality → evidence/history continuity;
- configurable scheduling, replanning and user confirmation;
- optional specialist capabilities without duplicating the common LifeOS foundation;
- web, Android and iOS clients with equivalent capability and platform-adapted UX;
- AI-assisted interpretation, planning and recalibration behind replaceable provider/tool interfaces;
- integrations with external apps, device data and services while preserving provider provenance and canonical-state boundaries;
- explainable, traceable and reversible significant changes;
- later multi-actor/collaboration capabilities without collapsing personal-first V1 semantics.

## Current technical direction — not implementation authorization

The following are current architectural directions or benchmark baselines. They do **not** authorize Physical Model, schema, API or backend implementation by themselves.

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend toolchain direction: Python + FastAPI + Pydantic; SQLAlchemy + Alembic remain conditional on the accepted Physical persistence design.
- Architecture: modular monolith first; extract specialized infrastructure only when it demonstrates material benefit in correctness, durability, security, evolvability, operational reliability, workload or migration risk.
- Physical persistence posture: PostgreSQL hybrid is the **current preferred baseline entering the future Physical benchmark**, not a final Physical selection.
- Mandatory Physical challenger: TypeDB.
- Neo4j/property graph, event-stream/event-store and document-store mechanisms remain bounded secondary candidates where justified; they are not accepted universal canonical ontologies.
- Generic EAV / generic-edge / universal meta-model design is rejected for the canonical kernel.
- File/object storage: provider-neutral boundary; S3-compatible/cloud providers may replace local development storage later.
- AI: replaceable gateway + bounded Context Builder + structured proposals + governed/validated effects; AI does not become canonical truth merely by producing an output.
- Integrations: provider adapters must preserve provenance and the distinction between canonical LifeOS state, provider state, derived/read state and unresolved/candidate state.
- Search/vector, caches, durable workflow engines and policy engines are benchmark/deferred infrastructure choices rather than implied defaults.
- Repository: **public monorepo**; `main` remains the single integrated source of accepted truth.

## Architecture and model sources of truth

Before any detailed persistence, API, AI-runtime, integration or backend implementation work, read the sources in this order of relevance:

- [`docs/product/product-identity-and-north-star.md`](docs/product/product-identity-and-north-star.md) — accepted product identity/North Star;
- [`docs/domain/README.md`](docs/domain/README.md) and [`docs/domain/language-map.md`](docs/domain/language-map.md) — accepted Core Domain Model / Domain Atlas;
- [`docs/logical-model/whole-logical-model-v1.md`](docs/logical-model/whole-logical-model-v1.md) — integrated Whole Logical Model;
- [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md) — canonical Logical closure checkpoint;
- [`docs/logical-model/decision-and-assumption-register-v1-part-9.md`](docs/logical-model/decision-and-assumption-register-v1-part-9.md) — final Whole-Logical decisions, hardenings and deferred Physical/runtime obligations;
- [`docs/decisions/ADR-007-domain-first-physical-modeling.md`](docs/decisions/ADR-007-domain-first-physical-modeling.md) — domain-first architecture correction/boundary;
- [`docs/workstreams/pre-physical-coherence.md`](docs/workstreams/pre-physical-coherence.md) — current bounded coherence workstream and unified pre-Physical roadmap.

Earlier architecture documents and ADRs remain important historical evidence but may be partially qualified or superseded by later Domain/Logical decisions. The active Pre-Physical Coherence workstream will make those relationships explicit before Physical Model authorization.

## Non-negotiable downstream model constraints

The closed Logical Model activates `WL-H01..WL-H12`, including governed effects, selective disclosure, unknown/absence semantics, expected-state concurrency, idempotency separation, truthful multi-owner consistency, provider/canonical separation, derived-state freshness, retention/tombstone integrity, AuthZ provenance and non-interference/inference-leakage pressure.

A future Physical/API/runtime design must preserve those constraints rather than reinterpret semantic ownership for implementation convenience.

## Git and environments

- `main` is the single integrated source of truth.
- Work happens on bounded `feature/*`, `fix/*`, `docs/*`, `chore/*` or `prototype/*` branches and returns through PRs.
- New production work starts from current `main` unless its active workstream handoff explicitly names another branch.
- Before merge, compare against current `main` and check semantic/documentation coherence, not only Git conflicts.
- DEV, UAT and PROD are deployment environments, not permanent Git branches.

See [`docs/development/agent-operating-manual.md`](docs/development/agent-operating-manual.md), [`docs/development/operating-rules.md`](docs/development/operating-rules.md) and [`docs/development/branching-and-environments.md`](docs/development/branching-and-environments.md).

## Documentation

Start from [`docs/README.md`](docs/README.md). Significant work is not considered complete until its relevant handoff and durable documentation are updated and remotely verified.