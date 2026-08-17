# LifeOS

LifeOS is an adaptive personal operating system for connecting intentions, plans, real time, actual reality, people/resources, evidence, history and adaptive future planning across web, Android and iOS.

## Current project state

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated into main via PR #10

LOGICAL MODEL
CLOSED — integrated into main via PR #11
Whole-Logical: PASS WITH HARDENING / REMOTE QA PASS
WD-03: PASS
WD-05: PASS

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
IN PROGRESS on chore/pre-physical-coherence
Phase 0–6 QA PASS
Coordinated Phase 7–9 architecture tranche NEXT

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED
```

Phase 4 Home/Today UX continues separately on `prototype/phase-4-today-home`.

For exact current state, read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md) and the active [`docs/workstreams/pre-physical-coherence.md`](docs/workstreams/pre-physical-coherence.md).

## How to resume work

Read in this order:

1. this README;
2. [`docs/README.md`](docs/README.md);
3. [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md);
4. [`docs/development/agent-operating-manual.md`](docs/development/agent-operating-manual.md);
5. [`docs/development/operating-rules.md`](docs/development/operating-rules.md);
6. [`docs/development/documentation-and-handoff.md`](docs/development/documentation-and-handoff.md);
7. [`docs/development/branching-and-environments.md`](docs/development/branching-and-environments.md);
8. the active workstream handoff;
9. the current model/architecture index and linked current sources;
10. relevant ADRs/evidence/methodologies;
11. relevant implementation/tests;
12. verify the current Git ref before writes.

Repository current truth outranks conversation memory and old/historical files. An active workstream branch may contain newer truth only inside its bounded scope.

## Documentation rule

LifeOS keeps current specifications clean:

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit supersession/qualification

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
= recoverable history
```

A stale current document may be replaced/deleted only after a knowledge-coverage check proves no meaningful requirement/rationale is lost.

A physical split is a tooling/layout concern, not separate authority: a canonical `*-part-N` chain must be read as one logical document. A split performed only because of size/tool limits is a **lossless physical partition of the complete logical payload**, never a summary, condensation or hidden semantic rewrite.

## Product direction

LifeOS is personal-first in V1 and is designed around whole-life orchestration rather than isolated feature silos.

Product/UI labels may include goals, programs/projects, activities, events, routines, reminders, measurements, people, resources, work, health, learning, travel and specialist contexts. These labels do not redefine the accepted Domain Atlas.

The product direction includes:

- adaptive Home/Today/time experience;
- intention → planning → execution/reality → evidence/history continuity;
- configurable scheduling/replanning and user confirmation;
- optional specialist capabilities without duplicating the common kernel;
- web, Android and iOS clients with equivalent capability and platform-adapted UX;
- AI-assisted interpretation/planning/recalibration behind replaceable provider/tool boundaries;
- integrations that preserve provider provenance and canonical-state boundaries;
- explainable/traceable significant changes;
- later multi-actor/collaboration capabilities without collapsing personal-first V1 semantics.

## Current technical direction — not implementation authorization

### Clients

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.

### Backend

- Python + FastAPI + Pydantic.
- Modular monolith first.
- SQLAlchemy + Alembic remain conditional implementation candidates depending on the accepted Physical persistence design.

### Physical persistence posture

No final Physical persistence is selected.

```text
PostgreSQL hybrid
CURRENT PREFERRED BASELINE — not final selection

TypeDB
MANDATORY CHALLENGER

Neo4j / property graph
SERIOUS SECONDARY / READ-PROJECTION CANDIDATE

event/document mechanisms
BOUNDED CANDIDATES

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

### Storage

Object/file storage remains behind a provider abstraction. Content Artifact identity is not the same thing as blob/path/URL/provider identity.

### AI / context / runtime

AI remains behind a replaceable/provider-neutral gateway and bounded Context Builder.

Current Phase 6 boundary keeps distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

AI output is classified as answer/explanation, candidate/unresolved interpretation, structured extraction, Proposal/proposal-like candidate, scenario/recommendation or governed-effect request as applicable. It does not become canonical truth/effect merely because a model produced it.

Runtime Agent/Principal is not Domain Actor automatically; tool invocation/protocol action is not authorization or the canonical governed operation. LifeOS does not use a generic second `AI memory` store as canonical truth.

### Integrations

Provider adapters preserve provenance and distinguish canonical LifeOS state from provider state, derived/read projections and unresolved/candidate state.

Current Integration Hub distinction:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider success/failure does not automatically determine canonical effect truth. MCP/A2A/future protocols remain adapters, not ontology/governance.

### Specialized infrastructure

Search/vector stores, caches, workflow engines, policy engines, graph/analytics/time-series systems and similar infrastructure are bounded candidates rather than defaults.

Specialized infrastructure requires demonstrated benefit from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

## Architecture/model sources of truth

Current architecture navigation starts at:

- [`docs/architecture/pre-physical-architecture-baseline.md`](docs/architecture/pre-physical-architecture-baseline.md)
- [`docs/architecture/requirements/README.md`](docs/architecture/requirements/README.md) and all four Phase 5 requirement packages
- [`docs/architecture/ai-context-runtime-boundaries.md`](docs/architecture/ai-context-runtime-boundaries.md)
- [`docs/architecture/integration-hub-boundaries.md`](docs/architecture/integration-hub-boundaries.md)
- [`docs/architecture/README.md`](docs/architecture/README.md)
- [`docs/architecture/system-overview.md`](docs/architecture/system-overview.md)
- [`docs/architecture/technical-decisions.md`](docs/architecture/technical-decisions.md)

Current semantic/model authority:

- [`docs/product/product-identity-and-north-star.md`](docs/product/product-identity-and-north-star.md)
- [`docs/domain/README.md`](docs/domain/README.md)
- [`docs/domain/language-map.md`](docs/domain/language-map.md)
- [`docs/logical-model/whole-logical-model-v1.md`](docs/logical-model/whole-logical-model-v1.md)
- [`docs/logical-model/decision-and-assumption-register-v1-part-9.md`](docs/logical-model/decision-and-assumption-register-v1-part-9.md)
- [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md)

Relevant ADRs include:

- [`ADR-002`](docs/decisions/ADR-002-backend.md) — backend platform direction, qualified at ORM/migration boundary;
- [`ADR-003`](docs/decisions/ADR-003-primary-database.md) — historical PostgreSQL selection rationale, superseded as final selection;
- [`ADR-004`](docs/decisions/ADR-004-storage.md) — storage abstraction;
- [`ADR-005`](docs/decisions/ADR-005-ai-gateway.md) — replaceable AI gateway, qualified by Phase 6 runtime boundaries;
- [`ADR-006`](docs/decisions/ADR-006-hybrid-personal-data-model.md) — superseded generic hybrid semantic model;
- [`ADR-007`](docs/decisions/ADR-007-domain-model-informed-persistence-boundaries.md) — current semantic persistence guardrail, qualified for Physical posture.

Historical Domain→Logical readiness files remain evidence and are explicitly separated from current architecture navigation in `docs/architecture/README.md`.

## Non-negotiable downstream constraints

The closed Logical Model activates `WL-H01..WL-H12`, including:

- justified material Agreement terms;
- governed operation/effect semantics;
- bounded projection/disclosure surfaces;
- absence/unknown not collapsing to false;
- expected-state consequential writes;
- idempotency distinct from identity;
- truthful multi-owner consistency;
- canonical/provider-state separation;
- derived-state freshness/material basis;
- retention/redaction/tombstone integrity;
- reconstructible consequential AuthZ provenance;
- non-interference/inference-leakage protection.

Phase 5 establishes current requirement packages for AuthN/AuthZ, security/privacy/retention/security-aware recovery, consistency/side effects and non-functional/multi-device/operational recovery. Open parameters recorded there remain explicit downstream obligations; they are not permission for implementation to pick arbitrary defaults.

Phase 6 establishes current AI/context/runtime and Integration Hub boundary contracts. Provider/model/agent/protocol/workflow mechanisms remain deferred and must not redefine these contracts.

Future Physical/API/runtime work must preserve these constraints rather than reinterpret semantics for implementation convenience.

## Git and environments

- `main` is the single integrated source of truth.
- Work happens on bounded `feature/*`, `fix/*`, `docs/*`, `chore/*` or `prototype/*` branches.
- Every remote write follows the exact PRE-SCOPE/write-gate/QA protocol.
- DEV/UAT/PROD are deployment environments, not permanent Git branches.

Significant work is not complete until relevant current documentation/handoff and remote QA are coherent.
