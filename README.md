# LifeOS

LifeOS is an adaptive personal operating system for connecting intentions, plans, real time, actual reality, people/resources, evidence, history and adaptive future planning across web, Android and iOS.

## Current project state

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated into main via PR #10
Whole-Domain: PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — integrated into main via PR #11
Whole-Logical: PASS WITH HARDENING / REMOTE QA PASS
WD-03: PASS
WD-05: PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
FINAL CLOSURE CANDIDATE on chore/pre-physical-coherence
Phase 0–11 QA PASS
Phase 12 clean-room QA closure record written
Phase 12 becomes QA PASS / CLOSED only when its exact final remote gate QA passes

AFTER PHASE 12
independent total repository audit required before definitive Pre-Physical closure
NO main integration yet

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Phase 4 Home/Today UX continues separately on `prototype/phase-4-today-home`.

For exact current state, read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md) and the active/final-verification [`docs/workstreams/pre-physical-coherence.md`](docs/workstreams/pre-physical-coherence.md).

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

GIT / PR HISTORY
= recoverable history
```

A stale current document may be replaced/deleted only after knowledge coverage proves no meaningful requirement/rationale is lost.

A physical split is a tooling/layout concern, not separate authority. A size/tool-limit split is a **lossless physical partition of the complete logical payload**, never a summary, condensation or hidden semantic rewrite.

## Current model authority

### Product

- [`docs/product/product-identity-and-north-star.md`](docs/product/product-identity-and-north-star.md) — current living product definition.

### Domain

The Domain Atlas is cumulative. Do not stop at the early entry payload when determining closure state.

Read:

- [`docs/domain/README.md`](docs/domain/README.md) — Domain Atlas entry payload;
- [`docs/domain/README-part-20.md`](docs/domain/README-part-20.md) — final corrected Domain closure/status continuation;
- [`docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md) — final closure evidence;
- [`docs/domain/language-map.md`](docs/domain/language-map.md) plus [`docs/domain/language-map-part-22.md`](docs/domain/language-map-part-22.md) — language authority and final disposition.

Current Domain state is **CLOSED**.

### Logical

Read:

- [`docs/logical-model/whole-logical-model-v1.md`](docs/logical-model/whole-logical-model-v1.md) — canonical content payload;
- complete `docs/logical-model/decision-and-assumption-register-v1*` logical document;
- [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md) — separate closure activation / CLOSED evidence.

Current Logical state is **CLOSED**.

## Current architecture sources

Start with:

- [`docs/architecture/README.md`](docs/architecture/README.md)
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
- [`docs/development/repository-engineering-safety.md`](docs/development/repository-engineering-safety.md)
- [`docs/architecture/pre-physical-clean-room-qa.md`](docs/architecture/pre-physical-clean-room-qa.md) — Phase 12 evidence/activation contract
- [`docs/architecture/system-overview.md`](docs/architecture/system-overview.md)
- [`docs/architecture/technical-decisions.md`](docs/architecture/technical-decisions.md)

## Current technical direction — not implementation authorization

### Clients

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.

### Backend

- Python + FastAPI + Pydantic.
- Modular monolith first.
- SQLAlchemy + Alembic remain conditional on accepted Physical persistence.

Backend implementation is **not started**.

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

Phase 10 decides **how** a later Physical benchmark must run, not what technology wins. `PREFERRED != SELECTED`.

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
bounded async
DB/worker/outbox style = valid baseline class

material durable execution
Restate   preferred candidate — NOT selected
Temporal  mandatory strongest challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

### Search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text baseline
semantic/vector bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent direction

CALENDAR
iCalendar / JSCalendar / providers = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics baseline
OR-Tools CP-SAT preferred specialized benchmark candidate — NOT implemented
```

## Repository safety

Phase 11 remotely verified `lifeos-main-safety` as active for protected `main` integration. Current owner-driven policy requires PR integration, blocks deletion/force-push, requires review-thread resolution, uses zero required approvals while no independent reviewer exists and has no required CI checks until real stable check contexts exist.

Do not work directly on `main` for normal work and do not invent required checks before the corresponding workflow exists.

## Phase 12 boundary

Phase 12 is the clean-room repository/architecture coherence phase. Its evidence record is [`docs/architecture/pre-physical-clean-room-qa.md`](docs/architecture/pre-physical-clean-room-qa.md).

The record is **conditionally activating**: Phase 12 is `QA PASS / CLOSED` only when the final remote compare proves the exact approved 11-path gate and `main` remains unchanged.

Even after that activation, current user instruction is:

```text
DO NOT MERGE TO MAIN YET
DO NOT DECLARE THE WHOLE PRE-PHYSICAL WORKSTREAM DEFINITIVELY CLOSED YET

NEXT
run an independent total repository audit
for mistakes, contradictions, lost knowledge and scope damage
```

Only after that total audit passes may the definitive Pre-Physical closure be separately authorized. Physical Model authorization and `main` integration remain later steps.
