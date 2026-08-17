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
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
IN PROGRESS on chore/pre-physical-coherence
Phase 0–10 QA PASS
Phase 11 repository engineering safety QA PASS
Phase 12 clean-room repository/architecture coherence QA NEXT

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
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
8. [`docs/development/repository-engineering-safety.md`](docs/development/repository-engineering-safety.md);
9. the active workstream handoff;
10. current architecture/model indexes and linked current sources;
11. relevant ADRs/evidence/methodologies and implementation/tests;
12. verify the current Git ref before any write.

Repository current truth outranks conversation memory and old/historical files. An active branch may contain newer truth only inside its explicitly bounded workstream.

## Documentation rule

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

A stale current document may be replaced/deleted only after knowledge coverage proves no meaningful requirement/rationale is lost.

A physical split is a tooling/layout concern, not separate authority. A size/tool-limit split is a **lossless physical partition of the complete logical payload**, never a summary, condensation or hidden semantic rewrite.

## Current architecture/model sources

Start with:

- [`docs/product/product-identity-and-north-star.md`](docs/product/product-identity-and-north-star.md)
- [`docs/domain/README.md`](docs/domain/README.md)
- [`docs/domain/language-map.md`](docs/domain/language-map.md)
- [`docs/logical-model/whole-logical-model-v1.md`](docs/logical-model/whole-logical-model-v1.md)
- complete `docs/logical-model/decision-and-assumption-register-v1*` logical document
- [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md)
- [`docs/architecture/pre-physical-architecture-baseline.md`](docs/architecture/pre-physical-architecture-baseline.md)
- [`docs/architecture/requirements/README.md`](docs/architecture/requirements/README.md) + all four Phase 5 packages
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

## Current technical direction — not implementation authorization

### Clients

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.

### Backend

- Python + FastAPI + Pydantic.
- Modular monolith first.
- SQLAlchemy + Alembic remain conditional on the accepted Physical persistence design.

### Physical persistence posture

No final Physical persistence is selected.

```text
PRIMARY CANONICAL
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline
vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first
specialized candidate only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Phase 10 decides **how** the later Physical benchmark must be run, not what technology wins. `PREFERRED != SELECTED`.

### AI / context / runtime

AI remains behind a replaceable/provider-neutral gateway and bounded Context Builder.

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

AI output/tool invocation does not become canonical truth/effect by itself. Runtime Agent/Principal is not Domain Actor automatically. Generic AI memory is not a second canonical truth store.

### Integration Hub

Five modes remain distinct:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider state/effect != canonical LifeOS state/effect automatically. MCP/A2A/future protocols remain adapters.

### Governed operations / effects

Consequential work uses the engine-/transport-neutral [`docs/architecture/governed-operation-effect-contract.md`](docs/architecture/governed-operation-effect-contract.md).

```text
route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation/effect

request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

### Durable execution

```text
BOUNDED ASYNC
DB + worker/outbox style remains a valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

### Search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text = baseline
semantic/vector = bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent = current direction
vendor = not selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules / heuristics = baseline
OR-Tools CP-SAT = preferred specialized benchmark candidate — NOT implemented
```

Search/vector/solver/telemetry state does not become canonical truth by convenience.

## Repository engineering safety

Phase 11 is QA-closed. Current policy: [`docs/development/repository-engineering-safety.md`](docs/development/repository-engineering-safety.md).

`main` is governed by active repository ruleset `lifeos-main-safety`:

```text
main deletion blocked
force-push/non-fast-forward blocked
pull request required
0 approvals while owner-driven
review-thread resolution required
merge commits only
required checks = 0 until real stable workflows exist
auto-delete merged head branches enabled
```

The repository must not invent required CI checks before the actual workflow/check exists and has emitted a stable context. Future production code must progressively add real tests/lint/types/security/Physical checks and only then promote material stable checks into main protection.

## Non-negotiable downstream constraints

The closed Logical Model activates `WL-H01..WL-H12`, including governed effects, expected-state writes, idempotency distinct from identity, truthful multi-owner consistency, canonical/provider separation, derived freshness, retention/redaction/tombstone integrity, reconstructible AuthZ provenance and non-interference/inference-leakage protection.

Phase 5 requirements, Phase 6 boundary contracts, Phase 7–9 architecture contracts, Phase 10 benchmark method and Phase 11 repository safety are mandatory downstream inputs. Open parameters remain explicit obligations rather than permission for arbitrary implementation defaults.

## Immediate next step

```text
PHASE 12
CLEAN-ROOM REPOSITORY / ARCHITECTURE COHERENCE QA
READ-ONLY FIRST

TARGET AFTER PHASE 12
REPOSITORY / ARCHITECTURE COHERENCE PASS
DOMAIN UNCHANGED / CLOSED
LOGICAL UNCHANGED / CLOSED
PHYSICAL MODEL READY FOR SEPARATE AUTHORIZATION / NOT STARTED
```

Physical Model and Backend Foundation remain unauthorized/not started until the required later gates are explicitly approved.
