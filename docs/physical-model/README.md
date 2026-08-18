# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-05 COMPLETE / PM-06+PM-07 JOINT NEXT**
- Branch: `feature/physical-model`
- Base: `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL**
- PM-02: **COMPLETE**
- PM-03: **STATIC COMPLETE / 0 REJECTS**
- PM-04A: **COMPLETE / 48 OF 48 CELLS CLASSIFIED / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED / NOT STARTED**
- PM-05: **COMPLETE / PRIMARY FINALISTS = POSTGRESQL + TYPEDB**
- PM-06+PM-07: **JOINT FINALIST QUALIFICATION NEXT**
- Direct hard-gate execution: **NOT RUN**
- Database/harness execution: **NOT STARTED**
- Technology selection: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Turn the closed LifeOS Domain + Logical model into an evidence-backed Physical Model without selecting technology by popularity, intuition, vendor marketing or ritual benchmarking.

```text
Domain + Logical
fixed semantic authority

Physical
technology discovery
→ candidate-native mapping
→ semantic preflight
→ evidence sufficiency
→ correctness scenario qualification
→ finalist scale/recovery qualification
→ secondary lanes
→ scoring/sensitivity
→ recommendation
→ explicit selection
```

## Authority order

Before new Physical work:

1. verify current `feature/physical-model` HEAD and relation to `main`;
2. read root/project status and development operating/safety rules;
3. read `docs/workstreams/physical-model.md` completely;
4. read this README;
5. read `execution-methodology-v1.md`;
6. read `execution-template-v1.md`;
7. read `acceptance-test-matrix-v1.md`;
8. read `result-register-v1.md`;
9. read PM-01 landscape;
10. read PM-02 overview + four mappings;
11. read PM-03 overview + four preflight records;
12. read PM-04A overview + four evidence records;
13. read PM-05 overview + four qualification records;
14. read Phase-10 benchmark specification/corpus/register;
15. read closed Whole-Logical authority and `WL-H01..WL-H12` where semantics are involved;
16. verify current external product/version facts from primary sources where material;
17. issue an exact write gate before every repository write.

Conversation memory never outranks repository current truth.

## Non-negotiable barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
STATIC/EVIDENCE SUFFICIENCY != DIRECT EXECUTION
PUBLIC BENCHMARK != LIFEOS BENCHMARK
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
```

Never reintroduce:

```text
universal Entity/Thing root
universal generic Relationship/edge root
generic EAV/property-bag canonical kernel
universal Rule/Fact/WorkItem/Command root
provider ID/revision as canonical identity/material state
missing row == false
storage/MVCC/system-time/changefeed token == MaterialStateRef
technical AuthZ == Domain Authority/Consent
AI/solver result == canonical truth/effect
per-recipient duplicate canonical reality
```

## Current primary finalist set

### P0 — PostgreSQL 18.4

```text
ROLE
current comparative leader / primary finalist

SUBJECT
PostgreSQL 18.4
self-hosted single-node qualification topology
psycopg 3.3.4

PM-02
PM02-PG-001 COMPLETE

PM-04A
0 execution-worthy gaps

PM-05
ADVANCE TO PM-06/07 JOINT

DIRECT HG
NOT RUN

PREFERRED
NO

SELECTED
NO
```

Strengths:

- native relational integrity/constraint ecosystem;
- true Serializable/locking paths;
- mature operations/recovery tooling;
- low aggregate primary-store structural risk;
- LifeOS mapping preserves explicit identity/history/state layers without meta-model collapse.

Current pressure:

- heterogeneous address anchors must remain purely technical;
- isolation/locking strength remains invariant-specific;
- RLS is not complete WL-H12 proof;
- finalist scale/recovery/evolution evidence remains.

### P1 — TypeDB CE 3.12.3

```text
ROLE
principal semantic challenger / primary finalist

SUBJECT
TypeDB CE 3.12.3
self-hosted single-node qualification topology
driver 3.12.3

PM-02
PM02-TDB-001 COMPLETE

PM-04A
0 execution-worthy gaps

PM-05
ADVANCE TO PM-06/07 JOINT
CONDITION narrow consistency-guard coverage required

DIRECT HG
NOT RUN

PREFERRED
NO

SELECTED
NO
```

Strengths:

- strongest typed relation/role/n-ary semantic fit;
- natural Agreement/common-ground representation;
- schema role/cardinality semantics;
- no generic canonical edge/object root required.

Current pressure:

- snapshot isolation remains the transaction model;
- correct consistency-guard scoping is mandatory for write-skew-sensitive invariants;
- explicit material-state/history structures remain required;
- operations/recovery/tooling burden must be compared against PostgreSQL.

## Deferred primary challengers — not rejected

### P2 — XTDB 2.1.0

```text
PM-05
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED

DISTINCTIVE VALUE
native bitemporality / serialized DML

CURRENT COST
no native FK
no general uniqueness beyond _id
manual ASSERT/address integrity discipline
non-interactive transaction ergonomics
production topology/single-writer sensitivity HOLD
```

Reopen only if native bitemporal value becomes decision-dominant, PostgreSQL/TypeDB exposes a material temporal weakness, or XTDB capability/topology materially changes.

### P3 — SurrealDB Community 3.2.3

```text
PM-05
DEFER FROM PRIMARY FINALIST SET
NOT REJECTED

DISTINCTIVE VALUE
constrained multimodel consolidation

CURRENT COST
snapshot-isolation guard discipline
explicit long-lived material history
comparatively weaker primary-store differentiator versus finalists
```

Reopen only if multimodel consolidation becomes decision-changing, a finalist exposes a material gap SurrealDB directly solves, or relevant engine capability materially changes.

## PM-05 scenario result

### Primary semantic scenarios — evidence-qualified

```text
SC-001 SC-002 SC-003 SC-009 SC-010 SC-012
SC-014 SC-015 SC-016 SC-022 SC-023 SC-024
```

No local execution is currently justified for these.

### System/runtime/provider boundary

```text
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034
```

These remain real LifeOS obligations but are not standalone reasons to benchmark four primary databases.

### PM-06/07 finalist scenarios

```text
SC-011 old-backup anti-resurrection
SC-013 deep-history scale
SC-030 V1 -> V2 evolution
SC-031 backup/restore semantic verification
SC-032 capacity/backpressure
```

### PM-08 specialist scenarios

```text
SC-017 SC-018 SC-019 SC-020 SC-021 SC-035
```

## Current evidence posture

```text
PM-05 EXECUTION-WORTHY gaps  0
PM-04B                        NOT REOPENED
FULL LOCAL BENCHMARK          NOT ADMITTED
TARGETED LOCAL PROOFS         0 ADMITTED
DATABASE/HARNESS              NOT STARTED
BENCHMARK HOST                HOLD / DORMANT
DIRECT HG PASS                0
```

The benchmark host becomes a blocker only before a separately admitted direct execution claim.

## PM-06 + PM-07 Joint Finalist Qualification

The next campaign covers only PostgreSQL + TypeDB unless a deferred-candidate reopen trigger is proven.

The campaign is operationally joint but preserves two result layers.

### PM-06

```text
scale/history efficiency
performance/resource behavior
contention sensitivity
storage/index growth
topology/resource cliffs
```

### PM-07

```text
backup/restore
anti-resurrection
evolution/migration
failure/backpressure
operations/HA/topology
RPO/RTO capability sensitivity
```

Default remains evidence-first. Direct tests occur only if a residual question is ranking-critical and test-resolvable or is genuinely mandatory for finalist closure.

Performance can never compensate for recovery/evolution failure.

## Secondary/specialist lanes — PM-08

```text
GRAPH
G0 no-specialist baseline
Neo4j or another graph specialist only on demonstrated value

SEARCH/VECTOR
primary structured/lexical baseline
pgvector when applicable
Qdrant/OpenSearch only on specialist trigger

LOCAL/OFFLINE
SQLite or equivalent bounded client role
```

The final system may use multiple technologies, but every additional engine must independently justify complexity and remain semantically bounded.

## Cost/exit posture

```text
TARGET
EUR 0 initial direct technology/license cost where realistically possible

BUT
quality/correctness outrank cost
paid != automatic rejection
free != automatic preference
```

Use candidate-native strengths where materially better; do not build gratuitous lowest-common-denominator abstraction.

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
qualification/*
```

The live save-game is `../workstreams/physical-model.md`.

## Fixed roadmap

```text
PM-00  Bootstrap                                      PASS
PM-01  Technology discovery/candidate freeze          PASS-CONDITIONAL
PM-02  Primary mapping design                         COMPLETE
PM-03  Semantic static preflight                      COMPLETE
PM-04A External evidence sufficiency                  COMPLETE
PM-04B Conditional harness                            NOT ADMITTED
PM-05  Correctness/destructive evidence qualification COMPLETE
PM-06  Scale/performance result layer                 NEXT — JOINT WITH PM-07
PM-07  Recovery/evolution/failure result layer        NEXT — JOINT WITH PM-06
PM-08  Secondary lanes                                NOT STARTED
PM-09  Scoring/sensitivity                            NOT STARTED
PM-10  Recommendation                                 NOT STARTED
PM-11  Explicit selection                             NOT STARTED
PM-12  Accepted Physical Model                        NOT STARTED
PM-13  Independent clean-room QA                      NOT STARTED
PM-14  Closure/protected-main integration             NOT STARTED
```

## Next

```text
PM-06/07 JOINT FINALIST QUALIFICATION
PostgreSQL + TypeDB
fresh explicit gate required
no local execution by default
no selection
no backend/API/Auth implementation
```
