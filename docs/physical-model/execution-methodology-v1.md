# Physical Model Execution Methodology v1

- Status: **CURRENT — PM-14 TARGET-ARCHITECTURE CLOSURE COMPLETE / INTEGRATED INTO MAIN VIA PR #15**
- Current product/app name: **DANTE** (`LifeOS` remains the previous working/project name in historical evidence and technical identifiers)
- Former workstream branch: `feature/physical-model` — **MERGED / AUTO-DELETED**
- Physical integration commit: `e6f191bad947388a44defe2c15f4939345084f58` via PR #15
- Main baseline during workstream: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Direct execution: **NOT STARTED**
- Primary finalists: **PostgreSQL 18.4 / TypeDB CE 3.12.3**
- PM-09 evidence-score leader: **PostgreSQL 18.4**
- PM-10 preferred: **PostgreSQL 18.4 / PASS-CONDITIONAL**
- PM-11 selected primary: **PostgreSQL 18.4**
- PM-12 accepted Physical Model: **ESTABLISHED**
- PM-13 clean-room architecture/documentation QA: **PASS**
- PM-14 branch/workstream closure: **COMPLETE**
- Protected-main lifecycle action after PM-14: **PR #15 COMPLETE**

## Purpose

Define how DANTE converts accepted Domain + Logical semantics into an evidence-backed Physical Model without selecting infrastructure by popularity, vendor marketing, ritual benchmark breadth or implementation convenience.

This methodology does not alter Domain/Logical authority or the Phase-10 semantic hard-gate corpus.

## Repository discipline

During the Physical workstream, every Physical write scope had to:

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

The workstream was merged into `main` through the protected repository lifecycle action PR #15 **after PM-14 branch/workstream closure**. Any later direct selected-stack validation or Physical reopen requires a fresh separately approved branch/write gate rather than reusing the deleted historical branch.

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
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
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

The reconciled Phase-10 specification distinguishes:

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

The evidence ledger supported PM-09 sensitivity, PM-10 recommendation and PM-11 selection. It does not change `DIRECT HG PASS`, does not make LOW/BASE/HIGH executed and does not waive selected-stack implementation validation.

If a ranking-critical residual uncertainty appears, evidence scoring stops and a bounded direct proof must be separately gated.

## Cost / architecture policy

Decision priority remains:

1. semantic correctness;
2. consistency/integrity/security/privacy/recovery;
3. DANTE workload/capability fit;
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

The accepted target architecture is one canonical primary plus bounded specialists/capabilities. A later Development Profile may choose activation/deployment modes without silently changing the target Physical architecture.

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
PM-14 Branch / workstream closure
```

**Protected-main integration is a repository lifecycle action after PM-14**, not a second semantic phase. For this workstream that action was PR #15, followed by remote post-merge verification and automatic deletion of the merged head branch.

PM-06 and PM-07 were operated as one Joint Finalist Qualification Campaign while keeping separate result layers.

## Phase state through PM-14 and integration

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
PM-10   COMPLETE / PREFERRED RECOMMENDATION + FINAL COMPANION STACK
PM-11   COMPLETE / EXPLICIT USER-APPROVED TARGET STACK SELECTION
PM-12   COMPLETE / ACCEPTED PHYSICAL MODEL ESTABLISHED
PM-13   QA PASS / ARCHITECTURE-DOCUMENTATION COHERENCE
PM-14   BRANCH / WORKSTREAM CLOSURE COMPLETE
PR #15  PROTECTED-MAIN INTEGRATION COMPLETE
PHYSICAL INTEGRATION COMMIT e6f191bad947388a44defe2c15f4939345084f58
FORMER  feature/physical-model MERGED / AUTO-DELETED
```

Deferred primary challengers remain historical comparative evidence only; the selected architecture excludes TypeDB, XTDB and SurrealDB from primary persistence.

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
POWERSYNC DIRECT TEST     NOT RUN
RESTATE DIRECT TEST       NOT RUN
OBJECT RECOVERY TEST      NOT RUN
SOLVER DIRECT TEST        NOT RUN
BENCHMARK HOST            HOLD / DORMANT
VERIFIED-RUN SCORE        NOT AVAILABLE
```

Do not mutate these values without direct execution artifacts.

## Selected primary state

### PostgreSQL 18.4

```text
PM-06
SCALE/PERFORMANCE VIABLE / HIGH CONFIDENCE

PM-07
MATERIAL OPERATIONS/RECOVERY/TOPOLOGY ADVANTAGE

PM-08
NATIVE FTS + PGVECTOR CONSOLIDATION ADVANTAGE

PM-09 EVIDENCE SCORE
89.25 / 100

SENSITIVITY
ROBUST LEADER

PM-10
PREFERRED / PASS-CONDITIONAL

PM-11
SELECTED — CANONICAL PRIMARY

PM-12
ACCEPTED PHYSICAL MODEL PRIMARY
```

### TypeDB CE 3.12.3

```text
PM-06
SCALE/PERFORMANCE VIABLE / MEDIUM-HIGH CONFIDENCE

PM-07
RECOVERY/EVOLUTION VIABLE / HIGHER SELF-HOSTED OPERATIONS COST

PM-08
SEMANTIC ADVANTAGE PRESERVED / EXTERNAL SEARCH-VECTOR SPECIALIST MORE LIKELY

PM-09 EVIDENCE SCORE
80.00 / 100

PM-10
NOT PREFERRED / RUNNER-UP

PM-11
NOT SELECTED

ROLE
HISTORICAL PRINCIPAL SEMANTIC CHALLENGER
```

## Accepted companion architecture

```text
PRIMARY
PostgreSQL 18.4

POSTGRESQL CAPABILITIES
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2

OFFLINE / SYNC
PowerSync Service 1.25.0 Open Edition
encrypted SQLite local state
PostgreSQL-backed PowerSync bucket storage

ASYNC CLASS A
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS B
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible subject
Restate Cloud EU allowed managed deployment

OBJECT
Cloudflare R2 Standard / EU jurisdiction / private

RECOVERY
pgBackRest 2.59.0 -> AWS S3 eu-south-1
R2 object backup -> separate AWS S3 eu-south-1 bucket

SOLVER
OR-Tools 9.15 CP-SAT

OBSERVABILITY
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
```

These mechanisms remain bounded by state ownership. None becomes a second canonical source of truth.

### Restate deployment rule

Restate is selected as the durable runtime; deployment is not globally fixed.

```text
SELF-HOSTED
FIRST-CLASS

CLOUD EU
ALLOWED MANAGED OPTION

GLOBAL DEFAULT
NONE
```

Current Restate documentation supports a self-contained binary/container and an EU Cloud region. Current client-side journal encryption is documented only for the TypeScript SDK, while the DANTE selected SDK path is Python. Therefore journal minimization is mandatory and deployment choice remains a later privacy/operability profile decision.

## Offline rule

Offline support is accepted as operation-specific capability, not global local-first authority.

```text
ENCRYPTED SQLITE
bounded local working copy

POWERSYNC
transport/sync projection

DANTE BACKEND
expected-state + governance + AuthZ + conflict authority

POSTGRESQL
canonical truth
```

A later-arriving offline mutation does not win by arrival order. Consequential LWW remains forbidden.

## Technology exclusion rule

PM-10 maintains the explicit exclusion register and PM-11 carries it into selection. Excluded technologies are not hidden future dependencies. Reintroduction requires a later architecture decision based on materially changed requirements/evidence.

## PM-09 scoring retained

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

```text
PostgreSQL 18.4     89.25
TypeDB CE 3.12.3    80.00
Delta               +9.25 PostgreSQL
```

Performance remains intentionally tied `8.0 / 8.0` because no direct LOW/BASE/HIGH DANTE run exists.

Accepted sensitivity remains:

```text
RANKING ROBUST
SENSITIVITY-DEPENDENT NO
PERFORMANCE-DEPENDENT NO
```

## Execution reopen decision

```text
SC-013 DEEP-HISTORY SCALE
REOPEN NO

PM-04B
REOPEN NO
```

Reason: selection does not depend on an unmeasured performance advantage and no ranking-critical direct execution gap emerged.

## Post-selection validation obligations

The dedicated selected-stack register remains authoritative:

```text
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

Core inherited obligations remain:

```text
SC-011 old-backup anti-resurrection
SC-030 actual DANTE V1 -> V2 mapping evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure truthful degradation
WL-H12 system-level non-interference
SC-017/018 search/non-interference
SC-019 vector recall after security filters
SC-020/021 projection freshness/deletion propagation
offline sync/reconciliation
```

Additional obligations cover PowerSync replication liveness, local encryption, Restate crash/replay/versioning and deployment privacy, R2/S3 object recovery, PostGIS/PgBouncer interactions, OR-Tools status semantics and observability privacy.

None is a direct PASS today unless separately executed and evidenced.

## PM-11..PM-14 / integration boundary

```text
PM-11
TARGET STACK SELECTED

PM-12
ACCEPTED PHYSICAL MODEL ESTABLISHED

PM-13
CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS

PM-14
TARGET-ARCHITECTURE BRANCH / WORKSTREAM CLOSURE COMPLETE

PR #15
PROTECTED-MAIN INTEGRATION COMPLETE

DIRECT EXECUTION
UNCHANGED / NOT STARTED

DEV-v0
SEPARATE NEXT OPERATIONAL PROFILE
```

## Current next step

```text
PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15
CANONICAL PRIMARY PostgreSQL 18.4
RESTATE DEPLOYMENT CONDITIONAL: SELF-HOSTED OR CLOUD EU
DIRECT HG PASS 0
VERIFIED-RUN SCORE NOT AVAILABLE

NEXT
separate Development Profile v0 scope

BACKEND
NOT STARTED / DEFERRED
```
