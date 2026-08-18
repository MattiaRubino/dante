# Workstream — Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-08 COMPLETE / PM-09 NEXT**
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
- PM-08: **SECONDARY/SPECIALIST LANE QUALIFICATION COMPLETE / NO DIRECT RUN**
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Deferred primary challengers: **XTDB 2.1.0 + SurrealDB Community 3.2.3 — NOT REJECTED**
- Current comparative leader: **PostgreSQL 18.4**
- Initial extra server specialists admitted: **0**
- pgvector 0.8.6: **ADMIT-CONDITIONAL**
- SQLite 3.53.4: **ADMIT BOUNDED LOCAL/OFFLINE CANDIDATE / NOT CANONICAL**
- Preferred: **NONE**
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
12. read `docs/physical-model/execution-methodology-v1.md`;
13. read `docs/physical-model/execution-template-v1.md` when direct evidence is relevant;
14. read `docs/physical-model/acceptance-test-matrix-v1.md`;
15. read `docs/physical-model/result-register-v1.md`;
16. read PM-01 landscape;
17. read PM-02 overview + all four mapping records;
18. read PM-03 overview + all four preflight records;
19. read PM-04A overview + all four evidence records;
20. read PM-05 overview + all four candidate qualification records;
21. read PM-06/07 joint overview + PM-06 + PM-07 + two finalist qualification records;
22. read PM-08 overview + graph/search-vector/local-offline/specialist-trigger records;
23. read Phase-10 benchmark specification/scenario corpus/register where scenario authority matters;
24. read complete Whole-Logical authority and relevant decision-register continuations when semantics are involved;
25. verify current external product/version/edition/topology facts from primary sources where material;
26. issue a fresh exact PRE-SCOPE/write gate before repository mutation.

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
MISSING != FALSE
EXTERNAL EVIDENCE != DIRECT LIFEOS RUN
PUBLIC/VENDOR BENCHMARK != LIFEOS BENCHMARK
EVIDENCE-QUALIFIED != EXECUTED HARD-GATE PASS
ADMIT != SELECTED
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
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

Decision order:

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

BUT
free != automatic preference
paid != automatic rejection
quality/correctness outrank cost
```

Final architecture may use one canonical primary plus bounded specialists. Every extra engine must earn complexity; no specialist may hide a primary hard-gate problem.

## 5. Historical checkpoints

```text
MAIN BASELINE
3de84bb49f9cef30e88e9bde4961ed84335daa79

PM-00 create
6d76bc150dfd7b3cefe56c6e05c96404e7494626

PM-00 content-QA
8549e1c95bef2e354bd47028259e6816bf5e9272

PM-00 QA-status
f5e7f5c3ea38dd02b54192705575b0a48ea3854c

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

PM-08 PRE-SCOPE
1e19793fdb9f51ba510f00ac4c927a6907e28c4b
```

The PM-08 terminal SHA must be taken from remote Git after this write scope and is not guessed inside its own creating payload.

## 6. Primary candidate history

PM-01 admitted:

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3
```

PM-02 completed candidate-native mappings for all four.

PM-03 produced 0 static rejects.

PM-04A classified all 48 candidate × HG cells and found 0 execution-worthy gaps.

PM-05 narrowed the primary finalist set:

```text
FINALISTS
PostgreSQL 18.4
TypeDB CE 3.12.3

DEFERRED / NOT REJECTED
XTDB 2.1.0
SurrealDB Community 3.2.3
```

## 7. PM-06/07 Joint Finalist Qualification

No local database execution was admitted.

### PM-06

```text
PostgreSQL
SCALE/PERFORMANCE VIABLE
confidence HIGH

TypeDB CE
SCALE/PERFORMANCE VIABLE
confidence MEDIUM-HIGH

LOW/BASE/HIGH
NOT RUN

performance-based reversal signal
NONE
```

### PM-07

```text
PostgreSQL
CLEAR OPERATIONS/RECOVERY/TOPOLOGY ADVANTAGE

TypeDB CE
RECOVERY/EVOLUTION VIABLE
HIGHER SELF-HOSTED OPERATIONS COST
```

Comparative result:

```text
POSTGRESQL
OVERALL LEAD STRENGTHENED

TYPEDB
SEMANTIC ADVANTAGE PRESERVED
PRINCIPAL CHALLENGER
```

The primary decision remains open.

## 8. PM-08 Secondary / Specialist Qualification

Status: **COMPLETE — EVIDENCE-FIRST / NO DIRECT EXECUTION**.

### Graph

```text
G0 primary-store baseline
ADVANCE

Neo4j
DEFER / NOT REJECTED
NO INITIAL GRAPH SPECIALIST
```

No accepted graph workload currently justifies a second graph persistence/service boundary.

Reopen only on decision-relevant graph traversal/recommendation/pathfinding/analytics or material primary-store graph isolation/performance pressure.

### Search / vector

```text
PostgreSQL native FTS
ADVANCE as P0 lexical baseline

pgvector 0.8.6
ADMIT-CONDITIONAL
PostgreSQL selected + accepted vector retrieval requirement

Qdrant 1.18.2
DEFER / NOT REJECTED / TRIGGER ONLY

OpenSearch 3.7
DEFER / NOT REJECTED / TRIGGER ONLY
```

Embedding/vector state is derived state. Real scope/Visibility filtering remains mandatory before exposing ranked results.

TypeDB retains its semantic advantage but is more likely to require a separate search/vector service once those capabilities are accepted. That probable extra server topology is carried into PM-09.

### Local / offline

```text
SQLite 3.53.4
ADMIT BOUNDED LOCAL/OFFLINE CANDIDATE
CANONICAL AUTHORITY NO
EXACT CLIENT ADAPTER DEFER
```

Local state may improve offline/client behavior but never becomes competing canonical truth or a default last-write-wins authority.

### Object/blob

```text
NO ENGINE ADMITTED NOW
DEFER / TRIGGER ONLY
```

Reopen only when concrete object type/size/volume/retention/security/distribution/durability requirements exist.

### Initial stack pressure

If PostgreSQL wins:

```text
PostgreSQL 18.4
canonical primary
+ native FTS
+ pgvector when required

SQLite 3.53.4
bounded local/offline when required

INITIAL EXTRA SERVER ENGINES
0
```

If TypeDB wins:

```text
TypeDB CE 3.12.3
canonical primary
+ likely external search/vector specialist when required

SQLite 3.53.4
bounded local/offline when required
```

No `PREFERRED` or `SELECTED` status is inferred from this architecture pressure.

## 9. Direct execution truth

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

GRAPH / SEARCH / VECTOR / SQLITE BENCHMARKS
NOT RUN

BENCHMARK HOST
HOLD / DORMANT
```

Do not convert evidence qualification to direct PASS.

## 10. Validation obligations / reopen triggers

Post-selection implementation validation remains mandatory where applicable:

```text
SC-011 redaction + old-backup anti-resurrection
SC-030 actual LifeOS V1→V2 mapping evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure truthful degradation
WL-H12 system-level non-interference
SC-017/018 search/non-interference
SC-019 filtered vector recall when active
SC-020/021 projection freshness/deletion propagation when active
local/offline sync/reconciliation validation when active
```

`SC-013` deep-history scale reopens before selection only if PM-09 becomes materially performance-sensitive.

`SC-035` reopens only if a graph specialist is later admitted.

## 11. PM-08 evidence paths

```text
docs/physical-model/pm-08-secondary-lanes-v1.md
docs/physical-model/secondary/graph-lane-v1.md
docs/physical-model/secondary/search-vector-lane-v1.md
docs/physical-model/secondary/local-offline-lane-v1.md
docs/physical-model/secondary/specialist-trigger-register-v1.md
```

## 12. Roadmap

```text
PM-00  PASS
PM-01  PASS-CONDITIONAL
PM-02  COMPLETE
PM-03  COMPLETE
PM-04A COMPLETE
PM-04B NOT ADMITTED
PM-05  COMPLETE
PM-06  COMPLETE — evidence qualification
PM-07  COMPLETE — evidence qualification
PM-08  COMPLETE — specialist qualification
PM-09  NEXT
PM-10  NOT STARTED
PM-11  NOT STARTED
PM-12  NOT STARTED
PM-13  NOT STARTED
PM-14  NOT STARTED
```

## 13. Write discipline

For every next write:

```text
BRANCH
feature/physical-model unless explicitly changed

PRE-SCOPE
actual remote HEAD immediately before write

CREATE
exact allow-list

UPDATE
exact allow-list

DELETE
exact allow-list
```

After write: compare PRE-SCOPE→HEAD, verify mutation/path set, verify branch-vs-main, remotely read back critical claims, then update/save handoff last where practical.

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

PRIMARY FINALISTS
PostgreSQL 18.4
TypeDB CE 3.12.3

CURRENT LEADER
PostgreSQL 18.4

DEFERRED / NOT REJECTED PRIMARY
XTDB 2.1.0
SurrealDB Community 3.2.3

PM-06
COMPLETE / NO DIRECT PERFORMANCE RUN

PM-07
COMPLETE / NO DIRECT DESTRUCTIVE RUN

PM-08
COMPLETE / NO DIRECT SPECIALIST RUN

INITIAL GRAPH SPECIALIST
NONE

POSTGRESQL SEARCH PATH
native FTS + pgvector conditional

LOCAL/OFFLINE
SQLite 3.53.4 admitted bounded candidate / not canonical

DEFERRED/TRIGGER-ONLY SPECIALISTS
Neo4j
Qdrant 1.18.2
OpenSearch 3.7
object/blob TBD

LOCAL TESTS
0 ADMITTED

PREFERRED
NONE

SELECTED
NONE

BACKEND
NOT STARTED / DEFERRED

NEXT
PM-09 scoring + sensitivity
fresh exact gate before write
```

The exact PM-08 final remote HEAD must be taken from Git after this handoff write.