# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-08 COMPLETE / PM-09 NEXT**
- Branch: `feature/physical-model`
- Main baseline: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL**
- PM-02: **COMPLETE**
- PM-03: **STATIC COMPLETE / 0 REJECTS**
- PM-04A: **COMPLETE / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED**
- PM-05: **COMPLETE**
- PM-06: **COMPLETE / DIRECT PERFORMANCE NOT RUN**
- PM-07: **COMPLETE / DIRECT DESTRUCTIVE RUNS NOT RUN**
- PM-08: **COMPLETE / SECONDARY-SPECIALIST EVIDENCE QUALIFICATION**
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Current overall leader: **PostgreSQL 18.4**
- Deferred primary challengers: **XTDB 2.1.0 + SurrealDB Community 3.2.3 — NOT REJECTED**
- Preferred: **NONE**
- Selected: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Turn accepted LifeOS Domain + Logical semantics into a durable, evidence-backed Physical Model without weakening semantics or manufacturing benchmarks that cannot change the decision.

```text
DOMAIN + LOGICAL
fixed semantic authority

PHYSICAL
research
→ candidate-native mapping
→ semantic preflight
→ evidence sufficiency
→ correctness qualification
→ finalist qualification
→ specialist lanes
→ scoring/sensitivity
→ recommendation
→ explicit selection
→ accepted model / clean-room QA / main integration
```

## Mandatory continuation order

Before any further Physical write:

1. verify remote `feature/physical-model` HEAD;
2. compare to current `main`;
3. read `docs/workstreams/physical-model.md` completely;
4. read this README;
5. read `execution-methodology-v1.md`;
6. read `acceptance-test-matrix-v1.md` and `result-register-v1.md`;
7. read PM-01 through PM-08 evidence relevant to the next phase;
8. read Phase-10 benchmark spec/corpus/register where scenario authority matters;
9. read Whole-Logical authority/WL-H01..WL-H12 where semantics are involved;
10. verify current official technology facts where temporally unstable;
11. issue exact PRE-SCOPE / CREATE / UPDATE / DELETE gate before write.

Conversation memory never outranks repository truth.

## Non-negotiable barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
CANONICAL != PROVIDER / DERIVED / SECURITY STATE
SECONDARY != CANONICAL
LOCAL != CANONICAL
MISSING != FALSE
EVIDENCE-QUALIFIED != EXECUTED PASS
PUBLIC BENCHMARK != LIFEOS BENCHMARK
ADMIT != SELECTED
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
```

No universal Entity/Thing/EAV/generic-edge canonical shortcut may be introduced for implementation convenience.

## Evidence-first execution policy

```text
LOCAL EXECUTION
last-mile evidence only
```

A direct run requires a residual question that remains unresolved, is materially decision-relevant, and can actually be resolved by controlled execution.

Current direct execution state:

```text
benchmark host          HOLD / DORMANT
database deployment     NOT STARTED
fixture/harness          NOT STARTED
LOW/BASE/HIGH            NOT RUN
direct HG PASS           0
restore rehearsal        NOT RUN
migration rehearsal      NOT RUN
failure injection        NOT RUN
graph benchmark          NOT RUN
vector benchmark         NOT RUN
search benchmark         NOT RUN
SQLite benchmark         NOT RUN
```

## Primary finalists

### PostgreSQL 18.4

```text
ROLE
current overall leader

PM-06
scale/performance viable / HIGH confidence

PM-07
clear operations/recovery/topology advantage

PM-08
native FTS baseline
pgvector conditional path
likely zero additional server engines initially

PREFERRED
NONE

SELECTED
NONE
```

Why it leads:

- accepted mapping preserves LifeOS semantics without a universal ontology root;
- mature integrity and Serializable primitives;
- strong backup/recovery/evolution/topology posture;
- native lexical search;
- vector retrieval can likely remain bounded inside PostgreSQL through pgvector;
- zero-license-cost self-hosted capability;
- lower aggregate canonical-store and initial-stack operational risk.

Remaining obligations remain implementation-specific: anchor discipline, operation-specific transaction policy, WL-H12 system proof, semantic restore/anti-resurrection, actual V1→V2 migration and activated search/vector validation.

### TypeDB CE 3.12.3

```text
ROLE
principal semantic challenger

PM-06
scale/performance viable / MEDIUM-HIGH confidence

PM-07
recovery/evolution viable / higher self-hosted operations cost

PM-08
semantic relationship advantage preserved
likely external search/vector specialist when that capability is accepted

PREFERRED
NONE

SELECTED
NONE
```

Why it remains a finalist:

- strongest direct relation/role/n-ary semantic representation;
- strong schema/cardinality semantics;
- credible scale-up and concurrent-query model;
- explicit cross-version export/import evolution path.

Material costs/conditions:

- snapshot-isolation hardening through correctly scoped consistency guards;
- CE single-node topology;
- self-hosted backup responsibility;
- likely additional search/vector service for accepted retrieval capabilities;
- greater aggregate operations/topology complexity than the PostgreSQL path.

## Deferred primary challengers

```text
XTDB 2.1.0
DEFER / NOT REJECTED
reopen on decision-dominant bitemporal need or material capability change

SurrealDB Community 3.2.3
DEFER / NOT REJECTED
reopen on decision-dominant multimodel consolidation or material capability change
```

## PM-08 result

### Graph

```text
G0 primary-store baseline
ADVANCE

Neo4j
DEFER / NOT REJECTED
NO INITIAL GRAPH SPECIALIST
```

No accepted current LifeOS graph workload justifies another graph persistence/service boundary.

### Search / vector

```text
PostgreSQL native FTS
ADVANCE as P0 baseline

pgvector 0.8.6
ADMIT-CONDITIONAL
PostgreSQL selected + accepted vector retrieval requirement

Qdrant 1.18.2
DEFER / SPECIALIST TRIGGER ONLY

OpenSearch 3.7
DEFER / SPECIALIST TRIGGER ONLY
```

Embedding/vector state remains derived state. Scope/Visibility filtering cannot be weakened for ANN quality.

### Local / offline

```text
SQLite 3.53.4
ADMIT BOUNDED LOCAL/OFFLINE CANDIDATE
CANONICAL AUTHORITY NO
EXACT CLIENT CONFIGURATION DEFER
```

SQLite solves a distinct client-local/offline problem rather than duplicating server authority.

### Object/blob

```text
NO ENGINE ADMITTED NOW
DEFER / TRIGGER ONLY
```

Do not preselect S3/R2/MinIO or another engine until concrete object-size/volume/security/durability/distribution requirements exist.

## Initial architecture pressure after PM-08

If PostgreSQL ultimately wins:

```text
PostgreSQL 18.4
canonical primary
+ native FTS
+ pgvector when required

SQLite 3.53.4
bounded client/local/offline when required

NO initial Neo4j
NO initial Qdrant
NO initial OpenSearch
```

If TypeDB wins:

```text
TypeDB CE 3.12.3
canonical primary
+
likely bounded external search/vector specialist when required

SQLite 3.53.4
bounded client/local/offline when required
```

This specialist implication is a PM-09 scoring/sensitivity input, not a selection.

## Scenario carry-forward

Still not waived and not direct PASS:

```text
SC-011 old-backup anti-resurrection
SC-030 V1→V2 mapping evolution
SC-031 semantic restore verification
SC-032 capacity/backpressure
SC-017/018 search/non-interference implementation validation
SC-019 filtered vector recall when vector lane is active
SC-020/021 projection freshness/deletion propagation when a projection exists
SC-035 only if graph specialist is later admitted
```

`SC-013` deep-history scale reopens before selection only if PM-09 becomes genuinely performance-sensitive.

## Current work products

```text
execution-methodology-v1.md
execution-template-v1.md
acceptance-test-matrix-v1.md
result-register-v1.md

pm-01-technology-landscape-v1.md
pm-02-primary-mapping-overview-v1.md
mappings/*
pm-03-semantic-hard-gate-preflight-v1.md
preflight/*
pm-04-external-evidence-sufficiency-v1.md
evidence/*
pm-05-correctness-evidence-qualification-v1.md
qualification/*-v1.md

pm-06-07-joint-finalist-qualification-v1.md
pm-06-scale-performance-evidence-v1.md
pm-07-recovery-evolution-evidence-v1.md
qualification/postgresql-18.4-pm-06-07-v1.md
qualification/typedb-3.12.3-pm-06-07-v1.md

pm-08-secondary-lanes-v1.md
secondary/graph-lane-v1.md
secondary/search-vector-lane-v1.md
secondary/local-offline-lane-v1.md
secondary/specialist-trigger-register-v1.md
```

## Roadmap

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

## Current exact next step

```text
PM-09
scoring + sensitivity
fresh exact gate required before repository mutation

CURRENT LEADER PostgreSQL
PREFERRED NONE
SELECTED NONE
BACKEND NOT STARTED / DEFERRED
```