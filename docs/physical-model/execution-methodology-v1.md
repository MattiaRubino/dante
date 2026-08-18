# Physical Model Execution Methodology v1

- Status: **CURRENT — PM-08 SECONDARY/SPECIALIST QUALIFICATION COMPLETE / PM-09 NEXT**
- Workstream: `feature/physical-model`
- Main baseline: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Direct execution: **NOT STARTED**
- Primary finalists: **PostgreSQL 18.4 / TypeDB CE 3.12.3**
- Current overall leader: **PostgreSQL 18.4**
- Preferred: **NONE**
- Selected: **NONE**

## Purpose

Define how LifeOS converts accepted Domain + Logical semantics into an evidence-backed Physical Model without selecting infrastructure by popularity, vendor marketing, ritual benchmark breadth or implementation convenience.

This methodology does not alter Domain/Logical authority or the Phase-10 semantic benchmark corpus.

## Repository discipline

Every Physical write scope must:

1. verify actual remote `feature/physical-model` HEAD;
2. compare against current `main`;
3. re-read the active workstream handoff and relevant authority;
4. perform temporally unstable research read-only first;
5. present exact PRE-SCOPE / CREATE / UPDATE / DELETE allow-list;
6. write only approved paths;
7. preserve evidence-history/current-truth separation;
8. compare PRE-SCOPE -> final HEAD remotely;
9. verify added/modified/deleted/unexpected paths;
10. read back critical output from the remote branch;
11. save/verify terminal handoff.

A tool invocation/no-op is not repository evidence.

## Semantic barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
PROVIDER STATE != CANONICAL STATE
DERIVED STATE != CANONICAL STATE
TECHNICAL AUTHZ != DOMAIN AUTHORITY
MISSING != FALSE
EVIDENCE-QUALIFIED != DIRECT PASS
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
SECONDARY != CANONICAL
LOCAL != CANONICAL
```

Do not introduce a universal Entity/Thing/EAV/generic-edge canonical kernel merely to fit a candidate.

`WL-H01..WL-H12` remain non-negotiable downstream obligations.

## Research/source policy

For current product capabilities, version/edition/topology, licensing, backup, HA, driver support and deployment constraints:

```text
official product documentation / release notes
= baseline authority
```

Secondary/public benchmark/case-study evidence may support context, but must disclose source class and cannot become a fictional LifeOS run.

## Evidence-first / execution-minimization rule

Direct execution is a last-mile evidence tool.

Before any fixture/harness/database deployment/local benchmark, classify the question:

```text
EXT-SUFFICIENT
MAP-SUFFICIENT
KNOWN-STRUCTURAL-COST
SYSTEM-BOUNDARY
DEFER-FINALIST / POST-SELECTION VALIDATION
RESIDUAL-GAP
EXECUTION-WORTHY
```

Execution opens only when:

```text
RESIDUAL-GAP
+ decision relevance
+ external/mapping evidence exhausted
+ controlled execution can resolve it
= EXECUTION-WORTHY
```

The benchmark-host HOLD remains dormant until a direct run is admitted.

## Cost/quality policy

```text
TARGET
initial direct technology/license cost = EUR 0 where realistically possible

BUT
free != automatic preference
paid != automatic rejection
quality/correctness outrank cost
```

Decision priority:

1. semantic correctness;
2. consistency/integrity/security/privacy/recovery;
3. LifeOS workload/capability fit;
4. maturity/operability/maintainability/Python tooling;
5. performance/resource efficiency where decision-relevant;
6. TCO/deployment requirements;
7. lock-in/exit/migration risk.

The final architecture may be one canonical primary plus bounded specialists. Every extra technology must earn its complexity.

## Fixed roadmap

```text
PM-00 Bootstrap / authority freeze
PM-01 Technology discovery / candidate freeze
PM-02 Primary mapping design
PM-03 Semantic static preflight
PM-04 Evidence sufficiency + conditional harness
PM-05 Correctness/destructive evidence qualification
PM-06 Scale/performance evidence
PM-07 Recovery/evolution/failure evidence
PM-08 Secondary/specialist lanes
PM-09 Scoring + sensitivity
PM-10 Recommendation
PM-11 Explicit selection
PM-12 Accepted Physical Model
PM-13 Independent clean-room QA
PM-14 Closure / protected-main integration
```

PM-06 and PM-07 were operated as one Joint Finalist Qualification Campaign while preserving separate result layers.

## Phase state through PM-08

```text
PM-00   QA PASS
PM-01   PASS-CONDITIONAL
PM-02   COMPLETE
PM-03   STATIC COMPLETE / 0 STATIC REJECTS
PM-04A  COMPLETE / 48 OF 48 CELLS / 0 EXECUTION-WORTHY GAPS
PM-04B  NOT ADMITTED / HARNESS NOT STARTED
PM-05   COMPLETE / PRIMARY FINALISTS POSTGRESQL + TYPEDB
PM-06   COMPLETE / EVIDENCE QUALIFICATION / DIRECT TIERS NOT RUN
PM-07   COMPLETE / EVIDENCE QUALIFICATION / DIRECT DESTRUCTIVE RUNS NOT RUN
PM-08   COMPLETE / SECONDARY-SPECIALIST EVIDENCE QUALIFICATION
PM-09   NEXT
```

Deferred primary challengers remain `XTDB 2.1.0` and `SurrealDB Community 3.2.3`, both `DEFER / NOT REJECTED`.

## Primary finalist state after PM-06/07

### PostgreSQL 18.4

```text
SCALE/PERFORMANCE
VIABLE / HIGH CONFIDENCE

RECOVERY/EVOLUTION/OPERATIONS
MATERIAL ADVANTAGE

CURRENT DISPOSITION
CURRENT OVERALL LEADER
NOT PREFERRED
NOT SELECTED
```

### TypeDB CE 3.12.3

```text
SCALE/PERFORMANCE
VIABLE / MEDIUM-HIGH CONFIDENCE

RECOVERY/EVOLUTION
VIABLE / HIGHER SELF-HOSTED OPERATIONS COST

CURRENT DISPOSITION
PRINCIPAL SEMANTIC CHALLENGER
NOT PREFERRED
NOT SELECTED
```

The remaining primary question is whether TypeDB's stronger relation/role/n-ary semantic model outweighs its consistency-guard, backup-operations and CE-topology burden versus PostgreSQL.

## Direct execution truth

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
LOW/BASE/HIGH            NOT RUN
DIRECT HG PASS            0
RESTORE REHEARSAL         NOT RUN
MIGRATION REHEARSAL       NOT RUN
FAILURE INJECTION         NOT RUN
BENCHMARK HOST            HOLD / DORMANT
```

Do not mutate these values without real execution artifacts.

## Post-selection validation obligations

The following remain mandatory where applicable and are not direct PASS today:

```text
SC-011 old-backup anti-resurrection
SC-030 actual LifeOS V1 -> V2 mapping evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure truthful degradation
```

`SC-013` deep-history scale reopens before selection only if PM-09 becomes materially performance-sensitive.

## PM-08 — Secondary / Specialist Lanes

Status: **COMPLETE — EVIDENCE-FIRST / NO DIRECT EXECUTION**.

PM-08 asks whether a specialist technology creates enough bounded value to justify another engine/service.

### Global secondary rule

```text
SECONDARY / PROJECTION / SEARCH / VECTOR / LOCAL STATE
!= CANONICAL TRUTH
```

Where derived from canonical truth, secondary mechanisms must define source basis, freshness/lag, deletion/redaction propagation, Visibility/scope enforcement and rebuild/reconciliation behavior.

### Graph lane

```text
G0 primary-store baseline
ADVANCE

Neo4j
DEFER / NOT REJECTED
NO INITIAL GRAPH SPECIALIST
```

PostgreSQL 18 already supports recursive traversal with `SEARCH`/`CYCLE`; TypeDB is already relationship-native. No current accepted LifeOS graph workload earns a second graph persistence/service boundary.

Neo4j may reopen only on concrete decision-relevant graph workload pressure such as large/deep path traversal, graph recommendation/pathfinding/analytics or unacceptable primary traversal isolation/performance.

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

Embedding/vector state remains derived state.

Vector quality must be evaluated after real scope/Visibility filtering. Security filtering cannot be weakened to improve ANN recall.

Qdrant may reopen on large vector scale, filtered-ANN limits, independent vector scaling or advanced dense+sparse/multi-stage retrieval requirements.

OpenSearch may reopen on large dedicated lexical/faceted/relevance/search-analytics requirements or material search isolation needs.

### TypeDB specialist implication

PM-08 does not establish a TypeDB-native equivalent to PostgreSQL FTS + pgvector.

If TypeDB wins primary selection and accepted lexical/vector retrieval is required, an external search/vector specialist is therefore more likely. That probable extra service is a PM-09 operability/topology/TCO input, not a semantic rejection.

### Local / offline lane

```text
SQLite 3.53.4
ADMIT AS BOUNDED LOCAL/OFFLINE CANDIDATE
CANONICAL AUTHORITY NO
EXACT CLIENT ADAPTER DEFER
```

SQLite earns admission because it solves device-local/offline persistence rather than duplicating canonical server authority.

The exact web/mobile/desktop configuration remains future client implementation design; browser/WASM/OPFS locking and concurrency trade-offs prevent PM-08 from pretending one universal configuration is already proven.

### Object/blob lane

```text
OBJECT/BLOB ENGINE
NO ADMISSION NOW
DEFER / TRIGGER ONLY
```

Reopen only when concrete object classes, sizes, volume, retention, security, distribution and durability requirements exist.

### PM-08 execution decision

```text
PM-08 EXECUTION-WORTHY GAPS  0
PM-04B REOPENED              NO
GRAPH BENCHMARK              NOT ADMITTED
VECTOR BENCHMARK             NOT ADMITTED NOW
SEARCH BENCHMARK             NOT ADMITTED NOW
SQLITE BENCHMARK             NOT ADMITTED NOW
```

### PM-08 scenario carry-forward

```text
SC-017 hidden-result non-interference
post-selection search/system validation

SC-018 FTS mixed filter/query
post-selection search implementation validation

SC-019 vector recall after security filter
reopen before selection only if vector path becomes ranking/performance-sensitive;
otherwise post-selection implementation validation

SC-020 stale index source
post-selection projection validation where a projection exists

SC-021 deletion propagation
post-selection projection validation where a projection exists

SC-035 graph projection divergence/rebuild
not applicable to initial stack; reopen if graph specialist is later admitted
```

None is a direct PASS.

## PM-09 — Scoring + Sensitivity

Next phase.

Primary 100-point dimensions remain:

```text
semantic mapping simplicity/evolvability 20
transaction/concurrency ergonomics       15
query/report/traversal                   15
history/current efficiency               10
operations/backup/restore/HA             15
schema evolution/migration               10
performance/resource efficiency          10
Python/tooling/cost/exit risk             5
```

PM-09 must incorporate PM-08 architecture implications rather than score the primary in isolation.

Important sensitivity:

```text
POSTGRESQL PATH
likely fewer initial server technologies because FTS + conditional vector stay in PostgreSQL

TYPEDB PATH
stronger semantic-native relation model but likely external search/vector specialist when that capability is accepted
```

Scores require evidence. Unexecuted measurements cannot be invented.

Ranking instability under scale/history/concurrency/topology/recovery/cost/specialist assumptions becomes `SENSITIVITY-DEPENDENT`.

## PM-10..PM-14

```text
PM-10 Recommendation may produce PREFERRED, never SELECTED
PM-11 explicit user-approved selection gate
PM-12 accepted Physical Model
PM-13 independent clean-room QA
PM-14 protected PR/merge/main verification
```

Physical closure does not automatically start Backend Foundation.

## Stop/reopen conditions

Stop and re-gate if:

- Domain/Logical contradiction appears;
- a candidate requires semantic weakening;
- a new semantic owner/root appears necessary;
- a specialist is proposed without bounded admission rationale;
- direct execution needs unapproved infrastructure/path scope;
- official capability evidence contradicts a frozen subject;
- a ranking-critical residual gap appears;
- selection is being inferred rather than explicitly authorized;
- a path outside the approved scope must be written.

## Current next step

```text
PM-08 COMPLETE
CURRENT LEADER PostgreSQL
PRINCIPAL CHALLENGER TypeDB
INITIAL EXTRA SERVER SPECIALISTS 0
PGVECTOR ADMIT-CONDITIONAL
SQLITE ADMIT BOUNDED LOCAL/OFFLINE CANDIDATE
PREFERRED NONE
SELECTED NONE

NEXT
PM-09 scoring + sensitivity after fresh explicit gate
```