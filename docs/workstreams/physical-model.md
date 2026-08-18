# Workstream — Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-10 COMPLETE / PM-11 NEXT**
- Branch: `feature/physical-model`
- Main baseline: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Started: 2026-08-18
- Domain: **CLOSED / INTEGRATED**
- Logical: **CLOSED / INTEGRATED / WL-H01..WL-H12 ACTIVE**
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL / benchmark-host HOLD-DORMANT**
- PM-02: **PRIMARY MAPPING DESIGN COMPLETE**
- PM-03: **STATIC PREFLIGHT COMPLETE / 0 STATIC REJECTS**
- PM-04A: **EVIDENCE SUFFICIENCY COMPLETE / 48 OF 48 CELLS / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED / HARNESS NOT STARTED**
- PM-05: **CORRECTNESS/DESTRUCTIVE EVIDENCE QUALIFICATION COMPLETE**
- PM-06: **SCALE/PERFORMANCE EVIDENCE QUALIFICATION COMPLETE / DIRECT RUN NOT EXECUTED**
- PM-07: **RECOVERY/EVOLUTION/FAILURE EVIDENCE QUALIFICATION COMPLETE / DIRECT RUN NOT EXECUTED**
- PM-08: **SECONDARY/SPECIALIST LANE QUALIFICATION COMPLETE**
- PM-09: **EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE**
- PM-10: **FINAL STACK RECOMMENDATION COMPLETE**
- Evidence-weighted score: **PostgreSQL 89.25 / TypeDB 80.00**
- Ranking: **ROBUST / NOT SENSITIVITY-DEPENDENT / NOT PERFORMANCE-DEPENDENT**
- Preferred primary: **PostgreSQL 18.4 / PASS-CONDITIONAL**
- Preferred companion stack: **ESTABLISHED / PASS-CONDITIONAL**
- Selected: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## 1. Purpose

Terminal save-game for the active Physical Model workstream. A new chat/agent must be able to resume from repository truth without reconstructing conversation history.

The workstream owns technology discovery, candidate-native mapping, Physical evidence qualification, specialist-lane decisions, scoring/sensitivity, recommendation, explicit selection, accepted Physical Model, clean-room QA and protected-main integration.

It does **not** authorize production backend/API/Auth implementation.

## 2. Mandatory continuation bootstrap

Before any further Physical write/action:

1. verify actual remote `feature/physical-model` HEAD;
2. compare it with current `main` and record ahead/behind truth;
3. read root `README.md`;
4. read `docs/README.md` and `docs/PROJECT-STATUS.md`;
5. read `docs/development/agent-operating-manual.md`;
6. read `docs/development/operating-rules.md`;
7. read `docs/development/documentation-and-handoff.md`;
8. read `docs/development/branching-and-environments.md`;
9. read `docs/development/repository-engineering-safety.md`;
10. read this file completely;
11. read `docs/physical-model/README.md`;
12. read `docs/architecture/physical-benchmark-specification.md` including the PM-09 scoring reconciliation;
13. read `docs/physical-model/execution-methodology-v1.md`;
14. read `docs/physical-model/execution-template-v1.md` when direct evidence is relevant;
15. read `docs/physical-model/acceptance-test-matrix-v1.md`;
16. read `docs/physical-model/result-register-v1.md`;
17. read PM-01 landscape;
18. read PM-02 overview + all four mapping records;
19. read PM-03 overview + all four preflight records;
20. read PM-04A overview + all four evidence records;
21. read PM-05 overview + all four candidate qualification records;
22. read PM-06/07 joint overview + PM-06 + PM-07 + two finalist qualification records;
23. read PM-08 overview + graph/search-vector/local-offline/specialist-trigger records;
24. read PM-09 overview + both candidate score records + sensitivity record;
25. read all PM-10 records:
    - `docs/physical-model/pm-10-recommendation-v1.md`;
    - `docs/physical-model/final-stack-audit-v1.md`;
    - `docs/physical-model/final-stack-capability-matrix-v1.md`;
    - `docs/physical-model/final-stack-simulation-v1.md`;
    - `docs/physical-model/recommendation/postgresql-18.4-v1.md`;
    - `docs/physical-model/recommendation/companion-stack-v1.md`;
    - `docs/physical-model/recommendation/technology-exclusion-register-v1.md`;
    - `docs/physical-model/recommendation/post-selection-validation-register-v1.md`;
26. read Phase-10 scenario corpus/register where scenario authority matters;
27. read complete Whole-Logical authority and relevant decision-register continuations when semantics are involved;
28. verify current external product/version/edition/topology facts from primary sources where material;
29. issue a fresh exact PRE-SCOPE/write gate before repository mutation.

Conversation memory is secondary to repository truth.

## 3. Non-negotiable guardrails

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
CANONICAL != PROVIDER / DERIVED / SECURITY STATE
SECONDARY != CANONICAL
LOCAL != CANONICAL
RUNTIME != DOMAIN HISTORY
MISSING != FALSE
EXTERNAL EVIDENCE != DIRECT LIFEOS RUN
PUBLIC/VENDOR BENCHMARK != LIFEOS BENCHMARK
EVIDENCE-QUALIFIED != EXECUTED HARD-GATE PASS
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
FINALIST != PREFERRED
PREFERRED != SELECTED
```

Never introduce by convenience:

```text
universal Entity/Thing root
universal semantic Relationship/edge root
generic EAV/property-bag canonical kernel
universal Rule/Fact/WorkItem/Command root
provider IDs/revisions as canonical identity/material state
storage/MVCC/system-time/changefeed token as MaterialStateRef
technical AuthZ as Domain Authority/Consent
AI/solver result as accepted canonical effect
per-recipient duplicate canonical reality
universal last-write-wins
local-first canonical authority
runtime workflow state as Domain history
```

Reference families remain:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

State layers remain distinguishable:

```text
canonical LifeOS state
material historical state
derived/projection state
external/provider state
candidate/unresolved state
security/runtime state
```

`WL-H01..WL-H12` remain active and non-negotiable.

## 4. Cost / architecture policy

Decision order remains:

1. semantic correctness;
2. consistency/integrity/security/privacy/recovery;
3. LifeOS capability/workload fit;
4. maturity/operability/maintainability/Python tooling;
5. performance/resource efficiency where decision-relevant;
6. TCO/deployment requirements;
7. lock-in/exit/migration risk.

```text
INITIAL DIRECT TECHNOLOGY/LICENSE TARGET
EUR 0 where realistically possible

free != automatic preference
paid != automatic rejection
quality/correctness outrank cost
```

Every companion mechanism must earn complexity and must never become an accidental second canonical authority.

## 5. Historical checkpoints

```text
MAIN BASELINE
3de84bb49f9cef30e88e9bde4961ed84335daa79

PM-01 terminal
fac3b5baf1813f886c4773594e6234810e5ba8c6

PM-02 terminal
db127af8c759aacf69b43d0f5a5444b04fd43759

PM-03 terminal
0e4212909bd94de076c9074302a79296d474e53f

PM-04A terminal
44d331f12951e2844186e6f5f885e1bcf1559a3b

PM-05 terminal
9a53c2577e8e25de6de63a830e9bab036521f040

PM-06/07 terminal
1e19793fdb9f51ba510f00ac4c927a6907e28c4b

PM-08 terminal
6aef5537edacff3e315d502a1bd3ede544dc149e

PM-09 terminal
016e4df07df9756d2c03d5582b489eed607aaecc

PM-10 PRE-SCOPE
016e4df07df9756d2c03d5582b489eed607aaecc
```

The final PM-10 remote HEAD must be read from Git after this terminal handoff write.

## 6. Primary-candidate history and recommendation

PM-01 admitted:

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

PM-05 narrowed to PostgreSQL + TypeDB. PM-06/07 established both as viable while identifying PostgreSQL's material operations/recovery advantage and TypeDB's semantic-model advantage. PM-08 evaluated secondary lanes. PM-09 produced:

```text
PostgreSQL 89.25
TypeDB      80.00

RANKING
ROBUST
NOT SENSITIVITY-DEPENDENT
NOT PERFORMANCE-DEPENDENT
```

PM-10 conclusion:

```text
PREFERRED PRIMARY
PostgreSQL 18.4 / PASS-CONDITIONAL

RUNNER-UP
TypeDB CE 3.12.3

SELECTED
NONE
```

PM-10 does not authorize PM-11 selection automatically.

## 7. Direct execution truth

```text
DATABASE INSTANCE
NOT STARTED

FIXTURE/HARNESS
NOT STARTED

DIRECT HG-01..HG-12
NOT RUN ALL CANDIDATES

DIRECT HG PASS
0

LOW/BASE/HIGH
NOT RUN

RESTORE
NOT RUN

MIGRATION
NOT RUN

FAILURE INJECTION
NOT RUN

GRAPH / SEARCH / VECTOR / SQLITE / POWERSYNC / RESTATE / OBJECT / SOLVER DIRECT VALIDATION
NOT RUN

BENCHMARK HOST
HOLD / DORMANT

VERIFIED-RUN BENCHMARK SCORE
NOT AVAILABLE
```

Do not convert evidence qualification, scoring or recommendation into direct PASS.

## 8. Phase-10 scoring reconciliation

The original executable Phase-10 benchmark ledger remains valid in its hard gates and weights.

```text
VERIFIED-RUN BENCHMARK SCORE
requires direct applicable HG PASS + direct execution artifacts

EVIDENCE-WEIGHTED DECISION SCORE
allowed only after evidence exhaustion and 0 ranking-critical execution-worthy gaps
```

PM-09/10 do not create direct hard-gate PASS and do not waive selected-implementation validation.

## 9. PM-10 preferred stack

### Canonical

```text
PostgreSQL 18.4
```

### PostgreSQL capabilities

```text
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2
```

### Offline / sync

```text
PowerSync Service 1.25.0 Open Edition
encrypted SQLite local state
PostgreSQL-backed PowerSync bucket storage
explicit client-safe sync projections
```

Offline rule:

```text
SQLite local copy != canonical truth
PowerSync arrival order != conflict resolution
consequential offline mutation -> LifeOS backend revalidation -> PostgreSQL
```

No universal consequential last-write-wins.

### Async / durable

```text
BOUNDED CLASS A
PostgreSQL transactional outbox + bounded worker

MATERIAL CLASS B
Restate Cloud EU
Restate Python SDK 1.0.3
Restate Server 1.7.2 reproducible local/self-hosted subject
```

### Object bytes

```text
Cloudflare R2 Standard
EU jurisdiction
private
```

PostgreSQL remains `ContentArtifact` authority. R2 stores raw bytes only.

### Recovery

```text
pgBackRest 2.59.0
-> AWS S3 Standard eu-south-1
-> Versioning
-> Object Lock GOVERNANCE
-> finite policy-bound retention

R2 object backup
-> separate AWS S3 eu-south-1 bucket
```

### Solver

```text
OR-Tools 9.15 CP-SAT
```

Candidate output only until accepted by applicable LifeOS semantics.

### Observability

```text
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

Telemetry remains privacy-minimized operational state.

## 10. Explicit PM-10 exclusions

Not part of the proposed selected Physical stack:

```text
TypeDB/XTDB/SurrealDB primary
Neo4j
Qdrant
OpenSearch
TimescaleDB
Redis/Valkey
Kafka
RabbitMQ
NATS
Debezium
dedicated event store
universal event sourcing
Temporal
DBOS
Celery + broker
Zero sync
Electric as full LifeOS mutation/sync engine
CRDT/local-first canonical authority
MongoDB for PowerSync
large bytea as standard object store
public R2
separate vector/graph/search server
data lake/Spark/Hudi
pg_cron as workflow system
Object Lock Compliance as default
```

These are not hidden deferred dependencies. Reintroduction requires a new explicit architecture decision with material evidence.

## 11. Post-selection validation obligations

The authoritative expanded register is:

```text
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

It includes at minimum:

```text
SC-011 anti-resurrection
SC-030 V1->V2 evolution
SC-031 destructive semantic restore
SC-032 capacity/backpressure
WL-H12 non-interference
search/vector/projection filtering/freshness/deletion
PowerSync replication liveness / conflicts / local encryption
Restate crash/replay/versioning/governance
R2/S3 object deletion/recovery
PostGIS/PgBouncer compatibility
pgBackRest archive/PITR
OR-Tools status/governance corpus
observability privacy
```

None is a direct PASS today.

## 12. PM-10 evidence paths

```text
docs/physical-model/pm-10-recommendation-v1.md
docs/physical-model/final-stack-audit-v1.md
docs/physical-model/final-stack-capability-matrix-v1.md
docs/physical-model/final-stack-simulation-v1.md
docs/physical-model/recommendation/postgresql-18.4-v1.md
docs/physical-model/recommendation/companion-stack-v1.md
docs/physical-model/recommendation/technology-exclusion-register-v1.md
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

## 13. Roadmap

```text
PM-00  PASS
PM-01  PASS-CONDITIONAL
PM-02  COMPLETE
PM-03  COMPLETE
PM-04A COMPLETE
PM-04B NOT ADMITTED
PM-05  COMPLETE
PM-06  COMPLETE
PM-07  COMPLETE
PM-08  COMPLETE
PM-09  COMPLETE
PM-10  COMPLETE
PM-11  NEXT
PM-12  NOT STARTED
PM-13  NOT STARTED
PM-14  NOT STARTED
```

## 14. Current resume summary

```text
ACTIVE WORKSTREAM
Physical Model

BRANCH
feature/physical-model

DOMAIN
CLOSED

LOGICAL
CLOSED / WL-H01..WL-H12 ACTIVE

PM-09 EVIDENCE SCORES
PostgreSQL 89.25
TypeDB 80.00

RANKING
ROBUST / NOT SENSITIVITY-DEPENDENT / NOT PERFORMANCE-DEPENDENT

PM-10 PREFERRED PRIMARY
PostgreSQL 18.4 / PASS-CONDITIONAL

PM-10 COMPANION STACK
ESTABLISHED / PASS-CONDITIONAL

LOCAL TESTS
0 ADMITTED

DIRECT HG PASS
0

VERIFIED-RUN SCORE
NOT AVAILABLE

SELECTED
NONE

BACKEND
NOT STARTED / DEFERRED

NEXT
PM-11 explicit user-approved stack selection
fresh exact gate before write
```

The exact PM-10 final remote HEAD must be taken from Git after this handoff write.
