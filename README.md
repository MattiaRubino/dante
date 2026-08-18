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
DEFINITIVE CLOSED / FINAL QA PASS — integrated into main via PR #13
Phase 0–11 QA PASS
Phase 12 QA PASS / CLOSED
Independent total audit PASS
final activation checkpoint 9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d
post-merge main checkpoint 74593ae283ce5a1d22335502480ee3fa54be0436

PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

MAIN INTEGRATION
COMPLETE / POST-MERGE VERIFIED
PR #13
```

Phase 4 Home/Today UX continues separately on `prototype/phase-4-today-home`.

For exact current state, read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md) and [`docs/workstreams/pre-physical-coherence.md`](docs/workstreams/pre-physical-coherence.md).

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
9. the relevant workstream handoff;
10. [`docs/architecture/README.md`](docs/architecture/README.md) and linked current sources;
11. Phase 12 + final independent audit evidence;
12. relevant ADRs/evidence/methodologies and implementation/tests;
13. verify current Git refs before any write.

Repository current truth outranks conversation memory and old/historical files. An active branch may contain newer truth only inside its explicitly bounded workstream.

## Documentation rule

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

A stale current document may be replaced/deleted only after knowledge coverage proves no meaningful requirement/rationale is lost.

A physical split is a tooling/layout concern, not separate authority. A size/tool-limit split is a **lossless physical partition of the complete logical payload**, never a summary, condensation or hidden semantic rewrite.

## Current model authority

### Product

- [`docs/product/product-identity-and-north-star.md`](docs/product/product-identity-and-north-star.md) — current living product definition.

### Domain

The Domain Atlas is cumulative. Do not stop at the early entry payload when determining closure state.

Read:

- [`docs/domain/README.md`](docs/domain/README.md) — entry payload;
- [`docs/domain/README-part-20.md`](docs/domain/README-part-20.md) — final corrected closure/status continuation;
- [`docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md) — final closure evidence;
- [`docs/domain/language-map.md`](docs/domain/language-map.md) plus [`docs/domain/language-map-part-22.md`](docs/domain/language-map-part-22.md) — language authority/final disposition.

Current Domain state is **CLOSED**.

### Logical

Read:

- [`docs/logical-model/whole-logical-model-v1.md`](docs/logical-model/whole-logical-model-v1.md);
- complete `docs/logical-model/decision-and-assumption-register-v1*` chain;
- [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md).

Current Logical state is **CLOSED**.

## Current architecture sources

Start with:

- [`docs/architecture/README.md`](docs/architecture/README.md)
- [`docs/architecture/pre-physical-architecture-baseline.md`](docs/architecture/pre-physical-architecture-baseline.md)
- [`docs/architecture/requirements/README.md`](docs/architecture/requirements/README.md) + all Phase 5 packages
- [`docs/architecture/ai-context-runtime-boundaries.md`](docs/architecture/ai-context-runtime-boundaries.md)
- [`docs/architecture/integration-hub-boundaries.md`](docs/architecture/integration-hub-boundaries.md)
- [`docs/architecture/durable-execution-benchmark.md`](docs/architecture/durable-execution-benchmark.md)
- [`docs/architecture/governed-operation-effect-contract.md`](docs/architecture/governed-operation-effect-contract.md)
- [`docs/architecture/search-observability-calendar-solver-boundaries.md`](docs/architecture/search-observability-calendar-solver-boundaries.md)
- [`docs/architecture/physical-benchmark-specification.md`](docs/architecture/physical-benchmark-specification.md)
- [`docs/architecture/physical-benchmark-scenario-corpus.md`](docs/architecture/physical-benchmark-scenario-corpus.md)
- [`docs/architecture/physical-benchmark-register.md`](docs/architecture/physical-benchmark-register.md)
- [`docs/development/repository-engineering-safety.md`](docs/development/repository-engineering-safety.md)
- [`docs/architecture/pre-physical-clean-room-qa.md`](docs/architecture/pre-physical-clean-room-qa.md) — Phase 12 evidence
- [`docs/architecture/pre-physical-final-coherence-audit.md`](docs/architecture/pre-physical-final-coherence-audit.md) — final independent audit/activation evidence
- [`docs/architecture/system-overview.md`](docs/architecture/system-overview.md)
- [`docs/architecture/technical-decisions.md`](docs/architecture/technical-decisions.md)

## Current technical direction — not implementation authorization

### Clients / backend direction

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend: Python + FastAPI + Pydantic; modular monolith first.
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

Synthetic LOW/BASE/HIGH tiers are qualification envelopes, not forecasts. An unexecuted envelope is not `VERIFIED-RUN`; progressive saturation/scaling evidence must be reported according to what actually ran.

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

Material consequential changes to model/model version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion.

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
          local/bounded Python use SQLite-capable
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

Phase 11 remotely verified `lifeos-main-safety` as active for protected `main` integration. Current owner-driven policy requires PR integration, blocks deletion/force-push, requires review-thread resolution, uses zero required approvals while no independent reviewer exists and has no required CI checks until real stable check contexts exist. Auto-delete merged head branches is enabled.

Do not work directly on `main` for normal work and do not invent required checks before the corresponding workflow exists.

## Definitive Pre-Physical closure and integration

Phase 12 is **QA PASS / CLOSED**.

The independent total audit then rechecked the entire Pre-Physical delta and found:

```text
Domain reopen required             0
Logical reopen required            0
major semantic contradiction       0
major architecture contradiction   0
major knowledge loss               0
Physical accidentally started      0
backend accidentally started       0
```

The bounded current-truth/factual/engineering repairs were applied under PRE-SCOPE `1bd142afe51221211bc777f6271a642911c650fc`. The activation checkpoint `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d` proved exactly:

```text
unique paths 23
added 1
modified 22
deleted 0
unexpected 0
behind_by 0
main unchanged at 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0
critical readback PASS
```

That checkpoint established the branch-local closure. PR #13 then integrated the closed workstream into protected `main` using merge commit `74593ae283ce5a1d22335502480ee3fa54be0436`. Post-merge verification proved the final branch tree and merged `main` tree differ by the merge commit only and by **zero files**. The merged head branch was auto-deleted.

Current result:

```text
INDEPENDENT TOTAL PRE-PHYSICAL AUDIT
PASS

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED INTO MAIN VIA PR #13
POST-MERGE VERIFIED

DOMAIN
UNCHANGED / CLOSED

LOGICAL
UNCHANGED / CLOSED

PHYSICAL READINESS
ESTABLISHED
PHYSICAL MODEL NOT STARTED / NOT AUTHORIZED

BACKEND
NOT STARTED / DEFERRED
```

Final audit evidence: [`docs/architecture/pre-physical-final-coherence-audit.md`](docs/architecture/pre-physical-final-coherence-audit.md).

## Next boundary

```text
PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED
```

Pre-Physical integration is complete. The next architecture/model action requires a **separate explicit authorization** to start the Physical Model. Backend Foundation remains deferred until a Physical result is separately accepted.