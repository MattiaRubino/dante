# Physical Model Result Register v1

- Status: **CURRENT — PM-04A EVIDENCE SUFFICIENCY COMPLETE / PM-04B NOT ADMITTED**
- Workstream: `feature/physical-model`
- Direct benchmark execution: **NOT STARTED**
- Technology selection: **NONE**
- PM-01 evidence: `pm-01-technology-landscape-v1.md`
- PM-02 evidence: `pm-02-primary-mapping-overview-v1.md` + candidate mappings
- PM-03 evidence: `pm-03-semantic-hard-gate-preflight-v1.md` + candidate preflight records
- PM-04A evidence: `pm-04-external-evidence-sufficiency-v1.md` + candidate evidence records

## 1. Result-language rule

```text
OFFICIAL CLAIM != EXECUTED PROOF
ADMIT != HARD-GATE PASS
MAPPING COMPLETE != HARD-GATE PASS
PM-03 PASS-CONDITIONAL != EXECUTED PASS
PM-04A EXT/MAP-SUFFICIENT != EXECUTED PASS
PUBLIC BENCHMARK != LIFEOS BENCHMARK
NOT RUN != PASS
PREFERRED != SELECTED
```

PM-04A classifies whether more execution is currently necessary. It does not fabricate direct-run results.

## 2. Current phase state

```text
PM-00
QA PASS

PM-01
PASS-CONDITIONAL
benchmark host HOLD / now dormant until direct execution admission

PM-02
PRIMARY MAPPING DESIGN COMPLETE

PM-03
STATIC PREFLIGHT COMPLETE
0 candidate REJECTs

PM-04A
EXTERNAL EVIDENCE SUFFICIENCY COMPLETE
48 / 48 candidate × HG cells classified
0 EXECUTION-WORTHY gaps

PM-04B
NOT ADMITTED
fixture/harness NOT STARTED

PM-05+
NOT STARTED

DIRECT PERFORMANCE
NOT STARTED

SELECTION
NONE
```

## 3. PM-03 cross-candidate preflight result

Historical/current preflight layer remains:

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

PM-04A does not rewrite this chronology. It adds a new evidence-sufficiency layer.

## 4. PM-04A evidence-sufficiency result

| Gate | P0 PostgreSQL | P1 TypeDB | P2 XTDB | P3 SurrealDB |
|---|---|---|---|---|
| HG-01 | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-02 | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST | EXT+MAP-SUFFICIENT |
| HG-03 | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | KNOWN-STRUCTURAL-COST | EXT+MAP-SUFFICIENT |
| HG-04 | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / guard condition | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / guard condition |
| HG-05 | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST |
| HG-06 | MAP-SUFFICIENT | MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT / KNOWN COST |
| HG-07 | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-08 | MAP-SUFFICIENT / DEFER-FINALIST | MAP-SUFFICIENT / DEFER-FINALIST | MAP-SUFFICIENT / DEFER-FINALIST | MAP-SUFFICIENT / DEFER-FINALIST |
| HG-09 | DEFER-FINALIST | DEFER-FINALIST / KNOWN OPS COST | DEFER-FINALIST | DEFER-FINALIST |
| HG-10 | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | EXT+MAP-SUFFICIENT | MAP-SUFFICIENT |
| HG-11 | DEFER-FINALIST | EXT+DEFER-FINALIST | KNOWN-STRUCTURAL-COST + DEFER-FINALIST | EXT+DEFER-FINALIST |
| HG-12 | EXT+DEFER-FINALIST | KNOWN OPS COST + DEFER-FINALIST | KNOWN OPS/TOPOLOGY COST + DEFER-FINALIST | EXT+DEFER-FINALIST |

Interpretation:

```text
EXT/MAP-SUFFICIENT
= enough for current comparative reasoning
!= direct PASS

KNOWN-STRUCTURAL-COST
= candidate burden that should count against the candidate
!= unresolved behavior needing a toy test

DEFER-FINALIST
= retain direct/system rehearsal obligation for a finalist if still material

EXECUTION-WORTHY
= would open PM-04B
```

Current count:

```text
EXECUTION-WORTHY
0
```

## 5. Direct hard-gate status

Unchanged and intentionally explicit:

```text
P0 PostgreSQL HG-01..HG-12   NOT RUN
P1 TypeDB HG-01..HG-12       NOT RUN
P2 XTDB HG-01..HG-12         NOT RUN
P3 SurrealDB HG-01..HG-12    NOT RUN
```

No candidate has a LifeOS direct-run hard-gate PASS and no measured score exists.

## 6. P0 — PostgreSQL 18.4

```text
ROLE
mandatory baseline / current comparative leader

EXACT SUBJECT
PostgreSQL 18.4
self-hosted single-node qualification topology
psycopg 3.3.4

PM-01
ADMIT

PM-02 MAPPING
PM02-PG-001 COMPLETE

PM-03
9 PASS-CONDITIONAL / 3 HOLD / 0 REJECT

PM-04A
HIGH engine-fundamental confidence
MEDIUM-HIGH LifeOS mapping confidence
0 execution-worthy gaps

DIRECT HG
NOT RUN

SCORE
NOT RUN

CURRENT DISPOSITION
CURRENT COMPARATIVE LEADER
NOT PREFERRED BY PM-09
NOT SELECTED
```

Current residual pressure:

- heterogeneous address anchors must stay purely technical;
- operation-specific transaction strength still matters despite strong Serializable/constraint primitives;
- RLS is a useful primitive, not complete WL-H12 proof;
- old-backup anti-resurrection and actual LifeOS V1→V2 continuity remain finalist obligations if still required.

Generic local CRUD/performance execution is not admitted.

## 7. P1 — TypeDB CE 3.12.3

```text
ROLE
principal semantic challenger

EXACT SUBJECT
TypeDB CE 3.12.3
self-hosted single-node qualification topology
official driver 3.12.3

PM-01
ADMIT

PM-02 MAPPING
PM02-TDB-001 COMPLETE

PM-03
HG-04/HG-05 HOLD

PM-04A
concurrency uncertainty narrowed to documented guard condition/design cost
0 execution-worthy gaps

DIRECT HG
NOT RUN

SCORE
NOT RUN

CURRENT DISPOSITION
PRINCIPAL SEMANTIC CHALLENGER
NOT SELECTED
```

PM-04A reasoning:

```text
snapshot isolation
+ documented same-data write conflict
+ every invariant-sharing operation mutates same narrow guard
→ credible common conflict point
```

This does not make snapshot isolation serializable. Correct guard scope/coverage remains a material mapping/operability burden and will count in later comparison.

Reopen targeted direct concurrency proof only if later ranking becomes materially dependent on it.

## 8. P2 — XTDB 2.1.0

```text
ROLE
temporal/bitemporal challenger

EXACT SUBJECT
XTDB 2.1.0
self-hosted qualification subject
Postgres-wire client path where applicable

PM-01
ADMIT / PRODUCTION TOPOLOGY HOLD

PM-02 MAPPING
PM02-XT-001 COMPLETE

PM-03
HG-02/HG-03 HOLD

PM-04A
HG-02/HG-03 uncertainty narrowed to KNOWN STRUCTURAL COST
serialized/serializable DML + ASSERT strongly supports HG-04/HG-05 path
0 execution-worthy gaps

PRODUCTION TOPOLOGY
HOLD

DIRECT HG
NOT RUN

SCORE
NOT RUN

CURRENT DISPOSITION
DISTINCTIVE TEMPORAL CHALLENGER
NOT SELECTED
```

Known structural costs:

- no native foreign keys;
- no general uniqueness beyond `_id`;
- referential/cardinality enforcement depends on deterministic IDs, ASSERT and complete mutation discipline;
- non-interactive transactions constrain governed-operation ergonomics;
- production/single-writer topology sensitivity remains.

A small local test cannot eliminate these architecture costs, so no such test is admitted now.

## 9. P3 — SurrealDB Community 3.2.3

```text
ROLE
constrained multimodel challenger

EXACT SUBJECT
SurrealDB Community 3.2.3
single-node RocksDB qualification topology
Python SDK 2.0.0

PM-01
ADMIT-CONDITIONAL

PM-02 MAPPING
PM02-SDB-001 COMPLETE

PM-03
HG-04/HG-05 HOLD

PM-04A
concurrency uncertainty narrowed to documented guard condition/design cost
explicit long-lived material history still required
0 execution-worthy gaps

DIRECT HG
NOT RUN

SCORE
NOT RUN

CURRENT DISPOSITION
CREDIBLE MULTIMODEL CHALLENGER
NOT SELECTED
```

The candidate's consolidation value remains real, but PM-04A did not find a unique primary-store benefit sufficient to overtake the current first three under LifeOS correctness-first priorities.

## 10. Non-scored comparative ordering

This is not PM-09 scoring and does not create `PREFERRED`.

```text
1 PostgreSQL
  current overall leader
  confidence HIGH

2 TypeDB
  principal semantic challenger
  confidence MEDIUM-HIGH

3 XTDB
  strongest distinctive temporal proposition
  confidence MEDIUM-HIGH temporal / MEDIUM overall primary fit

4 SurrealDB
  credible multimodel challenger
  confidence MEDIUM
```

Counts are not scores. The ordering may change during PM-05..PM-09 if new material evidence appears.

## 11. PM-04B admission result

```text
FULL FOUR-CANDIDATE LOCAL BENCHMARK
NOT ADMITTED

TARGETED LOCAL PROOFS
0 ADMITTED

FIXTURE GENERATOR
NOT STARTED

HARNESS
NOT STARTED

DATABASE DEPLOYMENT
NOT STARTED

BENCHMARK HOST
HOLD / DORMANT
```

The benchmark host becomes an active blocker only before a separately admitted direct execution claim.

## 12. Residual/direct obligations carried forward

### All candidates

```text
WL-H12 system-level non-interference
→ database mapping evidence sufficient for current comparison
→ finalist/downstream system proof may remain

old-backup anti-resurrection
→ DEFER-FINALIST

LifeOS V1 -> V2 semantic migration
→ DEFER-FINALIST

semantic post-restore verification
→ DEFER-FINALIST
```

### Candidate-specific

```text
PostgreSQL
anchor complexity = MAP-SUFFICIENT / reopen only on concrete leakage

TypeDB
consistency guard = MAP-SUFFICIENT + KNOWN DESIGN COST
reopen direct proof only if ranking-critical

XTDB
manual RI/cardinality = KNOWN STRUCTURAL COST
production topology HOLD remains

SurrealDB
consistency guard = MAP-SUFFICIENT + KNOWN DESIGN COST
reopen direct proof only if ranking-critical
```

## 13. Secondary lanes

### Graph

```text
G0 primary-store/no-specialized-store baseline
G1 Neo4j DEFER TO PM-08
```

### Search/vector

```text
S0 primary-native structured/lexical baseline
pgvector DEFER TO PM-08 when PostgreSQL applicable
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

Persistence work does not select workflow runtime.

## 14. Historical checkpoints

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

PM-03 PRE-SCOPE
db127af8c759aacf69b43d0f5a5444b04fd43759

PM-03 terminal HEAD
0e4212909bd94de076c9074302a79296d474e53f

PM-04A PRE-SCOPE
0e4212909bd94de076c9074302a79296d474e53f
```

The final PM-04A remote-QA checkpoint is recorded in the workstream handoff after verification.

## 15. Evidence paths

```text
PM-03
docs/physical-model/pm-03-semantic-hard-gate-preflight-v1.md
docs/physical-model/preflight/postgresql-18.4-v1.md
docs/physical-model/preflight/typedb-3.12.3-v1.md
docs/physical-model/preflight/xtdb-2.1.0-v1.md
docs/physical-model/preflight/surrealdb-3.2.3-v1.md

PM-04A
docs/physical-model/pm-04-external-evidence-sufficiency-v1.md
docs/physical-model/evidence/postgresql-18.4-v1.md
docs/physical-model/evidence/typedb-3.12.3-v1.md
docs/physical-model/evidence/xtdb-2.1.0-v1.md
docs/physical-model/evidence/surrealdb-3.2.3-v1.md
```

## 16. Direct-result mutation protocol

Before changing any direct hard-gate from `NOT RUN`:

1. prove the unresolved question is actually execution-worthy or a finalist/closure obligation;
2. obtain a fresh exact execution/write gate;
3. freeze actual benchmark host/runtime;
4. identify exact mapping/schema/harness revision;
5. identify scenario/corpus/fixture revision and seed;
6. retain raw assertion/concurrency output;
7. classify candidate-specific failure versus tooling/environment failure;
8. update only evidence-backed direct gates;
9. preserve unresolved items honestly;
10. remote-read back register and evidence;
11. never award measured performance values without a real run.

Before `SELECTED`, PM-11 explicit user-approved gate remains mandatory.

## 17. Current next step

```text
PM-04A
CONTENT COMPLETE
REMOTE QA REQUIRED FOR THIS WRITE SCOPE

PM-04B
NOT ADMITTED

PM-05
NEXT AFTER FRESH GATE
evidence-backed correctness/destructive qualification
no local execution by default

BENCHMARK HOST
HOLD / DORMANT

NO PERFORMANCE RUN
NO SELECTION
NO PRODUCTION BACKEND
```
