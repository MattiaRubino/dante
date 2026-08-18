# Physical Model Result Register v1

- Status: **CURRENT — PM-05 COMPLETE / PM-06+PM-07 JOINT NEXT**
- Workstream: `feature/physical-model`
- Direct benchmark execution: **NOT STARTED**
- Primary finalist set: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Deferred primary challengers: **XTDB 2.1.0 + SurrealDB Community 3.2.3 — NOT REJECTED**
- Technology selection: **NONE**

## 1. Result-language rule

```text
OFFICIAL CLAIM != DIRECT EXECUTION
ADMIT != HARD-GATE PASS
MAPPING COMPLETE != HARD-GATE PASS
PM-03 PASS-CONDITIONAL != DIRECT PASS
PM-04A EXT/MAP-SUFFICIENT != DIRECT PASS
PM-05 EVIDENCE-QUALIFIED != DIRECT PASS
PUBLIC BENCHMARK != LIFEOS BENCHMARK
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
NOT RUN != PASS
```

## 2. Current phase state

```text
PM-00   QA PASS
PM-01   PASS-CONDITIONAL
PM-02   PRIMARY MAPPING DESIGN COMPLETE
PM-03   STATIC PREFLIGHT COMPLETE / 0 STATIC REJECTS
PM-04A  EVIDENCE SUFFICIENCY COMPLETE / 48 OF 48 CELLS CLASSIFIED
PM-04B  NOT ADMITTED / HARNESS NOT STARTED
PM-05   CORRECTNESS/DESTRUCTIVE EVIDENCE QUALIFICATION COMPLETE

PM-05 EXECUTION-WORTHY GAPS
0

PRIMARY FINALISTS
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3

DEFERRED / NOT REJECTED
P2 XTDB 2.1.0
P3 SurrealDB Community 3.2.3

PM-06 + PM-07
JOINT FINALIST QUALIFICATION NEXT

PM-08+
NOT STARTED

DIRECT PERFORMANCE
NOT STARTED

SELECTION
NONE
```

Benchmark host remains `HOLD / DORMANT` until a direct run is separately admitted.

## 3. Evidence chain

```text
PM-01
docs/physical-model/pm-01-technology-landscape-v1.md

PM-02
docs/physical-model/pm-02-primary-mapping-overview-v1.md
+ mappings/*

PM-03
docs/physical-model/pm-03-semantic-hard-gate-preflight-v1.md
+ preflight/*

PM-04A
docs/physical-model/pm-04-external-evidence-sufficiency-v1.md
+ evidence/*

PM-05
docs/physical-model/pm-05-correctness-evidence-qualification-v1.md
+ qualification/*
```

Historical layers remain truthful and are not rewritten into direct execution results.

## 4. Direct hard-gate status

No direct LifeOS database correctness/destructive execution has occurred.

```text
P0 PostgreSQL HG-01..HG-12   NOT RUN
P1 TypeDB HG-01..HG-12       NOT RUN
P2 XTDB HG-01..HG-12         NOT RUN
P3 SurrealDB HG-01..HG-12    NOT RUN
```

Direct HG PASS count: `0`.

## 5. PM-05 corpus/scenario result

### Corpus

```text
C0  PRIMARY-EVIDENCE-SUFFICIENT
C1  PRIMARY-EVIDENCE-SUFFICIENT + PM-06/07-FINALIST scale
C2  PRIMARY-EVIDENCE-SUFFICIENT + candidate known costs
C3  persistence sufficient / full WL-H12 SYSTEM-BOUNDARY
C4  SYSTEM-BOUNDARY
C5  PRIMARY-EVIDENCE-SUFFICIENT
C6  primary baseline / specialist work PM-08
C7  PM-06/07-FINALIST
```

### Primary semantic scenario set

```text
SC-001 SC-002 SC-003 SC-009 SC-010 SC-012
SC-014 SC-015 SC-016 SC-022 SC-023 SC-024

RESULT
EVIDENCE-QUALIFIED FOR CURRENT PRIMARY COMPARISON
DIRECT RUN NOT REQUIRED NOW
```

### System/runtime/provider set

```text
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034

RESULT
SYSTEM-BOUNDARY
not a reason for four-primary local DB execution
```

### PM-06/07 finalist set

```text
SC-011 old-backup anti-resurrection
SC-013 deep-history scale
SC-030 V1 -> V2 evolution
SC-031 restore + semantic verification
SC-032 capacity/backpressure
```

### PM-08 secondary set

```text
SC-017 SC-018 SC-019 SC-020 SC-021 SC-035
```

## 6. P0 — PostgreSQL 18.4

```text
ROLE
mandatory baseline / current comparative leader

PM-01
ADMIT

PM-02
PM02-PG-001 COMPLETE

PM-03
9 PASS-CONDITIONAL / 3 HOLD / 0 REJECT

PM-04A
0 execution-worthy gaps

PM-05
PRIMARY FINALIST
ADVANCE PM-06/07 JOINT
0 PM-05 execution-worthy gaps

DIRECT HG
NOT RUN

PREFERRED
NO

SELECTED
NO
```

Current comparative strengths:

- native FK/constraint ecosystem;
- true Serializable/locking paths;
- low primary-store structural risk;
- mature recovery/operations ecosystem;
- explicit LifeOS history/material-state mapping without semantic collapse.

Current costs/conditions:

- heterogeneous address anchors must remain purely technical;
- transaction strength is operation/invariant-specific;
- explicit history is application schema, not built-in semantic history;
- RLS does not by itself satisfy WL-H12.

PM-06/07 obligations: SC-011/013/030/031/032 and finalist scale/recovery/evolution/TCO sensitivity.

## 7. P1 — TypeDB CE 3.12.3

```text
ROLE
principal semantic challenger

PM-01
ADMIT

PM-02
PM02-TDB-001 COMPLETE

PM-03
HG-04/HG-05 HOLD

PM-04A
concurrency unknown narrowed to documented guard condition/design cost
0 execution-worthy gaps

PM-05
PRIMARY FINALIST
ADVANCE PM-06/07 JOINT
CONDITION narrow consistency-guard coverage required
0 PM-05 execution-worthy gaps

DIRECT HG
NOT RUN

PREFERRED
NO

SELECTED
NO
```

Current comparative strengths:

- strongest typed relation/role/n-ary fit;
- schema-level role/cardinality semantics;
- clean mapping of Agreement/common-ground structures;
- no generic semantic object/edge root required.

Current costs/conditions:

- snapshot isolation remains the engine transaction model;
- correct narrow consistency-guard scoping is mandatory for write-skew-sensitive invariant sets;
- explicit material-state/history remains required;
- self-hosted operations/recovery/tooling maturity must be compared directly against PostgreSQL.

Reopen targeted concurrency execution only if PM-06/07 ranking becomes materially dependent on guard behavior rather than its known complexity cost.

## 8. P2 — XTDB 2.1.0

```text
ROLE
distinctive temporal/bitemporal challenger

PM-01
ADMIT / PRODUCTION TOPOLOGY HOLD

PM-02
PM02-XT-001 COMPLETE

PM-03
HG-02/HG-03 HOLD

PM-04A
reference/cardinality uncertainty narrowed to KNOWN STRUCTURAL COST
0 execution-worthy gaps

PM-05
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED

DIRECT HG
NOT RUN

SELECTED
NO
```

Reason for defer:

```text
native bitemporal value is real
BUT
no native FK
+ no general uniqueness beyond _id
+ manual ASSERT/address integrity discipline
+ non-interactive transaction ergonomics
+ production topology/single-writer sensitivity
→ aggregate primary-store burden currently exceeds finalist value
```

Reopen triggers:

- native bitemporality becomes decision-dominant under accepted requirements;
- PostgreSQL/TypeDB shows material history/temporal weakness;
- XTDB integrity/topology capability materially changes;
- later sensitivity analysis provides evidence that can change the recommendation.

## 9. P3 — SurrealDB Community 3.2.3

```text
ROLE
credible constrained multimodel challenger

PM-01
ADMIT-CONDITIONAL

PM-02
PM02-SDB-001 COMPLETE

PM-03
HG-04/HG-05 HOLD

PM-04A
concurrency unknown narrowed to guard condition/design cost
0 execution-worthy gaps

PM-05
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED

DIRECT HG
NOT RUN

SELECTED
NO
```

Reason for defer:

- SCHEMAFULL/typed-link multimodel design is credible;
- consistency-guard coverage remains a complexity cost;
- explicit long-lived material history remains required;
- no unique primary-store advantage currently offsets the comparative concurrency/history/operations burden enough to justify finalist scope.

Reopen triggers:

- multimodel consolidation becomes decision-changing;
- PostgreSQL/TypeDB exposes a material capability gap SurrealDB directly solves;
- relevant concurrency/history/operations capability changes materially;
- later TCO/sensitivity evidence can change the recommendation.

## 10. Primary finalist set

```text
P0 PostgreSQL 18.4
P1 TypeDB CE 3.12.3
```

This narrowing is evidence-driven scope management. It does not delete or invalidate PM-02..PM-05 evidence for XTDB/SurrealDB.

## 11. PM-06 + PM-07 joint campaign

PM-06 and PM-07 are operationally combined while retaining separate result semantics.

### PM-06 result layer

Qualify finalist evidence for:

```text
scale/history efficiency
resource behavior
contention/throughput sensitivity
storage/index growth
topology/resource cliffs
performance relevance to LifeOS
```

### PM-07 result layer

Qualify finalist evidence for:

```text
backup/restore
anti-resurrection
schema/data evolution
historical reference preservation
failure/backpressure
operations/HA/topology
RPO/RTO capability sensitivity
```

Evidence-first default applies. No direct run is authorized by this register.

## 12. Direct execution posture

```text
FULL LOCAL BENCHMARK
NOT ADMITTED

TARGETED LOCAL PROOFS
0 currently admitted

PM-04B
NOT REOPENED

DATABASE/HARNESS
NOT STARTED

BENCHMARK HOST
HOLD / DORMANT
```

Before any direct result changes from `NOT RUN`:

1. prove execution-worthiness or closure-mandatory status;
2. obtain fresh explicit gate;
3. freeze host/runtime/topology;
4. freeze mapping/schema/harness revision;
5. retain raw evidence;
6. distinguish candidate failure from tooling/environment failure.

## 13. Secondary lanes

```text
GRAPH
G0 primary/no-specialist baseline
Neo4j DEFER PM-08

SEARCH/VECTOR
primary structured/lexical baseline
pgvector DEFER PM-08 when applicable
Qdrant/OpenSearch trigger-only

LOCAL/OFFLINE
SQLite DEFER bounded client role

DURABLE RUNTIME
not selected by persistence workstream
```

## 14. Checkpoints

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

PM-05 PRE-SCOPE
44d331f12951e2844186e6f5f885e1bcf1559a3b
```

Final PM-05 remote-QA HEAD is recorded in the workstream handoff after final verification.

## 15. Current next step

```text
PM-05
COMPLETE subject to final remote QA

PM-06/07 JOINT
NEXT AFTER FRESH EXACT GATE
PostgreSQL + TypeDB only unless a deferred candidate reopen trigger is proven

PM-08+
NOT STARTED

NO DIRECT PERFORMANCE RUN
NO SELECTION
NO PRODUCTION BACKEND
```
