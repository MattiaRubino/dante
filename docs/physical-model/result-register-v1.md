# Physical Model Result Register v1

- Status: **CURRENT — PM-08 COMPLETE / PM-09 NEXT**
- Workstream: `feature/physical-model`
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Deferred primary challengers: **XTDB 2.1.0 + SurrealDB Community 3.2.3 — NOT REJECTED**
- Current overall leader: **PostgreSQL 18.4**
- Direct execution: **NOT STARTED**
- Preferred: **NONE**
- Selected: **NONE**

## Result-language rule

```text
OFFICIAL CLAIM != DIRECT EXECUTION
PUBLIC BENCHMARK != LIFEOS BENCHMARK
EVIDENCE-QUALIFIED != DIRECT PASS
ADMIT != SELECTED
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
SECONDARY != CANONICAL
LOCAL != CANONICAL
NOT RUN != PASS
```

## Phase state

```text
PM-00   QA PASS
PM-01   PASS-CONDITIONAL
PM-02   PRIMARY MAPPING COMPLETE
PM-03   STATIC PREFLIGHT COMPLETE / 0 STATIC REJECTS
PM-04A  EVIDENCE SUFFICIENCY COMPLETE / 48 OF 48 CELLS
PM-04B  NOT ADMITTED
PM-05   CORRECTNESS/DESTRUCTIVE EVIDENCE QUALIFICATION COMPLETE
PM-06   SCALE/PERFORMANCE EVIDENCE QUALIFICATION COMPLETE
PM-07   RECOVERY/EVOLUTION/FAILURE EVIDENCE QUALIFICATION COMPLETE
PM-08   SECONDARY/SPECIALIST LANE QUALIFICATION COMPLETE
PM-09   NEXT
PM-10+  NOT STARTED
```

## Primary finalist set

```text
P0 PostgreSQL 18.4
ADVANCE
CURRENT OVERALL LEADER

P1 TypeDB CE 3.12.3
ADVANCE
PRINCIPAL SEMANTIC CHALLENGER

P2 XTDB 2.1.0
DEFER / NOT REJECTED

P3 SurrealDB Community 3.2.3
DEFER / NOT REJECTED
```

## PM-06/07 carried result

### PostgreSQL

```text
SCALE/PERFORMANCE VIABLE
confidence HIGH

RECOVERY/EVOLUTION/OPERATIONS
MATERIAL ADVANTAGE
```

### TypeDB CE

```text
SCALE/PERFORMANCE VIABLE
confidence MEDIUM-HIGH

RECOVERY/EVOLUTION
VIABLE / HIGHER SELF-HOSTED OPERATIONS COST
```

Joint comparison:

```text
POSTGRESQL
OVERALL LEAD STRENGTHENED

TYPEDB
SEMANTIC ADVANTAGE PRESERVED
```

## PM-08 result

### Graph lane

```text
G0 primary-store graph baseline
ADVANCE

Neo4j
DEFER / NOT REJECTED
NO INITIAL GRAPH SPECIALIST
```

Rationale:

- PostgreSQL already provides recursive traversal primitives;
- TypeDB is already relationship-native;
- no accepted current LifeOS graph workload earns another persistence/service boundary;
- projection freshness, deletion, Visibility, rebuild and operations costs remain real.

### Search / vector lane

```text
PostgreSQL native FTS
ADVANCE as P0 lexical baseline

pgvector 0.8.6
ADMIT-CONDITIONAL
conditions: PostgreSQL selected primary + accepted vector retrieval requirement

Qdrant 1.18.2
DEFER / NOT REJECTED / SPECIALIST TRIGGER ONLY

OpenSearch 3.7
DEFER / NOT REJECTED / SPECIALIST TRIGGER ONLY
```

Vector/embedding state remains derived state.

Filtered ANN must preserve real scope/Visibility filtering. A security filter may not be weakened to improve recall.

### TypeDB search/vector implication

PM-08 does not establish a TypeDB-native equivalent to PostgreSQL FTS + pgvector.

If TypeDB wins and accepted lexical/vector retrieval is required, an external search/vector service is more likely. Qdrant is the current trigger candidate, not selected or admitted now.

This probable extra service is a PM-09 operability/topology/TCO input.

### Local / offline lane

```text
SQLite 3.53.4
ADMIT BOUNDED LOCAL/OFFLINE CANDIDATE
CANONICAL AUTHORITY NO
EXACT CLIENT IMPLEMENTATION DEFER
```

SQLite earns a distinct role for local/offline persistence, cache/projection, drafts and pending-operation staging. It never becomes competing canonical authority.

### Object/blob lane

```text
OBJECT/BLOB ENGINE
NO ADMISSION NOW
DEFER / TRIGGER ONLY
```

Reopen only on concrete object-size/volume/retention/security/distribution/durability requirements.

## PM-08 scenario carry-forward

```text
SC-017 hidden-result non-interference
POST-SELECTION SEARCH/SYSTEM VALIDATION

SC-018 FTS mixed filter/query
POST-SELECTION SEARCH IMPLEMENTATION VALIDATION

SC-019 vector recall after security filter
REOPEN BEFORE SELECTION only if vector path becomes ranking/performance-sensitive;
otherwise implementation validation

SC-020 stale index source
POST-SELECTION PROJECTION VALIDATION when projection exists

SC-021 deletion propagation
POST-SELECTION PROJECTION VALIDATION when projection exists

SC-035 graph projection divergence/rebuild
NOT APPLICABLE to initial stack; reopen if graph specialist is later admitted
```

None is a direct PASS.

## Direct execution truth

```text
P0 HG-01..HG-12       NOT RUN
P1 HG-01..HG-12       NOT RUN
P2 HG-01..HG-12       NOT RUN
P3 HG-01..HG-12       NOT RUN

DIRECT HG PASS         0
DATABASE DEPLOYMENT    NOT STARTED
HARNESS                 NOT STARTED
LOW/BASE/HIGH           NOT RUN
RESTORE                  NOT RUN
MIGRATION                NOT RUN
FAILURE INJECTION        NOT RUN
GRAPH BENCHMARK          NOT RUN
VECTOR BENCHMARK         NOT RUN
SEARCH BENCHMARK         NOT RUN
SQLITE BENCHMARK         NOT RUN
BENCHMARK HOST           HOLD / DORMANT
```

## Specialist trigger state

```text
INITIAL EXTRA SERVER ENGINES ADMITTED
0

CONDITIONAL IN-PRIMARY EXTENSION
pgvector 0.8.6

BOUNDED LOCAL/OFFLINE CANDIDATE
SQLite 3.53.4

DEFERRED/TRIGGER-ONLY SERVER SPECIALISTS
Neo4j
Qdrant 1.18.2
OpenSearch 3.7
object/blob engine TBD
```

## Architecture pressure entering PM-09

```text
POSTGRESQL PATH
PostgreSQL canonical
+ native FTS
+ pgvector conditional in same database
+ SQLite bounded local/offline when needed
=> likely zero additional server engines initially

TYPEDB PATH
TypeDB canonical
+ stronger relation/role/n-ary semantic model
+ likely external search/vector service when accepted retrieval requires it
+ SQLite bounded local/offline when needed
=> probable additional server topology/operations cost
```

This makes PostgreSQL's current lead stronger on overall architecture consolidation/operability, but it does not create `PREFERRED` or `SELECTED` before PM-09/10/11.

## Post-selection implementation validation

Still mandatory where applicable:

```text
SC-011 old-backup anti-resurrection
SC-030 actual LifeOS V1->V2 evolution
SC-031 semantic restore verification
SC-032 capacity/backpressure
WL-H12 system-level non-interference
search/vector/projection validation for activated lanes
client local/offline sync/reconciliation validation
```

`SC-013` deep-history scale remains a pre-selection reopen trigger only if PM-09 becomes materially performance-sensitive.

## Evidence paths

```text
PM-01
pm-01-technology-landscape-v1.md

PM-02
pm-02-primary-mapping-overview-v1.md
mappings/*

PM-03
pm-03-semantic-hard-gate-preflight-v1.md
preflight/*

PM-04A
pm-04-external-evidence-sufficiency-v1.md
evidence/*

PM-05
pm-05-correctness-evidence-qualification-v1.md
qualification/*-v1.md

PM-06/07
pm-06-07-joint-finalist-qualification-v1.md
pm-06-scale-performance-evidence-v1.md
pm-07-recovery-evolution-evidence-v1.md
qualification/postgresql-18.4-pm-06-07-v1.md
qualification/typedb-3.12.3-pm-06-07-v1.md

PM-08
pm-08-secondary-lanes-v1.md
secondary/graph-lane-v1.md
secondary/search-vector-lane-v1.md
secondary/local-offline-lane-v1.md
secondary/specialist-trigger-register-v1.md
```

## Historical checkpoints

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

PM-08 PRE-SCOPE
1e19793fdb9f51ba510f00ac4c927a6907e28c4b
```

PM-08 terminal HEAD is determined by remote Git after the current write scope.

## Next

```text
PM-09
SCORING + SENSITIVITY
fresh gate required

PREFERRED NONE
SELECTED NONE
BACKEND NOT STARTED / DEFERRED
```