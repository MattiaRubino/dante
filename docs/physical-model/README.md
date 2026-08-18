# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-04A EVIDENCE SUFFICIENCY COMPLETE / PM-04B NOT ADMITTED**
- Branch: `feature/physical-model`
- Base / bootstrap PRE-SCOPE: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00 bootstrap: **QA PASS**
- PM-01 technology/candidate freeze: **PASS-CONDITIONAL**
- PM-01 benchmark-host freeze: **HOLD / DORMANT UNTIL DIRECT EXECUTION**
- PM-02 primary mapping design: **COMPLETE**
- PM-03 semantic hard-gate preflight: **STATIC COMPLETE / 0 REJECTS**
- PM-04A external evidence sufficiency: **COMPLETE / 0 EXECUTION-WORTHY GAPS**
- PM-04B fixture/harness: **NOT ADMITTED / NOT STARTED**
- Executed hard gates: **NOT RUN**
- Database execution: **NOT STARTED**
- Performance benchmark: **NOT STARTED**
- Selected primary persistence: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Turn the accepted Domain + Logical architecture into an evidence-backed Physical Model without selecting infrastructure by intuition, popularity, incumbent bias, vendor marketing or ritual benchmarking.

```text
DOMAIN + LOGICAL
fixed semantic authority

PHASE 10
how evidence is judged

PHYSICAL MODEL
candidate discovery
-> candidate-native mapping
-> semantic preflight
-> external-evidence sufficiency
-> direct proof only where genuinely necessary
-> performance/operations only where decision-relevant
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
12. read `pm-04-external-evidence-sufficiency-v1.md` + all four evidence records;
13. read Phase-10 benchmark specification/scenario corpus/register;
14. read CLOSED Whole-Logical authority and `WL-H01..WL-H12` when semantics are involved;
15. verify current official product facts when version-sensitive;
16. issue an exact PRE-SCOPE/write gate before every new write scope.

Conversation memory never outranks repository current truth.

## Non-negotiable semantic/evidence barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
PREFERRED != SELECTED
MAPPING COMPLETE != HARD-GATE PASS
STATIC PREFLIGHT != EXECUTED PROOF
EXTERNAL EVIDENCE != DIRECT LIFEOS RUN
PUBLIC BENCHMARK != LIFEOS BENCHMARK
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

PM-04A
CURRENT COMPARATIVE LEADER
engine fundamentals confidence HIGH
LifeOS mapping confidence MEDIUM-HIGH
0 EXECUTION-WORTHY gaps

DIRECT HG
NOT RUN

STATUS
NOT PM-09 PREFERRED
NOT SELECTED
```

Current pressure: heterogeneous anchors must remain purely technical; strong transactional primitives still require correct operation-specific use; RLS does not by itself satisfy WL-H12; restore/evolution are finalist obligations if still material.

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
HG-04 / HG-05 concurrency HOLD

PM-04A
PRINCIPAL SEMANTIC CHALLENGER
snapshot-isolation uncertainty narrowed to documented guard condition/design cost
0 EXECUTION-WORTHY gaps

DIRECT HG
NOT RUN

STATUS
NOT SELECTED
```

TypeDB retains the strongest relation/role/n-ary semantic fit. The narrow consistency guard is conditionally credible because invariant-sharing transactions deliberately write the same conflict point; correct guard coverage/scoping remains a real complexity cost rather than an unknown engine primitive.

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
HG-02 / HG-03 reference/constraint HOLD

PM-04A
DISTINCTIVE TEMPORAL/BITEMPORAL CHALLENGER
no-FK/no-general-uniqueness uncertainty narrowed to KNOWN STRUCTURAL COST
serialized/serializable DML + ASSERT strongly supports concurrency path
0 EXECUTION-WORTHY gaps

DIRECT HG
NOT RUN

STATUS
PRODUCTION TOPOLOGY HOLD
NOT SELECTED
```

XTDB's chronology proposition is unusually relevant to LifeOS, but manual referential/cardinality enforcement, non-interactive transaction ergonomics and production topology/single-writer sensitivity remain material costs. A laptop test cannot erase them.

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
HG-04 / HG-05 concurrency HOLD

PM-04A
CREDIBLE MULTIMODEL CHALLENGER
concurrency uncertainty narrowed to documented guard condition/design cost
explicit material history remains required
0 EXECUTION-WORTHY gaps

DIRECT HG
NOT RUN

STATUS
NOT SELECTED
```

SurrealDB's consolidation value is real, but PM-04A found no unique primary-store advantage yet large enough to overcome the comparative maturity/history/concurrency-discipline burden versus the leaders.

## PM-04A evidence rule

PM-04A classifies evidence sufficiency, not test outcomes.

```text
EXT-SUFFICIENT
MAP-SUFFICIENT
KNOWN-STRUCTURAL-COST
DEFER-FINALIST
RESIDUAL-GAP
EXECUTION-WORTHY
```

Only an unresolved, decision-relevant `EXECUTION-WORTHY` question normally opens PM-04B.

Current result:

```text
48 / 48 candidate × HG cells classified
EXECUTION-WORTHY gaps       0
FULL LOCAL BENCHMARK        NOT ADMITTED
TARGETED LOCAL PROOFS       0 ADMITTED
PM-04B HARNESS              NOT ADMITTED
DIRECT HG-01..HG-12         NOT RUN all candidates
```

## Non-scored comparative ordering

This is current decision pressure only. It is **not PM-09 score**, `PREFERRED` or `SELECTED`.

```text
1 PostgreSQL
  current overall leader
  confidence HIGH

2 TypeDB
  principal semantic challenger
  confidence MEDIUM-HIGH

3 XTDB
  distinctive temporal challenger
  confidence MEDIUM-HIGH temporal / MEDIUM overall primary fit

4 SurrealDB
  credible multimodel challenger
  confidence MEDIUM
```

The ordering remains reopenable by material PM-05..PM-09 evidence.

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

pm-04-external-evidence-sufficiency-v1.md
evidence/postgresql-18.4-v1.md
evidence/typedb-3.12.3-v1.md
evidence/xtdb-2.1.0-v1.md
evidence/surrealdb-3.2.3-v1.md
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

## Residual obligations carried forward

### All candidates

```text
WL-H12 system-level non-interference
→ database evidence sufficient for current comparative reasoning
→ downstream/finalist proof may remain

old-backup anti-resurrection
→ DEFER-FINALIST

actual LifeOS V1 -> V2 semantic migration
→ DEFER-FINALIST

semantic post-restore verification
→ DEFER-FINALIST
```

### Candidate-specific

```text
PostgreSQL
anchor complexity = mapping/evolvability pressure

TypeDB
consistency-guard coverage = known design/operability cost

XTDB
manual RI/cardinality = known structural cost
production topology HOLD remains

SurrealDB
consistency-guard coverage = known design/operability cost
explicit long-lived history remains required
```

## Benchmark-host HOLD

The exact execution host remains unresolved by design.

```text
BENCHMARK HOST
HOLD / DORMANT
```

It does **not** block evidence-only work. Before any reproducible direct execution claim, freeze and record:

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

Do not silently infer the host from conversation hardware.

## Secondary/specialist lanes

PM-04A does not activate these lanes.

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
no hard-gate PASS from documentation
no direct-run claim from external evidence
no score from static/evidence-only mapping
no performance measurement without an actual run
missing material evidence = HOLD or explicit condition
known structural limitation = candidate cost, not automatic test request
candidate failure != tooling failure
product + version + edition + deployment = subject
same semantics + same assertions + idiomatic candidate mapping when direct comparison is admitted
```

## Fixed Physical roadmap

```text
PM-00  Bootstrap / authority freeze                         PASS
PM-01  Technology discovery / candidate freeze             PASS-CONDITIONAL
PM-02  Primary candidate mapping design                    COMPLETE
PM-03  Semantic hard-gate static preflight                 COMPLETE
PM-04A External evidence sufficiency                       COMPLETE
PM-04B Conditional fixture/oracle/harness                  NOT ADMITTED
PM-05  Correctness/destructive evidence qualification      NEXT / NOT STARTED
PM-06  Scale/performance evidence                           NOT STARTED
PM-07  Recovery/evolution/failure evidence                 NOT STARTED
PM-08  Secondary lanes where justified                     NOT STARTED
PM-09  Scoring + sensitivity                               NOT STARTED
PM-10  Recommendation                                      NOT STARTED
PM-11  Explicit selection gate                             NOT STARTED
PM-12  Accepted Physical Model                             NOT STARTED
PM-13  Independent clean-room QA                           NOT STARTED
PM-14  Closure / protected main integration                NOT STARTED
```

The numbered sequence remains fixed; PM-04A/PM-04B are sub-stages inside PM-04.

## Current exact next step

```text
PM-04A
CONTENT COMPLETE
REMOTE QA REQUIRED FOR CURRENT WRITE SCOPE

PM-04B
NOT ADMITTED

PM-05
NEXT AFTER FRESH EXPLICIT GATE
evidence-backed correctness/destructive qualification
no local execution by default

BENCHMARK HOST
HOLD / DORMANT

NO performance run
NO technology selection
NO backend/API/Auth implementation
```
