# SurrealDB Community 3.2.3 — PM-04A Evidence Sufficiency v1

- Candidate: SurrealDB Community 3.2.3 / single-node RocksDB / Python SDK 2.0.0
- Mapping: `PM02-SDB-001`
- Status: **EXTERNAL EVIDENCE REVIEW COMPLETE / DIRECT EXECUTION NOT RUN**
- Selection: **NONE**
- Evidence confidence: **MEDIUM-HIGH documented capability / MEDIUM net LifeOS primary advantage**

## 1. PM-04A conclusion

SurrealDB remains a credible constrained multimodel challenger. Official documentation confirms SCHEMAFULL/typed data modeling, typed graph relation structures and snapshot-isolated transactions with write-write conflict detection.

The PM-03 HG-04/HG-05 uncertainty is narrowed in the same way as TypeDB: PM-02's narrow `consistency_guard` is conditionally credible when every transaction sharing a write-skew-sensitive invariant boundary mutates the same guard record, deliberately creating a common write-write conflict point.

The remaining question is not whether the engine has a conflict primitive. It is whether SurrealDB's overall multimodel consolidation creates enough LifeOS value to offset explicit-history/concurrency-discipline and maturity costs versus the current leaders.

```text
EXECUTION-WORTHY GAP NOW
0

PM-04B REQUIRED NOW
NO

DIRECT HG PASS CREATED
NO
```

## 2. Primary source ledger

| Topic | Source | Evidence use |
|---|---|---|
| SurrealDB 3.2 releases | https://surrealdb.com/releases/3.2 | exact 3.2.3 subject/release context |
| architecture | https://surrealdb.com/docs/architecture | transaction/isolation and storage architecture |
| graph relations | https://surrealdb.com/docs/learn/data-models/graph/creating-relations | typed relation model / `TYPE RELATION` |
| record links | https://surrealdb.com/docs/learn/data-models/relationships | typed record-link model |
| `RELATE` | https://surrealdb.com/docs/surrealql/statements/relate | relation semantics/integrity behavior |
| changefeeds | https://surrealdb.com/docs/learn/querying/real-time/changefeeds | bounded changefeed semantics |
| self-hosted backup/recovery | https://surrealdb.com/docs/manage/self-hosted/backups-and-recovery | logical export/import recovery path |
| 2.x -> 3.x migration | https://surrealdb.com/docs/build/migrating/from-old-surrealdb-versions/2x-to-3x | evolution/migration evidence |

## 3. Supporting benchmark / production evidence

Supporting only; vendor-owned material is not treated as neutral LifeOS proof.

| Evidence | Source | Relevance |
|---|---|---|
| open CRUD benchmark harness | https://github.com/surrealdb/crud-bench | disclosed multi-database benchmark implementation / viability evidence |
| SurrealDB benchmark material | https://surrealdb.com/blog | supporting performance context only |
| production case studies | https://surrealdb.com/casestudies | evidence of real deployments and multimodel workloads |

A generic CRUD result does not establish LifeOS correctness and therefore does not justify reproducing the benchmark locally unless performance later becomes recommendation-critical.

## 4. Gate-by-gate sufficiency

| Gate | PM-04A class | Rationale |
|---|---|---|
| HG-01 | MAP-SUFFICIENT | owner-specific SCHEMAFULL tables prevent the document layer from becoming a generic ontology when mapping discipline holds |
| HG-02 | EXT+MAP-SUFFICIENT | typed record links/unions plus separate address treatment can preserve target-family discrimination |
| HG-03 | EXT+MAP-SUFFICIENT | specific typed binary relations plus contextual records for n-ary/material semantics preserve relation fidelity |
| HG-04 | MAP-SUFFICIENT / CONDITION | expected-state record check + shared consistency guard provides explicit same-record conflict point under snapshot isolation |
| HG-05 | MAP-SUFFICIENT / KNOWN DESIGN COST | multi-record transaction + shared guard gives a viable co-located invariant strategy; guard coverage remains mandatory |
| HG-06 | MAP-SUFFICIENT / KNOWN COST | explicit material-state history remains required; bounded changefeed cannot replace canonical long-term history |
| HG-07 | MAP-SUFFICIENT | canonical/provider/projection/runtime structures remain explicitly classified despite one multimodel engine |
| HG-08 | MAP-SUFFICIENT / DEFER-FINALIST | graph/query capabilities help but system-level non-interference remains outside database-only proof |
| HG-09 | DEFER-FINALIST | backup/export exists; LifeOS deletion/redaction anti-resurrection needs finalist rehearsal |
| HG-10 | MAP-SUFFICIENT | explicit semantic temporal structures avoid treating datetime/graph features as recurrence ontology |
| HG-11 | EXT+DEFER-FINALIST | migration tooling/evidence exists; actual LifeOS ID/history continuity needs concrete finalist mapping |
| HG-12 | EXT+DEFER-FINALIST | logical export/import gives recovery path; semantic restore proof remains later finalist evidence |

## 5. Snapshot isolation and consistency guard

SurrealDB documents snapshot isolation and write-write conflict detection. Snapshot isolation does not by itself guarantee freedom from write skew across disjoint records.

PM-02 therefore deliberately makes relevant transactions share a technical write target:

```text
T1
read invariant I
write semantic A
write consistency_guard(I)

T2
read same invariant I
write semantic B
write consistency_guard(I)
```

If both transactions reach commit concurrently, the guard changes the physical conflict shape from disjoint writes to a common write target.

PM-04A conclusion:

```text
ENGINE PRIMITIVE
sufficiently documented

GUARD PATTERN
reasonably supported conditionally

FUTURE GUARD COVERAGE
architecture discipline cost

LOCAL TOY RACE NEEDED NOW
NO
```

This does not promote snapshot isolation to serializable isolation and does not permit a single global guard.

## 6. Multimodel advantage and risk

SurrealDB's strongest proposition is consolidation:

```text
structured records
+ direct record links
+ graph relations
+ document-shaped bounded data
+ search/vector capabilities in one engine family
```

That can reduce operational component count if the capabilities prove sufficient.

LifeOS still forbids using this flexibility to collapse semantics:

```text
no generic object table
no generic edge ontology
no FLEXIBLE canonical kernel
no changefeed-as-history
no graphification of Agreement or material state
```

PM-04A therefore counts multimodel consolidation as a possible later benefit but not enough, by itself, to overtake PostgreSQL/TypeDB/XTDB as primary.

## 7. History/changefeed boundary

SurrealDB changefeeds are useful for change propagation, sync and projection invalidation, but their bounded/operational retention makes them unsuitable as the canonical source of long-lived LifeOS material history.

PM-02's explicit state records remain required.

This produces a comparative cost:

```text
MULTIMODEL CONVENIENCE
positive

NATIVE LONG-LIVED SEMANTIC HISTORY ADVANTAGE
not established

EXPLICIT MATERIAL HISTORY
still required
```

## 8. Reference/relation fidelity

Typed record links and typed relation endpoints provide a credible path for bounded Reference Contracts and binary LR-03 relations.

N-ary/common-ground semantics remain normal contextual records rather than inferred stars of binary graph edges.

This removes the need for a local graph toy test at PM-04A: the main decision is mapping policy, already explicit in PM-02.

## 9. Recovery/evolution

SurrealDB supplies self-hosted logical export/import recovery mechanisms and documented migration guidance.

PM-04A records:

```text
ENGINE CAPABILITY
externally sufficient for comparison

LIFEOS OLD-BACKUP ANTI-RESURRECTION
DEFER-FINALIST

LIFEOS V1 -> V2 SEMANTIC CONTINUITY
DEFER-FINALIST
```

A four-candidate destructive restore exercise is not admitted now.

## 10. Current disposition

```text
P3 SURREALDB COMMUNITY 3.2.3
CREDIBLE MULTIMODEL CHALLENGER
HG-04/HG-05 UNKNOWN -> NARROWED TO DOCUMENTED DESIGN CONDITION
EXPLICIT HISTORY COST REMAINS
NO UNIQUE PRIMARY ADVANTAGE YET LARGE ENOUGH TO LEAD
NO PM-04B EXECUTION ADMITTED
EXECUTED HG STILL NOT RUN
NO SCORE
NO SELECTION
```

Reopen direct concurrency/performance work only if later evidence makes SurrealDB competitive enough that those measurements could materially change the recommendation.
