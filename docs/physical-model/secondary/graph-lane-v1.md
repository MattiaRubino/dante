# PM-08 Graph Lane v1

- Status: **COMPLETE — PRIMARY-STORE BASELINE ADVANCES / NO INITIAL GRAPH SPECIALIST**
- Workstream: `feature/physical-model`
- Direct execution: **NOT RUN**
- Selection: **NONE**

## Question

Does a dedicated graph engine create enough LifeOS value to justify another persistence/service boundary after the primary shortlist has narrowed to PostgreSQL 18.4 and TypeDB CE 3.12.3?

## Baselines

### PostgreSQL

PostgreSQL 18 supports recursive CTEs for hierarchical/graph traversal. `SEARCH` supports breadth/depth ordering and `CYCLE` supports cycle detection.

This does not make PostgreSQL a graph-native database. It establishes that ordinary/deep-ish traversal is not automatically a specialist gap.

### TypeDB

TypeDB's principal finalist strength is already its semantic relation/role/n-ary model. Adding a second graph engine beside a TypeDB primary would therefore require an unusually strong read/analytics benefit.

## Neo4j evidence

Neo4j remains a strong graph specialist with Cypher/path-oriented graph ergonomics.

Edition boundary matters:

```text
Community Edition
single-instance deployment

Enterprise Edition
clustering architecture
online backup
additional scale/availability features
```

A production graph projection would also require:

```text
canonical -> graph projection pipeline
freshness/lag tracking
Visibility/scope propagation
redaction/deletion propagation
correction propagation
rebuild/reconciliation
second backup/operations/security surface
```

## Verdict

```text
G0 PRIMARY-STORE GRAPH BASELINE
ADVANCE

NEO4J
DEFER / NOT REJECTED
NO INITIAL ADMISSION

GRAPH DIRECT BENCHMARK
NOT ADMITTED
```

The absence of an admitted graph specialist is an intentional architecture result, not a missing task.

## Reopen triggers

Neo4j or another graph specialist may be reconsidered only if a concrete accepted workload shows material net value, including examples such as:

```text
large/deep variable-length traversal
shortest/path-finding as a major product capability
graph recommendation
large relationship-network analytics
primary-store traversal latency/resource isolation materially unacceptable
graph query ergonomics materially blocking accepted product capability
```

Any reopen must compare the gain against projection/recovery/security complexity and must keep graph state secondary/rebuildable unless a separately accepted semantic decision says otherwise.

## Scenario carry-forward

```text
SC-035 graph projection divergence/rebuild
NOT APPLICABLE TO INITIAL STACK
reopen if graph projection is later admitted

SC-015 typed n-ary relation fidelity
remains a primary semantic requirement; graph specialization does not redefine it

SC-016/017 visibility/non-interference
remain mandatory for any later graph-exposed result surface
```

## Source ledger

- PostgreSQL 18 `WITH` / recursive query documentation.
- PostgreSQL 18 `SELECT` documentation for `SEARCH` and `CYCLE`.
- Neo4j Operations Manual current edition boundary.

## Closure

```text
INITIAL GRAPH TECHNOLOGY COUNT
0 additional engines

NEO4J
DEFER / NOT REJECTED

PREFERRED
NONE
SELECTED
NONE
```