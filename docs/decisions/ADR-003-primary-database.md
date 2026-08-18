# ADR-003: Primary Database

- Status: **Superseded as final selection / retained as historical rationale**
- Date: 2026-08-02
- Updated: 2026-08-10
- Superseded for current execution: 2026-08-17
- Current authority: closed Whole Logical Model + future separately authorized Physical Model benchmark

## Original decision

Use PostgreSQL as the primary source of truth.

The original decision assumed a hybrid persistence model:

- typed relational structures for stable domain concepts and invariants;
- metadata/JSONB for genuinely flexible properties;
- graph-like relationship mechanisms for personal/emergent links;
- version/audit/event history for traceability.

## Original rationale

LifeOS requires strong transactions, constraints, indexing, relational consistency, history and cross-domain queryability while also supporting bounded flexible/provider-specific data. PostgreSQL offered a practical single-primary-database foundation without introducing multiple specialized stores prematurely.

## Current status

This ADR no longer selects the final Physical database.

The closed Logical Model establishes the current benchmark posture:

```text
PostgreSQL hybrid
CURRENT PREFERRED PHYSICAL BASELINE
NOT FINAL SELECTION

TypeDB
MANDATORY PHYSICAL BENCHMARK CHALLENGER

Neo4j / property graph
SERIOUS SECONDARY / READ-PROJECTION CANDIDATE

event/document mechanisms
BOUNDED CANDIDATES

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

PostgreSQL therefore remains a strong preferred baseline because the original transactional/relational/history rationale is still relevant, but it must compete against the accepted challengers on LifeOS-specific correctness and operational pressure.

## Current consequences

- no Physical database is yet selected;
- no PostgreSQL schema/table/index/key strategy is authorized;
- Mongo/document storage is not accepted as a universal canonical kernel;
- a graph store is not accepted as a universal canonical ontology;
- specialized stores may be adopted where demonstrated benefit justifies them;
- persistence must preserve the closed Domain + Logical semantics regardless of technology;
- any final primary-store decision requires the separate Physical Model scope and benchmark.

## Historical value retained

The original rationale remains useful evidence for why PostgreSQL is the current preferred baseline. It is not current authority for bypassing the Physical benchmark.
