# LifeOS Roadmap

- Last updated: 2026-08-18
- Purpose: current delivery/architecture-stage sequence, not a calendar commitment

## Completed foundations

### Product / North Star

Accepted current LifeOS identity/North Star and supporting product studies are integrated.

### Core Domain Model / Domain Atlas

**CLOSED — integrated into `main` via PR #10.**

```text
Whole-Domain PASS WITH HARDENING
POST-WRITE QA PASS
```

### Logical Model

**CLOSED — integrated into `main` via PR #11.**

```text
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream
```

### Pre-Physical Repository & Architecture Coherence

**DEFINITIVE CLOSED / FINAL QA PASS / integrated / post-merge verified.**

```text
Phase 0–11         QA PASS
Phase 12           QA PASS / CLOSED
Independent audit  PASS
PR #13              Pre-Physical integration
PR #14              post-merge current-truth alignment
Physical base main  3de84bb49f9cef30e88e9bde4961ed84335daa79
```

## Active architecture/model track — Physical Model

The user separately authorized the Physical Model on 2026-08-18.

```text
BRANCH
feature/physical-model

BASE / BOOTSTRAP PRE-SCOPE
3de84bb49f9cef30e88e9bde4961ed84335daa79

PM-00
BOOTSTRAP QA PASS

CURRENT NEXT
PM-01 READ-ONLY candidate/environment freeze

MAPPING
NOT STARTED

BENCHMARK
NOT STARTED

SELECTION
NONE
```

PM-00 created the execution rules, evidence/test contracts, current navigation and live handoff. It did **not** authorize candidate schemas, SQL/TypeQL/Cypher, benchmark harness code, database deployment or technology selection.

## Physical execution sequence

```text
PM-00  Bootstrap / authority freeze                                      QA PASS
PM-01  Candidate + version/edition/deployment/environment freeze         NEXT / READ-ONLY FIRST
PM-02  Primary candidate mapping design                                  NOT STARTED
PM-03  Semantic hard-gate preflight                                      NOT STARTED
PM-04  Fixture/oracle/harness design                                     NOT STARTED
PM-05  Correctness/destructive execution                                 NOT STARTED
PM-06  LOW/BASE/HIGH + performance                                       NOT STARTED
PM-07  Recovery/evolution/failure                                        NOT STARTED
PM-08  Secondary lanes where justified                                   NOT STARTED
PM-09  Scoring + sensitivity                                             NOT STARTED
PM-10  Recommendation                                                    NOT STARTED
PM-11  Explicit selection gate                                           NOT STARTED
PM-12  Accepted Physical Model                                           NOT STARTED
PM-13  Independent clean-room QA                                         NOT STARTED
PM-14  Closure / protected-main integration                              NOT STARTED
```

No phase may be skipped merely because one technology appears attractive early.

## Current Physical benchmark posture

```text
PRIMARY CANONICAL
P0 PostgreSQL hybrid — preferred mandatory baseline — NOT SELECTED / NOT RUN
P1 TypeDB            — mandatory challenger        — NOT SELECTED / NOT RUN

SECONDARY GRAPH
G0 no-specialized-store baseline
G1 Neo4j specialized secondary/read projection — NOT SELECTED / NOT RUN

SEARCH / VECTOR
S0 structured + lexical/full-text baseline
S1 pgvector where PostgreSQL is present/applicable — NOT SELECTED / NOT RUN

EVENT / DOCUMENT
bounded native mechanisms first
specialist only after explicit admission trigger
```

Mandatory decision discipline:

```text
HG-01..HG-12 before primary scoring
CG-01..CG-04 for secondary/index lanes
C0..C7 common corpus
SC-001..SC-035 scenarios
same semantics + candidate-idiomatic physical mapping
product + exact version + edition + deployment = benchmark subject
raw evidence before summary
NOT RUN != PASS
unexecuted tier != VERIFIED-RUN
missing/contradictory evidence = HOLD
PREFERRED != SELECTED
```

LOW/BASE/HIGH remain synthetic qualification envelopes, not business forecasts.

## PM-00 QA evidence

```text
PRE-SCOPE
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

Post-QA status propagation remains confined to the same already-approved 22 physical paths.

## Immediate next — PM-01

```text
PM-01 — READ-ONLY FIRST
```

PM-01 must:

1. freeze exact current PostgreSQL and TypeDB versions/editions/deployment modes to be evaluated;
2. verify version-sensitive capability claims from official primary documentation;
3. capture exact Python driver/client compatibility;
4. verify backup/restore/HA/schema/evolution claims for exact subjects;
5. freeze the available benchmark host/environment constraints;
6. identify unavailable external infrastructure/tooling honestly;
7. build the execution inventory and evidence plan;
8. STOP before first Physical mapping/schema/harness write;
9. present a fresh exact PM-02+ write gate.

PM-01 does not choose PostgreSQL or TypeDB.

## Active parallel product/design track

### Phase 4 — UX prototype/product-structure validation

Separate workstream on `prototype/phase-4-today-home`.

It may continue independently but does not redefine accepted Domain/Logical/Physical authority.

## Current upstream constraints

The Physical workstream must preserve:

- CLOSED Domain Atlas and final closure/language authority;
- CLOSED Whole Logical Model + complete decision register + `WL-H01..WL-H12`;
- Phase 5 AuthN/AuthZ, security/privacy/retention/recovery, consistency/side-effects and NFR/multi-device/recovery requirements;
- Phase 6 AI/context/runtime and Integration Hub boundaries;
- consequential AI behavior-change evaluation requirement;
- Phase 7 durable-execution posture;
- Phase 8 governed operation/effect contract;
- Phase 9 search/observability/calendar/solver boundaries;
- Phase 10 benchmark specification/corpus/register;
- Phase 11 effective repository engineering safety;
- Pre-Physical clean-room/final-audit evidence.

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
```

## Current runtime/search/solver posture

```text
DURABLE EXECUTION
bounded async → DB/worker/outbox style baseline class
material durable orchestration → dedicated engine structurally justified
Restate preferred candidate — NOT selected
Temporal mandatory strongest challenger — NOT selected
DBOS conditional challenger — NOT selected
     local/bounded Python SQLite-capable
     production PostgreSQL-recommended
     distributed multi-server PostgreSQL-coupled

SEARCH
structured + lexical/full-text baseline
semantic/vector bounded
no dedicated service by default

OBSERVABILITY
OpenTelemetry-first / equivalent direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / providers = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics baseline
OR-Tools CP-SAT preferred benchmark candidate — NOT implemented
```

## AI evaluation posture

Material consequential changes to model/version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

## Repository engineering safety

`main` remains protected by `lifeos-main-safety`. `feature/physical-model` is the active bounded Physical branch. Benchmark fixtures/artifacts must contain no real personal production data or credentials. Benchmark-only code/evidence does not become production infrastructure or required CI automatically.

## Backend Foundation — later only

Backend Foundation remains:

```text
NOT STARTED / DEFERRED
```

It becomes eligible for a separate authorization only after an accepted Physical result exists and all remaining prerequisites are satisfied.

## Explicitly unauthorized now

```text
direct main write
candidate Physical schema/tables/indexes/constraints
SQL / TypeQL / Cypher implementation
benchmark harness/fixture-generator code
database/container deployment
PostgreSQL / TypeDB / Neo4j / pgvector selection
production migrations
concrete API routes / DTOs
Auth implementation
Restate / Temporal / DBOS adoption
provider adapters
AI provider/model/agent framework
MCP/A2A adoption
dedicated search/vector deployment
observability vendor
solver implementation
production backend code
feature/backend-foundation
Domain/Logical changes without explicit reopen
```