# Workstream — Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-09 COMPLETE / PM-10 NEXT**
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
- PM-09: **EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE**
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Evidence-weighted score: **PostgreSQL 89.25 / TypeDB 80.00**
- Ranking: **ROBUST / NOT SENSITIVITY-DEPENDENT / NOT PERFORMANCE-DEPENDENT**
- Current evidence-score leader: **PostgreSQL 18.4**
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
25. read Phase-10 scenario corpus/register where scenario authority matters;
26. read complete Whole-Logical authority and relevant decision-register continuations when semantics are involved;
27. verify current external product/version/edition/topology facts from primary sources where material;
28. issue a fresh exact PRE-SCOPE/write gate before repository mutation.

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
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
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

Final architecture may use one canonical primary plus bounded specialists. Every extra engine must earn complexity; no specialist may hide a primary hard-gate problem.

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

PM-09 PRE-SCOPE
6aef5537edacff3e315d502a1bd3ede544dc149e
```

The final PM-09 HEAD must be read from remote Git after the current write scope; do not guess a self-referential SHA inside this creating payload.

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

PM-06/07 established both finalists as viable, with PostgreSQL holding the material operations/recovery/topology advantage and TypeDB preserving the semantic-model advantage.

PM-08 admitted no initial extra server specialist, admitted pgvector conditionally for a PostgreSQL vector path, and admitted SQLite only as bounded local/offline candidate state.

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

GRAPH / SEARCH / VECTOR / SQLITE BENCHMARKS
NOT RUN

BENCHMARK HOST
HOLD / DORMANT

VERIFIED-RUN BENCHMARK SCORE
NOT AVAILABLE
```

Do not convert evidence qualification or PM-09 scoring into direct PASS.

## 8. Phase-10 scoring reconciliation

The original executable Phase-10 benchmark ledger remains valid and unchanged in its hard gates and weights.

PM-09 adds a separate evidence-first ledger:

```text
VERIFIED-RUN BENCHMARK SCORE
requires direct applicable HG PASS + direct execution artifacts

EVIDENCE-WEIGHTED DECISION SCORE
allowed only after evidence exhaustion and 0 ranking-critical execution-worthy gaps
```

```text
EVIDENCE-WEIGHTED DECISION SCORE
!= VERIFIED-RUN BENCHMARK SCORE
```

The original 100-point weights remain unchanged:

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

PM-09 does not create a direct hard-gate PASS and does not waive selected-implementation validation.

## 9. PM-09 scoring result

### PostgreSQL 18.4

```text
semantic      8.5
transaction   9.5
query         9.0
history       8.5
operations    9.5
evolution     9.0
performance   8.0
tooling       9.5

EVIDENCE-WEIGHTED TOTAL
89.25 / 100
```

Disposition:

```text
ROBUST EVIDENCE-SCORE LEADER
ADVANCE PM-10
PREFERRED NONE
SELECTED NONE
```

### TypeDB CE 3.12.3

```text
semantic      9.5
transaction   7.0
query         8.5
history       8.5
operations    6.5
evolution     8.0
performance   8.0
tooling       7.0

EVIDENCE-WEIGHTED TOTAL
80.00 / 100
```

Disposition:

```text
PRINCIPAL SEMANTIC CHALLENGER
ADVANCE PM-10 COMPARATIVE RECORD
PREFERRED NONE
SELECTED NONE
```

Performance is deliberately tied `8.0 / 8.0`; no unexecuted throughput/latency advantage is invented.

## 10. PM-09 sensitivity

Accepted scenarios:

```text
S0 Phase-10 base
PG 89.25 / TypeDB 80.00 / PG +9.25

S1 semantic-heavy
PG 88.75 / TypeDB 83.00 / PG +5.75

S2 early single-node / semantic-friendly
PG 88.75 / TypeDB 81.50 / PG +7.25

S3 operations/recovery-heavy
PG 90.00 / TypeDB 77.50 / PG +12.50

S4 strongly TypeDB-friendly accepted stress
PG 88.00 / TypeDB 85.25 / PG +2.75
```

Verdict:

```text
RANKING ROBUST
SENSITIVITY-DEPENDENT NO
PERFORMANCE-DEPENDENT NO
```

Adversarial boundary only:

```text
semantic 50%
PG 87.375
TypeDB 87.500
TypeDB +0.125
```

This is not an accepted LifeOS priority distribution.

If the seven non-semantic dimensions retain their original relative proportions, semantic mapping must reach approximately `58.44%` of total weight before TypeDB reaches break-even.

## 11. Execution reopen decision

```text
PM-09 EXECUTION-WORTHY GAPS
0

SC-013 DEEP-HISTORY SCALE
REOPEN NO

PM-04B HARNESS
REOPEN NO

BENCHMARK HOST
HOLD / DORMANT
```

The current ranking does not depend on an unmeasured performance advantage.

## 12. PM-08 specialist state

```text
GRAPH
G0 primary baseline ADVANCE
Neo4j DEFER / NOT REJECTED
initial graph specialist NONE

SEARCH/VECTOR
PostgreSQL native FTS ADVANCE as P0 baseline
pgvector 0.8.6 ADMIT-CONDITIONAL
Qdrant 1.18.2 DEFER / TRIGGER ONLY
OpenSearch 3.7 DEFER / TRIGGER ONLY

LOCAL/OFFLINE
SQLite 3.53.4 ADMIT BOUNDED LOCAL/OFFLINE CANDIDATE
CANONICAL AUTHORITY NO

OBJECT/BLOB
NO ENGINE ADMITTED
TRIGGER ONLY
```

If PostgreSQL wins, the minimum credible initial server path remains PostgreSQL + native FTS + conditional pgvector, with no initial Neo4j/Qdrant/OpenSearch server.

If TypeDB wins, its semantic advantage remains real but an external search/vector specialist is more likely once advanced retrieval becomes accepted; that burden is part of the PM-09 score.

## 13. Post-selection implementation validation obligations

Still mandatory where applicable:

```text
SC-011 redaction + old-backup anti-resurrection
SC-030 actual LifeOS V1→V2 mapping evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure truthful degradation
WL-H12 system-level non-interference
SC-017/018 search/non-interference where active
SC-019 vector recall after real security filter where active
SC-020/021 projection freshness/deletion propagation where active
local/offline sync/reconciliation validation where active
```

None is a direct PASS today.

## 14. PM-09 evidence paths

```text
docs/physical-model/pm-09-scoring-sensitivity-v1.md
docs/physical-model/scoring/postgresql-18.4-v1.md
docs/physical-model/scoring/typedb-3.12.3-v1.md
docs/physical-model/scoring/sensitivity-analysis-v1.md
```

Phase-10 reconciliation lives in:

```text
docs/architecture/physical-benchmark-specification.md
```

## 15. Roadmap

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
PM-10  NEXT
PM-11  NOT STARTED
PM-12  NOT STARTED
PM-13  NOT STARTED
PM-14  NOT STARTED
```

## 16. Current resume summary

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

PM-09 EVIDENCE SCORES
PostgreSQL 89.25
TypeDB 80.00

CURRENT EVIDENCE-SCORE LEADER
PostgreSQL 18.4

RANKING
ROBUST / NOT SENSITIVITY-DEPENDENT / NOT PERFORMANCE-DEPENDENT

DEFERRED / NOT REJECTED PRIMARY
XTDB 2.1.0
SurrealDB Community 3.2.3

LOCAL TESTS
0 ADMITTED

DIRECT HG PASS
0

VERIFIED-RUN SCORE
NOT AVAILABLE

PREFERRED
NONE

SELECTED
NONE

BACKEND
NOT STARTED / DEFERRED

NEXT
PM-10 recommendation
fresh exact gate before write
```

The exact PM-09 final remote HEAD must be taken from Git after this handoff write.