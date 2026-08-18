# PostgreSQL 18.4 — PM-04A Evidence Sufficiency v1

- Candidate: PostgreSQL 18.4 / self-hosted single-node / psycopg 3.3.4
- Mapping: `PM02-PG-001`
- Status: **EXTERNAL EVIDENCE REVIEW COMPLETE / DIRECT EXECUTION NOT RUN**
- Selection: **NONE**
- Evidence confidence: **HIGH engine fundamentals / MEDIUM-HIGH LifeOS mapping**

## 1. PM-04A conclusion

PostgreSQL remains the current overall primary-store leader without requiring a local four-way benchmark.

The engine capabilities most relevant to LifeOS integrity are already strongly established by versioned official documentation: foreign keys and other constraints, true serializable transaction isolation, explicit serialization-failure/retry semantics, mature backup/PITR mechanisms and controlled major-version upgrade tooling.

The remaining LifeOS risk is mapping discipline rather than uncertainty about those primitives.

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
| PostgreSQL 18 documentation | https://www.postgresql.org/docs/18/ | exact major subject baseline |
| PostgreSQL 18.4 release | https://www.postgresql.org/docs/release/18.4/ | exact frozen point release |
| constraints / FK / unique / exclusion | https://www.postgresql.org/docs/18/ddl-constraints.html | HG-02/HG-03 structural integrity |
| transaction isolation | https://www.postgresql.org/docs/current/transaction-iso.html | HG-04/HG-05 serializable semantics |
| serialization failure handling | https://www.postgresql.org/docs/18/mvcc-serialization-failure-handling.html | explicit retry requirement |
| row security | https://www.postgresql.org/docs/18/ddl-rowsecurity.html | HG-08 supporting primitive + limitations |
| backup | https://www.postgresql.org/docs/18/backup.html | HG-09/HG-12 operational capability |
| continuous archiving / PITR | https://www.postgresql.org/docs/18/continuous-archiving.html | HG-12 recovery capability |
| pg_upgrade | https://www.postgresql.org/docs/18/pgupgrade.html | HG-11 upgrade path |
| upgrading | https://www.postgresql.org/docs/18/upgrading.html | HG-11 operational path |
| date/time types | https://www.postgresql.org/docs/18/datatype-datetime.html | HG-10 temporal primitives |
| range types | https://www.postgresql.org/docs/18/rangetypes.html | HG-10 interval/range support |

## 3. Supporting production evidence

Supporting only; not engine authority or LifeOS mapping proof.

| Evidence | Source | Relevance |
|---|---|---|
| Notion PostgreSQL/data-lake architecture | https://www.notion.com/blog/building-and-scaling-notions-data-lake | demonstrates very large PostgreSQL-backed operational estate and separation of OLTP from analytics |
| Notion sharding architecture | https://www.notion.com/blog/sharding-postgres-at-notion | reinforces locality/transaction-boundary lessons and distributed partial-write risk |
| Notion re-sharding | https://www.notion.com/blog/the-great-re-shard | mature operational evolution evidence |

These cases are not used as proof that LifeOS will have the same scale or topology.

## 4. Gate-by-gate sufficiency

| Gate | PM-04A class | Rationale |
|---|---|---|
| HG-01 | MAP-SUFFICIENT | owner-specific tables/history/relation families avoid a universal ontology; this is mapping design, not a missing engine primitive |
| HG-02 | EXT+MAP-SUFFICIENT | homogeneous references have native FK support; heterogeneous references use bounded technical anchors with explicit family enforcement |
| HG-03 | EXT+MAP-SUFFICIENT | relational constraints plus relation-specific tables can preserve typed/n-ary semantics; Agreement remains contextual/n-ary rather than generic edge |
| HG-04 | EXT+MAP-SUFFICIENT | expected MaterialStateRef check plus conditional write/lock/Serializable provides explicit conflict path |
| HG-05 | EXT+MAP-SUFFICIENT | one transaction + Serializable/locking/constraints provides a viable co-located atomic boundary |
| HG-06 | MAP-SUFFICIENT | explicit material-state/current bindings preserve current + historical reconstruction without replay |
| HG-07 | MAP-SUFFICIENT | separate canonical/history/integration/projection/technical structures preserve semantic state layers |
| HG-08 | MAP-SUFFICIENT / DEFER-FINALIST | RLS/query policies can help, but WL-H12 is a system disclosure contract; RLS alone is not accepted as complete proof |
| HG-09 | DEFER-FINALIST | engine backup/restore exists; LifeOS anti-resurrection requires finalist restore/reconciliation rehearsal |
| HG-10 | EXT+MAP-SUFFICIENT | rich date/time/range primitives exist; PM-02 preserves named-zone/floating/recurrence semantics explicitly |
| HG-11 | DEFER-FINALIST | strong migration/upgrade tooling exists; actual LifeOS V1→V2 semantic continuity requires a concrete mapping |
| HG-12 | EXT+DEFER-FINALIST | backup/PITR capability is mature; semantic post-restore proof remains finalist evidence |

## 5. Concurrency evidence interpretation

PostgreSQL Serializable is not treated as a magic global setting. PM-02 still requires operation-specific expected-state checks and the narrowest viable mechanism.

Correct conclusion:

```text
DOCUMENTED SERIALIZABLE + CONSTRAINT/LOCKING PRIMITIVES
= strong engine capability evidence

BUT
transaction design still matters
```

A local toy race would only confirm a documented property. It is not currently capable of changing the candidate ranking enough to justify PM-04B.

## 6. Heterogeneous address anchors

The principal PostgreSQL-specific LifeOS pressure remains the bounded technical address anchor used where a logical Reference Contract can target unrelated native tables.

PM-04A classifies this as mapping complexity, not an unknown engine behavior.

Required condition remains:

```text
anchor contains address/control metadata only
anchor does not own generic Domain fields/lifecycle
homogeneous references keep direct FK where possible
contract-specific target-family eligibility is enforced
Native/Scoped/Material/External address spaces remain distinct
```

Reopen direct proof only if later concrete schema work demonstrates anchor leakage or unmaintainable enforcement.

## 7. Governance caveat

PostgreSQL row-level security is a useful physical enforcement primitive but is not LifeOS Domain Authority/Consent and is not by itself sufficient for WL-H12.

The system must still reason about:

```text
hidden existence
counts/aggregates
ranking
errors/not-found
relation/source visibility
explanations
timing where material
```

This is why HG-08 remains finalist/system evidence rather than receiving a direct PASS from PostgreSQL documentation.

## 8. Recovery/evolution treatment

PM-04A does not require four separate destructive restore labs merely because all candidates expose backup facilities.

For PostgreSQL:

```text
ENGINE RECOVERY CAPABILITY
externally sufficient for current comparison

LIFEOS OLD-BACKUP ANTI-RESURRECTION
DEFER-FINALIST

LIFEOS V1 -> V2 HISTORICAL/REFERENCE CONTINUITY
DEFER-FINALIST
```

## 9. Performance evidence treatment

PostgreSQL has abundant public production evidence and benchmark literature. PM-04A finds no credible reason to run a generic laptop CRUD benchmark.

Performance becomes direct execution work only if later evidence shows the recommendation is sensitivity-dependent on a LifeOS-specific workload or resource envelope.

## 10. Current disposition

```text
P0 POSTGRESQL 18.4
CURRENT OVERALL LEADER
NO PM-04B EXECUTION ADMITTED
EXECUTED HG STILL NOT RUN
NO SCORE
NO PREFERRED RESULT CREATED HERE
NO SELECTION
```
