# Physical Model Result Register v1

- Status: **CURRENT — PM-03 STATIC PREFLIGHT COMPLETE / EXECUTED HARD GATES NOT RUN**
- Workstream: `feature/physical-model`
- Benchmark execution: **NOT STARTED**
- Technology selection: **NONE**
- PM-01 evidence: `pm-01-technology-landscape-v1.md`
- PM-02 evidence: `pm-02-primary-mapping-overview-v1.md` + candidate mappings
- PM-03 evidence: `pm-03-semantic-hard-gate-preflight-v1.md` + candidate preflight records

## 1. Result-language rule

```text
OFFICIAL CLAIM != EXECUTED PROOF
ADMIT != HARD-GATE PASS
MAPPING COMPLETE != HARD-GATE PASS
PM-03 PASS-CONDITIONAL != EXECUTED PASS
NOT RUN != PASS
PREFERRED != SELECTED
```

PM-03 is a static mapping preflight. Executed hard-gate results remain `NOT RUN` until direct scenario evidence exists.

## 2. Current phase state

```text
PM-00
QA PASS

PM-01
PASS-CONDITIONAL
benchmark host HOLD

PM-02
PRIMARY MAPPING DESIGN COMPLETE

PM-03
STATIC PREFLIGHT COMPLETE
0 candidate REJECTs

PM-04
NOT STARTED

PM-05+
NOT STARTED

PERFORMANCE
NOT STARTED

SELECTION
NONE
```

## 3. PM-03 cross-candidate preflight result

| Gate | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB |
|---|---|---|---|---|
| HG-01 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-02 | PASS-CONDITIONAL | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL |
| HG-03 | PASS-CONDITIONAL | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL |
| HG-04 | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL | HOLD |
| HG-05 | PASS-CONDITIONAL | HOLD | PASS-CONDITIONAL | HOLD |
| HG-06 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-07 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-08 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-09 | HOLD | HOLD | HOLD | HOLD |
| HG-10 | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL | PASS-CONDITIONAL |
| HG-11 | HOLD | HOLD | HOLD | HOLD |
| HG-12 | HOLD | HOLD | HOLD | HOLD |

This table records static preflight only.

## 4. Executed hard-gate status

```text
P0 PostgreSQL HG-01..HG-12   NOT RUN
P1 TypeDB HG-01..HG-12       NOT RUN
P2 XTDB HG-01..HG-12         NOT RUN
P3 SurrealDB HG-01..HG-12    NOT RUN
```

No candidate is score-eligible.

## 5. P0 — PostgreSQL 18.4

```text
ROLE
mandatory preferred baseline

EXACT SUBJECT
PostgreSQL 18.4
self-hosted single-node qualification topology
psycopg 3.3.4

PM-01
ADMIT

PM-02 MAPPING
PM02-PG-001 COMPLETE

PM-03 PREFLIGHT
9 PASS-CONDITIONAL
3 HOLD
0 REJECT

CANDIDATE-SPECIFIC STATIC BLOCKER
NONE

GENERIC EXECUTION HOLDS
HG-09 retention/restore
HG-11 evolution
HG-12 recoverability

EXECUTED HG
NOT RUN

SCORE
NOT RUN

CURRENT DISPOSITION
ADVANCE / PRE-EXISTING PREFERRED BASELINE / NOT SELECTED
```

Primary executable risks:

- heterogeneous address-anchor family/existence integrity;
- same-base/predicate race behavior under selected transaction pattern;
- non-interference when constraints/RLS/application filtering interact;
- history structure maintainability.

## 6. P1 — TypeDB CE 3.12.3

```text
ROLE
mandatory semantic challenger

EXACT SUBJECT
TypeDB CE 3.12.3
self-hosted single-node qualification topology
official driver 3.12.3

PM-01
ADMIT

PM-02 MAPPING
PM02-TDB-001 COMPLETE

PM-03 PREFLIGHT
7 PASS-CONDITIONAL
5 HOLD
0 REJECT

CANDIDATE-SPECIFIC HOLDS
HG-04 expected-state/predicate concurrency
HG-05 multi-owner write-skew consistency

GENERIC EXECUTION HOLDS
HG-09 HG-11 HG-12

EXECUTED HG
NOT RUN

SCORE
NOT RUN

CURRENT DISPOSITION
ADVANCE WITH CONCURRENCY HOLD / NOT SELECTED
```

The narrow `consistency-guard` design must be executed. Snapshot-isolation documentation alone is not sufficient.

## 7. P2 — XTDB 2.1.0

```text
ROLE
PM-01-admitted temporal/bitemporal challenger

EXACT SUBJECT
XTDB 2.1.0
self-hosted qualification subject
Postgres-wire client path where applicable

PM-01
ADMIT / PRODUCTION TOPOLOGY HOLD

PM-02 MAPPING
PM02-XT-001 COMPLETE

PM-03 PREFLIGHT
7 PASS-CONDITIONAL
5 HOLD
0 REJECT

CANDIDATE-SPECIFIC HOLDS
HG-02 reference-family enforcement
HG-03 role/cardinality/uniqueness enforcement

GENERIC EXECUTION HOLDS
HG-09 HG-11 HG-12

PRODUCTION TOPOLOGY
HOLD

EXECUTED HG
NOT RUN

SCORE
NOT RUN

CURRENT DISPOSITION
ADVANCE WITH REFERENCE/CONSTRAINT HOLD / NOT SELECTED
```

Serialized DML transactions + `ASSERT` provide a strong path for HG-04/HG-05, but conventional FK/cardinality safety is not assumed.

## 8. P3 — SurrealDB Community 3.2.3

```text
ROLE
PM-01-admitted constrained multimodel challenger

EXACT SUBJECT
SurrealDB Community 3.2.3
single-node RocksDB qualification topology
Python SDK 2.0.0

PM-01
ADMIT-CONDITIONAL

PM-02 MAPPING
PM02-SDB-001 COMPLETE

PM-03 PREFLIGHT
7 PASS-CONDITIONAL
5 HOLD
0 REJECT

CANDIDATE-SPECIFIC HOLDS
HG-04 expected-state/predicate concurrency
HG-05 multi-owner write-skew consistency

GENERIC EXECUTION HOLDS
HG-09 HG-11 HG-12

EXECUTED HG
NOT RUN

SCORE
NOT RUN

CURRENT DISPOSITION
ADVANCE WITH CONCURRENCY HOLD / NOT SELECTED
```

The `consistency_guard` design and recipient/system-user disclosure boundary require direct proof.

## 9. Static preflight interpretation

```text
PostgreSQL
lowest static primary risk among current mappings
NOT a winner

TypeDB
strongest relation/role semantic mapping
concurrency guard is material uncertainty

XTDB
strongest native chronology/serialized-write hypothesis
reference/cardinality enforcement is material uncertainty

SurrealDB
multimodel mapping survives only under strict SCHEMAFULL/specific-relation discipline
concurrency guard is material uncertainty
```

This section is qualitative pressure, not scoring.

## 10. Required next executable proof themes

```text
COMMON
SC-001 stale-base race
SC-003 atomic multi-owner mutation
SC-009 offline/stale divergence
SC-010 correction without false rewrite
SC-012 NativeRef non-reuse
SC-015 n-ary relation fidelity
SC-016 selective disclosure
SC-022/023 DST gap/fold
SC-024 occurrence override
SC-030 V1->V2 evolution
SC-011/031 restore + anti-resurrection

P1 TypeDB
write-skew negative control + shared guard positive control

P2 XTDB
wrong-family/missing reference + cardinality/uniqueness ASSERT pressure

P3 SurrealDB
write-skew negative control + shared guard positive control

P0 PostgreSQL
anchor integrity + Read-Committed negative control + stronger transaction positive control
```

## 11. Secondary lanes

### Graph

```text
G0 primary-store/no-specialized-store baseline
G1 Neo4j DEFER TO PM-08
```

No graph store is selected or admitted as canonical primary by PM-03.

### Search/vector

```text
S0 primary-native structured/lexical baseline
pgvector DEFER TO PM-08 when PostgreSQL is applicable
Qdrant/OpenSearch specialist trigger only
```

### Local/offline

```text
SQLite
DEFER — future bounded local/client role
```

### Durable runtime

```text
Restate  NOT SELECTED
Temporal NOT SELECTED
DBOS     NOT SELECTED
```

Persistence preflight does not select workflow runtime.

## 12. PM-00 / PM-01 / PM-02 checkpoints

```text
MAIN BASELINE
3de84bb49f9cef30e88e9bde4961ed84335daa79

PM-00 create checkpoint
6d76bc150dfd7b3cefe56c6e05c96404e7494626

PM-00 content-QA checkpoint
8549e1c95bef2e354bd47028259e6816bf5e9272

PM-00 QA-status checkpoint
f5e7f5c3ea38dd02b54192705575b0a48ea3854c

PM-01 research PRE-SCOPE
622767d5435d59766459bb25a57e5afeb7dd7336

PM-01 terminal handoff before PM-02
fac3b5baf1813f886c4773594e6234810e5ba8c6

PM-02 PRE-SCOPE
fac3b5baf1813f886c4773594e6234810e5ba8c6

PM-02 terminal HEAD
 db127af8c759aacf69b43d0f5a5444b04fd43759
```

## 13. PM-03 evidence paths

```text
docs/physical-model/pm-03-semantic-hard-gate-preflight-v1.md
docs/physical-model/preflight/postgresql-18.4-v1.md
docs/physical-model/preflight/typedb-3.12.3-v1.md
docs/physical-model/preflight/xtdb-2.1.0-v1.md
docs/physical-model/preflight/surrealdb-3.2.3-v1.md
```

The final PM-03 commit/remote-QA checkpoint is recorded in the workstream handoff after verification.

## 14. Result mutation protocol

Before changing any executed hard-gate from `NOT RUN`:

1. freeze actual benchmark host/runtime;
2. identify exact mapping/schema/harness revision;
3. identify scenario/corpus/fixture revision and seed;
4. retain raw assertion/concurrency output;
5. classify candidate-specific failure versus tooling/environment failure;
6. update only evidence-backed gates;
7. preserve unresolved items as HOLD;
8. remote-read back register and evidence;
9. never award performance score before applicable hard gates pass.

Before `SELECTED`, PM-11 explicit user-approved gate remains mandatory.

## 15. Current next step

```text
PM-03
STATIC PREFLIGHT COMPLETE
REMOTE QA REQUIRED FOR THIS WRITE SCOPE

PM-04
NOT STARTED

BENCHMARK HOST
HOLD — must close before reproducible executable evidence

NO PERFORMANCE
NO SELECTION
NO PRODUCTION BACKEND
```
