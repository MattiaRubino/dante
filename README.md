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
Phase 0–9 QA PASS
Phase 10 Physical benchmark method package CURRENT / content QA PASS
Phase 11 repository engineering safety NEXT after Phase 10 closure

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED
```

Phase 4 Home/Today UX continues separately on `prototype/phase-4-today-home`.

For exact current state and closure status, read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md) and the active [`docs/workstreams/pre-physical-coherence.md`](docs/workstreams/pre-physical-coherence.md).

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
PRIMARY CANONICAL PERSISTENCE
PostgreSQL hybrid
CURRENT PREFERRED BASELINE — NOT SELECTED

TypeDB
MANDATORY CHALLENGER — NOT SELECTED

SECONDARY GRAPH / TRAVERSAL
no-specialized-store baseline
vs Neo4j/property graph

SEARCH / SEMANTIC RETRIEVAL
structured + lexical/full-text baseline
vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first
specialized candidate only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

### Phase 10 benchmark method

Phase 10 has created the current method package:

- [`docs/architecture/physical-benchmark-specification.md`](docs/architecture/physical-benchmark-specification.md);
- [`docs/architecture/physical-benchmark-scenario-corpus.md`](docs/architecture/physical-benchmark-scenario-corpus.md);
- [`docs/architecture/physical-benchmark-register.md`](docs/architecture/physical-benchmark-register.md).

It decides **how** the later separately authorized Physical Model must be compared; it does not select a winner or design Physical schemas.

Primary candidates must pass non-compensable semantic/correctness hard gates before weighted scoring. The common corpus covers consequential concurrency, multi-owner consistency, deep history, governance/disclosure, provider divergence, deletion + restore, recurrence/DST, search/vector filtering, solver freshness, recovery and schema evolution.

LOW/BASE/HIGH values are synthetic qualification tiers, not business forecasts. Open RPO/RTO/latency/availability/scale values remain sensitivity inputs until accepted targets exist.

Every future benchmark subject is pinned to exact product + version + edition/license + deployment mode. `PREFERRED != SELECTED`.

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

### Governed operations / effects

Consequential requests use the current engine-/transport-neutral [`docs/architecture/governed-operation-effect-contract.md`](docs/architecture/governed-operation-effect-contract.md).

```text
route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation/effect meaning
```

Where material, the contract keeps semantic target/effect, expected state, purpose/context, Principal/Actor/represented party, governance, confirmation/autonomy, idempotency/correlation, execution class and independent canonical/provider/runtime/conflict/reconciliation result semantics.

```text
request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

Concrete routes/DTOs/API style remain later decisions.

### Durable execution

LifeOS distinguishes bounded asynchronous work from material long-running durable coordination.

```text
BOUNDED ASYNC
DB + worker/outbox style remains a valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

Dedicated durable execution is structurally justified for operation classes involving material long waits, human review, provider callbacks, crash-resume, cancellation/timeouts, compensation or reconciliation. No runtime is implemented or selected by this posture.

### Search / retrieval

Current posture:

```text
structured filters + lexical/full-text search
BASELINE

semantic/vector retrieval
BOUNDED CANDIDATE

pgvector
BOUNDED CANDIDATE IF POSTGRESQL SURVIVES PHYSICAL SELECTION

dedicated search/vector service
NOT JUSTIFIED BY DEFAULT
```

Search/index/ranking/vector state remains derived. Search miss does not prove canonical nonexistence; vector similarity does not establish semantic truth.

### Observability

OpenTelemetry-first or equivalent standards-based instrumentation is the current direction; no telemetry vendor is selected.

Telemetry IDs/state remain technical and do not replace Domain Provenance, security audit or required material effect history.

### Calendar interoperability

iCalendar, JSCalendar and provider calendar APIs are interoperability/adapter pressure, not LifeOS ontology. Provider recurrence IDs, sync tokens and revisions do not become LifeOS native/material identity automatically.

### Solver

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE — NOT implemented

AI
interpretation / ambiguity / explanation / cross-domain reasoning
NOT deterministic constraint authority
```

Solver output remains candidate/scenario state and reaches accepted Schedule/Plan/etc state only through the governed-operation/effect contract. `UNKNOWN != INFEASIBLE`.

### Specialized infrastructure

Search/vector stores, caches, workflow engines, policy engines, graph/analytics/time-series systems, solver runtimes and similar infrastructure are bounded candidates rather than defaults.

Specialized infrastructure requires demonstrated benefit from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

Phase 10 additionally requires specialized candidates to compete against a role-specific no-specialized/native baseline and records the added consistency/operational burden.

## Architecture/model sources of truth

Current architecture navigation starts at:

- [`docs/architecture/pre-physical-architecture-baseline.md`](docs/architecture/pre-physical-architecture-baseline.md)
- [`docs/architecture/requirements/README.md`](docs/architecture/requirements/README.md) and all four Phase 5 requirement packages
- [`docs/architecture/ai-context-runtime-boundaries.md`](docs/architecture/ai-context-runtime-boundaries.md)
- [`docs/architecture/integration-hub-boundaries.md`](docs/architecture/integration-hub-boundaries.md)
- [`docs/architecture/durable-execution-benchmark.md`](docs/architecture/durable-execution-benchmark.md)
- [`docs/architecture/governed-operation-effect-contract.md`](docs/architecture/governed-operation-effect-contract.md)
- [`docs/architecture/search-observability-calendar-solver-boundaries.md`](docs/architecture/search-observability-calendar-solver-boundaries.md)
- [`docs/architecture/physical-benchmark-specification.md`](docs/architecture/physical-benchmark-specification.md)
- [`docs/architecture/physical-benchmark-scenario-corpus.md`](docs/architecture/physical-benchmark-scenario-corpus.md)
- [`docs/architecture/physical-benchmark-register.md`](docs/architecture/physical-benchmark-register.md)
- [`docs/architecture/README.md`](docs/architecture/README.md)
- [`docs/architecture/system-overview.md`](docs/architecture/system-overview.md)
- [`docs/architecture/technical-decisions.md`](docs/architecture/technical-decisions.md)

Current semantic/model authority:

- [`docs/product/product-identity-and-north-star.md`](docs/product/product-identity-and-north-star.md)
- [`docs/domain/README.md`](docs/domain/README.md)
- [`docs/domain/language-map.md`](docs/domain/language-map.md)
- [`docs/logical-model/whole-logical-model-v1.md`](docs/logical-model/whole-logical-model-v1.md)
- the complete `docs/logical-model/decision-and-assumption-register-v1*` logical document
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

Phase 6 establishes current AI/context/runtime and Integration Hub boundary contracts. Phase 7–9 establishes current durable-execution posture, governed-operation/effect contract and search/observability/calendar/solver pressure. Phase 10 establishes the current benchmark method that a later authorized Physical Model must execute. Preferred/registered candidates remain candidates, not implementation authorization.

Future Physical/API/runtime work must preserve these constraints rather than reinterpret semantics for implementation convenience.

## Immediate architecture next step

```text
PHASE 11
REPOSITORY ENGINEERING SAFETY
READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED
```

Phase 11 prepares repository/CI/protection safety only. Phase 12 then performs clean-room Pre-Physical closure before the user may separately authorize the Physical Model.

## Git and environments

- `main` is the single integrated source of truth.
- Work happens on bounded `feature/*`, `fix/*`, `docs/*`, `chore/*` or `prototype/*` branches.
- Every remote write follows the exact PRE-SCOPE/write-gate/QA protocol.
- DEV/UAT/PROD are deployment environments, not permanent Git branches.

Significant work is not complete until relevant current documentation/handoff and remote QA are coherent.
