# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-03 STATIC PREFLIGHT COMPLETE / PM-04 NOT STARTED**
- Branch: `feature/physical-model`
- Base / bootstrap PRE-SCOPE: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00 bootstrap: **QA PASS**
- PM-01 technology/candidate freeze: **PASS-CONDITIONAL**
- PM-01 benchmark-host freeze: **HOLD**
- PM-02 primary mapping design: **COMPLETE**
- PM-03 semantic hard-gate preflight: **STATIC COMPLETE / 0 REJECTS**
- Executed hard gates: **NOT RUN**
- Database/harness execution: **NOT STARTED**
- Performance benchmark: **NOT STARTED**
- Selected primary persistence: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Turn the accepted Domain + Logical architecture into an evidence-backed Physical Model without selecting infrastructure by intuition, popularity, incumbent bias or vendor marketing.

```text
DOMAIN + LOGICAL
fixed semantic authority

PHASE 10
how evidence is judged

PHYSICAL MODEL
candidate discovery
-> candidate-native mapping
-> semantic preflight
-> executable correctness/destructive proof
-> performance/operations
-> bounded specialization
-> recommendation
-> explicit selection
```

## Mandatory authority order

Before new Physical work:

1. verify current `feature/physical-model` HEAD and compare to `main`;
2. read root/project status and development operating/safety rules;
3. read `docs/workstreams/physical-model.md` completely;
4. read this README;
5. read `execution-methodology-v1.md`;
6. read `execution-template-v1.md`;
7. read `acceptance-test-matrix-v1.md`;
8. read `result-register-v1.md`;
9. read `pm-01-technology-landscape-v1.md`;
10. read `pm-02-primary-mapping-overview-v1.md` + all four mapping files;
11. read `pm-03-semantic-hard-gate-preflight-v1.md` + all four preflight records;
12. read Phase-10 benchmark specification/scenario corpus/register;
13. read CLOSED Whole-Logical authority and `WL-H01..WL-H12` when semantics are involved;
14. verify current official product facts when version-sensitive;
15. issue an exact PRE-SCOPE/write gate before every new write scope.

Conversation memory never outranks repository current truth.

## Non-negotiable semantic barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
PREFERRED != SELECTED
MAPPING COMPLETE != HARD-GATE PASS
STATIC PREFLIGHT != EXECUTED PROOF
USED ELSEWHERE != RIGHT FOR LIFEOS
```

Never reintroduce as canonical shortcuts:

```text
universal Entity / Thing root
universal generic Relationship/edge root
generic EAV/property-bag kernel
universal Rule/Fact/WorkItem/Command root
provider ID/revision as canonical identity/state
missing row == false
storage/MVCC/changefeed token == MaterialStateRef
AI/solver output == accepted canonical effect
technical AuthZ allow == Domain Authority
per-recipient duplicate canonical reality
```

## Current primary candidates

### P0 — PostgreSQL 18.4

```text
SUBJECT
PostgreSQL 18.4
self-hosted single-node qualification topology
psycopg 3.3.4

PM-01
ADMIT

PM-02
PM02-PG-001 COMPLETE

PM-03
9 PASS-CONDITIONAL / 3 HOLD / 0 REJECT
ADVANCE

EXECUTED HG
NOT RUN

STATUS
pre-existing preferred baseline / NOT SELECTED
```

Primary pressure: heterogeneous address anchors, strong concurrency path selection, selective-disclosure leakage, history/evolution/restore.

### P1 — TypeDB CE 3.12.3

```text
SUBJECT
TypeDB CE 3.12.3
self-hosted single-node qualification topology
official driver 3.12.3

PM-01
ADMIT

PM-02
PM02-TDB-001 COMPLETE

PM-03
7 PASS-CONDITIONAL / 5 HOLD / 0 REJECT
ADVANCE WITH CONCURRENCY HOLD

CANDIDATE-SPECIFIC HOLD
HG-04 / HG-05 snapshot-isolation write-skew proof

EXECUTED HG
NOT RUN

STATUS
NOT SELECTED
```

### P2 — XTDB 2.1.0

```text
SUBJECT
XTDB 2.1.0
self-hosted qualification subject

PM-01
ADMIT / PRODUCTION TOPOLOGY HOLD

PM-02
PM02-XT-001 COMPLETE

PM-03
7 PASS-CONDITIONAL / 5 HOLD / 0 REJECT
ADVANCE WITH REFERENCE/CONSTRAINT HOLD

CANDIDATE-SPECIFIC HOLD
HG-02 / HG-03 ASSERT-based reference/cardinality enforcement

EXECUTED HG
NOT RUN

STATUS
NOT SELECTED
```

### P3 — SurrealDB Community 3.2.3

```text
SUBJECT
SurrealDB Community 3.2.3
single-node RocksDB qualification topology
Python SDK 2.0.0

PM-01
ADMIT-CONDITIONAL

PM-02
PM02-SDB-001 COMPLETE

PM-03
7 PASS-CONDITIONAL / 5 HOLD / 0 REJECT
ADVANCE WITH CONCURRENCY HOLD

CANDIDATE-SPECIFIC HOLD
HG-04 / HG-05 snapshot-isolation write-skew proof

EXECUTED HG
NOT RUN

STATUS
NOT SELECTED
```

## PM-03 result-layer rule

PM-03 deliberately separates static design confidence from executed evidence.

```text
STATIC PREFLIGHT
P0 ADVANCE
P1 ADVANCE WITH CONCURRENCY HOLD
P2 ADVANCE WITH REFERENCE/CONSTRAINT HOLD
P3 ADVANCE WITH CONCURRENCY HOLD

STATIC REJECTS
0

EXECUTED HG-01..HG-12
NOT RUN for every candidate
```

Generic future execution HOLDs remain for every candidate:

```text
HG-09 retention/redaction/tombstone/old-backup restore
HG-11 schema/data evolution
HG-12 recoverability/evidence quality
```

No candidate receives weighted score until all applicable executed hard gates pass.

## Current Physical work products

```text
execution-methodology-v1.md
execution-template-v1.md
acceptance-test-matrix-v1.md
result-register-v1.md

pm-01-technology-landscape-v1.md

pm-02-primary-mapping-overview-v1.md
mappings/postgresql-18.4-v1.md
mappings/typedb-3.12.3-v1.md
mappings/xtdb-2.1.0-v1.md
mappings/surrealdb-3.2.3-v1.md

pm-03-semantic-hard-gate-preflight-v1.md
preflight/postgresql-18.4-v1.md
preflight/typedb-3.12.3-v1.md
preflight/xtdb-2.1.0-v1.md
preflight/surrealdb-3.2.3-v1.md
```

The live save-game is `../workstreams/physical-model.md`.

## Primary hard gates

```text
HG-01 Semantic ownership preservation
HG-02 Reference-family integrity
HG-03 Typed / n-ary relation fidelity
HG-04 Expected-state consequential concurrency
HG-05 Multi-owner consistency truthfulness
HG-06 History / correction / reconciliation reconstructibility
HG-07 State-layer separation
HG-08 Governance / selective disclosure
HG-09 Retention / redaction / tombstone / restore integrity
HG-10 Temporal / recurrence / timezone fidelity
HG-11 Schema / data evolution integrity
HG-12 Recoverability / evidence quality
```

Performance cannot compensate for any material hard-gate failure.

## Next executable proof priorities

The first implementation/run work must target uncertainty, not benchmark speed.

Shared priority:

```text
SC-001 same-base consequential race
SC-003 atomic multi-owner mutation
SC-009 stale/offline divergence
SC-010 correction without false rewrite
SC-012 NativeRef non-reuse
SC-015 n-ary relation fidelity
SC-016 selective disclosure
SC-022/023 DST gap/fold
SC-024 individual recurrence override
SC-030 V1->V2 evolution
SC-011 + SC-031 restore/anti-resurrection
```

Candidate-specific priority:

```text
PostgreSQL
anchor integrity + transaction-strength negative/positive controls

TypeDB
snapshot write-skew negative control + shared consistency-guard positive control

XTDB
wrong-family/missing-reference + cardinality/uniqueness ASSERT pressure

SurrealDB
snapshot write-skew negative control + shared consistency-guard positive control
```

## Benchmark-host HOLD

The exact execution host remains unresolved.

Before reproducible executable evidence begins, freeze and record:

```text
host identity
CPU/RAM available to benchmark
OS/build
container/native strategy
filesystem/storage device
free disk budget
network/topology
resource limits
background-load policy
clock/timezone
```

Do not silently infer the host from remembered hardware in conversation.

## Secondary/specialist lanes

PM-03 does not activate these lanes.

```text
GRAPH
G0 no-specialized-store baseline
Neo4j DEFER PM-08

SEARCH/VECTOR
primary-native structured/lexical baseline
pgvector DEFER PM-08 when PostgreSQL applicable
Qdrant/OpenSearch specialist trigger only

LOCAL/OFFLINE
SQLite future bounded client role

DURABLE EXECUTION
Restate / Temporal / DBOS not selected by persistence workstream
```

The final system may use multiple technologies, but every extra engine must prove net semantic/operational value. No secondary engine may hide a hard-gate failure in the primary canonical store.

## Cost/exit policy

```text
TARGET
EUR 0 initial direct technology/license cost where realistically possible

BUT
quality/correctness outrank cost
paid != automatic rejection
free != automatic preference
```

Preserve portability where cheap/useful; use candidate-native strengths where materially better; do not build gratuitous lowest-common-denominator abstraction.

## Evidence-before-claim rules

```text
no benchmark from documentation
no hard-gate PASS from marketing
no score from static mapping
no performance before correctness
missing evidence = HOLD
candidate failure != tooling failure
product + version + edition + deployment = subject
same semantics + same assertions + idiomatic candidate mapping
```

## Current exact next step

```text
PM-03
STATIC PREFLIGHT COMPLETE
FINAL REMOTE QA OF PM-03 WRITE SCOPE REQUIRED

PM-04
NOT STARTED

BEFORE EXECUTABLE EVIDENCE
close benchmark-host HOLD

NO performance scoring
NO technology selection
NO backend/API/Auth implementation
```
