# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-06/07 JOINT COMPLETE / PM-08 NEXT**
- Branch: `feature/physical-model`
- Main baseline: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL**
- PM-02: **COMPLETE**
- PM-03: **STATIC COMPLETE / 0 REJECTS**
- PM-04A: **COMPLETE / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED**
- PM-05: **COMPLETE**
- PM-06: **EVIDENCE QUALIFICATION COMPLETE / DIRECT PERFORMANCE NOT RUN**
- PM-07: **EVIDENCE QUALIFICATION COMPLETE / DIRECT DESTRUCTIVE RUNS NOT RUN**
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Deferred challengers: **XTDB 2.1.0 + SurrealDB Community 3.2.3 — NOT REJECTED**
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
7. read PM-01 through PM-07 current evidence relevant to the next phase;
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
MISSING != FALSE
EVIDENCE-QUALIFIED != EXECUTED PASS
PUBLIC BENCHMARK != LIFEOS BENCHMARK
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
```

## Current primary finalists

### PostgreSQL 18.4

```text
ROLE
current overall leader

PM-06
scale/performance viable / HIGH confidence

PM-07
clear operations/recovery/topology advantage

PREFERRED
NONE

SELECTED
NONE
```

Why it leads:

- accepted mapping preserves LifeOS semantics without a universal ontology root;
- mature integrity and Serializable primitives;
- WAL/PITR and full/incremental base-backup paths;
- mature physical/logical replication and standby/failover primitives;
- several upgrade/migration paths;
- zero-license-cost self-hosted database capability;
- lower aggregate canonical-store operational risk.

Remaining obligations are implementation-specific: anchor discipline, operation-specific transaction policy, system-level WL-H12, semantic restore/anti-resurrection, actual LifeOS V1→V2 migration.

### TypeDB CE 3.12.3

```text
ROLE
principal semantic challenger

PM-06
scale/performance viable / MEDIUM-HIGH confidence

PM-07
recovery/evolution viable / higher self-hosted operations cost

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

- snapshot-isolation hardening via correctly scoped consistency guards;
- each query currently single-threaded;
- CE is single-node;
- self-hosted backup implementation is LifeOS-owned;
- documented self-hosted backup options are non-incremental;
- clustering/horizontal read scaling belong to Cloud/Enterprise rather than CE.

## Deferred primary challengers

```text
XTDB 2.1.0
DEFER / NOT REJECTED
reopen on decision-dominant bitemporal need or material capability change

SurrealDB Community 3.2.3
DEFER / NOT REJECTED
reopen on decision-dominant multimodel consolidation or material capability change
```

## PM-06/07 conclusion

```text
PostgreSQL
OVERALL LEAD STRENGTHENED

TypeDB
SEMANTIC ADVANTAGE PRESERVED

LOCAL PERFORMANCE TESTS
0 ADMITTED

LOCAL DESTRUCTIVE TESTS
0 ADMITTED
```

The remaining primary decision is now a tradeoff between TypeDB's semantic-native model and PostgreSQL's stronger aggregate integrity/operations/recovery/topology posture.

## Post-selection implementation validation

These remain mandatory where applicable; they are not waived and are not direct PASS today:

```text
SC-011 old-backup anti-resurrection
SC-030 actual V1→V2 mapping evolution
SC-031 semantic backup/restore verification
SC-032 capacity/backpressure behavior
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
```

## PM-08 — next

PM-08 evaluates bounded specialist lanes after the primary comparison has narrowed.

Questions include:

```text
GRAPH
Does a graph projection create enough traversal/read value to justify another engine?

SEARCH/VECTOR
Is primary-native search sufficient?
If PostgreSQL remains applicable, does pgvector earn its bounded role?
When would Qdrant/OpenSearch earn another service?

LOCAL/OFFLINE
Does SQLite earn a bounded client/local role without becoming competing canonical truth?
```

Rules:

- no infrastructure zoo;
- specialist state must remain bounded and reconciliable/rebuildable where required;
- no specialist may compensate for a primary semantic failure;
- no technology is selected merely because it is useful elsewhere;
- cost/operations/security/freshness/delete propagation all count.

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
PM-08  NEXT
PM-09  NOT STARTED
PM-10  NOT STARTED
PM-11  NOT STARTED
PM-12  NOT STARTED
PM-13  NOT STARTED
PM-14  NOT STARTED
```

## Current exact next step

```text
PM-08
read-only specialist-lane evidence first
fresh exact write gate required before repository mutation

PREFERRED NONE
SELECTED NONE
BACKEND NOT STARTED / DEFERRED
```