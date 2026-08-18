# Project Status

- Last updated: 2026-08-18
- Canonical integrated branch: `main`
- Current accepted `main` / Physical bootstrap base: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Active Physical branch: `feature/physical-model`
- Physical bootstrap PRE-SCOPE: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00 bootstrap: **QA PASS**
- PM-01 candidate/environment freeze: **READY / NOT STARTED — READ-ONLY FIRST**
- Production application code: **NOT STARTED**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Current stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated through PR #10
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — integrated through PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED
PR #13 + post-merge alignment PR #14

PHYSICAL READINESS
ESTABLISHED

PHYSICAL MODEL
AUTHORIZED / IN PROGRESS
PM-00 BOOTSTRAP QA PASS
PM-01 READ-ONLY NEXT
branch feature/physical-model
base 3de84bb49f9cef30e88e9bde4961ed84335daa79
mapping NOT STARTED
benchmark execution NOT STARTED
technology selection NONE

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

Phase 4 UX remains a separate active product/design workstream on `prototype/phase-4-today-home`.

## Read this first

1. [`README.md`](../README.md)
2. [`docs/README.md`](README.md)
3. this file
4. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
5. [`development/operating-rules.md`](development/operating-rules.md)
6. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
7. [`development/branching-and-environments.md`](development/branching-and-environments.md)
8. [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
9. [`workstreams/physical-model.md`](workstreams/physical-model.md)
10. [`physical-model/README.md`](physical-model/README.md)
11. [`physical-model/execution-methodology-v1.md`](physical-model/execution-methodology-v1.md)
12. [`physical-model/execution-template-v1.md`](physical-model/execution-template-v1.md)
13. [`physical-model/acceptance-test-matrix-v1.md`](physical-model/acceptance-test-matrix-v1.md)
14. [`physical-model/result-register-v1.md`](physical-model/result-register-v1.md)
15. [`architecture/README.md`](architecture/README.md) and the full Phase-5..10 authority it links
16. complete Domain/Logical closure authority when mapping semantics are involved
17. relevant ADR/evidence/methodology
18. current Git refs/branch relation to `main`

Conversation history is secondary to repository truth.

## Accepted/current foundations

- Product/North Star — **CURRENT**.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**; `WL-H01..WL-H12` active downstream.
- Pre-Physical Architecture Baseline — **CURRENT / CLOSED / integrated**.
- Phase 5 requirements — **CURRENT**.
- Phase 6 AI/context/runtime + Integration Hub boundaries — **CURRENT**.
- Phase 7 durable execution — **CURRENT / conditional ranking only**.
- Phase 8 governed operation/effect — **CURRENT**.
- Phase 9 search/observability/calendar/solver — **CURRENT**.
- Phase 10 benchmark method — **CURRENT / QA PASS / ACTIVE INPUT**.
- Phase 11 repository engineering safety — **QA PASS**.
- Phase 12 clean-room QA — **QA PASS / CLOSED**.
- Independent total Pre-Physical audit — **PASS**.
- Pre-Physical protected-main integration — **PR #13 / POST-MERGE VERIFIED**.
- Post-merge current-truth alignment — **PR #14**; `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`.
- Physical PM-00 bootstrap — **QA PASS**.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.
- SQLAlchemy/Alembic — conditional on accepted Physical persistence.

## Domain / Logical closure

```text
DOMAIN
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED

LOGICAL
PASS WITH HARDENING
REMOTE QA PASS
CLOSED
WD-03 PASS
WD-05 PASS
```

The Physical workstream must consume these models without implicit semantic reopen. Any genuine contradiction requires a separate explicit reopen scope.

## Active Physical Model

Current execution authority:

- [`physical-model/README.md`](physical-model/README.md);
- [`physical-model/execution-methodology-v1.md`](physical-model/execution-methodology-v1.md);
- [`physical-model/execution-template-v1.md`](physical-model/execution-template-v1.md);
- [`physical-model/acceptance-test-matrix-v1.md`](physical-model/acceptance-test-matrix-v1.md);
- [`physical-model/result-register-v1.md`](physical-model/result-register-v1.md);
- [`workstreams/physical-model.md`](workstreams/physical-model.md).

Phase-10 method authority remains:

- `architecture/physical-benchmark-specification.md`;
- `architecture/physical-benchmark-scenario-corpus.md`;
- `architecture/physical-benchmark-register.md`.

Current role posture:

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT SELECTED
TypeDB            — mandatory challenger, NOT SELECTED

SECONDARY GRAPH
G0 no-specialized-store vs G1 Neo4j

SEARCH / VECTOR
S0 structured + lexical/full-text vs S1 pgvector where applicable

EVENT / DOCUMENT
bounded native mechanisms first; specialist only after explicit admission
```

Current result state:

```text
P0 PostgreSQL   NOT RUN / NOT SELECTED
P1 TypeDB       NOT RUN / NOT SELECTED
G1 Neo4j        NOT RUN / NOT SELECTED
S1 pgvector     NOT RUN / NOT SELECTED
ED specialized  NOT ADMITTED
```

## Physical execution rules

```text
hard semantic/correctness gates before scoring
same semantics + candidate-idiomatic mapping
product + exact version + edition + deployment = benchmark subject
raw evidence before summary
NOT RUN != PASS
official product claim != direct execution evidence
unexecuted tier != VERIFIED-RUN
missing/contradictory evidence = HOLD
PREFERRED != SELECTED
```

Primary hard gates remain `HG-01..HG-12`; cross-lane hard gates `CG-01..CG-04`; corpus `C0..C7`; scenarios `SC-001..SC-035`.

LOW/BASE/HIGH remain synthetic qualification envelopes, not business forecasts.

## PM progression

```text
PM-00  bootstrap / authority freeze                 QA PASS
PM-01  candidate + version/edition/deployment/environment freeze — READ-ONLY FIRST — NEXT
PM-02  primary mapping design                       NOT STARTED
PM-03  semantic hard-gate preflight                 NOT STARTED
PM-04  fixtures/oracle/harness design               NOT STARTED
PM-05  correctness/destructive execution            NOT STARTED
PM-06  scale/performance tiers                      NOT STARTED
PM-07  recovery/evolution/failure                   NOT STARTED
PM-08  secondary lanes                              NOT STARTED
PM-09  scoring/sensitivity                          NOT STARTED
PM-10  recommendation                               NOT STARTED
PM-11  explicit selection gate                      NOT STARTED
PM-12  accepted Physical Model                      NOT STARTED
PM-13  independent clean-room QA                    NOT STARTED
PM-14  closure/protected-main integration           NOT STARTED
```

PM-01 is read-only. No SQL/TypeQL/Cypher, candidate schemas, benchmark harness code, database/container deployment or technology selection is authorized yet.

## Phase-5..9 constraints remain active

### Requirements

AuthN/AuthZ, security/privacy/retention/recovery, consistency/side effects and non-functional/multi-device/recovery remain mandatory Physical pressure. Open RPO/RTO/latency/availability/scale/offline values remain explicit until legitimately resolved.

### AI / context / integration

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Generic AI memory is not a second canonical truth store. Runtime Agent/Principal != Domain Actor automatically; tool invocation != authorization/effect.

Material consequential AI changes require versioned/reproducible evaluation before promotion.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

Integration Hub preserves canonical import, sync/mirror, live federated read, retrieval/index projection and action/tool integration. `ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider state/effect != canonical state/effect automatically.

### Durable execution

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional challenger — NOT selected
          SQLite-capable local/bounded Python use
          PostgreSQL-recommended production
          distributed multi-server PostgreSQL-coupled
```

Physical evidence may affect infrastructure coupling, but may not select a workflow runtime implicitly.

### Governed operation/effect

```text
HTTP/UI/tool/AuthZ/workflow step != canonical governed operation
request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

### Search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text baseline
semantic/vector bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics baseline
OR-Tools CP-SAT preferred benchmark candidate — NOT implemented
UNKNOWN != INFEASIBLE
```

## Repository safety

`lifeos-main-safety` remains the protected-main policy. `feature/physical-model` is an active bounded branch. No direct-main work, no invented required checks, no production secrets/personal data in benchmark fixtures, and no benchmark-only code automatically promoted to production infrastructure.

## PM-00 QA evidence

```text
BOOTSTRAP PRE-SCOPE
3de84bb49f9cef30e88e9bde4961ed84335daa79

CREATE CHECKPOINT
6d76bc150dfd7b3cefe56c6e05c96404e7494626
6 added / 0 modified / behind 0

CONTENT-QA CHECKPOINT
8549e1c95bef2e354bd47028259e6816bf5e9272
22 unique paths
6 added
16 modified
0 deleted
0 unexpected
behind 0

main
3de84bb49f9cef30e88e9bde4961ed84335daa79 unchanged
```

Final save-game propagation stays on the same approved 22-path physical scope.

## Active workstreams

### Physical Model

- **AUTHORIZED / IN PROGRESS**
- **PM-00 QA PASS**
- **PM-01 READ-ONLY NEXT**
- branch `feature/physical-model`
- mapping **NOT STARTED**
- benchmark **NOT STARTED**
- selection **NONE**

### Phase 4 — Home / Today UX

- **IN PROGRESS — separate product/design workstream**
- branch `prototype/phase-4-today-home`

### Backend Foundation

**NOT STARTED / DEFERRED.** It remains blocked until the Physical result is explicitly selected/accepted and all remaining prerequisites are satisfied.

## Immediate next work

```text
PM-01 — READ-ONLY FIRST

- freeze exact current PostgreSQL and TypeDB versions/editions/deployment modes
- verify version-sensitive capabilities from official primary sources
- capture Python driver/client compatibility
- verify backup/restore/HA/schema/evolution claims for exact subjects
- freeze available benchmark environment
- identify unavailable infrastructure/tooling honestly
- produce execution inventory/evidence plan
- STOP before mapping/schema/harness/database writes
- present fresh exact PM-02+ gate
```

Do not choose PostgreSQL or TypeDB during PM-01.