# Physical Model Execution Methodology v1

- Status: **CURRENT — PM-09 EVIDENCE-WEIGHTED SCORING COMPLETE / PM-10 NEXT**
- Workstream: `feature/physical-model`
- Main baseline: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Direct execution: **NOT STARTED**
- Primary finalists: **PostgreSQL 18.4 / TypeDB CE 3.12.3**
- Current evidence-score leader: **PostgreSQL 18.4**
- Preferred: **NONE**
- Selected: **NONE**

## Purpose

Define how LifeOS converts accepted Domain + Logical semantics into an evidence-backed Physical Model without selecting infrastructure by popularity, vendor marketing, ritual benchmark breadth or implementation convenience.

This methodology does not alter Domain/Logical authority or the Phase-10 semantic hard-gate corpus.

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
SECONDARY != CANONICAL
LOCAL != CANONICAL
TECHNICAL AUTHZ != DOMAIN AUTHORITY
MISSING != FALSE
EVIDENCE-QUALIFIED != DIRECT PASS
EVIDENCE SCORE != VERIFIED-RUN SCORE
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
```

Do not introduce a universal Entity/Thing/EAV/generic-edge canonical kernel merely to fit a candidate.

`WL-H01..WL-H12` remain non-negotiable downstream obligations.

## Evidence-first / execution-minimization rule

Direct execution is a last-mile evidence tool.

Before fixture/harness/database deployment/local benchmark, classify the question:

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

## Two evidence ledgers

The reconciled Phase-10 specification now distinguishes:

```text
VERIFIED-RUN BENCHMARK SCORE
requires direct hard-gate PASS + direct benchmark evidence

EVIDENCE-WEIGHTED DECISION SCORE
comparative decision aid allowed after evidence exhaustion
when 0 ranking-critical execution-worthy gaps remain
```

```text
EVIDENCE-WEIGHTED DECISION SCORE
!= VERIFIED-RUN BENCHMARK SCORE
```

The evidence ledger may support PM-09 sensitivity and PM-10 recommendation. It does not change `DIRECT HG PASS`, does not make LOW/BASE/HIGH executed and does not select infrastructure.

If a ranking-critical residual uncertainty appears, evidence scoring stops and a bounded direct proof must be separately gated.

## Cost / architecture policy

Decision priority remains:

1. semantic correctness;
2. consistency/integrity/security/privacy/recovery;
3. LifeOS workload/capability fit;
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

PM-06 and PM-07 were operated as one Joint Finalist Qualification Campaign while keeping separate result layers.

## Phase state through PM-09

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
PM-09   COMPLETE / EVIDENCE-WEIGHTED SCORING + SENSITIVITY
PM-10   NEXT
```

Deferred primary challengers remain `XTDB 2.1.0` and `SurrealDB Community 3.2.3`, both `DEFER / NOT REJECTED`.

## Direct execution truth

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG-01..HG-12      NOT RUN
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE REHEARSAL         NOT RUN
MIGRATION REHEARSAL       NOT RUN
FAILURE INJECTION         NOT RUN
GRAPH BENCHMARK           NOT RUN
VECTOR BENCHMARK          NOT RUN
SEARCH BENCHMARK          NOT RUN
SQLITE BENCHMARK          NOT RUN
BENCHMARK HOST            HOLD / DORMANT
VERIFIED-RUN SCORE        NOT AVAILABLE
```

Do not mutate these values without direct execution artifacts.

## Primary finalist state

### PostgreSQL 18.4

```text
PM-06
SCALE/PERFORMANCE VIABLE / HIGH CONFIDENCE

PM-07
MATERIAL OPERATIONS/RECOVERY/TOPOLOGY ADVANTAGE

PM-08
NATIVE FTS + CONDITIONAL PGVECTOR CAN KEEP INITIAL SEARCH/VECTOR SERVER TOPOLOGY CONSOLIDATED

PM-09 EVIDENCE SCORE
89.25 / 100

SENSITIVITY
ROBUST LEADER

PREFERRED
NONE

SELECTED
NONE
```

### TypeDB CE 3.12.3

```text
PM-06
SCALE/PERFORMANCE VIABLE / MEDIUM-HIGH CONFIDENCE

PM-07
RECOVERY/EVOLUTION VIABLE / HIGHER SELF-HOSTED OPERATIONS COST

PM-08
SEMANTIC ADVANTAGE PRESERVED / EXTERNAL SEARCH-VECTOR SPECIALIST MORE LIKELY WHEN ADVANCED RETRIEVAL IS ACCEPTED

PM-09 EVIDENCE SCORE
80.00 / 100

SENSITIVITY
PRINCIPAL SEMANTIC CHALLENGER / NO ACCEPTED REVERSAL

PREFERRED
NONE

SELECTED
NONE
```

## PM-08 secondary state carried into scoring

```text
GRAPH
G0 primary-store baseline ADVANCE
Neo4j DEFER / NOT REJECTED / no initial graph specialist

SEARCH/VECTOR
PostgreSQL native FTS ADVANCE as P0 baseline
pgvector 0.8.6 ADMIT-CONDITIONAL if PostgreSQL selected + vector requirement exists
Qdrant 1.18.2 DEFER / TRIGGER ONLY
OpenSearch 3.7 DEFER / TRIGGER ONLY

LOCAL/OFFLINE
SQLite 3.53.4 ADMIT BOUNDED LOCAL/OFFLINE CANDIDATE
canonical authority NO

OBJECT/BLOB
NO ENGINE ADMITTED / TRIGGER ONLY
```

## PM-09 scoring rules

The original Phase-10 dimensions and weights remain unchanged:

```text
semantic mapping simplicity/evolvability 20
transaction/concurrency ergonomics       15
query/report/traversal                   15
history/current efficiency               10
operations/backup/restore/HA             15
schema evolution/migration               10
performance/resource efficiency          10
Python/tooling/cost/exit risk             5
TOTAL                                   100
```

Dimension grades must be traceable to PM-02 through PM-08 evidence. Unexecuted performance cannot be invented.

### Base PM-09 score

```text
PostgreSQL 18.4     89.25
TypeDB CE 3.12.3    80.00
Delta               +9.25 PostgreSQL
```

Performance is intentionally tied `8.0 / 8.0` because no direct LOW/BASE/HIGH LifeOS run exists.

### Accepted sensitivity

```text
S0 Phase-10 base                  PG +9.25
S1 semantic-heavy                 PG +5.75
S2 early single-node              PG +7.25
S3 operations/recovery-heavy      PG +12.50
S4 strongly TypeDB-friendly       PG +2.75
```

Result:

```text
RANKING ROBUST
SENSITIVITY-DEPENDENT NO
PERFORMANCE-DEPENDENT NO
```

An adversarial, non-accepted weighting with semantic mapping at 50% produces only a `+0.125 TypeDB` boundary. Keeping all non-semantic dimensions proportional to their Phase-10 relative weights, semantic mapping must reach approximately `58.44%` before TypeDB reaches break-even.

This boundary is evidence about sensitivity, not an accepted change to LifeOS priorities.

## Execution reopen decision

```text
SC-013 DEEP-HISTORY SCALE
REOPEN NO

PM-04B
REOPEN NO
```

Reason: the PM-09 ranking is not performance-dependent and no ranking-critical residual execution gap remains.

## Post-selection validation obligations

These are mandatory where applicable and remain unexecuted:

```text
SC-011 old-backup anti-resurrection
SC-030 actual LifeOS V1 -> V2 mapping evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure truthful degradation
WL-H12 system-level non-interference
SC-017/018 search/non-interference when search active
SC-019 vector recall after security filter when vector active
SC-020/021 projection freshness/deletion propagation when projection active
local/offline reconciliation validation when local role active
```

## PM-10 boundary

PM-10 may consume:

```text
PM-02..PM-08 evidence
PM-09 evidence-weighted score
PM-09 sensitivity
known conditions / post-selection validation obligations
```

PM-10 may produce a bounded `PREFERRED` recommendation under this evidence-first methodology.

It may not produce `SELECTED`.

PM-11 remains the separate explicit user-approved selection gate.

## Current next step

```text
PM-09 COMPLETE
CURRENT EVIDENCE-SCORE LEADER PostgreSQL 18.4
SCORE 89.25 vs 80.00
RANKING ROBUST
PREFERRED NONE
SELECTED NONE

NEXT
PM-10 recommendation after fresh explicit gate
```