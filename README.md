# LifeOS

LifeOS is an adaptive personal operating system for connecting intentions, plans, real time, actual reality, people/resources, evidence, history and adaptive future planning across web, Android and iOS.

## Current project state

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated into main via PR #10
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — integrated into main via PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS — integrated via PR #13
POST-MERGE CURRENT-TRUTH ALIGNMENT — PR #14

PHYSICAL MODEL
AUTHORIZED / IN PROGRESS
PM-00 BOOTSTRAP QA PASS
PM-01 READ-ONLY NEXT
branch feature/physical-model
base main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79
mapping NOT STARTED
benchmark execution NOT STARTED
technology selection NONE

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Phase 4 Home/Today UX continues separately on `prototype/phase-4-today-home`.

For exact current state read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md) and the active [`docs/workstreams/physical-model.md`](docs/workstreams/physical-model.md).

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
9. [`docs/workstreams/physical-model.md`](docs/workstreams/physical-model.md);
10. [`docs/physical-model/README.md`](docs/physical-model/README.md);
11. [`docs/physical-model/execution-methodology-v1.md`](docs/physical-model/execution-methodology-v1.md);
12. [`docs/physical-model/execution-template-v1.md`](docs/physical-model/execution-template-v1.md);
13. [`docs/physical-model/acceptance-test-matrix-v1.md`](docs/physical-model/acceptance-test-matrix-v1.md);
14. [`docs/physical-model/result-register-v1.md`](docs/physical-model/result-register-v1.md);
15. [`docs/architecture/README.md`](docs/architecture/README.md) and the complete Phase-5..10 authority it links;
16. complete CLOSED Domain/Logical authority where mapping semantics are involved;
17. relevant ADRs/evidence;
18. verify current Git refs before any write.

Repository current truth outranks conversation memory and old/historical files. The active Physical branch may contain newer truth only inside its explicitly bounded workstream.

## Documentation rule

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

A stale current document may be replaced/deleted only after knowledge coverage proves no meaningful requirement/rationale is lost.

A size/tool-limit split is a **lossless physical partition of the complete logical payload**, never a summary, condensation or hidden semantic rewrite.

## Current model authority

### Product

- [`docs/product/product-identity-and-north-star.md`](docs/product/product-identity-and-north-star.md) — current living product definition.

### Domain

The Domain Atlas is cumulative. Do not stop at the early entry payload when determining closure state.

Read:

- [`docs/domain/README.md`](docs/domain/README.md);
- [`docs/domain/README-part-20.md`](docs/domain/README-part-20.md);
- [`docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md);
- [`docs/domain/language-map.md`](docs/domain/language-map.md) + [`docs/domain/language-map-part-22.md`](docs/domain/language-map-part-22.md).

Current Domain state is **CLOSED**.

### Logical

Read:

- [`docs/logical-model/whole-logical-model-v1.md`](docs/logical-model/whole-logical-model-v1.md);
- complete `docs/logical-model/decision-and-assumption-register-v1*` chain;
- [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md).

Current Logical state is **CLOSED**.

## Active Physical authority

The Physical workstream consumes the accepted Domain/Logical/Pre-Physical state; it does not reopen it implicitly.

Current Physical execution documents:

- [`docs/physical-model/README.md`](docs/physical-model/README.md) — execution authority/index;
- [`docs/physical-model/execution-methodology-v1.md`](docs/physical-model/execution-methodology-v1.md) — PM-00..PM-14 sequence;
- [`docs/physical-model/execution-template-v1.md`](docs/physical-model/execution-template-v1.md) — reproducible evidence template;
- [`docs/physical-model/acceptance-test-matrix-v1.md`](docs/physical-model/acceptance-test-matrix-v1.md) — HG/CG/corpus/scenario ledger;
- [`docs/physical-model/result-register-v1.md`](docs/physical-model/result-register-v1.md) — current result/disposition state;
- [`docs/workstreams/physical-model.md`](docs/workstreams/physical-model.md) — live save-game.

Phase-10 method authority remains:

- [`docs/architecture/physical-benchmark-specification.md`](docs/architecture/physical-benchmark-specification.md)
- [`docs/architecture/physical-benchmark-scenario-corpus.md`](docs/architecture/physical-benchmark-scenario-corpus.md)
- [`docs/architecture/physical-benchmark-register.md`](docs/architecture/physical-benchmark-register.md)

## Current Physical posture

No final Physical persistence is selected.

```text
PRIMARY CANONICAL
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
G0 no-specialized-store baseline vs G1 Neo4j

SEARCH / VECTOR
S0 structured + lexical/full-text baseline
vs S1 bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first
specialized candidate only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Mandatory Physical rules:

```text
hard semantic/correctness gates before score
same semantics + candidate-idiomatic mapping
product + version + edition + deployment = benchmark subject
raw evidence before summary
NOT RUN != PASS
unexecuted tier != VERIFIED-RUN
PREFERRED != SELECTED
```

PM-00 bootstrap is complete and QA-verified. The next step is **PM-01 READ-ONLY FIRST**: freeze current exact candidate subjects and available benchmark environment using official primary sources, then stop before the first mapping/harness write.

## Current technical direction — not backend implementation authorization

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend: Python + FastAPI + Pydantic; modular monolith first.
- SQLAlchemy + Alembic remain conditional on accepted Physical persistence.

Backend implementation is **not started**.

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

Material consequential AI changes require versioned/reproducible evaluation before promotion.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

### Integration Hub

Five modes remain distinct: canonical import, sync/mirror, live federated read, retrieval/index projection and action/tool integration.

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
DBOS      conditional challenger — NOT selected
          local/bounded Python SQLite-capable
          production PostgreSQL-recommended
          distributed multi-server PostgreSQL-coupled
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

`main` remains protected by the remotely verified `lifeos-main-safety` policy. `feature/physical-model` is the active bounded Physical branch. Do not work directly on `main`, do not invent required CI checks, and do not treat benchmark-only code/evidence as production infrastructure automatically.

## Completed Pre-Physical boundary

Pre-Physical is **DEFINITIVE CLOSED / FINAL QA PASS / integrated / post-merge verified**. PR #13 integrated the workstream and PR #14 aligned current truth. Physical starts from `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`.

## Next boundary

```text
PM-00 BOOTSTRAP
QA PASS

NEXT
PM-01 READ-ONLY FIRST
exact candidate/version/edition/deployment/environment freeze

MAPPING
NOT STARTED

BENCHMARK
NOT STARTED

SELECTION
NONE

BACKEND
NOT STARTED / DEFERRED
```