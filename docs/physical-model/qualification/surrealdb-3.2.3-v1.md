# SurrealDB Community 3.2.3 — PM-05 Correctness Evidence Qualification v1

- Candidate: SurrealDB Community 3.2.3 / single-node RocksDB / Python SDK 2.0.0
- Mapping: `PM02-SDB-001`
- PM-05 disposition: **DEFER FROM PRIMARY FINALIST SET / NOT REJECTED**
- Direct LifeOS execution: **NOT RUN**
- Selection: **NONE**

## 1. Qualification thesis

SurrealDB remains a credible constrained multimodel engine, but PM-05 finds no unique primary-store advantage large enough to justify carrying a fourth candidate into finalist qualification after PostgreSQL and TypeDB remain stronger on aggregate LifeOS fit.

The result is a comparative defer, not a failure of the mapping or a hard rejection.

## 2. Primary semantic scenario coverage

### SC-001 / SC-003 / SC-009 — concurrency and multi-owner correctness

SurrealDB's snapshot-isolation model with write-write conflict detection supports the accepted narrow consistency-guard pattern for invariant scopes that would otherwise permit write-skew.

Classification:

```text
PRIMARY-EVIDENCE-SUFFICIENT
KNOWN DESIGN CONDITION/COST
```

Correct guard coverage remains mandatory and adds system complexity.

### SC-010 / SC-014 — correction and historical reconstruction

The PM-02 design deliberately uses explicit material-state records rather than bounded changefeeds as canonical LifeOS history.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT / KNOWN HISTORY COST`.

### SC-012 — NativeRef non-reuse

Stable typed record identity plus explicit tombstone/address continuity can preserve non-reuse. Anti-resurrection remains a finalist/PM-07 concern only if SurrealDB is reopened.

### SC-015 — typed n-ary relation fidelity

Binary relation tables remain limited to true binary LR-03 relations. N-ary Agreement and material contextual structures remain explicit records rather than inferred graph stars.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`.

### SC-016 — selective disclosure

Representable through explicit recipient/context filtering and projection boundaries, but full non-interference remains a system concern. No unique SurrealDB advantage is established here.

### SC-022 / 023 / 024 — temporal/recurrence

LifeOS temporal and recurrence semantics remain explicit and do not depend on generic document/graph features.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`.

## 3. Known costs

```text
snapshot isolation + mandatory consistency-guard discipline for some invariants
explicit long-lived material history remains required
multimodel flexibility must remain constrained to avoid generic canonical meta-model drift
comparatively less mature operational ecosystem than PostgreSQL
no demonstrated primary-store advantage decisive enough to overtake PostgreSQL/TypeDB
```

## 4. Why defer now

PM-05 found no ranking-critical unresolved question likely enough to justify a dedicated local SurrealDB proof now.

The candidate's consolidation value is real, but the present evidence indicates that it does not offset the combined concurrency/history/operational discipline cost strongly enough to warrant finalist scope.

## 5. Reopen triggers

```text
multimodel consolidation becomes a demonstrated decision-changing LifeOS requirement
or
PostgreSQL/TypeDB finalist qualification exposes a material capability gap SurrealDB directly solves
or
relevant concurrency/history/operations capabilities materially change
or
PM-08/PM-09 sensitivity proves a consolidation/TCO advantage large enough to alter the recommendation
```

## 6. Disposition

```text
PRIMARY FINALIST
NO

CURRENT PRIMARY DISPOSITION
DEFER

REJECTED
NO

PM-05 EXECUTION-WORTHY GAP
0

DIRECT HG
NOT RUN

PREFERRED
NO

SELECTED
NO
```
