# Workstream — Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-05 COMPLETE / PM-06+PM-07 JOINT NEXT**
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
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Deferred primary challengers: **XTDB 2.1.0 + SurrealDB Community 3.2.3 — NOT REJECTED**
- Direct hard-gate execution: **NOT RUN**
- Database/harness execution: **NOT STARTED**
- Benchmark/performance execution: **NOT STARTED**
- Primary persistence selected: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## 1. Purpose

This file is the terminal save-game for the active Physical Model workstream.

A new chat/agent must be able to resume from repository truth without reconstructing conversation history.

The workstream currently performs:

```text
technology discovery
candidate-native mapping
semantic pressure
external-evidence sufficiency
correctness/destructive scenario qualification
primary finalist narrowing
joint scale/recovery finalist qualification
secondary-lane justification
scoring/sensitivity
recommendation
explicit selection
accepted Physical Model
clean-room QA
protected-main integration
```

It does **not** authorize production backend/API/Auth implementation.

## 2. Mandatory continuation bootstrap

Before any further Physical write/action:

1. verify actual remote `feature/physical-model` HEAD;
2. compare branch with current `main` and confirm `behind_by` truth;
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
13. read `docs/physical-model/execution-template-v1.md`;
14. read `docs/physical-model/acceptance-test-matrix-v1.md`;
15. read `docs/physical-model/result-register-v1.md`;
16. read PM-01 landscape;
17. read PM-02 overview + all four mapping records;
18. read PM-03 overview + all four preflight records;
19. read PM-04A overview + all four evidence records;
20. read PM-05 overview + all four qualification records;
21. read Phase-10 benchmark specification, scenario corpus and register;
22. when semantics are involved, read complete Whole-Logical authority and relevant decision-register continuations;
23. verify current external product/version/edition/topology facts from primary sources where material;
24. issue a fresh exact PRE-SCOPE/write gate before any repository write.

Conversation memory is secondary to repository truth.

## 3. Non-negotiable semantic/evidence guardrails

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
EXTERNAL EVIDENCE != DIRECT LIFEOS RUN
PUBLIC/VENDOR BENCHMARK != LIFEOS BENCHMARK
EVIDENCE-QUALIFIED != EXECUTED HARD-GATE PASS
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
missing row == false
storage/MVCC/system-time/changefeed token == MaterialStateRef
technical AuthZ allow/deny == Domain Authority/Consent
AI/solver result == accepted canonical effect
per-recipient duplicate canonical reality
```

Reference families remain:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

State layers remain:

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
4. maturity/operability/Python tooling;
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

Final architecture may be:

```text
one primary canonical store
+
bounded specialists only where each earns complexity
```

No secondary engine may compensate for a primary semantic/integrity failure.

## 5. Historical phase checkpoints

```text
MAIN BASELINE
3de84bb49f9cef30e88e9bde4961ed84335daa79

PM-00 create checkpoint
6d76bc150dfd7b3cefe56c6e05c96404e7494626

PM-00 content-QA checkpoint
8549e1c95bef2e354bd47028259e6816bf5e9272

PM-00 QA-status checkpoint
f5e7f5c3ea38dd02b54192705575b0a48ea3854c

PM-01 terminal
fac3b5baf1813f886c4773594e6234810e5ba8c6

PM-02 terminal
db127af8c759aacf69b43d0f5a5444b04fd43759

PM-03 terminal
0e4212909bd94de076c9074302a79296d474e53f

PM-04A terminal
44d331f12951e2844186e6f5f885e1bcf1559a3b

PM-05 PRE-SCOPE
44d331f12951e2844186e6f5f885e1bcf1559a3b
```

The exact final PM-05 HEAD is determined by Git after this handoff write and must not be guessed inside its own creating commit.

## 6. PM-01 — candidate subjects

```text
P0 PostgreSQL 18.4
self-hosted single-node / psycopg 3.3.4

P1 TypeDB CE 3.12.3
self-hosted single-node / driver 3.12.3

P2 XTDB 2.1.0
self-hosted qualification subject
production topology HOLD

P3 SurrealDB Community 3.2.3
single-node RocksDB / Python SDK 2.0.0
```

Primary reserves remain deferred: MariaDB 11.8 LTS, Gel 7, CockroachDB, YugabyteDB.

Secondary candidates remain PM-08/trigger-only: Neo4j, pgvector, Qdrant/OpenSearch, SQLite bounded local/offline.

## 7. PM-02 — mapping state

```text
P0 PM02-PG-001 COMPLETE
P1 PM02-TDB-001 COMPLETE
P2 PM02-XT-001 COMPLETE
P3 PM02-SDB-001 COMPLETE
```

No PM-02 mapping is selected merely by existence.

## 8. PM-03 — static preflight state

```text
STATIC PREFLIGHT COMPLETE
STATIC REJECTS 0
DIRECT HG NOT RUN
```

Candidate-specific static pressures were:

```text
PostgreSQL
no candidate-specific blocker

TypeDB
HG-04/HG-05 concurrency

XTDB
HG-02/HG-03 reference/cardinality

SurrealDB
HG-04/HG-05 concurrency
```

## 9. PM-04A — evidence sufficiency state

```text
48 / 48 candidate × HG cells CLASSIFIED
EXECUTION-WORTHY gaps 0
FULL LOCAL BENCHMARK NOT ADMITTED
TARGETED LOCAL PROOFS 0 ADMITTED
PM-04B NOT ADMITTED
BENCHMARK HOST HOLD / DORMANT
```

Key comparative state after PM-04A:

```text
1 PostgreSQL
2 TypeDB
3 XTDB
4 SurrealDB
```

This ordering was non-scored and not `PREFERRED`/`SELECTED`.

## 10. PM-05 — correctness/destructive evidence qualification

Evidence:

```text
docs/physical-model/pm-05-correctness-evidence-qualification-v1.md
docs/physical-model/qualification/postgresql-18.4-v1.md
docs/physical-model/qualification/typedb-3.12.3-v1.md
docs/physical-model/qualification/xtdb-2.1.0-v1.md
docs/physical-model/qualification/surrealdb-3.2.3-v1.md
```

### Corpus disposition

```text
C0 PRIMARY-EVIDENCE-SUFFICIENT
C1 PRIMARY-EVIDENCE-SUFFICIENT + finalist scale
C2 PRIMARY-EVIDENCE-SUFFICIENT + candidate known costs
C3 persistence sufficient / full WL-H12 SYSTEM-BOUNDARY
C4 SYSTEM-BOUNDARY
C5 PRIMARY-EVIDENCE-SUFFICIENT
C6 primary baseline / PM-08 specialist work
C7 PM-06/07-FINALIST
```

### Primary semantic scenarios

```text
SC-001 SC-002 SC-003 SC-009 SC-010 SC-012
SC-014 SC-015 SC-016 SC-022 SC-023 SC-024
```

Result:

```text
EVIDENCE-QUALIFIED FOR CURRENT PRIMARY COMPARISON
DIRECT EXECUTION NOT REQUIRED NOW
```

### System/runtime/provider scenarios

```text
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034
```

Result: `SYSTEM-BOUNDARY` — real obligations, but not four-database local benchmark reasons.

### PM-06/07 finalist scenarios

```text
SC-011 old-backup anti-resurrection
SC-013 deep-history current-state scale
SC-030 V1 -> V2 evolution
SC-031 backup/restore semantic verification
SC-032 capacity/backpressure
```

### PM-08 secondary scenarios

```text
SC-017 SC-018 SC-019 SC-020 SC-021 SC-035
```

### PM-05 execution admission

```text
EXECUTION-WORTHY gaps 0
PM-04B NOT REOPENED
DATABASE/HARNESS NOT STARTED
DIRECT HG PASS 0
```

## 11. Primary finalist set after PM-05

### P0 PostgreSQL 18.4

```text
PRIMARY FINALIST
ADVANCE PM-06/07 JOINT
NOT PREFERRED
NOT SELECTED
```

Current strengths:

- native integrity/constraint ecosystem;
- true Serializable/locking paths;
- mature recovery/operations tooling;
- lowest aggregate primary-store structural burden.

Carry forward:

- heterogeneous anchors must stay technical;
- operation-specific transaction strength;
- WL-H12 system proof;
- finalist scale/recovery/evolution/TCO.

### P1 TypeDB CE 3.12.3

```text
PRIMARY FINALIST
ADVANCE PM-06/07 JOINT
CONDITION narrow consistency-guard coverage required
NOT PREFERRED
NOT SELECTED
```

Current strengths:

- strongest relation/role/n-ary semantic fit;
- natural Agreement/common-ground mapping;
- schema-level role/cardinality semantics.

Carry forward:

- snapshot isolation remains engine model;
- correct consistency-guard scoping remains mandatory;
- explicit history/material states;
- operations/recovery/tooling comparison against PostgreSQL.

### P2 XTDB 2.1.0

```text
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED
NOT SELECTED
PRODUCTION TOPOLOGY HOLD remains
```

Reason: strong bitemporal/serialized-write proposition does not currently offset no-FK/no-general-uniqueness, manual integrity discipline, transaction ergonomics and topology burden enough to justify finalist scope.

Reopen triggers:

```text
native bitemporal value becomes decision-dominant
or finalists expose material temporal weakness
or XTDB integrity/topology capability materially changes
or later sensitivity shows recommendation-changing value
```

### P3 SurrealDB Community 3.2.3

```text
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED
NOT SELECTED
```

Reason: credible multimodel design, but no unique primary-store advantage currently offsets guard/history/operations burden enough for finalist scope.

Reopen triggers:

```text
multimodel consolidation becomes decision-changing
or finalists expose a material capability gap SurrealDB solves
or relevant engine capability materially changes
or later TCO/sensitivity evidence changes the recommendation
```

## 12. Direct execution truth

```text
P0 PostgreSQL HG-01..HG-12 NOT RUN
P1 TypeDB HG-01..HG-12     NOT RUN
P2 XTDB HG-01..HG-12       NOT RUN
P3 SurrealDB HG-01..HG-12  NOT RUN

LOW/BASE/HIGH
NOT RUN

DATABASE INSTANCE
NOT STARTED

FIXTURE/HARNESS
NOT STARTED
```

Do not promote external/mapping/scenario qualification to executed PASS.

## 13. Benchmark host

```text
BENCHMARK HOST
HOLD / DORMANT
```

Not a blocker for evidence-only work. It becomes blocking only before an admitted reproducible direct run.

Then freeze:

```text
host identity
CPU/RAM
storage/filesystem/free disk
OS/build/kernel
container/native runtime
network/topology
resource limits
background-load policy
clock/timezone
```

Never infer the host from remembered conversation hardware.

## 14. PM-06 + PM-07 Joint Finalist Qualification — NEXT

User-authorized process revision:

```text
PM-06 and PM-07 are one operational finalist evidence campaign
BUT remain two separate result layers
```

Finalists:

```text
PostgreSQL 18.4
TypeDB CE 3.12.3
```

### PM-06 result layer

Evaluate evidence for:

```text
scale/history efficiency
performance/resource behavior
contention sensitivity
storage/index growth
topology/resource cliffs
published/production performance quality
```

No direct LOW/BASE/HIGH execution is assumed.

### PM-07 result layer

Evaluate evidence for:

```text
backup/restore
anti-resurrection
evolution/migration
historical reference preservation
failure/backpressure
operations/HA/topology
RPO/RTO capability sensitivity
```

A documented backup feature is not a direct LifeOS restore/anti-resurrection PASS.

### Joint evidence order

```text
authoritative product/operations evidence
+ credible production evidence
+ published benchmark evidence with method/bias disclosed
+ LifeOS mapping implications
        ↓
residual ranking-critical question?
        ↓ only if yes and test-resolvable
fresh PM-04B/direct execution gate
```

Performance can never compensate for a PM-07 integrity/recovery failure.

## 15. Roadmap

```text
PM-00  PASS
PM-01  PASS-CONDITIONAL
PM-02  COMPLETE
PM-03  COMPLETE
PM-04A COMPLETE
PM-04B NOT ADMITTED
PM-05  COMPLETE
PM-06  NEXT — JOINT WITH PM-07
PM-07  NEXT — JOINT WITH PM-06
PM-08  NOT STARTED
PM-09  NOT STARTED
PM-10  NOT STARTED
PM-11  NOT STARTED
PM-12  NOT STARTED
PM-13  NOT STARTED
PM-14  NOT STARTED
```

## 16. Exact current resume summary

```text
REPO
MattiaRubino/lifeos

BRANCH
feature/physical-model

MAIN BASELINE
3de84bb49f9cef30e88e9bde4961ed84335daa79

PM-05 PRE-SCOPE
44d331f12951e2844186e6f5f885e1bcf1559a3b

PM-05
CONTENT WRITTEN
FINAL REMOTE QA REQUIRED AFTER THIS HANDOFF WRITE

PRIMARY FINALISTS
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3

DEFERRED / NOT REJECTED
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3

PM-05 EXECUTION-WORTHY gaps
0

PM-04B
NOT REOPENED

DIRECT HG
NOT RUN ALL CANDIDATES

DATABASE/HARNESS
NOT STARTED

BENCHMARK HOST
HOLD / DORMANT

SELECTION
NONE

BACKEND
NOT STARTED / DEFERRED

NEXT
PM-06 + PM-07 JOINT FINALIST QUALIFICATION
fresh exact gate required
EVIDENCE-FIRST
NO local execution by default
```

The final validated PM-05 HEAD must be taken from the remote branch after final compare/readback QA.
